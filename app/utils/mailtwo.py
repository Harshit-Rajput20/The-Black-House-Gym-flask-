import smtplib

def send_fee_due_email(receiver_email, package_type):
    # Define email content based on the package type
    print("inside mail two")
    if package_type == 1:
        subject = "Fee Due Reminder: Package Type 1"
        message = "This is a reminder that your fee for Package Type 1 is due. Please submit your payment at your earliest convenience."
    elif package_type == 2:
        subject = "Fee Due Reminder: Package Type 2"
        message = "This is a reminder that your fee for Package Type 2 is due. Please submit your payment at your earliest convenience."
    elif package_type == 3:
        subject = "Fee Due Reminder: Package Type 3"
        message = "This is a reminder that your fee for Package Type 3 is due. Please submit your payment at your earliest convenience."
    elif package_type == 4:
        subject = "Fee Due Reminder: Package Type 4"
        message = "This is a reminder that your fee for Package Type 4 is due. Please submit your payment at your earliest convenience."

    # Construct the email text
    email_text = f"Subject: {subject}\n\n{message}"

    # Connect to the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # Log in to the SMTP server
    server.login("harshitrajput778@gmail.com", "gdjf epis oivt aocj")

    # Send the email
    server.sendmail("harshitrajput778@gmail.com", receiver_email, email_text)

    # Close the connection to the SMTP server
    server.quit()

    print("Fee due email sent successfully")





send_fee_due_email("dev.harshitrajput@gmail.com", 1)