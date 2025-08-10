import tkinter as tk
from tkinter import messagebox, scrolledtext
from whatsapp_bulk_sender import WhatsAppBulkSender
import threading

def send_messages():
    numbers = phone_entry.get()
    message = message_text.get("1.0", tk.END).strip()
    if not numbers or not message:
        messagebox.showwarning("Input Error", "Please enter phone numbers and a message.")
        return
    
    # Split numbers by comma, strip whitespace
    phone_list = [num.strip() for num in numbers.split(",") if num.strip()]
    if not phone_list:
        messagebox.showwarning("Input Error", "Please enter at least one phone number.")
        return
    
    # Prepare contacts list for WhatsAppBulkSender
    contacts = [{"phone": num, "name": "", "message": message} for num in phone_list]
    
    def run_sender():
        sender = WhatsAppBulkSender()
        result = sender.send_bulk_messages(contacts, message)
        messagebox.showinfo("Done", f"Sent: {result['success']}\nFailed: {result['failed']}")
    
    threading.Thread(target=run_sender).start()

root = tk.Tk()
root.title("WhatsApp Bulk Sender GUI")
root.geometry("500x400")

# Message label and box
tk.Label(root, text="Message:").pack(anchor="w", padx=10, pady=(10,0))
message_text = scrolledtext.ScrolledText(root, height=6, width=60)
message_text.pack(padx=10, pady=5)

# Phone numbers label and entry
tk.Label(root, text="Phone Numbers (comma separated):").pack(anchor="w", padx=10, pady=(10,0))
phone_entry = tk.Entry(root, width=60)
phone_entry.pack(padx=10, pady=5)

# Send button
tk.Button(root, text="Send", command=send_messages, bg="#25D366", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

root.mainloop()
