# python-firewall-manager
Python CLI for managing Linux iptables firewall rules with backup, restore and audit logging.

# Linux iptables Firewall Manager

A Python-based command-line tool for managing Linux `iptables` firewall rules in a simpler and safer way.

The project was developed as a practical exercise in Python automation, Linux system administration, and security operations. It provides an interactive CLI for common firewall management tasks while adding validation, automatic backups, restore capabilities, and audit logging.

> **Status:** v0.1.0  
> **Environment:** Linux  
> **Purpose:** Educational, lab, and portfolio project

---

## Features

- List current `iptables` rules
- Display rule numbers for easier management
- Dynamic discovery of existing chains
- Support for built-in and existing custom chains
- Create firewall rules
- Update existing rules
- Delete rules by rule number
- Validate protocols, ports, chains, and rule numbers
- Preview commands before applying changes
- Require confirmation before modifications
- Automatically back up the current firewall configuration before changes
- Create manual timestamped backups
- Restore previous firewall configurations
- Maintain an audit log of operations
- Validate root privileges before execution
- Handle command and filesystem errors

---

## How It Works

The application acts as a CLI management layer over Linux `iptables`.

```text
              ┌─────────────────────┐
              │   Firewall Manager  │
              │     Python CLI      │
              └──────────┬──────────┘
                         │
             ┌───────────┴───────────┐
             │ Validation / Preview  │
             │ Confirmation / Backup │
             └───────────┬───────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     iptables       iptables-save  iptables-restore
          │              │              │
          └──────────────┼──────────────┘
                         │
                    Netfilter
```

Python executes system commands through `subprocess` without relying on `shell=True`.

Before modifying firewall rules, the application creates a backup of the current configuration using `iptables-save`.

Backups can later be restored using `iptables-restore`.

---

## Requirements

- Linux
- Python 3
- `iptables`
- Root privileges

Check your Python installation:

```bash
python3 --version
```

Check `iptables`:

```bash
iptables --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/firewall-manager.git
```

Enter the project directory:

```bash
cd firewall-manager
```

Run the application with root privileges:

```bash
sudo python3 firewall_manager.py
```

Root privileges are required because modifying Linux firewall rules is a privileged operation.

---

## Usage

When started, the application presents an interactive menu:

```text
===== IPTABLES MANAGER =====
1 - List rules
2 - Create rule
3 - Update rule
4 - Delete rule
5 - Backup rules
6 - Restore rules
0 - Exit
```

### Listing rules

The application lists current firewall rules using:

```bash
iptables -L -n -v --line-numbers
```

Rule numbers are displayed so individual rules can later be updated or removed.

### Creating a rule

The user selects an existing chain and provides:

```text
Chain
Protocol
Destination port
Action
```

Example:

```text
Chain: INPUT
Protocol: tcp
Port: 443
Action: ACCEPT
```

Equivalent `iptables` operation:

```bash
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

Before execution, the application:

1. validates the provided values;
2. displays the command;
3. requests confirmation;
4. creates a firewall backup;
5. executes the change;
6. records the operation in the audit log.

### Updating a rule

Existing rules can be replaced using their rule number.

Internally, this uses:

```bash
iptables -R
```

Example:

```bash
iptables -R INPUT 2 -p tcp --dport 8443 -j ACCEPT
```

> `iptables -R` replaces the entire selected rule rather than modifying only one attribute.

### Deleting a rule

Rules can be removed by selecting the chain and rule number.

Example:

```bash
iptables -D INPUT 3
```

A backup is automatically created before deletion.

---

## Dynamic Chain Discovery

The application does not rely only on the default:

```text
INPUT
FORWARD
OUTPUT
```

It dynamically discovers chains currently available in `iptables`.

This allows the manager to operate on existing custom chains such as:

```text
DOCKER
DOCKER-USER
SSH_GUARD
LOG_DROP
```

Custom chain creation and deletion are not currently implemented.

---

## Backup and Restore

Backups are generated using:

```bash
iptables-save
```

and stored inside:

```text
backups/
```

with timestamped filenames:

```text
iptables_backup_20260826_163010.rules
```

Before create, update, delete, or restore operations, the current firewall state is automatically backed up.

Previous configurations can be restored through:

```bash
iptables-restore
```

The Python implementation provides the selected backup through the process standard input rather than using shell redirection.

---

## Audit Logging

Successful firewall operations are recorded under:

```text
logs/iptables_manager.log
```

Example:

```text
2026-08-26 16:30:10 BACKUP file=iptables_backup_20260826_163010.rules
2026-08-26 16:30:10 CREATE chain=INPUT protocol=tcp port=443 action=ACCEPT
2026-08-26 16:32:45 UPDATE chain=INPUT rule_number=2 protocol=tcp port=8443 action=ACCEPT
2026-08-26 16:35:20 DELETE chain=INPUT rule_number=3
2026-08-26 16:38:02 RESTORE file=iptables_backup_20260826_163010.rules
```


---

## Project Structure

```text
firewall-manager/
│
├── firewall_manager.py
├── README.md
├── .gitignore
│
├── backups/
│   └── generated at runtime
│
└── logs/
    └── generated at runtime
```

## Safety Considerations

Firewall modifications can interrupt network connectivity or block administrative access.

For this reason, the project implements:

- root privilege validation;
- input validation;
- command previews;
- explicit confirmation before changes;
- automatic backups before modifications;
- restore functionality;
- audit logging.

When testing remotely over SSH, special care should be taken when modifying `INPUT` rules related to the active SSH connection.

---

## Current Limitations

Version `0.1.0` intentionally focuses on basic `iptables` filter-rule management.

The current version does not provide:

- source or destination CIDR configuration;
- network interface selection;
- connection-state / conntrack rules;
- NAT management;
- `mangle` or `raw` table management;
- custom chain creation/deletion;
- IPv6 management;
- native `nftables` management;
- firewall persistence across reboot;
- automated tests;
- package installation.

These limitations are intentional to keep the first release focused and auditable.

---

## Roadmap

Possible improvements for future releases include:

### v0.2

- Source and destination IP/CIDR support
- Input/output interface selection
- Custom chain creation and deletion
- Rule comments
- Improved rule inspection
- Duplicate-rule detection
- Enhanced audit events

### Future

- `nftables` support
- IPv6 support
- Persistent configuration management
- Configuration files
- Automated testing
- Packaging
- Additional safety and rollback mechanisms

---

## Development Goals

This project was created to practice and demonstrate practical skills involving:

- Python
- Linux administration
- Security automation
- Firewall administration
- `subprocess`
- File handling
- Exception handling
- Input validation
- CLI development
- Backup and recovery concepts
- Audit logging
- Git-based software development

The goal is not to replace native Linux firewall tooling, but to explore how Python can be used to build safer and more structured administrative automation around existing system utilities.

---

## Disclaimer

This project is intended for educational, lab, and portfolio purposes.

It has not been validated for production environments. Incorrect firewall rules can result in loss of connectivity or unintended security exposure.

Always review changes and maintain an independent recovery method when testing firewall configurations.
