import os
import fnmatch
from pathlib import Path

# Function to read .gitignore and create ignore patterns
def read_gitignore(gitignore_path=".gitignore"):
    ignore_patterns = []
    with open(gitignore_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ignore_patterns.append(line)
    return ignore_patterns

# Function to check if a path is ignored
def is_ignored(path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

# Recursive function to mimic the `tree` command
def display_tree(root, ignore_patterns, prefix=""):
    contents = sorted(os.listdir(root))
    
    for i, name in enumerate(contents):
        path = os.path.join(root, name)
        if is_ignored(path, ignore_patterns):
            continue
        
        connector = "└── " if i == len(contents) - 1 else "├── "
        print(prefix + connector + name)
        
        if os.path.isdir(path):
            new_prefix = "    " if i == len(contents) - 1 else "│   "
            display_tree(path, ignore_patterns, prefix + new_prefix)


def tree_excluding_gitignore():
    """
    Function to display the directory structure of the current directory excluding .gitignore patterns
    """
    root_dir = "."  # You can change this to the root directory you want
    gitignore_path = os.path.join(root_dir, ".gitignore")
    
    if not os.path.exists(gitignore_path):
        print("No .gitignore file found in the root directory.")
        return
    
    ignore_patterns = read_gitignore(gitignore_path)
    print(f"Directory structure of {os.path.abspath(root_dir)} (excluding .gitignore patterns):\n")
    display_tree(root_dir, ignore_patterns)

if __name__ == "__main__":
    tree_excluding_gitignore()
