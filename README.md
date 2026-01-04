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

## Installation via CyberPanel Plugin Installer

### Step 1: Package the Plugin
You need to create a zip archive of the repository.
1. Download the code as a ZIP file from GitHub (or zip your local folder).
2. **Important**: Rename the zip file to `HostCheckr.zip`.

### Step 2: Upload to Server
Upload `HostCheckr.zip` to your CyberPanel server in the directory:
`/usr/local/CyberCP/pluginInstaller`

You can upload the file manually, **OR** simply download it directly on the server:

```bash
cd /usr/local/CyberCP/pluginInstaller
wget https://github.com/bajpangosh/cp-hostcheckr/archive/refs/heads/main.zip -O HostCheckr.zip
```

### Step 3: Run the Installer
SSH into your server and execute the official installer script:

```bash
cd /usr/local/CyberCP/pluginInstaller
python3 pluginInstaller.py install --pluginName HostCheckr
```

## Uninstalling
To remove the plugin:

```bash
cd /usr/local/CyberCP/pluginInstaller
python3 pluginInstaller.py remove --pluginName HostCheckr
```
