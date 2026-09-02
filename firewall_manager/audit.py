<<<<<<< HEAD
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"


def write_audit_log(message):
    try:
        LOG_DIR.mkdir(exist_ok=True)

        log_file = LOG_DIR / "iptables_manager.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a") as file:
            file.write(f"{timestamp} {message}\n")

    except OSError as error:
=======
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"


def write_audit_log(message):
    try:
        LOG_DIR.mkdir(exist_ok=True)

        log_file = LOG_DIR / "iptables_manager.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a") as file:
            file.write(f"{timestamp} {message}\n")

    except OSError as error:
>>>>>>> 5b5421398db67d5734fc71484739817a178ba918
        print(f"Warning: failed to write audit log: {error}")