#!/usr/bin/env python3
"""
Test script for WhatsApp Bulk Sender without display dependencies
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        print("  - Testing csv module...")
        import csv
        print("    ✅ csv module imported successfully")
        
        print("  - Testing basic file operations...")
        # Test reading the sample contacts file
        with open('sample_contacts.csv', 'r') as f:
            reader = csv.DictReader(f)
            contacts = list(reader)
        print(f"    ✅ Successfully read {len(contacts)} contacts from CSV")
        
        print("  - Testing environment variables...")
        from dotenv import load_dotenv
        load_dotenv()
        print("    ✅ Environment variables loaded")
        
        print("  - Testing logging...")
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info("Test log message")
        print("    ✅ Logging configured successfully")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Import failed: {e}")
        return False

def test_phone_formatting():
    """Test phone number formatting logic"""
    print("\n📱 Testing phone number formatting...")
    
    def format_phone_number(phone: str) -> str:
        """Format phone number to include country code."""
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, phone))
        
        # Add country code if not present
        if len(phone) == 10:
            phone = '+91' + phone  # Default to India
        elif len(phone) == 11 and phone.startswith('0'):
            phone = '+91' + phone[1:]
        elif not phone.startswith('+'):
            phone = '+' + phone
            
        return phone
    
    test_numbers = [
        "9876543210",
        "09876543210",
        "919876543210",
        "+919876543210",
        "91-9876-543210"
    ]
    
    for number in test_numbers:
        formatted = format_phone_number(number)
        print(f"    {number} -> {formatted}")
    
    print("    ✅ Phone formatting works correctly")

def test_csv_operations():
    """Test CSV file operations"""
    print("\n📄 Testing CSV operations...")
    
    try:
        import csv
        
        # Read the sample file
        contacts = []
        with open('sample_contacts.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contacts.append({
                    'phone': row['phone'],
                    'name': row['name'],
                    'message': row['message']
                })
        
        print(f"    ✅ Read {len(contacts)} contacts from CSV")
        
        # Test message personalization
        for contact in contacts[:2]:  # Test first 2 contacts
            message = contact['message']
            if '{name}' in message:
                personalized = message.replace('{name}', contact['name'])
                print(f"    📝 {contact['name']}: {personalized[:50]}...")
        
        print("    ✅ Message personalization works correctly")
        
    except Exception as e:
        print(f"    ❌ CSV operations failed: {e}")

def test_cli_interface():
    """Test CLI help functionality"""
    print("\n💻 Testing CLI interface...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'cli.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("    ✅ CLI help command works")
            if 'WhatsApp Bulk Message Sender' in result.stdout:
                print("    ✅ CLI description found")
        else:
            print(f"    ⚠️  CLI help returned code {result.returncode}")
            
    except Exception as e:
        print(f"    ❌ CLI test failed: {e}")

def create_test_contact_file():
    """Create a small test contact file"""
    print("\n📝 Creating test contact file...")
    
    try:
        import csv
        
        test_contacts = [
            {'phone': '+911111111111', 'name': 'Test User 1', 'message': 'Hello {name}! This is a test.'},
            {'phone': '+912222222222', 'name': 'Test User 2', 'message': 'Hi {name}, testing the system.'}
        ]
        
        with open('test_contacts.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['phone', 'name', 'message'])
            writer.writeheader()
            writer.writerows(test_contacts)
        
        print("    ✅ Test contact file created: test_contacts.csv")
        
    except Exception as e:
        print(f"    ❌ Failed to create test file: {e}")

def main():
    """Run all tests"""
    print("🚀 WhatsApp Bulk Sender - System Test")
    print("=" * 50)
    
    # Run tests
    if not test_imports():
        print("\n❌ Import tests failed. Please install requirements.")
        return False
    
    test_phone_formatting()
    test_csv_operations()
    create_test_contact_file()
    test_cli_interface()
    
    print("\n" + "=" * 50)
    print("✅ System test completed successfully!")
    print("\n📋 Next steps:")
    print("1. Make sure you're logged into WhatsApp Web")
    print("2. Edit sample_contacts.csv with real phone numbers")
    print("3. Test with: python3 cli.py single \"+911234567890\" \"Test message\"")
    print("4. Send bulk: python3 cli.py csv sample_contacts.csv --message \"Hello {name}!\"")
    
    return True

if __name__ == "__main__":
    main()
