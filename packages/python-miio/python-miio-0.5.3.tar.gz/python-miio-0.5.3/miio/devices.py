import click
import logging
from miio.click_common import DeviceGroup
from miio import Discovery, Device
from miio.miioprotocol import MiIOProtocol
from pathlib import Path
import toml
from appdirs import user_config_dir
import attr
from typing import List, Dict

_LOGGER = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class DeviceEntry:
    name: str
    mdns: str
    host: str
    token: str = None
    device_class: str = attr.ib(default="Device")
    info: Dict = None


def convert_device_list(x):
    return [DeviceEntry(**info) for info in x]

@attr.s(auto_attribs=True)
class Config:
    devices: List[DeviceEntry] = attr.ib(default=attr.Factory(list), converter=convert_device_list)


class Database:
    def __init__(self, config_file=None):
        if config_file is None:
            config_dir = Path(user_config_dir("python-miio"))
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_file = config_dir / "miio.db"
        else:
            self.config_file = Path(config_file)

        if self.config_file.exists():
            self.config = self.parse_config(self.config_file)
        elif config_file is None:
            self.config = self.create_config()
        else:
            raise Exception("Config file does not exist.")

    def create_config(self):
        conf = Config()
        _LOGGER.info("Created config: %s", conf)
        return conf

    @property
    def devices(self) -> List[DeviceEntry]:
        return self.config.devices

    def initialize_device(self, dev):
        import importlib
        module = importlib.import_module("miio")
        class_ = getattr(module, dev.device_class)  # type: Device
        instance = class_(dev.host, dev.token)
        return instance

    def load_devices(self):
        for dev in self.config.devices:
            instance = self.initialize_device(dev)
            print(instance.info())

    def discover_and_sync(self):
        devlist = self.config.devices
        existing_hosts = [dev.host for dev in self.devices]
        def cb(host, dev, info):

            dev = DeviceEntry(name=info.name, mdns=info.name, host=host, device_class=dev.__class__.__name__, token=dev.token)
            print("got device: %s", dev)
            if dev.host not in existing_hosts:
                devlist.append(dev)


        Discovery.discover_mdns(timeout=3, callback=cb)
        _LOGGER.info("Discovery done, found %s devices", len(devlist))
        MiIOProtocol.discover()

    def sync(self):
        _LOGGER.info("Going to synchronize: %s", self.config)
        for dev in self.config.devices:
            print(dev)
            inst = self.initialize_device(dev)
            try:
                dev.info = inst.info().raw
            except Exception as ex:
                _LOGGER.warning("Unable to request info..")




        print("Going to write %s", self.config_file)
        self.config_file.write_text(toml.dumps(attr.asdict(self.config)))

    def add(self, host, token):
        dev = Device(host, token=token)
        self.config.devices.append(dev)
        self.sync()

    def parse_config(self, file):
        _LOGGER.error("parsing config")
        try:
            conf = toml.load(file)
            _LOGGER.info(conf)
            return Config(**conf)
        except Exception as ex:
            _LOGGER.info("Unable to parse config: %s", ex)


pass_db = click.make_pass_decorator(Database)

@click.group()
@click.pass_context
def devices(ctx):
    print("context: %s" % ctx)
    ctx.obj = Database()
    ctx.obj.sync()

@devices.command(name="list")
@pass_db
def list_(db: Database):
    for dev in db.devices:
        print(dev)

@devices.command()
@click.argument("host")
@click.argument("token")
@pass_db
def add(db: Database, host, token):
    click.echo("Adding device: %s with token %s", host, token)
    db.add(host, token)

@devices.command()
def sync():
    click.echo("Going to sync")