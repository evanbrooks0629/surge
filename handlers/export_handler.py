import csv
from handlers import account_handler


def export_file(filename):
    if filename:
        accounts = account_handler.get_all_accounts()
        top_row = ['First', 'Last', 'Email', 'Phone', 'Address', 'City', 'State', 'Zip', 'Card', 'Exp', 'CVV',
                   'Name', 'Address', 'City', 'State', 'Zip']
        with open(filename, 'w') as exportfile:
            newfile = csv.writer(exportfile, dialect='excel')
            newfile.writerow(top_row)
            for account in accounts:
                newfile.writerow(account)
