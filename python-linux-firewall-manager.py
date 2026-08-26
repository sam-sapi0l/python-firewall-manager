import subprocess
import os
import sys


from datetime import datetime
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / "backups"

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

def get_available_chains():
    success, output = run_command([
        "iptables",
        "-L",
        "-n"
    ])

    if not success:
        print("Failed to retrieve available chains.")
        return []

    chains = []

    for line in output.splitlines():
        if line.startswith("Chain "):
            parts = line.split()

            if len(parts) >= 2:
                chains.append(parts[1])

    return chains


def get_chain():
    chains = get_available_chains()

    if not chains:
        print("No chains available.")
        return None

    print("\n===== AVAILABLE CHAINS =====")

    for index, chain_name in enumerate(chains, start=1):
        print(f"{index} - {chain_name}")

    try:
        choice = int(input("Select chain: "))
    except ValueError:
        print("Selection must be an integer.")
        return None

    if choice < 1 or choice > len(chains):
        print("Invalid chain number.")
        return None

    return chains[choice - 1]

def list_rules(chain=None):
    command = [
        "iptables",
        "-L"
    ]

    if chain is not None:
        available_chains = get_available_chains()

        if chain not in available_chains:
            print("Chain does not exist.")
            return

        command.append(chain)

    command.extend([
        "-n",
        "-v",
        "--line-numbers"
    ])

    success, output = run_command(command)

    if success:
        print(output)
    else:
        print("Failed to list rules.")
        print(output)


def create_rule():
    chain = get_chain()

    if chain is None:
        return

    protocol = input("Protocol (tcp/udp): ").lower()

    if protocol not in ["tcp", "udp"]:
        print("Invalid protocol. Please enter either tcp or udp.")
        return

    try:
        port = int(input("Port: "))

    except ValueError:
        print("Port must be an integer.")
        return

    if port < 1 or port > 65535:
        print("Port must be between 1 and 65535.")
        return

    action = input("Action (ACCEPT/DROP): ").upper()

    if action not in ["ACCEPT", "DROP"]:
        print("Invalid action.  Please enter either ACCEPT or DROP.")
        return


    command =[
        "iptables",
        "-A",
        chain,
        "-p",
        protocol,
        "--dport",
        str(port),
        "-j",
        action
    ]

    print("Command to be executed:")
    print(" ".join(command))

    confirm = input("Apply this rule? (y/n): ").lower()

    if confirm != "y":
        print("Operation cancelled.")
        return

    if not backup_rules():
        print("Rule creation aborted because backup failed.")
        return

    success, output = run_command(command)

    if success:
        print("Rule created successfully.")

        write_audit_log(
            f"CREATE chain={chain} protocol={protocol} port={port} action={action}"
)

        if output:
            print(output)
    else:
        print("Failed to create rule.")

        if output:
            print(output)


def update_rule():
    chain = get_chain()

    if chain is None:
        return

    try:
        rule_number = int(input("Rule number: "))
    except ValueError:
        print("Rule number must be an integer.")
        return

    if rule_number < 1:
        print("Rule number must be greater than zero.")
        return

    protocol = input("Protocol (tcp/udp): ").lower()

    if protocol not in ["tcp", "udp"]:
        print("Invalid protocol.")
        return

    try:
        port = int(input("Port: "))
    except ValueError:
        print("Port must be an integer.")
        return

    if port < 1 or port > 65535:
        print("Port must be between 1 and 65535.")
        return

    action = input("Action (ACCEPT/DROP): ").upper()

    if action not in ["ACCEPT", "DROP"]:
        print("Invalid action.")
        return

    command = [
        "iptables",
        "-R",
        chain,
        str(rule_number),
        "-p",
        protocol,
        "--dport",
        str(port),
        "-j",
        action
    ]

    print("\n===== RULE UPDATE PREVIEW =====")
    print(" ".join(command))

    confirm = input("Update this rule? (y/n): ").lower()

    if confirm != "y":
        print("Operation cancelled.")
        return

    if not backup_rules():
        print("Rule update aborted because backup failed.")
        return

    success, output = run_command(command)

    if success:
        print("Rule updated successfully.")
        write_audit_log(
            f"UPDATE chain={chain} rule_number={rule_number} protocol={protocol} port={port} action={action}"
        )
        list_rules(chain)
    else:
        print("Failed to update rule.")

        if output:
            print(output)



