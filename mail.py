import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# Function to validate email address
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

# Function to send the email
def send_email(student_email, subject):
    admin_email = "raniachawali12@gmail.com"  # Replace with the administration's email address
    smtp_server = "smtp.gmail.com"  # SMTP server
    smtp_port = 587  # Port for Gmail
    admin_password = "Bad Day 123456789"  # Admin email password (store securely)
    
    # Standardized email body
    body = f"This email was sent by a student with the identifier: {student_email}\n\nSubject: {subject}"
    
    # Create the email
    message = MIMEMultipart()
    message["From"] = student_email
    message["To"] = admin_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Establish connection with SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(admin_email, admin_password)  # Login as admin to send the email
            server.sendmail(student_email, admin_email, message.as_string())
        print(f"Email successfully sent to the administration at {admin_email}!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# Function to handle user interaction
def interact_with_user():
    print("Welcome to the AI Email Assistant!")
    
    # Ask user if they want to send an email
    user_query = input("How can I help you today? ").strip().lower()
    
    if "send an email to the administration" in user_query:
        # Ask for subject
        subject = input("Please specify the subject of the email: ").strip()
        
        # Ask for the user's email
        while True:
            student_email = input("Please provide your email (must contain your identifier): ").strip()
            if is_valid_email(student_email):
                break
            else:
                print("Invalid email address. Please try again.")
        
        # Confirm and send the email
        print("Sending your email...")
        send_email(student_email, subject)
    else:
        print("Okay! Let me know if you need help with something else.")

if __name__ == "__main__":
    interact_with_user()
