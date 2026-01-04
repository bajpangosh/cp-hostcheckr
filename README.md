# HostCheckr - CyberPanel Optimization Plugin

A robust resource optimization plugin for CyberPanel that integrates directly with Linux/LiteSpeed/MariaDB to monitor and clean your server.

## Features
- **Real-Time Monitoring**: CPU, RAM, Disk usage.
- **Smart Scoring**: 0-100 Health Score with color-coded status.
- **One-Click Fix**:
  - Drops filesystem cache (PageCache/Dentries).
  - Optimizes MariaDB tables (`mysqlcheck -a`).
  - Resycles LiteSpeed PHP processes (`killall lsphp`).
  - Flushes Redis cache (if detected).
- **Responsive UI**: Bootstrap 5 dashboard with AJAX updates.

## Quick Installation
Run this single command as root to install or update the plugin automatically:

```bash
wget -O - https://raw.githubusercontent.com/bajpangosh/cp-hostcheckr/main/install.sh | bash
```

This script handles cloning, directory structuring, zipping, installing, and permission fixing for you.

## Uninstalling
To remove the plugin:

```bash
cd /usr/local/CyberCP/pluginInstaller
python3 pluginInstaller.py remove --pluginName HostCheckr
```
