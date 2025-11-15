from jinja2 import Template
import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from modules.MDtoHTML import md_to_html

def check_attachments(attachments=None):
    attachmentsList = []
    if attachments:
        for filePath in attachments:
            if not os.path.exists(filePath):
                attachmentsList.append(filePath)

    return attachmentsList

def render_template(variables, template_str):
    template = Template(template_str)
    return template.render(variables)

def build_email(emailFrom, emailTo, subject, body_text, attachments=None):
    msg = MIMEMultipart()
    msg["From"] = emailFrom
    msg["To"] = emailTo
    msg["Subject"] = subject

    # Body
    msg.attach(MIMEText(body_text, "html", "utf-8"))

    # Attachments
    if attachments:
        for filePath in attachments:
            with open(filePath, "rb") as f:
                fileName = os.path.basename(filePath)

                part = MIMEApplication(f.read(), Name=fileName)
                part['Content-Disposition'] = f'attachment; filename="{fileName}"'

                msg.attach(part)

    return msg

def send_emails(email, password, csv_path, varEmail, emailSubject, template_str, attachments=None, log_callback=None, progress_callback=None):
    emailFrom = email
    emailPassword = password

    # connection to Google SMTP server
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=emailFrom, password=emailPassword)

    # check Attachments
    errorAttachmentsList = check_attachments(attachments=attachments)
    for filePath in errorAttachmentsList:
        log_callback(f"[WARN] Attachment not found: {filePath}")

    # open CSV file with email address
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_dict = csv.DictReader(file)
        rows = list(csv_dict)
        total = len(rows)

        for idx, row in enumerate(rows, start=1):
            emailTo = row.get(varEmail)
            if not emailTo:
                log_callback(f"Missing email field in row {idx}")
                log_callback(f"Failed to send to {emailTo}")
                continue
            elif log_callback:
                log_callback(f"Sending email to {emailTo}")

            # Render dynamic subject/body and build email
            subject = render_template(row, emailSubject)
            bodyMD = render_template(row, template_str)
            bodyHTML = md_to_html(bodyMD)

            msg = build_email(emailFrom=emailFrom, emailTo=emailTo, subject=subject, body_text=bodyHTML, attachments=attachments)

            # Send email
            try:
                connection.sendmail(from_addr=emailFrom, to_addrs=emailTo, msg=msg.as_string())
                if log_callback:
                    log_callback(f"Email sent to {emailTo}")

            except Exception as e:
                if log_callback:
                    log_callback(f"Failed to send to {emailTo}")

            # Progress bar
            if progress_callback:
                progress_callback(idx/total)
    
    log_callback(f"Tasks done")
                

    connection.quit()