# Account Class
# Author: Chan Khine

class Account:

    def __init__(self, customer_name, customer_type, balance, fees_charged):
        self.customer_name = customer_name
        self.customer_type = customer_type
        self.balance = balance
        self.fees_charged = fees_charged

    ACCOUNTS = []

    @classmethod
    def create_account(cls, c_name, c_type):
        """
        Create new account if the account does not exist.
        Check existing accounts with both customer name and type in case
        there are same name and type.
        c_name: customer name
        c_type: customer type retail (R) or business (B)
        """
        # print("creating new account")
        customer_name = c_name
        customer_type = c_type
        balance = 0
        fees_charged = 0
        new_account = Account(customer_name, customer_type, balance, fees_charged)
        cls.add(new_account)
        # print(customer_name, customer_type, balance)
        index = len(cls.ACCOUNTS) - 1
        # print("Account created\n")
        return index

    @classmethod
    def add(cls, account):
        """
        Add each account to the account list.
        """
        cls.ACCOUNTS.append(account)

    @classmethod
    def check_existing_accounts(cls, c_name, c_type):
        """
        Return new account index if the account list is empty.
        Return the index of an existing account with same customer name and type.
        Return new account index if account does not exist in the system.
        c_name: customer name
        c_type: customer type retail (R) or business (B)
        """
        # print("Checking account")
        if len(cls.ACCOUNTS) == 0:
            # print("Empty list")
            index = cls.create_account(c_name, c_type)

        else:
            for i in cls.ACCOUNTS:
                # checking after taking all white space out and making them lower case
                if i.customer_name.lower().replace(" ", "") == c_name.lower().replace(" ", "") \
                        and i.customer_type.lower().replace(" ", "") == c_type.lower().replace(" ", ""):
                    index = cls.ACCOUNTS.index(i)
                    # print("Account Exist")
                    # print("account index")
                    return index

            # print("No account")
            index = cls.create_account(c_name, c_type)

        # print("pass index")
        return index

    @classmethod
    def account_deposit(cls, c_name, c_type, tran):
        """
        Add deposits to existing account.
        If account does not exist, create new account and add deposit.
        c_name: customer_name
        c_type: customer_type retail (R) or business (B)
        tran: transaction
        """
        account = cls.check_existing_accounts(c_name, c_type)
        customer_account = cls.ACCOUNTS[account]
        # print(customer_account.customer_name, customer_account.balance, tran)
        customer_account.balance += tran
        # print("Deposit processed.\n")

    @classmethod
    def account_withdrawal(cls, c_name, c_type, tran):
        """
            Withdraw from existing account if balance is greater than the withdrawal amount.
            c_name: customer_name
            c_type: customer_type retail (R) or business (B)
            tran: transaction
        """
        account = cls.check_existing_accounts(c_name, c_type)
        customer_account = cls.ACCOUNTS[account]
        # print(customer_account.customer_name, customer_account.balance, tran)
        customer_account.balance -= tran
        # print("Withdrawal processed")


class Retail(Account):

    """
    Retail account has the same properties as the bank account except for overdrawn fees.
    """

    def __init__(self, customer_name, customer_type, balance, fees_charged):
        super().__init__(customer_name, customer_type, balance, fees_charged)

    @classmethod
    def account_withdrawal(cls, c_name, c_type, tran):
        """
        If a retail customer is overdrawn, 30 USD fee is applied and withdrawal is not processed.
        If there is no account, a new account is created and overdrawn fee is charged.
        """

        account = super().check_existing_accounts(c_name, c_type)
        customer_account = cls.ACCOUNTS[account]

        if customer_account.balance >= tran:
            super().account_withdrawal(c_name, c_type, tran)

        else:
            # print("Retail overdrawn")
            overdrawn_fee = 30
            customer_account.fees_charged += overdrawn_fee
            customer_account.balance -= overdrawn_fee
            # print(customer_account.customer_name, customer_account.balance, tran, overdrawn_fee)
            # print("Fees charged and withdrawal not processed.\n")


class Business(Account):

    """
    Business account has the same properties as the bank account except for overdrawn fees.
    """
    def __init__(self, customer_name, customer_type, balance, fees_charged):
        super().__init__(customer_name, customer_type, balance, fees_charged)

    @classmethod
    def account_withdrawal(cls, c_name, c_type, tran):
        """
        If a business customer is overdrawn, 1% of amount overdrawn is applied and withdrawal is not processed.
        If there is no account, a new account is created and overdrawn fee is charged.
        """

        account = super().check_existing_accounts(c_name, c_type)
        customer_account = cls.ACCOUNTS[account]

        if customer_account.balance >= tran:
            super().account_withdrawal(c_name, c_type, tran)

        else:
            # print("Business overdrawn")
            # overdrawn calculation
            overdrawn_fee = 0.01
            overdrawn_amount = tran - customer_account.balance
            total_fee = overdrawn_amount * overdrawn_fee
            customer_account.fees_charged += total_fee
            customer_account.balance -= total_fee
            # print(customer_account.customer_name, customer_account.balance, tran, total_fee)
            # print("Fees charged and withdrawal not processed\n")
