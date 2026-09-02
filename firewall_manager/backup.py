from pathlib import Path
from datetime import datetime
import subprocess

from firewall_manager.commands import run_command
from firewall_manager.audit import write_audit_log


BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = BASE_DIR / "backups"


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

  #      list_rules()
    else:
        print("Failed to restore rules.")

        if result.stderr:
            print(result.stderr)