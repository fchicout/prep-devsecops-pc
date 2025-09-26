# Role: base_hardening

This role performs basic security hardening on Debian-based systems (like Debian and Ubuntu). It is designed to be idempotent and apply a baseline set of security configurations to reduce the attack surface of a server.

The primary tasks performed by this role include:
- Updating all system packages to their latest versions.
- Installing security-related tools like `fail2ban`.
- Configuring `fail2ban` to protect against brute-force attacks on services like SSH.

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
