# Bank Class
# Author: Chan Khine

import os
import pandas as pd
from tabulate import tabulate

from account import Account
from account import Retail
from account import Business


class Bank:

    """
    Will read transaction files, process the transactions, and print out the results.
    file_name: each transaction file name
    customer_name: name
    customer_type: retail (R) or business (B)
    transaction_type: deposit (D) or withdrawal (W)
    transaction: monetary amount
    """

    def __init__(self, customer_name, customer_type, transaction_type, transaction):
        self.customer_name = customer_name
        self.customer_type = customer_type
        self.transaction_type = transaction_type
        self.transaction = transaction

    FILES_LIST = []
    ALL_TRANSACTIONS = []

    @classmethod
    def load_all(cls, path):
        """
        Load all transaction files, sort the names, and put into a list.
        """
        # sort files in folder
        dir_list = os.listdir(path)
        for f in dir_list:
            if f.endswith(".csv"):
                cls.FILES_LIST.append(f)
        cls.FILES_LIST.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

        # load sorted files
        for file in cls.FILES_LIST:
            with open(path + '/' + file, encoding="ISO-8859-1") as f:
                lines = f.read().splitlines()
                for line in lines:
                    words = line.split(',')
                    customer_name = words[0].strip()
                    # strip white space and take initials only if there are words
                    ct = words[1].upper().replace(" ", "")
                    ct = ct[0]
                    customer_type = ct
                    tt = words[2].upper().replace(" ", "")
                    tt = tt[0]
                    transaction_type = tt
                    transaction = float(words[3])
                    customer = Bank(customer_name, customer_type, transaction_type, transaction)
                    cls.add(customer)

    @classmethod
    def add(cls, customer):
        """
        Add each transaction to the transactions list.
        """
        cls.ALL_TRANSACTIONS.append(customer)

    @classmethod
    def process_account(cls):
        """
        Process deposits and withdrawals for Retail and Business accounts in the transaction list.
        """
        # print("Processing account")
        for t in cls.ALL_TRANSACTIONS:
            if t.transaction_type == 'D':
                # print("Deposits")
                Account.account_deposit(t.customer_name, t.customer_type, t.transaction)

            if t.transaction_type == 'W':
                if t.customer_type == 'R':
                    Retail.account_withdrawal(t.customer_name, t.customer_type, t.transaction)
                else:
                    Business.account_withdrawal(t.customer_name, t.customer_type, t.transaction)

    @classmethod
    def display(cls):
        """
        Display the overall balance of the bank and a table containing customer type, total balance, and fees charged.
        """
        df = pd.DataFrame({'Customer Name': pd.Series(dtype='str'),
                           'Customer Type': pd.Series(dtype='str'),
                           'Fees': pd.Series(dtype='float'),
                           'Balance': pd.Series(dtype='str'),
                           })

        for account in Account.ACCOUNTS:
            df.loc[len(df)] = [account.customer_name, account.customer_type,
                               account.fees_charged, account.balance]

        df = df.sort_values('Balance', ascending=False)

        total_deposits = df['Balance'].sum()
        print(f'{"Bank Overall Deposited Balance"}:', f'{total_deposits}')
        print(tabulate(df, showindex=False, headers=df.columns,
                       tablefmt="pretty", colalign=("left", "center", "right", "right")))

    @classmethod
    def process_transaction(cls, path):
        """
        Call all functions to automate the transaction process.
        path: path for data files
        """
        # instantiate recommender and load data
        print('\nLoading data ...', end=' ')  # if you don't put end, it will go to newline
        Bank.load_all(path)
        print('Done\n')

        print('Processing transactions...', end=' ')
        Bank.process_account()
        print('Done\n')

        Bank.display()
