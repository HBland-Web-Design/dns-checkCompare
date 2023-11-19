import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_html_email(sender_email, receiver_email, subject, html_content):
    # Set up SMTP server and credentials
    smtp_server = 'smtp.example.com'  # Replace with your SMTP server address
    smtp_port = 587  # Replace with your SMTP port (e.g., 587 for TLS)
    smtp_username = 'your_username'
    smtp_password = 'your_password'

    # Create message container - MIME multipart
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach HTML content to the email
    html_body = MIMEText(html_content, 'html')
    msg.attach(html_body)

    # Connect to the SMTP server
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

# Example usage:
sender_email = 'your_email@example.com'
receiver_email = 'recipient@example.com'
email_subject = 'HTML Email Test'

html_template = """
<html>
<head><title>HTML Email</title></head>
<body>
    <h1>Hello!</h1>
    <p>This is an HTML email template.</p>
</body>
</html>
"""

send_html_email(sender_email, receiver_email, email_subject, html_template)
