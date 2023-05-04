import os
from treelib import Node, Tree

def generate_tree(path, parent, tree, ignored_directories=None):
    if ignored_directories is None:
        ignored_directories = []

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and item in ignored_directories:
            continue

        node = tree.create_node(item, parent=parent)
        if os.path.isdir(item_path):
            generate_tree(item_path, node.identifier, tree, ignored_directories)

def print_directory_tree(start_path, ignored_directories=None):
    tree = Tree()
    tree.create_node(start_path, "root")
    generate_tree(start_path, "root", tree, ignored_directories)
    tree.show()

if __name__ == "__main__":
    start_path = "."
    ignored_directories = ['venv','.git']
    print_directory_tree(start_path, ignored_directories)
