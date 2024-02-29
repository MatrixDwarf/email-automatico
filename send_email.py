import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv

PORT = 587
EMAIL_SERVER = "email-ssl.com.br"

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

sender_email = os.getenv('EMAIL')
password_email = os.getenv('PASSWORD')


def send_email(subject, receiver_email, name, due_date, invoice_no):

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(('Lembrete | Potere Seguro Auto', f'{sender_email}'))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        {name},
        Sua próxima fatura de Seguro chegou!
        Segue em anexo, o Boleto de sua parcela nº {invoice_no} com vencimento para dia {due_date}, ou acesse pelo portal:
        https://potere.splitrisk.com.br/

        em caso de dúvidas, ficamos á disposição!
        """
    )

    msg.add_alternative (
        f"""
        <html>
            <body>
                <p>{name},</p>
                <p><strong>Sua próxima fatura de Seguro chegou!</strong></p>
                <p>Segue em anexo, o Boleto de sua parcela nº {invoice_no} com vencimento para dia <strong>{due_date}</strong>, ou acesse pelo portal:</p>
                <p>https://potere.splitrisk.com.br/</p>
                <p>em caso de dúvidas, ficamos á disposição!</p>
            </body>
        </html>
    """,
    subtype='html',)

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__=="__main__":
    send_email(
        subject= "Lembrete Seguro Automóvel",
        name = "Caio Galvão",
        receiver_email= 'administrativo2@solucoescorretora.com.br',
        due_date= "10/03/2024",
        invoice_no="05",
    )

print("sucesso")


