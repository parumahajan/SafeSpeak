import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import threading
import socket

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Safe Chat - Cyberbullying Detection")
        self.root.geometry("800x600")
        
        # Create GUI elements
        self.create_widgets()
        
        # Connect to server
        self.connect_to_server()
        
        # Start receiving messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()
    
    def create_widgets(self):
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=20)
        self.chat_display.pack(padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)
        
        # Message input
        self.msg_input = tk.Entry(self.root, width=60)
        self.msg_input.pack(padx=10, pady=5)
        self.msg_input.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)
    
    def connect_to_server(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('localhost', 5555))
            self.display_message("System", "Connected to chat server!")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {str(e)}")
            self.root.destroy()
    
    def send_message(self, event=None):
        message = self.msg_input.get().strip()
        if message:
            # Check for cyberbullying
            try:
                response = requests.post('http://localhost:5000/predict', 
                                      json={'text': message})
                result = response.json()
                
                if result['is_bullying']:
                    messagebox.showwarning("Warning", 
                        "This message contains cyberbullying content and will not be sent!")
                    self.msg_input.delete(0, tk.END)
                    return
                
                # Send message to chat server
                self.client.send(message.encode('utf-8'))
                self.msg_input.delete(0, tk.END)
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not check message: {str(e)}")
    
    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    self.display_message("Other", message)
            except:
                break
    
    def display_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
