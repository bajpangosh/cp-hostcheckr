#!/bin/bash

# Configuration
PLUGIN_NAME="HostCheckr"
INSTALL_DIR="/usr/local/CyberCP/pluginInstaller"
REPO_URL="https://github.com/bajpangosh/cp-hostcheckr.git"
TEMP_DIR="cp-hostcheckr-temp"

echo "🚀 Starting HostCheckr installation..."

# 1. Navigate to installer directory
cd $INSTALL_DIR || { echo "❌ Error: Could not find CyberPanel installer directory."; exit 1; }

# 2. Clean previous artifacts
echo "cleaning up old files..."
rm -rf $TEMP_DIR
rm -rf $PLUGIN_NAME
rm -f "$PLUGIN_NAME.zip"

# 3. Clone Repository
echo "📦 Cloning repository..."
git clone $REPO_URL $TEMP_DIR > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Error: Git clone failed."
    exit 1
fi

# 4. Prepare directory structure
# Move the inner 'HostCheckr' folder out to the current directory
echo "📂 Preparing directory structure..."
if [ -d "$TEMP_DIR/$PLUGIN_NAME" ]; then
    mv "$TEMP_DIR/$PLUGIN_NAME" .
else
    echo "❌ Error: Plugin folder '$PLUGIN_NAME' not found in repository."
    rm -rf $TEMP_DIR
    exit 1
fi

# 5. Create Zip Archive
echo "🤐 Zipping plugin..."
zip -r "$PLUGIN_NAME.zip" $PLUGIN_NAME > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Error: Zip failed. Please install zip (apt install zip / yum install zip)."
    rm -rf $TEMP_DIR
    rm -rf $PLUGIN_NAME
    exit 1
fi

# 6. Cleanup temp files
rm -rf $TEMP_DIR
rm -rf $PLUGIN_NAME

# 7. Run CyberPanel Installer
echo "💿 Running CyberPanel Installer..."
python3 pluginInstaller.py install --pluginName $PLUGIN_NAME

# 8. Set Permissions (Critical Fix)
echo "🔒 Fixing permissions..."
chown -R cyberpanel:cyberpanel "/usr/local/CyberCP/$PLUGIN_NAME"
chmod -R 755 "/usr/local/CyberCP/$PLUGIN_NAME"
systemctl restart lscpd

echo "✅ Installation Complete! Check CyberPanel sidebar."
