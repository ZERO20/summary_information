# -*- coding: utf-8 -*-
###############################################################################
#   Summary Information                                                       #
#   Lambda to send summary information                                      #
###############################################################################

import logging
import os
from io import BytesIO

import boto3
from dotenv import load_dotenv
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from db.models import Account, Transaction

load_dotenv()


# ===================== Log Configuration ===================== #
LOG_FORMAT = '{levelname}:{name}:{funcName}:{message}'
LOG_STYLE = '{'
logging.basicConfig(format=LOG_FORMAT, style=LOG_STYLE) # noqa
logger = logging.getLogger('Summary information')
logger.setLevel(logging.DEBUG)


# ===================== Environment Variables ===================== #
# SENDGRID
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
SENDGRID_SUMMARY_TEMPLATE_ID = os.getenv('SENDGRID_SUMMARY_TEMPLATE_ID', '')

# AWS - S3
S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', '')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', '')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', '')
S3_REGION = os.getenv('S3_REGION', '')
S3_KEY = os.getenv('S3_KEY', '')

# PROJECT
FROM_EMAIL = os.getenv('FROM_EMAIL', '')
TO_EMAIL = os.getenv('TO_EMAIL', '')
FILE_DIRECTORY = os.getenv('FILE_DIRECTORY', '')


def read_csv() -> pd.DataFrame:
    """
    Read a csv file from a directory or S3 Bucket
    Returns:
        pd.DataFrame: csv information with the headers: number, date, ammount
    """
    logger.info('Reading csv file...')
    if FILE_DIRECTORY == 'S3':
        logger.info(f'Getting the csv from S3: {S3_BUCKET_NAME}/{S3_KEY}')
        s3 = boto3.client(
            's3',
            region_name=S3_REGION,
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY
        )
        obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=S3_KEY)
        _csv = (BytesIO(obj['Body'].read()))
    else:
        logger.info('Getting the csv locally')
        _csv = 'summaries_information/summary_information.csv'

    df = pd.read_csv(_csv, delimiter=',', skip_blank_lines=True, encoding='utf8')
    df.rename(columns={"Id": "number", "Date": "date", "Transaction": "amount"}, inplace=True)
    return df


def get_summary_information(account: Account, df: pd.DataFrame) -> dict:
    """
    Generates the summary information
    Args:
        account (Account): Account to use.
        df (pd.DataFrame):  Data frame to extract the summary information

    Returns:
        dict: Summary information.
        Examples:
            {'username': 'Edgar de la Cruz', 'total_balance': 39.74, 'average_credit_amount': 35.25,
            'average_debit_amount': -15.38, 'month_transactions': {'July': 2, 'August': 2}}
    """
    logger.info('Summary information')
    total_balance = df['amount'].sum().round(2)
    average_credit_amount = df[df['amount'] > 0]['amount'].mean().round(2)
    average_debit_amount = df[df['amount'] < 0]['amount'].mean().round(2)
    df['formatted_date'] = pd.to_datetime(df['date'], format='%m/%d')
    month_transactions = df.groupby(pd.Grouper(key='formatted_date', freq='M'))['amount'].count()
    month_transactions.index = month_transactions.index.strftime('%B')
    logger.info(f'Total balance is {total_balance}')
    logger.info(f'Average credit amount: {average_credit_amount}')
    logger.info(f'Average debit amount: {average_debit_amount}')
    for month, total in month_transactions.iteritems():
        logger.info(f'Number of transactions in {month}: {total}')
    summary_information = {
        "username": f"{account.name} {account.paternal_surname}",
        "total_balance": total_balance,
        "average_credit_amount": average_credit_amount,
        "average_debit_amount": average_debit_amount,
        "month_transactions": month_transactions.to_dict(),
    }
    return summary_information


def save_db(account: Account, df: pd.DataFrame) -> bool:
    """
    Save the account transactions
    Args:
        account (Account): Account record to save the transactions
        df (pd.DataFrame): Data frame from csv with the transactions
    Returns:
        bool: True for success, False otherwise.
    Returns:

    """
    logger.info('Saving transactions...')
    try:
        df['account'] = account.id
        transactions = df[['number', 'date', 'amount', 'account']].to_dict(orient='records')
        Transaction.insert_many(transactions).execute()
        return True
    except Exception as e:
        logger.info(f'An error occurred while saving the transactions: {str(e)}')
        return False


def send_mail(summary_information: dict) -> bool:
    """
    Sends an email with the summary information
    Args:
        summary_information (dict): summary information.
            {'username': 'Edgar de la Cruz', 'total_balance': 39.74, 'average_credit_amount': 35.25,
            'average_debit_amount': -15.38, 'month_transactions': {'July': 2, 'August': 2}}
    Returns:
        bool: True for success, False otherwise.
    """
    logger.info('Sending email...')
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL
    )
    message.dynamic_template_data = summary_information
    message.template_id = SENDGRID_SUMMARY_TEMPLATE_ID
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(response.status_code)
        logger.info(response.body)
        logger.info(response.headers)
        return True
    except Exception as e:
        logger.info(f'An error occurred while sending the summary information: {str(e)}')
        return False


def get_account() -> Account:
    """
    Gets or creates an account with the email assigned to the environment variable TO_EMAIL
    Returns:
        Account: Account to use.
    """
    logger.info('Getting the account...')
    account, created = Account.get_or_create(
        email=TO_EMAIL,
        defaults={'name': 'Edgar', 'paternal_surname': 'de la Cruz', 'maternal_surname': 'Vasconcelos'}
    )
    return account


def lambda_handler(event=None, context=None) -> dict:
    account = get_account()
    df = read_csv()
    summary_information = get_summary_information(account, df)
    save_db(account, df)
    send_mail(summary_information)
    return {
        "message": "Processed information"
    }


if __name__ == '__main__':
    lambda_handler()
