# -*- coding: utf-8 -*-
###############################################################################
#   Summary Information                                                       #
#   Lambda to send a summary information                                      #
###############################################################################

import os
from dotenv import load_dotenv
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

# SENDGRID
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
SENDGRID_SUMMARY_TEMPLATE_ID = os.getenv('SENDGRID_SUMMARY_TEMPLATE_ID', '')
SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', '')


def read_csv() -> pd.DataFrame:
    df = pd.read_csv('summaries_information/summary_information.csv', delimiter=',', skip_blank_lines=True)
    return df


def process_data(df: pd.DataFrame) -> dict:
    total_balance = df['Transaction'].sum()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d')
    month_transactions = df.groupby(df.Date.dt.month_name())['Transaction'].count()
    average_credit_amount = df[df['Transaction'] > 0]['Transaction'].mean()
    average_debit_amount = df[df['Transaction'] < 0]['Transaction'].mean()
    print(f'Total balance is {total_balance}')
    for month, total in month_transactions.iteritems():
        print(f'Number of transactions in {month}: {total}')
    print(f'Average credit amount: {average_credit_amount}')
    print(f'Average debit amount: {average_debit_amount}')
    summary_information = {
        "total_balance": total_balance,
        "average_credit_amount": average_credit_amount,
        "average_debit_amount": average_debit_amount,
        "month_transactions": month_transactions.to_dict(),
    }
    return summary_information


def save_db():
    pass


def send_mail(summary_information: dict) -> bool:
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL,
        to_emails='edgargdcv@gmail.com'
    )
    message.dynamic_template_data = summary_information
    message.template_id = SENDGRID_SUMMARY_TEMPLATE_ID
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(f'An error occurred while sending the summary information: {str(e)}')
        return False


def handler(event=None, context=None):
    data = read_csv()
    summary_information = process_data(data)
    print(summary_information)
    # save_db()
    send_mail(summary_information)


if __name__ == '__main__':
    handler()
