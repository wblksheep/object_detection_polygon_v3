import os

def print_directory_structure(start_path="."):
    start_path = os.path.abspath(start_path)  # 获取绝对路径
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}{os.sep}")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

print_directory_structure()
