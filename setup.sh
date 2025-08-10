#!/bin/bash

# WhatsApp Bulk Sender Setup Script

echo "🚀 Setting up WhatsApp Bulk Message Sender..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully!"
else
    echo "❌ Failed to install packages. Please check the error messages above."
    exit 1
fi

# Create sample files
echo "📄 Creating sample files..."
python3 -c "
from whatsapp_bulk_sender import WhatsAppBulkSender
sender = WhatsAppBulkSender()
sender.create_sample_contacts_file('sample_contacts.csv')
print('✅ Sample CSV created: sample_contacts.csv')
"

# Make CLI script executable
chmod +x cli.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure you're logged into WhatsApp Web on your default browser"
echo "2. Edit sample_contacts.csv with your actual contacts"
echo "3. Test with a single message: python3 cli.py single \"+911234567890\" \"Test message\""
echo "4. Send bulk messages: python3 cli.py csv sample_contacts.csv --message \"Hello {name}!\""
echo ""
echo "📖 For more help, check the README.md file or run: python3 whatsapp_bulk_sender.py"
