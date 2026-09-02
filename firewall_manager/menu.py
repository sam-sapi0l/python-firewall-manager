<<<<<<< HEAD
from firewall_manager.rules import (
    list_rules,
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
=======
from firewall_manager.rules import (
    list_rules,
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
>>>>>>> 5b5421398db67d5734fc71484739817a178ba918
            print("Invalid option.")