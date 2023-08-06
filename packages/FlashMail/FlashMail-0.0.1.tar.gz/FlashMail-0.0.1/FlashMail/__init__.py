import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from IPython.display import Markdown, display
from email.mime.base import MIMEBase
from email import encoders

# if __name__ == "__main__":

def send_email(send_to_email, your_email, your_email_password, email_subject, email_message, **kwargs):

    if type(send_to_email) != str or type(your_email) != str or type(your_email_password) != str or type(email_subject) != str or type(email_message) != str:
        raise Exception("Function set_up_mail requires five string inputs and two optional inputs")
    else:
        msg = MIMEMultipart("alternative")
        msg["From"] = your_email
        msg["To"] = send_to_email
        msg["Subject"] = email_subject

        if "email_message_html" not in kwargs:
            msg.attach(MIMEText(email_message, "plain"))
        else:
            msg.attach(MIMEText(email_message, "plain"))
            msg.attach(MIMEText(kwargs["email_message_html"], "html"))

        if "filenames" in kwargs:
            for file in kwargs["filenames"]:
                filename = file
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                msg.attach(p)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(your_email, your_email_password)
        text = msg.as_string()
        server.sendmail(your_email, send_to_email, text)
        server.quit()
