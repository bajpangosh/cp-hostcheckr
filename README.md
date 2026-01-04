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

## Installation

To install **HostCheckr** using the official CyberPanel plugin installer, follow these steps to ensure the directory structure is correct.

### Step 1: Prepare the Plugin Package
SSH into your server and run the following commands to create a compatible `HostCheckr.zip`.

```bash
# Go to the installer directory
cd /usr/local/CyberCP/pluginInstaller/

# Remove any old versions
rm -rf cp-hostcheckr
rm -rf HostCheckr
rm -f HostCheckr.zip

# Clone the latest code
git clone https://github.com/bajpangosh/cp-hostcheckr.git cp-hostcheckr

# Move the plugin app folder to the current directory
mv cp-hostcheckr/HostCheckr .

# Create the zip archive required by the installer
# (You may need to install zip: apt install zip -y or yum install zip -y)
zip -r HostCheckr.zip HostCheckr

# Cleanup
rm -rf cp-hostcheckr
rm -rf HostCheckr
```

### Step 2: Run the Installer
Now that `HostCheckr.zip` is ready, run the installer:

```bash
python3 pluginInstaller.py install --pluginName HostCheckr
```

## Uninstalling
To remove the plugin:

```bash
cd /usr/local/CyberCP/pluginInstaller
python3 pluginInstaller.py remove --pluginName HostCheckr
```
