import pywhatkit as kit
import pandas as pd
import time
import logging
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional
import schedule
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_bulk_sender.log'),
        logging.StreamHandler()
    ]
)

class WhatsAppBulkSender:
    def __init__(self):
        self.message_delay = int(os.getenv('MESSAGE_DELAY', '15'))  # seconds between messages
        self.tab_close_delay = int(os.getenv('TAB_CLOSE_DELAY', '3'))  # seconds before closing tab
        
    def load_contacts_from_csv(self, file_path: str) -> List[Dict]:
        """
        Load contacts from a CSV file.
        Expected columns: 'phone', 'name', 'message' (optional)
        """
        try:
            df = pd.read_csv(file_path)
            contacts = []
            
            for _, row in df.iterrows():
                contact = {
                    'phone': self._format_phone_number(str(row['phone'])),
                    'name': row.get('name', ''),
                    'message': row.get('message', '')
                }
                contacts.append(contact)
            
            logging.info(f"Loaded {len(contacts)} contacts from {file_path}")
            return contacts
            
        except Exception as e:
            logging.error(f"Error loading contacts from CSV: {e}")
            return []
    
    def load_contacts_from_excel(self, file_path: str, sheet_name: str = 'Sheet1') -> List[Dict]:
        """
        Load contacts from an Excel file.
        Expected columns: 'phone', 'name', 'message' (optional)
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            contacts = []
            
            for _, row in df.iterrows():
                contact = {
                    'phone': self._format_phone_number(str(row['phone'])),
                    'name': row.get('name', ''),
                    'message': row.get('message', '')
                }
                contacts.append(contact)
            
            logging.info(f"Loaded {len(contacts)} contacts from {file_path}")
            return contacts
            
        except Exception as e:
            logging.error(f"Error loading contacts from Excel: {e}")
            return []
    
    def _format_phone_number(self, phone: str) -> str:
        """
        Format phone number to include country code.
        Assumes Indian numbers if no country code is provided.
        """
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
    
    def send_bulk_messages(self, contacts: List[Dict], default_message: str = "", 
                          start_hour: int = None, start_minute: int = None) -> Dict:
        """
        Send bulk messages to a list of contacts.
        
        Args:
            contacts: List of contact dictionaries
            default_message: Default message to send if contact doesn't have specific message
            start_hour: Hour to start sending (24-hour format)
            start_minute: Minute to start sending
        """
        results = {
            'success': 0,
            'failed': 0,
            'failed_contacts': []
        }
        
        # If no start time specified, start immediately
        if start_hour is None or start_minute is None:
            now = datetime.now()
            start_hour = now.hour
            start_minute = now.minute + 1
        
        logging.info(f"Starting bulk message sending to {len(contacts)} contacts")
        logging.info(f"Start time: {start_hour:02d}:{start_minute:02d}")
        
        for i, contact in enumerate(contacts):
            try:
                phone = contact['phone']
                name = contact.get('name', '')
                message = contact.get('message', default_message)
                
                # Personalize message with name if available
                if name and '{name}' in message:
                    message = message.replace('{name}', name)
                
                # Calculate send time (add delay between messages)
                send_time = datetime.now() + timedelta(minutes=i * (self.message_delay / 60))
                send_hour = send_time.hour
                send_minute = send_time.minute
                
                logging.info(f"Sending message to {phone} ({name}) at {send_hour:02d}:{send_minute:02d}")
                
                # Send message
                kit.sendwhatmsg(
                    phone_no=phone,
                    message=message,
                    time_hour=send_hour,
                    time_min=send_minute,
                    wait_time=self.tab_close_delay
                )
                
                results['success'] += 1
                logging.info(f"Message sent successfully to {phone}")
                
                # Wait between messages to avoid being blocked
                time.sleep(self.message_delay)
                
            except Exception as e:
                logging.error(f"Failed to send message to {contact['phone']}: {e}")
                results['failed'] += 1
                results['failed_contacts'].append({
                    'phone': contact['phone'],
                    'name': contact.get('name', ''),
                    'error': str(e)
                })
        
        logging.info(f"Bulk sending completed. Success: {results['success']}, Failed: {results['failed']}")
        return results
    
    def send_single_message(self, phone: str, message: str, hour: int = None, minute: int = None):
        """
        Send a single message to a phone number.
        """
        try:
            phone = self._format_phone_number(phone)
            
            if hour is None or minute is None:
                now = datetime.now()
                hour = now.hour
                minute = now.minute + 1
            
            logging.info(f"Sending message to {phone} at {hour:02d}:{minute:02d}")
            
            kit.sendwhatmsg(
                phone_no=phone,
                message=message,
                time_hour=hour,
                time_min=minute,
                wait_time=self.tab_close_delay
            )
            
            logging.info(f"Message sent successfully to {phone}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send message to {phone}: {e}")
            return False
    
    def schedule_bulk_messages(self, contacts: List[Dict], message: str, 
                             send_time: str, date: str = None):
        """
        Schedule bulk messages to be sent at a specific time.
        
        Args:
            contacts: List of contact dictionaries
            message: Message to send
            send_time: Time in HH:MM format
            date: Date in YYYY-MM-DD format (optional, defaults to today)
        """
        def job():
            self.send_bulk_messages(contacts, message)
        
        if date:
            schedule.every().day.at(send_time).do(job).tag(f'bulk_{date}')
        else:
            schedule.every().day.at(send_time).do(job)
        
        logging.info(f"Scheduled bulk messages for {send_time}" + (f" on {date}" if date else ""))
    
    def create_sample_contacts_file(self, file_path: str = "sample_contacts.csv"):
        """
        Create a sample contacts file for reference.
        """
        sample_data = {
            'phone': ['+91XXXXXXXXXX', '+91XXXXXXXXXX', '+91XXXXXXXXXX'],
            'name': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'message': [
                'Hello {name}, this is a personalized message!',
                'Hi {name}, how are you doing?',
                'Hey {name}, check out our new product!'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(file_path, index=False)
        logging.info(f"Sample contacts file created: {file_path}")


def main():
    """
    Main function to demonstrate usage
    """
    sender = WhatsAppBulkSender()
    
    print("WhatsApp Bulk Message Sender")
    print("=" * 30)
    print("1. Send bulk messages from CSV")
    print("2. Send bulk messages from Excel")
    print("3. Send single message")
    print("4. Create sample contacts file")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == '1':
        file_path = input("Enter CSV file path: ")
        message = input("Enter default message (use {name} for personalization): ")
        
        contacts = sender.load_contacts_from_csv(file_path)
        if contacts:
            result = sender.send_bulk_messages(contacts, message)
            print(f"\nResults: {result['success']} sent, {result['failed']} failed")
    
    elif choice == '2':
        file_path = input("Enter Excel file path: ")
        sheet_name = input("Enter sheet name (default: Sheet1): ") or 'Sheet1'
        message = input("Enter default message (use {name} for personalization): ")
        
        contacts = sender.load_contacts_from_excel(file_path, sheet_name)
        if contacts:
            result = sender.send_bulk_messages(contacts, message)
            print(f"\nResults: {result['success']} sent, {result['failed']} failed")
    
    elif choice == '3':
        phone = input("Enter phone number: ")
        message = input("Enter message: ")
        
        success = sender.send_single_message(phone, message)
        print("Message sent successfully!" if success else "Failed to send message")
    
    elif choice == '4':
        file_path = input("Enter file path for sample (default: sample_contacts.csv): ") or "sample_contacts.csv"
        sender.create_sample_contacts_file(file_path)
        print(f"Sample file created: {file_path}")
    
    elif choice == '5':
        print("Goodbye!")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
