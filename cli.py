#!/usr/bin/env python3
"""
Simple command-line interface for WhatsApp Bulk Sender
"""

import argparse
import sys
from whatsapp_bulk_sender import WhatsAppBulkSender

def main():
    parser = argparse.ArgumentParser(description='WhatsApp Bulk Message Sender')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Single message command
    single_parser = subparsers.add_parser('single', help='Send a single message')
    single_parser.add_argument('phone', help='Phone number (with country code)')
    single_parser.add_argument('message', help='Message to send')
    single_parser.add_argument('--hour', type=int, help='Hour to send (24-hour format)')
    single_parser.add_argument('--minute', type=int, help='Minute to send')
    
    # Bulk CSV command
    csv_parser = subparsers.add_parser('csv', help='Send bulk messages from CSV file')
    csv_parser.add_argument('file', help='CSV file path')
    csv_parser.add_argument('--message', help='Default message (use {name} for personalization)')
    csv_parser.add_argument('--hour', type=int, help='Hour to start sending (24-hour format)')
    csv_parser.add_argument('--minute', type=int, help='Minute to start sending')
    
    # Bulk Excel command
    excel_parser = subparsers.add_parser('excel', help='Send bulk messages from Excel file')
    excel_parser.add_argument('file', help='Excel file path')
    excel_parser.add_argument('--sheet', default='Sheet1', help='Sheet name (default: Sheet1)')
    excel_parser.add_argument('--message', help='Default message (use {name} for personalization)')
    excel_parser.add_argument('--hour', type=int, help='Hour to start sending (24-hour format)')
    excel_parser.add_argument('--minute', type=int, help='Minute to start sending')
    
    # Sample file command
    sample_parser = subparsers.add_parser('sample', help='Create sample contacts file')
    sample_parser.add_argument('--file', default='sample_contacts.csv', help='Output file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    sender = WhatsAppBulkSender()
    
    try:
        if args.command == 'single':
            success = sender.send_single_message(
                args.phone, 
                args.message, 
                args.hour, 
                args.minute
            )
            if success:
                print("✅ Message sent successfully!")
            else:
                print("❌ Failed to send message")
                sys.exit(1)
        
        elif args.command == 'csv':
            contacts = sender.load_contacts_from_csv(args.file)
            if not contacts:
                print("❌ Failed to load contacts from CSV file")
                sys.exit(1)
            
            default_message = args.message or "Hello {name}!"
            results = sender.send_bulk_messages(
                contacts, 
                default_message, 
                args.hour, 
                args.minute
            )
            
            print(f"✅ Bulk sending completed!")
            print(f"📤 Sent: {results['success']}")
            print(f"❌ Failed: {results['failed']}")
            
            if results['failed_contacts']:
                print("\n❌ Failed contacts:")
                for contact in results['failed_contacts']:
                    print(f"  - {contact['phone']} ({contact['name']}): {contact['error']}")
        
        elif args.command == 'excel':
            contacts = sender.load_contacts_from_excel(args.file, args.sheet)
            if not contacts:
                print("❌ Failed to load contacts from Excel file")
                sys.exit(1)
            
            default_message = args.message or "Hello {name}!"
            results = sender.send_bulk_messages(
                contacts, 
                default_message, 
                args.hour, 
                args.minute
            )
            
            print(f"✅ Bulk sending completed!")
            print(f"📤 Sent: {results['success']}")
            print(f"❌ Failed: {results['failed']}")
            
            if results['failed_contacts']:
                print("\n❌ Failed contacts:")
                for contact in results['failed_contacts']:
                    print(f"  - {contact['phone']} ({contact['name']}): {contact['error']}")
        
        elif args.command == 'sample':
            sender.create_sample_contacts_file(args.file)
            print(f"✅ Sample contacts file created: {args.file}")
    
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
