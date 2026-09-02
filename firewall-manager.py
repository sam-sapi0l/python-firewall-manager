<<<<<<< HEAD
import sys

from firewall_manager.menu import menu_options
from firewall_manager.commands import check_root


def main():
    if not check_root():
        sys.exit(1)

    menu_options()

if __name__ == "__main__":
=======
import sys

from firewall_manager.menu import menu_options
from firewall_manager.commands import check_root


def main():
    if not check_root():
        sys.exit(1)

    menu_options()

if __name__ == "__main__":
>>>>>>> 5b5421398db67d5734fc71484739817a178ba918
    main()