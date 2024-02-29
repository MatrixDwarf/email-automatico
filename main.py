from datetime import date
import pandas as pd
from send_email import send_email



SHEET_ID = "1y8Htf6aSTiDaTYnsf_PfNZpUuQJERU2JM8tPmN482HQ"
SHEET_NAME = "Sheet1"
# alternativo = "/edit?usp=sharing"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def load_df(url):
    parse_dates = ['due_date', 'reminder_date']
    df = pd.read_csv(url, parse_dates=parse_dates, dayfirst=True)
    return df



print(load_df(URL))


def query_data_and_send_emails(df):
    present = date.today()
    email_counter = 0
    for _,  row in df.iterrows():
        if(present >= row["reminder_date"].date()) and (row["has_paid"] == 'no'):
            send_email(
                subject=f'Lembrete Seguro Auto | Fatura: {row["invoice_no"]}',
                receiver_email=row["email"],
                name=row["name"],
                due_date=row["due_date"].strftime("%d, %b %Y"),
                invoice_no=row["invoice_no"],
            )
            email_counter += 1
    return f"Total enviados: {email_counter}"


df = load_df(URL)
result = query_data_and_send_emails(df)
print(result)