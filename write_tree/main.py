from pathlib import Path
import ast
from collections import namedtuple

# prefix
space = '   '
branch = '│   '
# con trỏ
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


# hàm in cấu trúc file dạng tree
def tree_file(Path, prefix=''):
    # lấy ra danh sách list các đường dẫn
    listpath = list(Path.iterdir())
    # list các con trỏ ├── ở cuối là └──
    pointers = [tee] * (len(listpath) - 1) + [last]
    for pointer, path in zip(pointers, listpath):
        print(prefix + pointer + path.name)
        if path.suffix == ".py":
            LST2.append(path.as_posix())
        # lọc tất cả file có trong dect lang{} đã khai báo
        for x in Lang:
            if Lang[x] == path.suffix:
                LST1.append(path.suffix)
        if path.is_dir():
            extension = branch if pointer == tee else space
            # đệ quy hàm tree_file
            yield from tree_file(path, prefix=prefix + extension)


# cho người dùng nhập vào url
folder_url = input("-nhập url: ")
# chạy hàm tree_file và in cấu trúc file dạng tree
for line in tree_file(Path.home() / folder_url):
    print(line)

print("\n\n")
dem = 0
# thống kê file và ngôn ngữ trong file
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


# hàm kiểm tra module & library được import vào projects
def get_imports(path):
    # dọc file
    with open(path) as f:
        root = ast.parse(f.read(), path)
    # lặp qua danh sách các node con và kiểm tra
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):  # trả về True thì module = []
            module = []
        elif isinstance(node, ast.ImportFrom):  # trả về True thì module = node.module.split('.')
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            # in ra module và library
            yield Import(module, n.name.split('.'), n.asname)

for x in LST2:
    for imp in get_imports(x):
        print(imp)
