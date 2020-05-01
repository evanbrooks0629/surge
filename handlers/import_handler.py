import csv
from handlers import account_handler


def import_file(csv_file):
    if csv_file:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            new_accounts = []
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    new_account = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]]
                    new_accounts.append(new_account)
                line_count += 1
            all_accounts = account_handler.get_all_accounts()
            all_accounts += new_accounts
            account_handler.insert_accounts(all_accounts)
