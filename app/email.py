from flask_mail import Message
from app import mail, app
from flask import render_template
from threading import Thread
from app.models import User

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user: User):
    token = user.get_reset_password_token()
    send_email('[APP] Reset your password',
        app.config['ADMINS'][0],
        user.email,
        render_template('email/reset_password.txt', user=user, token=token),
        render_template('email/reset_password.html', user=user, token=token)
    )
