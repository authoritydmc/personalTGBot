import subprocess
import json
import os
import platform
import getpass
import datetime
import sys

# Path to version.json file
DATA_FOLDER = "data"
VERSION_FILE_PATH = os.path.join(".","version.json")

# Function to execute a git command and return its output
def get_git_info(command):
    try:
        # Run the git command and capture the output
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        # Decode from bytes to string and strip any whitespace characters
        return output.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        # If an error occurs (e.g., not in a git repository), return None
        return None

# Function to generate Git version information
def generate_git_info():
    git_info = {}
    git_info['commit_hash'] = get_git_info("git rev-parse HEAD")
    git_info['branch_name'] = get_git_info("git rev-parse --abbrev-ref HEAD")
    git_info['tag'] = get_git_info("git describe --tags --abbrev=0")
    git_info['commit_date'] = get_git_info("git log -1 --format=%cd --date=iso-strict")
    git_info['remote_url'] = get_git_info("git config --get remote.origin.url")
    git_info['commit_count'] = get_git_info("git rev-list --count HEAD")
    git_info['versionID']=generate_version_id(git_info.get('tag'),git_info.get('commit_count'))
    return git_info

# Function to gather system information
def generate_system_info():
    system_info = {}
    system_info['os'] = platform.system()
    system_info['os_version'] = platform.version()
    system_info['platform'] = platform.platform()
    system_info['machine'] = platform.machine()
    system_info['processor'] = platform.processor()
    system_info['python_version'] = platform.python_version()
    system_info['python_implementation'] = platform.python_implementation()
    system_info['architecture'] = platform.architecture()[0]
    return system_info

# Function to gather environment and build information
def generate_build_info():
    build_info = {}
    build_info['username'] = getpass.getuser()
    build_info['hostname'] = platform.node()
    build_info['build_timestamp'] = datetime.datetime.utcnow().isoformat() + 'Z'  # UTC time in ISO format
    build_info['cwd'] = os.getcwd()
    
    # Optionally, include environment variables
    # Warning: Be cautious as this may include sensitive information
    # Uncomment the following lines if you need environment variables
    # build_info['environment'] = dict(os.environ)
    
    return build_info

# Function to generate the complete version information
def generate_version_info():
    version_info = {}
    version_info['git'] = generate_git_info()
    version_info['system'] = generate_system_info()
    version_info['build'] = generate_build_info()
    return version_info

# Function to save version info to JSON file
def save_version_info(version_info, file_path):
    # Ensure the directory exists before saving the file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the version information as JSON with indentation for readability
    with open(file_path, "w") as json_file:
        json.dump(version_info, json_file, indent=4)
    
    print(f"Version information saved to {file_path}")

# Function to parse the Git tag (e.g., "v1.0.0") and convert to integers
def parse_git_tag(tag):
    if tag and tag.startswith('v'):
        try:
            # Split the tag into major, minor, and patch parts
            major, minor, patch = map(int, tag[1:].split('.'))
            return major, minor, patch
        except ValueError:
            # If the tag doesn't follow the expected format, return default values
            return 0, 0, 0
    return 0, 0, 0

# Function to generate the integer-based version ID
def generate_version_id(tag, commit_count):
    major, minor, patch = parse_git_tag(tag)
    try:
        commit_count = int(commit_count)
    except (ValueError, TypeError):
        commit_count = 0

    # Calculate the integer-based version ID
    version_id = (major * 10000) + (minor * 100) + patch + commit_count
    return version_id

# Function to load version info from JSON file
def load_version_info(file_path=VERSION_FILE_PATH):
    """Load version information from a JSON file."""
    if not os.path.exists(file_path):
        print(f"Version file {file_path} does not exist.")
        return None
    
    try:
        with open(file_path, "r") as json_file:
            version_info = json.load(json_file)
        print(f"Version information loaded from {file_path}")
        return version_info
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading {file_path}: {e}")
        return None

# Main function to generate and save version info
def main():
    # Check if the user wants to generate or load version info
    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate":
            version_info = generate_version_info()
            json_file_path = VERSION_FILE_PATH
            save_version_info(version_info, json_file_path)
        elif sys.argv[1] == "--load":
            version_info = load_version_info()
            if version_info:
                print(json.dumps(version_info, indent=4))
        else:
            print("Usage:")
            print("  python version.py --generate  # To generate version.json")
            print("  python version.py --load      # To load and display version.json")
    else:
        # Default action is to generate version.json
        version_info = generate_version_info()
        json_file_path = VERSION_FILE_PATH
        save_version_info(version_info, json_file_path)

if __name__ == "__main__":
    main()
