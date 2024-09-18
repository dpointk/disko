import os
import re

def find_flask_servers(directory="backend"):
    """Recursively find Flask servers by scanning Python files."""
    print(f"Scanning directory: {os.path.abspath(directory)}")
    flask_servers = []
    flask_import_pattern = re.compile(r'^\s*(from\s+flask\s+import\s+.*|import\s+flask.*)', re.MULTILINE)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if re.search(flask_import_pattern, content):
                            flask_servers.append(file_path)
                            print(f"Found Flask server candidate in: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return flask_servers

if __name__ == "__main__":
    # Find all Flask servers
    flask_servers = find_flask_servers()
    
    if not flask_servers:
        print("No Flask servers found.")
    else:
        print(f"Discovered {len(flask_servers)} Flask server(s).")
