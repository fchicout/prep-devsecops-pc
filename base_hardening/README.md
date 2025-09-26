# Role: base_hardening

This role performs basic security hardening on Debian-based systems (like Debian and Ubuntu). It is designed to be idempotent and apply a baseline set of security configurations to reduce the attack surface of a server.

The primary tasks performed by this role include:
- Updating all system packages to their latest versions.
- Installing security-related tools like `fail2ban` and `auditd`.
- Configuring `fail2ban` to protect against brute-force attacks on services like SSH.
- Applying a comprehensive set of `auditd` rules based on industry benchmarks (CIS, STIG) to log security-relevant events.

Requirements
------------

This role is designed for Debian-based distributions. You will need `sudo` access on the target machine for the role to apply system-level changes.

Role Variables
--------------

The following variables can be overridden to customize the `fail2ban` configuration. They are defined in `defaults/main.yml`.

`fail2ban_bantime`
: Specifies the duration for which an IP address is banned.
: Default: `1h`

`fail2ban_maxretry`
: The number of failed login attempts before an IP address is banned.
: Default: `5`

Fail2ban Configuration
----------------------

This role installs and configures `fail2ban`, an intrusion prevention framework that protects servers from brute-force attacks.

`fail2ban` works by monitoring log files (e.g., `/var/log/auth.log`) for specific patterns, such as repeated failed login attempts. When a malicious IP address is detected, `fail2ban` automatically updates the system's firewall rules to block it for a configured amount of time.

This role specifically enables protection for the **SSH service (`sshd`)**. It creates a local configuration file (`/etc/fail2ban/jail.local`) to enable the SSH jail and apply the `bantime` and `maxretry` settings.

The key settings are:
- **`bantime`**: How long an IP is banned (default `1h`).
- **`maxretry`**: How many failed attempts trigger a ban (default `5`).

These can be easily customized by overriding the role variables, as shown in the "Example Playbook" section.

Auditd Configuration
--------------------

This role configures the Linux Audit Daemon (`auditd`) by applying a comprehensive ruleset. The rules are sourced from the Neo23x0/auditd project and are included in this repository as a **git submodule**. This approach ensures that the role uses a specific, version-controlled set of rules, making the hardening process stable and repeatable without requiring an internet connection on the target machine during execution.

The ruleset is a combination of best practices from the Center for Internet Security (CIS) benchmarks and the Security Technical Implementation Guides (STIG).

The applied rules provide extensive logging for a wide range of security-relevant activities, including:

*   **Identity and Access Management:**
    *   Changes to user/group information (`/etc/passwd`, `/etc/shadow`, etc.).
    *   Modifications to discretionary access control permissions (`chmod`, `chown`).
*   **System Integrity:**
    *   Events that modify the system's date and time.
    *   Changes to the system's network environment (`sethostname`, `/etc/hosts`).
    *   Loading and unloading of kernel modules.
    *   Mount and unmount operations.
*   **Suspicious Activity:**
    *   Use of privileged commands (`sudo`, `su`).
    *   Attempts to access files with failed permissions (access denied).
    *   File deletion events by specific user IDs.
*   **Log Monitoring:**
    *   Modifications to the audit logs themselves (`/var/log/audit/`).

Each audit event is tagged with a key (e.g., `time-change`, `identity`, `logins`) to make searching and analysis easier. For a complete list of all rules, you can inspect the source file at `/etc/audit/audit.rules` on a system where this role has been applied.

> **Note:** The `auditd` service is configured to restart upon rule changes, ensuring the new policy is applied immediately. Since the auditd rules are a git submodule, you must clone this repository using the `--recurse-submodules` flag to ensure the rule files are downloaded:
> ```bash
> git clone --recurse-submodules <repository-url>
> ```

Dependencies
------------

This role has no dependencies on other Ansible Galaxy roles.

Example Playbook
----------------

Here is an example of how to use this role in a playbook.

### Default Usage

```yaml
- hosts: all
  become: yes
  roles:
    - ufpe.base_hardening
```

### With Custom Variables

To customize the `fail2ban` settings, you can pass variables to the role.

```yaml
- hosts: all
  become: yes
  roles:
    - role: ufpe.base_hardening
      fail2ban_bantime: 24h
      fail2ban_maxretry: 3
```

License
-------

MIT

Author Information
------------------
This role was created by Fabio Chicout as part of a project for the Federal University of Pernambuco (UFPE).
