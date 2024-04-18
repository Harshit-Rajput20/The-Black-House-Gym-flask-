import smtplib

email = "harshitrajput778@gmail.com"
receiver_email= "dev.harshitrajput@gmail.com"

subject = "this is subject"
message = "this is  message"

text = f"subject:{subject}\n\n {message}"

server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(email,"gdjf epis oivt aocj")
server.sendmail(email,receiver_email,text)
print("email is sent")