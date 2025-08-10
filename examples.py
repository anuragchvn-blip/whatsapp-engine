from whatsapp_bulk_sender import WhatsAppBulkSender
import pandas as pd

def example_usage():
    """
    Examples of how to use the WhatsApp Bulk Sender
    """
    
    # Initialize the sender
    sender = WhatsAppBulkSender()
    
    # Example 1: Create and use sample data
    print("=== Example 1: Creating sample contacts ===")
    sender.create_sample_contacts_file("example_contacts.csv")
    
    # Example 2: Load contacts from CSV and send messages
    print("\n=== Example 2: Sending bulk messages ===")
    
    # Create some example contacts programmatically
    contacts_data = [
        {
            'phone': '+911234567890',
            'name': 'Alice',
            'message': 'Hello {name}! This is a test message.'
        },
        {
            'phone': '+919876543210', 
            'name': 'Bob',
            'message': 'Hi {name}, how are you today?'
        },
        {
            'phone': '+918765432109',
            'name': 'Charlie',
            'message': 'Hey {name}, check out our new service!'
        }
    ]
    
    # Note: Replace with real phone numbers to actually send messages
    print("Contacts loaded:", len(contacts_data))
    
    # Example 3: Send a single message
    print("\n=== Example 3: Sending single message ===")
    # sender.send_single_message("+911234567890", "Hello! This is a test message.")
    
    # Example 4: Schedule messages
    print("\n=== Example 4: Scheduling messages ===")
    # sender.schedule_bulk_messages(contacts_data, "Scheduled message!", "14:30")
    
    # Example 5: Load from Excel file
    print("\n=== Example 5: Working with Excel files ===")
    
    # Create an example Excel file
    df = pd.DataFrame({
        'phone': ['+911111111111', '+912222222222', '+913333333333'],
        'name': ['Person 1', 'Person 2', 'Person 3'],
        'message': [
            'Hello {name}, welcome!',
            'Hi {name}, thanks for joining!',
            'Hey {name}, have a great day!'
        ]
    })
    df.to_excel('example_contacts.xlsx', index=False)
    print("Example Excel file created: example_contacts.xlsx")
    
    # Load from Excel
    # excel_contacts = sender.load_contacts_from_excel('example_contacts.xlsx')
    # print(f"Loaded {len(excel_contacts)} contacts from Excel")

def advanced_example():
    """
    Advanced example with error handling and logging
    """
    sender = WhatsAppBulkSender()
    
    # Example with mixed message types
    contacts = [
        {
            'phone': '+911111111111',
            'name': 'John',
            'message': 'Personal message for {name}'
        },
        {
            'phone': '+912222222222',
            'name': 'Jane',
            'message': ''  # Will use default message
        }
    ]
    
    default_message = "Hello {name}, this is a default message from our service!"
    
    print("=== Advanced Example: Mixed message types ===")
    print(f"Sending to {len(contacts)} contacts with default message fallback")
    
    # Uncomment to actually send messages
    # results = sender.send_bulk_messages(contacts, default_message)
    # print(f"Results: {results}")

if __name__ == "__main__":
    print("WhatsApp Bulk Sender - Examples")
    print("=" * 40)
    
    # Run examples
    example_usage()
    print("\n" + "=" * 40)
    advanced_example()
    
    print("\n" + "=" * 40)
    print("Note: To actually send messages, uncomment the relevant lines")
    print("and replace phone numbers with real ones.")
    print("Make sure WhatsApp Web is logged in on your default browser.")
