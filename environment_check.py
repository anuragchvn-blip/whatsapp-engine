#!/usr/bin/env python3
"""
WhatsApp Bulk Sender - Environment Check and Setup Guide
"""

import os
import sys

def check_environment():
    """Check if the environment is suitable for running WhatsApp bulk sender"""
    print("🔍 Environment Check")
    print("=" * 30)
    
    # Check if running in a display environment
    display = os.environ.get('DISPLAY')
    if not display:
        print("⚠️  No DISPLAY environment variable found")
        print("   This appears to be a headless environment (like a dev container)")
        print("")
        print("🖥️  To use WhatsApp Bulk Sender, you need:")
        print("   1. A desktop environment with display")
        print("   2. A web browser (Chrome, Firefox, etc.)")
        print("   3. Access to WhatsApp Web")
        print("")
        print("💡 Solutions:")
        print("   1. Run on your local machine with desktop environment")
        print("   2. Use X11 forwarding if connecting via SSH")
        print("   3. Use a VNC or remote desktop solution")
        print("   4. Run in a local development environment")
        return False
    else:
        print(f"✅ DISPLAY found: {display}")
        return True

def show_local_setup_guide():
    """Show guide for setting up on local machine"""
    print("\n📋 Local Machine Setup Guide")
    print("=" * 35)
    print("")
    print("1. 📥 Clone the repository to your local machine:")
    print("   git clone <repository-url>")
    print("   cd whatsapp-engine")
    print("")
    print("2. 🐍 Install Python dependencies:")
    print("   pip install -r requirements.txt")
    print("")
    print("3. 🌐 Open WhatsApp Web in your browser:")
    print("   - Go to https://web.whatsapp.com")
    print("   - Log in by scanning QR code with your phone")
    print("   - Keep this tab open")
    print("")
    print("4. 📝 Prepare your contacts:")
    print("   - Edit sample_contacts.csv with real phone numbers")
    print("   - Format: phone,name,message")
    print("   - Use +countrycode format (e.g., +911234567890)")
    print("")
    print("5. 🚀 Test sending:")
    print("   python3 cli.py single \"+911234567890\" \"Test message\"")
    print("")
    print("6. 📤 Send bulk messages:")
    print("   python3 cli.py csv sample_contacts.csv --message \"Hello {name}!\"")

def show_file_formats():
    """Show supported file formats"""
    print("\n📄 Supported File Formats")
    print("=" * 30)
    print("")
    print("CSV Format (comma-separated):")
    print("phone,name,message")
    print("+911234567890,John Doe,Hello {name}!")
    print("+919876543210,Jane Smith,Hi {name}, welcome!")
    print("")
    print("Excel Format (.xlsx):")
    print("Same columns as CSV but in Excel format")
    print("You can specify sheet name with --sheet parameter")

def show_usage_examples():
    """Show usage examples"""
    print("\n💡 Usage Examples")
    print("=" * 20)
    print("")
    print("Single message:")
    print("python3 cli.py single \"+911234567890\" \"Hello! This is a test.\"")
    print("")
    print("Bulk from CSV:")
    print("python3 cli.py csv contacts.csv --message \"Hi {name}!\"")
    print("")
    print("Bulk from Excel:")
    print("python3 cli.py excel contacts.xlsx --sheet \"Customers\" --message \"Hello {name}!\"")
    print("")
    print("Schedule messages (specify time):")
    print("python3 cli.py csv contacts.csv --message \"Good morning {name}!\" --hour 9 --minute 30")
    print("")
    print("Create sample file:")
    print("python3 cli.py sample --file my_contacts.csv")

def show_troubleshooting():
    """Show troubleshooting tips"""
    print("\n🔧 Troubleshooting")
    print("=" * 20)
    print("")
    print("❌ 'DISPLAY' error:")
    print("   - Run on a machine with desktop environment")
    print("   - Not compatible with headless servers/containers")
    print("")
    print("❌ Browser not opening:")
    print("   - Check if default browser is set")
    print("   - Ensure you have a GUI environment")
    print("")
    print("❌ Messages not sending:")
    print("   - Verify WhatsApp Web is logged in")
    print("   - Check phone number format (+countrycode)")
    print("   - Ensure browser tab stays open")
    print("")
    print("❌ Rate limiting:")
    print("   - Increase MESSAGE_DELAY in .env file")
    print("   - Send smaller batches")
    print("   - Wait between bulk sends")

def create_docker_compose():
    """Create a docker-compose file for GUI environment"""
    print("\n🐳 Creating Docker setup for GUI environment...")
    
    docker_compose = """version: '3.8'
services:
  whatsapp-sender:
    build: .
    environment:
      - DISPLAY=:0
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
      - .:/app
    working_dir: /app
    network_mode: host
    stdin_open: true
    tty: true
    command: bash
"""
    
    dockerfile = """FROM python:3.11-slim

# Install system dependencies for GUI
RUN apt-get update && apt-get install -y \\
    python3-tk \\
    python3-dev \\
    xvfb \\
    xauth \\
    firefox-esr \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x *.py

CMD ["bash"]
"""
    
    try:
        with open('docker-compose.yml', 'w') as f:
            f.write(docker_compose)
        
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile)
        
        print("✅ Created docker-compose.yml and Dockerfile")
        print("💡 To run with GUI support:")
        print("   1. On Linux: xhost +local:docker")
        print("   2. docker-compose up")
        print("   3. docker-compose exec whatsapp-sender bash")
        
    except Exception as e:
        print(f"❌ Failed to create Docker files: {e}")

def main():
    """Main function"""
    print("🚀 WhatsApp Bulk Message Sender")
    print("=" * 40)
    print("")
    
    # Check environment
    can_run = check_environment()
    
    if not can_run:
        show_local_setup_guide()
        create_docker_compose()
    
    show_file_formats()
    show_usage_examples()
    show_troubleshooting()
    
    print("\n" + "=" * 40)
    print("📚 Additional Resources:")
    print("   - README.md for detailed documentation")
    print("   - sample_contacts.csv for file format example")
    print("   - .env for configuration options")
    print("")
    print("⚠️  Important: Always obtain consent before sending messages!")

if __name__ == "__main__":
    main()
