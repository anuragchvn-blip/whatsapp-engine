#!/usr/bin/env python3
"""
WhatsApp Bulk Sender - Demo Mode (Safe Testing)
This demonstrates the functionality without actually sending messages
"""

import csv
import logging
from datetime import datetime

def demo_phone_formatting():
    """Demo phone number formatting"""
    print("📱 Phone Number Formatting Demo")
    print("-" * 35)
    
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
        "91-9876-543210",
        "+91 9876 543210",
        "919876543210"
    ]
    
    for number in test_numbers:
        formatted = format_phone_number(number)
        print(f"  {number:15} → {formatted}")
    print()

def demo_message_personalization():
    """Demo message personalization"""
    print("💬 Message Personalization Demo")
    print("-" * 35)
    
    template = "Hello {name}! Welcome to our service. We're excited to have you on board!"
    
    contacts = [
        {"name": "John Doe", "phone": "+911234567890"},
        {"name": "Jane Smith", "phone": "+919876543210"},
        {"name": "Mike Johnson", "phone": "+918765432109"}
    ]
    
    for contact in contacts:
        personalized = template.replace("{name}", contact["name"])
        print(f"  📞 {contact['phone']}")
        print(f"  👤 {contact['name']}")
        print(f"  💌 {personalized}")
        print()

def demo_csv_loading():
    """Demo CSV file loading"""
    print("📄 CSV Loading Demo")
    print("-" * 20)
    
    try:
        with open('sample_contacts.csv', 'r') as f:
            reader = csv.DictReader(f)
            contacts = list(reader)
        
        print(f"  ✅ Loaded {len(contacts)} contacts from CSV")
        print("  📋 Sample contacts:")
        
        for i, contact in enumerate(contacts[:3], 1):
            print(f"     {i}. {contact['name']} ({contact['phone']})")
            message = contact['message'].replace('{name}', contact['name'])
            print(f"        Message: {message[:50]}...")
        
        if len(contacts) > 3:
            print(f"     ... and {len(contacts) - 3} more contacts")
        print()
        
    except Exception as e:
        print(f"  ❌ Error loading CSV: {e}")

def demo_bulk_sending_simulation():
    """Demo bulk sending simulation (no actual sending)"""
    print("📤 Bulk Sending Simulation")
    print("-" * 30)
    
    try:
        with open('sample_contacts.csv', 'r') as f:
            reader = csv.DictReader(f)
            contacts = list(reader)
        
        print(f"  🎯 Would send to {len(contacts)} contacts")
        print(f"  ⏰ Estimated time: {len(contacts) * 15} seconds")
        print(f"  📅 Start time: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        for i, contact in enumerate(contacts, 1):
            message = contact['message'].replace('{name}', contact['name'])
            print(f"  [{i}/{len(contacts)}] 📱 {contact['phone']} ({contact['name']})")
            print(f"            💌 {message[:50]}...")
            print(f"            ✅ Would send successfully")
            print()
        
        print("  🎉 Bulk sending simulation complete!")
        print()
        
    except Exception as e:
        print(f"  ❌ Error in simulation: {e}")

def demo_cli_commands():
    """Demo CLI commands that would be used"""
    print("💻 CLI Commands Demo")
    print("-" * 20)
    
    commands = [
        ("Single message", "python3 cli.py single \"+911234567890\" \"Hello! This is a test message.\""),
        ("Bulk from CSV", "python3 cli.py csv sample_contacts.csv --message \"Hello {name}!\""),
        ("Bulk from Excel", "python3 cli.py excel contacts.xlsx --message \"Hi {name}!\""),
        ("Scheduled bulk", "python3 cli.py csv sample_contacts.csv --message \"Good morning {name}!\" --hour 9 --minute 30"),
        ("Create sample", "python3 cli.py sample --file my_contacts.csv")
    ]
    
    for description, command in commands:
        print(f"  📝 {description}:")
        print(f"     {command}")
        print()

def main():
    """Run all demos"""
    print("🎭 WhatsApp Bulk Sender - Demo Mode")
    print("=" * 40)
    print("This demo shows functionality without sending actual messages")
    print()
    
    demo_phone_formatting()
    demo_message_personalization()
    demo_csv_loading()
    demo_bulk_sending_simulation()
    demo_cli_commands()
    
    print("=" * 40)
    print("✅ Demo completed successfully!")
    print()
    print("🚀 To use for real:")
    print("   1. Run on a machine with desktop environment")
    print("   2. Login to WhatsApp Web")
    print("   3. Replace demo numbers with real contacts")
    print("   4. Execute the CLI commands shown above")
    print()
    print("⚠️  Remember: Always get consent before sending messages!")

if __name__ == "__main__":
    main()
