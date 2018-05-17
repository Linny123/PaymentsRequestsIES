
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail.message import EmailMessage



def send_e_mail(to_email, Subject, message, attachment):

    email = EmailMessage()
    email.subject = Subject
    email.body = message
    email.from_email = 'PaymentRequests'
    email.to = to_email
    if attachment:
        email.attach_file(attachment)

    email.send()

def send_confirmation_mail(invoice):
    to = settings.ACCOUNTANCY_PROGRAM
    Subject = "Invoice Confirmed"
    #to_email = ["lindadc90@gmail.com"]
    message = " The invoice for project: " + invoice.project.name + " has been confirmed"
    send_e_mail(to, Subject, message, invoice.invoice.path)


def received_request(invoice, to):
    to.append(settings.ACCOUNTANCY_PROGRAM)
    Subject = "You received a new invoice"
    message = " There is a new invoice for project, " + invoice.project.name + " please confirm or deny this invoice at" + settings.WEB_LINK
    send_e_mail(to, Subject, message, invoice.invoice.path)