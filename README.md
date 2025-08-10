# WhatsApp Bulk Message Sender

A comprehensive Python application for sending bulk WhatsApp messages using the pywhatkit library. This tool allows you to send personalized messages to multiple contacts from CSV or Excel files.

## Features

- 🚀 **Bulk messaging** from CSV and Excel files
- 📱 **Single message** sending
- 🎯 **Message personalization** with name placeholders
- ⏰ **Scheduled messaging** for specific times
- 📊 **Progress tracking** and error handling
- 🔧 **Command-line interface** for easy automation
- 📝 **Comprehensive logging** for monitoring
- 🛡️ **Phone number formatting** with country code support

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd whatsapp-engine
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure you have WhatsApp Web logged in on your default browser

## Quick Start

### Using the Interactive Interface

```bash
python whatsapp_bulk_sender.py
```

### Using the Command Line Interface

```bash
# Send a single message
python cli.py single "+911234567890" "Hello! This is a test message."

# Send bulk messages from CSV
python cli.py csv sample_contacts.csv --message "Hello {name}! This is a bulk message."

# Send bulk messages from Excel
python cli.py excel contacts.xlsx --message "Hi {name}!" --sheet "Sheet1"

# Create a sample contacts file
python cli.py sample --file my_contacts.csv
```

## File Formats

### CSV Format
Your CSV file should have the following columns:
- `phone`: Phone number with country code (e.g., +911234567890)
- `name`: Contact name (optional, used for personalization)
- `message`: Custom message for this contact (optional, falls back to default)

Example:
```csv
phone,name,message
+911234567890,John Doe,Hello {name}! Welcome to our service.
+919876543210,Jane Smith,Hi {name}! Thanks for joining us.
```

### Excel Format
Same structure as CSV but in Excel format (.xlsx). You can specify the sheet name.

## Message Personalization

Use `{name}` in your messages to automatically replace it with the contact's name:

```python
message = "Hello {name}! Welcome to our service."
# For contact "John Doe", this becomes: "Hello John Doe! Welcome to our service."
```

## Configuration

Edit the `.env` file to customize settings:

```env
MESSAGE_DELAY=15        # Seconds between messages
TAB_CLOSE_DELAY=3      # Seconds before closing browser tab
DEFAULT_COUNTRY_CODE=+91  # Default country code for phone numbers
```

## Python API Usage

```python
from whatsapp_bulk_sender import WhatsAppBulkSender

# Initialize sender
sender = WhatsAppBulkSender()

# Load contacts from CSV
contacts = sender.load_contacts_from_csv('contacts.csv')

# Send bulk messages
results = sender.send_bulk_messages(contacts, "Hello {name}!")

# Send single message
sender.send_single_message("+911234567890", "Hello! This is a test.")

# Schedule messages
sender.schedule_bulk_messages(contacts, "Scheduled message!", "14:30")
```

## Advanced Features

### Scheduled Messaging
```python
# Schedule messages for a specific time
sender.schedule_bulk_messages(contacts, "Good morning {name}!", "09:00")

# Schedule for a specific date
sender.schedule_bulk_messages(contacts, "Reminder!", "14:00", "2024-12-25")
```

### Error Handling and Logging
- All operations are logged to `whatsapp_bulk_sender.log`
- Failed messages are tracked with error details
- Comprehensive error reporting in results

### Phone Number Formatting
The system automatically formats phone numbers:
- Adds country code if missing (defaults to +91 for India)
- Removes non-digit characters
- Handles various input formats

## Command Line Options

### Single Message
```bash
python cli.py single <phone> <message> [--hour HOUR] [--minute MINUTE]
```

### Bulk from CSV
```bash
python cli.py csv <file> [--message MESSAGE] [--hour HOUR] [--minute MINUTE]
```

### Bulk from Excel
```bash
python cli.py excel <file> [--sheet SHEET] [--message MESSAGE] [--hour HOUR] [--minute MINUTE]
```

### Create Sample File
```bash
python cli.py sample [--file FILE]
```

## Important Notes

⚠️ **Before using this tool:**

1. **WhatsApp Web Login**: Make sure you're logged into WhatsApp Web on your default browser
2. **Rate Limiting**: The tool includes delays between messages to avoid being blocked by WhatsApp
3. **Phone Numbers**: Always include country codes in phone numbers (e.g., +911234567890)
4. **Testing**: Test with a small number of contacts first
5. **Compliance**: Ensure you have permission to send messages to all contacts
6. **Browser**: The tool will open browser tabs automatically - don't interfere during sending

## Example Workflow

1. **Prepare your contacts file:**
   ```bash
   python cli.py sample --file my_contacts.csv
   # Edit the file with your actual contacts
   ```

2. **Test with a single message:**
   ```bash
   python cli.py single "+911234567890" "Test message"
   ```

3. **Send bulk messages:**
   ```bash
   python cli.py csv my_contacts.csv --message "Hello {name}! This is our newsletter."
   ```

4. **Check the logs:**
   ```bash
   tail -f whatsapp_bulk_sender.log
   ```

## Troubleshooting

- **Browser not opening**: Make sure your default browser is set correctly
- **Messages not sending**: Verify WhatsApp Web is logged in
- **Phone number errors**: Ensure all numbers have proper country codes
- **Rate limiting**: Increase `MESSAGE_DELAY` in `.env` if messages are being blocked

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## License

This project is open source. Please use responsibly and in compliance with WhatsApp's terms of service.

## Disclaimer

This tool is for educational and legitimate business purposes only. Users are responsible for:
- Obtaining proper consent before sending messages
- Complying with local regulations and WhatsApp's terms of service
- Using the tool responsibly to avoid spam or harassment

The developers are not responsible for any misuse of this tool.