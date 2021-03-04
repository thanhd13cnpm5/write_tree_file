from pathlib import Path
import ast
from collections import namedtuple

space = '   '
branch = '│   '
tee = '├──'
last = '└── '
Lang = {
    "Javascript": ".js",
    "Css": ".css",
    "Html": ".html",
    "Python": ".py",
    "Php": ".php",
    "C++": ".cpp",
    "C#": ".cs",
    "Golang": ".go",
    "Typescript": ".ts",
    "Ruby": ".rb",
    "Sql": ".sql",
    "Rust": ".r"
}
LST1 = []
LST2 = []

def tree_file(Path, prefix = ''):
    listpath = list(Path.iterdir())
    pointers = [tee] * (len(listpath) - 1) + [last]
    for pointer, path in zip(pointers, listpath):
        print(prefix + pointer + path.name)
        if path.suffix == ".py":
            LST2.append(path.as_posix())
        for x in Lang:
            if Lang[x] == path.suffix:
                LST1.append(path.suffix)
        if path.is_dir():
            extension = branch if pointer == tee else space
            yield from tree_file(path, prefix=prefix + extension)

for line in tree_file(Path.home() / 'C:\\Users\\DELL\\PycharmProjects\\write_root'):
    print(line)

print("\n\n")
dem = 0
for x in Lang:
    for y in LST1:
        if Lang[x] == y:
            dem = dem + 1
    if dem > 0:
        d = str(dem)
        print(d + " files : " + x)
    dem = 0

print("\n\n")

Import = namedtuple("Import", ["module", "name", "alias"])

def get_imports(path):
    with open(path) as f:
       root = ast.parse(f.read(), path)
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)

for x in LST2:
    for imp in get_imports(x):
        print(imp)

