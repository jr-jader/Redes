import tkinter as tk

class Chat:
    def __init__(self, user_name, send_message_callback):
        self.user_name = user_name
        self.root = tk.Tk()
        self.root.title(f"Chat P2P - {user_name}")

        chat_frame = tk.Frame(self.root)
        chat_frame.pack(pady=10)

        self.chat_text = tk.Text(chat_frame, width=50, height=20)
        self.chat_text.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.chat_text.yview)

        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(pady=10)
        self.message_entry.bind("<Return>", self.send_on_enter)

        send_button = tk.Button(self.root, text="Enviar", command=self.send_message)
        send_button.pack()

        self.send_message_callback = send_message_callback

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_on_enter(self, event):
        self.send_message()

    def send_message(self):
        message = self.message_entry.get()
        if message.lower() == "sair":
            self.send_message_callback(message)
            self.root.quit()
        else:
            formatted_message = f"{self.user_name}: {message}"
            self.send_message_callback(formatted_message)
            self.insert_message(formatted_message)
            self.message_entry.delete(0, tk.END)

    def insert_message(self, message):
        self.chat_text.insert(tk.END, message + "\n")

    def on_close(self):
        self.send_message_callback("sair")
        self.root.quit()

    def start(self):
        self.root.mainloop()
