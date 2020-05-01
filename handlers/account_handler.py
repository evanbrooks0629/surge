import json

def get_all_accounts():
    with open("user_files/accounts.json", "r") as file:
        accounts = json.load(file)

    return accounts

def get_account(index):
    with open("user_files/accounts.json", "r") as file:
        accounts = json.load(file)

    return accounts[index]

def get_num_accounts():
    with open("user_files/accounts.json", "r") as file:
        accounts = json.load(file)

    return len(accounts)

def insert_accounts(accounts):
    with open("user_files/accounts.json", "w") as file:
        json.dump(accounts, file)

def get_accounts_as_string():
    with open("user_files/accounts.json", "r") as file:
        accounts = json.load(file)

    accounts_list = []

    for account in accounts:
        new_account_string = []
        account_string = []
        name = account[0] + ' ' + account[1]
        email = account[2]
        address = account[4]
        billing = account[8]
        billing = billing[-4:]
        billing = "ending in " + billing
        account_string.append(name)
        account_string.append(email)
        account_string.append(address)
        account_string.append(billing)
        for account_item in account_string:
            if len(account_item) > 22:
                account_item = account_item[0:18] + '...'
                new_account_string.append(account_item)
            else:
                space = ''
                for i in range(1, 22 - len(account_item)):
                    space += ' '
                account_item += space

                new_account_string.append(account_item)
        accounts_list.append(new_account_string)

    return accounts_list
