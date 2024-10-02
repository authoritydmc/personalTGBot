import subprocess
import json
import os
import platform
import getpass
import datetime
import sys

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

# Main function to generate and save version info
def main():
    version_info = generate_version_info()
    json_file_path = "data/version.json"
    save_version_info(version_info, json_file_path)

if __name__ == "__main__":
    main()
