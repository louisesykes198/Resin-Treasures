import smtplib

smtp_server = 'smtp.ionos.co.uk'
port = 587
sender_email = 'Store@resintreasures.co.uk'
password = 'NewHouse2025!'  # Replace with your real password
receiver_email = 'lindseycombes1@gmail.com'

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    message = """\
Subject: Test Email from Python

This is a test email sent from Python script."""
    server.sendmail(sender_email, receiver_email, message)
    print("Email sent successfully!")
except Exception as e:
    print("Error:", e)
finally:
    server.quit()

