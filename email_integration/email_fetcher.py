import imaplib
import email
from email.parser import BytesParser
from email.policy import default
import datetime
from models import UserEmail, Message


async def fetch_emails():
    user_email = UserEmail.objects.first()
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user_email.email, user_email.password)

    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    mail_ids = data[0].split()

    total_emails = len(mail_ids)

    for idx, email_id in enumerate(mail_ids):
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]

        msg = BytesParser(policy=default).parsebytes(raw_email)
        subject = msg['subject']
        date_sent = email.utils.parsedate_to_datetime(msg['date'])
        date_received = datetime.datetime.now()
        description = msg.get_payload(decode=True).decode()

        attachments = []
        for part in msg.iter_attachments():
            filename = part.get_filename()
            if filename:
                attachments.append(filename)

        # Save to the database
        Message.objects.create(
            subject=subject,
            send_date=date_sent,
            received_date=date_received,
            description=description,
            attachments=attachments
        )

        progress = (idx + 1) / total_emails * 100

        yield {
            'email_id': email_id.decode(),
            'subject': subject,
            'progress': progress,
        }

    yield {
        'status': 'Completed',
    }