def delete_rule():
    chain = get_chain()

    if chain is None:
        return

    try:
        rule_number = int(input("Rule number: "))
    except ValueError:
        print("Rule number must be an integer.")
        return

    if rule_number < 1:
        print("Rule number must be greater than zero.")
        return

    command = [
        "iptables",
        "-D",
        chain,
        str(rule_number)
    ]

    print("\n===== RULE PREVIEW =====")
    print(" ".join(command))

    confirm = input("Apply this rule? (y/n): ").lower()

    if confirm != "y":
        print("Operation cancelled.")
        return

    if not backup_rules():
        print("Rule deletion aborted because backup failed.")
        return
    
    success, output = run_command(command)


    if success:
        print("Rule deleted successfully.")

        write_audit_log(
           f"DELETE chain={chain} rule_number={rule_number}"
        )

        list_rules(chain)

    else:
        print("Failed to delete rule.")
        print(output)


def backup_rules():
    BACKUP_DIR.mkdir(exist_ok=True)

    success, output = run_command(["iptables-save"])

    if not success:
        print("Failed to backup rules.")
        print(output)
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = BACKUP_DIR / f"iptables_backup_{timestamp}.rules"

    try:
        with open(filename, "w") as backup_file:
            backup_file.write(output)
    except OSError as error:
        print(f"Failed to write backup file: {error}")
        return False

    print(f"Backup created successfully: {filename}")
    write_audit_log(
        f"BACKUP file={filename.name}"
    )

    return True

    

def restore_rules():
    backups = sorted(BACKUP_DIR.glob("*.rules"))

    if not backups:
        print("No backup files found.")
        return

    print("\n===== AVAILABLE BACKUPS =====")

    for index, backup in enumerate(backups, start=1):
        print(f"{index} - {backup.name}")

    try:
        choice = int(input("Select backup: "))
    except ValueError:
        print("Selection must be an integer.")
        return

    if choice < 1 or choice > len(backups):
        print("Invalid backup number.")
        return

    selected_backup = backups[choice - 1]

    print(f"\nSelected backup: {selected_backup.name}")

    confirm = input("Restore this backup? (y/n): ").lower()

    if confirm != "y":
        print("Operation cancelled.")
        return

    if not backup_rules():
        print("Restore aborted because current rules could not be backed up.")
        return

    try:
        with open(selected_backup, "r") as backup_file:
            result = subprocess.run(
                ["iptables-restore"],
                stdin=backup_file,
                capture_output=True,
                text=True,
                check=False
            )

    except OSError as error:
        print(f"Failed to open backup file: {error}")
        return

    if result.returncode == 0:
        print("Rules restored successfully.")

        write_audit_log(
            f"RESTORE file={selected_backup.name}"
        )

        list_rules()
    else:
        print("Failed to restore rules.")

        if result.stderr:
            print(result.stderr)


def write_audit_log(message):
    log_dir = BASE_DIR / "logs"

    try:
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "iptables_manager.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a") as file:
            file.write(f"{timestamp} {message}\n")

    except OSError as error:
        print(f"Warning: failed to write audit log: {error}")

def menu_options():
    while True:
        print("\n===== IPTABLES MANAGER =====")
        print("1 - List rules")
        print("2 - Create rule")
        print("3 - Update rule")
        print("4 - Delete rule")
        print("5 - Backup rules")
        print("6 - Restore rules")
        print("0 - Exit")

        option = input("Option: ")

        if option == "1":
            list_rules()
        elif option == "2":
            create_rule()
        elif option == "3":
            update_rule()
        elif option == "4":
            delete_rule()
        elif option == "5":
            backup_rules()
        elif option == "6":
            restore_rules()
        elif option == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option.")


if not check_root():
    sys.exit(1)


menu_options()
