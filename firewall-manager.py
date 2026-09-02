import sys

from firewall_manager.menu import menu_options
from firewall_manager.commands import check_root


def main():
    if not check_root():
        sys.exit(1)

    menu_options()

if __name__ == "__main__":
    main()