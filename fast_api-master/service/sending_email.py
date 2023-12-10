import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader


def sending_email(data):
    email_address = "hieu.dh3t1@gmail.com"
    email_password = "mgcduoaczanjwwzk"

    # Load Jinja2 template
    template_loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=template_loader)
    template = env.get_template("email_template.html")

    # Render the template with data
    email_content = template.render(
        name=data.get('name'),
        email=data.get('email'),
        message=data.get('message')
    )

    # Create email
    msg = EmailMessage()
    msg['Subject'] = "Happy new year !!"
    # Set the "From" address with the display name
    msg['From'] = "Admin FutureLove <" + email_address + ">"

    msg['To'] = data.get('email')
    msg.add_alternative(email_content, subtype='html')

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

    return "Email successfully sent"


data = {
    'name': 'Admin futurelove',
    'email': 'lizhongxiao95@gmail.com',
    'message': 'This is a happy new year email !'
}

