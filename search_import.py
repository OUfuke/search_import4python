import re
import glob
import pathlib

import_list = []


def remove_head_space(line):
    line = re.sub(r"^\s*", "", line)
    return line


def remove_space(line):
    line = re.sub(r"\s*", "", line)
    return line


def check_import(line):
    """
    Get import package from line.
    """
    line = remove_head_space(line)
    if re.match(r"^import\s", line):
        line = re.sub(r"^import\s*", "", line)
        line = line.split(" as ")[0]
        line = remove_space(line)
        return line
    elif re.match(r"^from\s", line):
        line = re.sub(r"^from\s*", "", line)
        line = line.split(" import ")[0]
        line = remove_space(line)
        return line
    return 0


def add_package_list(packages):
    """
    Add package to import_list.
    """
    package_list = packages.split(",")
    for package in package_list:
        master_slave = package.split(".")
        if not(master_slave in import_list):
            import_list.append(master_slave)


def show_tree(import_list=import_list):
    """
    Tree view from import_list.
    """
    import_list = sorted(import_list)
    stock = []
    for package in import_list:
        num = len(set(stock) & set(package))
        for i in range(num, len(package)):
            if i > 0:
                print("\t  " * (i - 1) + "\t\_", end="")
            print(package[i])
        stock = package


def files_list(path):
    """
    Get python file in folder.
    """
    if pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path))
    else:
        path = str(pathlib.Path(path).resolve())
    python_file_list = glob.glob(path + "/**/*.py", recursive=True)
    return python_file_list


if __name__ == "__main__":
    python_file_list = files_list("../hoge_dir")
    for file in python_file_list:
        with open(file) as f:
            for line in f:
                packages = check_import(line)
                if packages:
                    add_package_list(packages)
    show_tree()
