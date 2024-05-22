import os
import fnmatch

def load_gitignore_patterns(gitignore_path):
    with open(gitignore_path, 'r') as file:
        patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return patterns

def is_ignored(path, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, os.path.join('**', pattern)):
            return True
    return False

def write_markdown(output_file, root_dir, gitignore_patterns):
    with open(output_file, 'w') as markdown_file:
        for root, dirs, files in os.walk(root_dir):
            # Create relative path from root directory for pattern matching
            rel_root = os.path.relpath(root, root_dir)
            # Filter out directories to be ignored
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(rel_root, d), gitignore_patterns)]

            for file in files:
                rel_file = os.path.join(rel_root, file)
                if file.endswith('.py') and not is_ignored(rel_file, gitignore_patterns):
                    file_path = os.path.join(root, file)
                    markdown_file.write(f'## {file_path}\n\n')
                    try:
                        with open(file_path, 'r', errors='ignore') as py_file:
                            content = py_file.read()
                            markdown_file.write(f'```python\n{content}\n```\n\n')
                    except Exception as e:
                        markdown_file.write(f'Error reading file {file_path}: {e}\n\n')

def main():
    root_directory = '.'  # Change this to the directory you want to start the tree from
    output_file = 'python_files.md'
    gitignore_path = os.path.join(root_directory, '.gitignore')

    gitignore_patterns = []
    if os.path.exists(gitignore_path):
        gitignore_patterns = load_gitignore_patterns(gitignore_path)

    write_markdown(output_file, root_directory, gitignore_patterns)

if __name__ == '__main__':
    main()
