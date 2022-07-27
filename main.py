import pandas as pd


def read_csv():
    df = pd.read_csv('summaries_information/summary_information.csv', delimiter=',', skip_blank_lines=True)
    return df


def process_data(df):
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


def send_mail():
    pass


def handler(event=None, context=None):
    data = read_csv()
    summary_information = process_data(data)
    print(summary_information)


if __name__ == '__main__':
    handler()




