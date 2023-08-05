import typer
import ast
from pprint import pprint

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"classes": []}

    def visit_ClassDef(self, node):
        #breakpoint()
        name = node.name
        bases = node.bases
        
        for base in bases:
            print(base.id)
        got_device = any([x.id == 'Device' for x in bases])
        if got_device:
            print(f"Got device {name}")
            
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)

def main(file: typer.FileText = typer.Option(...)):
    breakpoint()
    tree = ast.parse(file.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()




if __name__ == "__main__":
    typer.run(main)
