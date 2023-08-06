FlashMail - The simplest and fastest Python email module out there!

With Flash, you can send emails, with text, optional attachments, and even HTML modification, all with less than 10 lines of code; which have normally have been accompished with more than 25 lines.

Overview

The FlashMail Python module was written with speed, and simplicity of use in mind. It provides these key features that no other python email module provides

  - Fast - Send emails with less than 10 lines of code
  - Powerful - Custamize your emails, with attachments, and HTML modification
  - Easy - Great for beginners, and really simple, and easy to understand

How to use it?

Read the detailed information below to find out how easy it is to get started sending emails with this powerful python module

Downloading it

To download FlashMail, install via pip.

pip install FlashMail


Utilizing it's power

The first step is to import it


import FlashMail
send_to_mail = "who_are_you_sending_this_to@gmail.com"
yours = "your_email@gmail.com"
password = "your_password"
subject = "email_subject"
message = "email_message"
# Optional Vars
html_message = "your message in html. Add bolding, and other modifications, with html"
filename = "your filename"
FlashMail.send_email(send_to_mail, yours, password, subject, message, email_message_html=html_message, filenames=[filename])


Now navigate to the link below, and turn less secure app access on. The module is completely safe to use. Then run the code!
https://myaccount.google.com/lesssecureapps

