# Main Banking Program
# Author: Chan Khine

from bank import Bank


def main(path):
    """
    Main program to automate the transactions in file
    path: path to data files
    """
    app_title = 'Bank Transaction Program'
    print(len(app_title) * '-')
    print(app_title)
    print(len(app_title) * '-')

    Bank.process_transaction(path)

# MAIN PROGRAM
if __name__ == '__main__':
    main('data')
