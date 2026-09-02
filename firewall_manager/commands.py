import os
import subprocess

def check_root():
    if os.geteuid() != 0:
        print("This program must be executed as root.")
        print("Run: sudo python3 iptables_manager.py")
        return False

    return True

def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            return True, result.stdout

        return False, result.stderr

    except FileNotFoundError as error:
        return False, f"Command not found: {error}"