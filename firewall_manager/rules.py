from firewall_manager.commands import run_command
from firewall_manager.audit import write_audit_log
from firewall_manager.backup import backup_rules


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