# 📧 AutoMail — Bulk Email Sender with CSV, Markdown, Jinja2, and Attachments

AutoMail is a desktop application built with **Python** that lets you:

- Load a **CSV file** containing email and data  
- Write an email template using **Markdown** + **Jinja2 variables**  
- Send personalized **HTML emails** to every recipient  
- Attach multiple files with size limits  
- Track progress in a separate status window  
- Generate logs automatically  
- Run everything without needing a browser or external editor  

---

## 🚀 Features

### ✔ CSV List  
- Load any CSV with headers  
- Choose which column contains email addresses  
- All other columns become Jinja2 variables  
- Example variables: `{{ id }}`, `{{ name }}`, `{{ number1 }}`  

### ✔ Markdown Editor  
- Write your email template in Markdown  
- Convert Markdown → HTML automatically before sending  

### ✔ Jinja2 Variable Support  
Variables come from CSV column names

### ✔ Attachments  
- Add multiple attachments  
- Remove attachments anytime  

### ✔ Email Sending  
- SMTP login  
- Gmail-compatible (can extend to Naver/Daum/Outlook)  
- Sends:
  - HTML email  
  - Attachments  
- Runs in a thread (UI stays responsive)  
- Shows progress + live logs  

### ✔ Status Window  
- Real-time logs  
- Progress bar  
- Export log to file  
- Auto-named logs using date/time  

---

## 📌 Password is from Gmail app password(You do NOT use your normail Gmail password)
1. go to https://myaccount.google.com/security
2. enable 2-Step verification
3. go to https://myaccount.google.com/apppasswords
4. get app password(16-character password)

---

## 📦 Installation
1. Clone the repository
    - git clone https://github.com/GoldenKey223/AutoMail.git
2. Create a virtual enviroment
    - python -m venv venv
3. Activate the virtual enviroment
    - Windows(cmd): venv\Scripts\activate.bat
    - Mac/Linux: source venv/bin/activate
3. Install dependencies
    - pip install -r requirements.txt

---
## 📌 TODO
- Attachment file size restriction(20MB)
- Drag-and-drop attachments
- Insert variable dropdown
- automatic sender email SMTP detection(currently only using google SMTP)