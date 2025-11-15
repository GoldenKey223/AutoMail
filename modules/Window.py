import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

import os
import threading
import datetime

from modules.AutoMail import send_emails

class EmailSenderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoMail")
        self.geometry("900x600")
        self.resizable(False, False)

        base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from /modules
        icon_path = os.path.join(base_dir, "assets", "icon.png")
        
        icon = tk.PhotoImage(file = icon_path)
        self.iconphoto(True, icon)

        self.csv_path = tk.StringVar()
        self.emailFrom = tk.StringVar()
        self.password = tk.StringVar()
        self.varEmail = tk.StringVar()
        self.template_subject = tk.StringVar()
        self.attachments = []

        self.create_widgets()

    def create_widgets(self):
        # Top frame for credentials and CSV
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=5)
        top_frame.columnconfigure(1, weight=1)

        # Frame for credentials
        credentials_frame = ttk.LabelFrame(top_frame, text="Sender Credentials", padding=10)
        credentials_frame.grid(row=0, column=0, padx=10, sticky="n")

        ttk.Label(credentials_frame, text="Email:").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Entry(credentials_frame, textvariable=self.emailFrom, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(credentials_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Entry(credentials_frame, textvariable=self.password, show="*", width=30).grid(row=1, column=1, padx=5, pady=5)

        # Hover tooltip for credentials
        self.tip_credentials = "Use gmail for Email.\nGet password from https://myaccount.google.com/apppasswords"
        self.create_tooltip(credentials_frame, self.tip_credentials)

        # CSV input
        csv_frame = ttk.LabelFrame(top_frame, text="Recipients List", padding=10)
        csv_frame.grid(row=0, column=1, padx=10, sticky="ew")

        ttk.Label(csv_frame, text="CSV location:").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Entry(csv_frame, textvariable=self.csv_path, width=45).grid(row=0, column=1, sticky="e", padx=5, pady=5)
        ttk.Button(csv_frame, text="Browse...", command=self.browse_csv).grid(row=0, column=2, padx=5)

        ttk.Label(csv_frame, text="Email column:").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Entry(csv_frame, textvariable=self.varEmail, width=45).grid(row=1, column=1, padx=5, pady=5)

        # Hover tooltip for credentials
        self.tip_CSV = "Enter name of column that has recipents's email."
        self.create_tooltip(csv_frame, self.tip_CSV)

        # Email template        
        # Subject
        template_frame = ttk.LabelFrame(self, text="Email Template (Markdown and Jinja2)", padding=10)
        template_frame.pack(fill="both", expand=True, padx=10, pady=5)
        template_frame.columnconfigure(1, weight=1)

        ttk.Label(template_frame, text="Subject:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(template_frame, textvariable=self.template_subject).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # body
        self.template_text = ScrolledText(template_frame, wrap="word", width=90, height=16)
        self.template_text.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Hover tooltip for template syntax
        self.tip_template = "**bold**, *italic*, # Header\nUse {{ var }} to insert value of variable.\nExample: Hello {{ name }}."
        self.create_tooltip(template_frame, self.tip_template)

        # Attachment frame
        attach_frame = ttk.LabelFrame(self, text="Attachments", padding=10)
        attach_frame.pack(fill="x", padx=10)
        attach_frame.columnconfigure(1, weight=1)
        
        # Listbox to show attached files
        self.attach_listbox = tk.Listbox(attach_frame, width=100, height=5)
        self.attach_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # attachment button frame
        attach_button_frame = ttk.Frame(attach_frame)
        attach_button_frame.grid(row=0, column=1, sticky="e")

        # Add attachment button
        ttk.Button(attach_button_frame, text="Add Attachment...", command=self.add_attachment).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Remove selected attachment
        ttk.Button(attach_button_frame, text="Remove Selected", command=self.remove_attachment).grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Send email button
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # ttk.Button(button_frame, text="Preview Template", command=self.preview_template).grid(row=0, column=0, padx=10)

        ttk.Button(button_frame, text="Send Emails", command=self.send_emails).grid(row=0, column=1, padx=10)

    def browse_csv(self):
        path = filedialog.askopenfilename(
            title="Select Student List CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if path:
            self.csv_path.set(path)

    def add_attachment(self):
        files = filedialog.askopenfilenames(
            title="Select attachments",
            filetypes=[("All files", "*.*")]
        )

        # Add files to list and show in listbox
        for f in files:
            if f not in self.attachments:
                self.attachments.append(f)
                self.attach_listbox.insert("end", f)

    def remove_attachment(self):
        selected = self.attach_listbox.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an attachment to remove.")
            return

        # Remove from both Listbox and internal list
        index = selected[0]
        filepath = self.attach_listbox.get(index)

        self.attach_listbox.delete(index)
        self.attachments.remove(filepath)

    def send_emails(self):
        email = self.emailFrom.get()
        password = self.password.get()
        csv_path = self.csv_path.get()
        varEmail = self.varEmail.get()
        emailSubject = self.template_subject.get()
        template = self.template_text.get("1.0", tk.END)

        if not email or not password or not csv_path:
            messagebox.showwarning("Missing Fields", "Please fill out all fields before sending.")
            return
        elif email.split("@")[-1] != "gmail.com":
            messagebox.showwarning("Inappropriate email", "Please put gmail for Email")
            return

        # Status Window popup
        self.status_window = StatusWindow(self)

        # Run send_email in background
        threading.Thread(target=lambda: send_emails(email, password, csv_path, varEmail, emailSubject, template, attachments=self.attachments, log_callback=self.status_window.log, progress_callback=self.status_window.update_progress), daemon=True).start()        

    def create_tooltip(self, widget, text):
        """Create hover tooltip for a widget."""
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        tooltip.wm_attributes("-topmost", True)
        label = ttk.Label(tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1, padding=5)
        label.pack()

        def enter(event):
            tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)


# Progress bar and log box and download button in new window
class StatusWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Progress...")
        self.geometry("600x400")

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=560, mode="determinate")
        self.progress.pack(pady=10)

        # Log box
        self.log_text = ScrolledText(self, wrap="word", height=15, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Download log button
        download_btn = ttk.Button(self, text="Download Log", command=self.download_log)
        download_btn.pack(pady=(0, 10))

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        finalMessage = f"{timestamp} {message}"

        self.log_text.config(state="normal")
        self.log_text.insert("end", finalMessage + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.update_idletasks()

    def update_progress(self, ratio):
        self.progress["value"] = ratio * 100
        self.update_idletasks()

    def download_log(self):
        # Generate a default filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_name = f"AutoMail_{timestamp}.txt"

        # Ask where to save
        file_path = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Log As..."
        )

        # If user canceled
        if not file_path:
            return

        # Get the log text
        log_content = self.log_text.get("1.0", "end").strip()

        # Write to file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(log_content)

        messagebox.showinfo("Saved", "Log file saved successfully!")