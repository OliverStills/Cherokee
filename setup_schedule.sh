#!/bin/bash

# Setup script for scheduling the AI News Digest to run daily at 7 AM

echo "AI News Digest - Schedule Setup"
echo "================================"
echo ""

# Get the absolute path to the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/ai_news_digest.py"
ENV_FILE="$SCRIPT_DIR/.env"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure your settings."
    exit 1
fi

# Find Python executable
PYTHON_CMD=$(which python3)
if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: python3 not found!"
    exit 1
fi

echo "Python found at: $PYTHON_CMD"
echo "Script location: $PYTHON_SCRIPT"
echo ""

# Create a wrapper script that loads the .env file
WRAPPER_SCRIPT="$SCRIPT_DIR/run_digest.sh"
cat > "$WRAPPER_SCRIPT" << EOF
#!/bin/bash
# Auto-generated wrapper script for AI News Digest

# Load environment variables
export \$(grep -v '^#' "$ENV_FILE" | xargs)

# Run the Python script
cd "$SCRIPT_DIR"
"$PYTHON_CMD" "$PYTHON_SCRIPT" >> "$SCRIPT_DIR/digest.log" 2>&1
EOF

chmod +x "$WRAPPER_SCRIPT"

echo "Created wrapper script at: $WRAPPER_SCRIPT"
echo ""

# Create cron entry
CRON_ENTRY="0 7 * * * $WRAPPER_SCRIPT"

echo "Setting up cron job to run daily at 7:00 AM..."
echo ""
echo "Cron entry to be added:"
echo "  $CRON_ENTRY"
echo ""

# Check if cron entry already exists
if crontab -l 2>/dev/null | grep -q "$PYTHON_SCRIPT"; then
    echo "WARNING: A cron entry for this script already exists."
    echo "Please check your crontab with: crontab -l"
    echo ""
    read -p "Do you want to continue and potentially create a duplicate? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted. No changes made."
        exit 0
    fi
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

if [ $? -eq 0 ]; then
    echo "✓ Cron job successfully added!"
    echo ""
    echo "Your AI News Digest will run every day at 7:00 AM."
    echo ""
    echo "To view your cron jobs: crontab -l"
    echo "To remove this job: crontab -e (then delete the line)"
    echo ""
    echo "Logs will be saved to: $SCRIPT_DIR/digest.log"
    echo ""
    echo "To test the script manually, run:"
    echo "  $WRAPPER_SCRIPT"
else
    echo "✗ Failed to add cron job."
    echo "You can manually add this line to your crontab with 'crontab -e':"
    echo "  $CRON_ENTRY"
fi

echo ""
echo "Setup complete!"
