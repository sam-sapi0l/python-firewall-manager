from firewall_manager.rules import (
    list_rules,
    list_chains,
    create_rule,
    update_rule,
    delete_rule,
)
from firewall_manager.backup import (
    backup_rules,
    restore_rules,
)


def menu_options():
    while True:
        print("\n===== IPTABLES MANAGER =====")
        print("1 - List rules")
        print("2 - List chains")
        print("3 - Create rule")
        print("4 - Update rule")
        print("5 - Delete rule")
        print("6 - Backup rules")
        print("7 - Restore rules")
        print("0 - Exit")

        option = input("Option: ")

        if option == "1":
            list_rules()
        elif option == "2":
            list_chains()
        elif option == "3":
            create_rule()
        elif option == "4":
            update_rule()
        elif option == "5":
            delete_rule()
        elif option == "6":
            backup_rules()
        elif option == "7":
            restore_rules()
        elif option == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option.")