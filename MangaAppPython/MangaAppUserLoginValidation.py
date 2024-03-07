# Importing necessary function from a helper module
from MangaAppHelpers_PrettyTable import read_query

# Function to validate user login credentials
def validate_user_login(connection):
    print("\nManga Login")

    # Loop until valid option is selected
    option = ''
    while option not in ['1', '2', '3']:
        option = input("Enter 1 or 2 or 3:\n    1) Login\n    2) Create An Account\n    3) Quit\n")

        # Option for existing users to login
        if option == '1':
            # Variable to control login validation loop
            validity = False
            while not validity:
                print("\nEnter Login Information")
                user_name = input("Enter user name: ").upper()
                user_password = input("Enter password: ")

                # Query to check user login credentials
                q1 = ''' CALL user_login_check('{u}', '{p}');'''.format(u=user_name, p=user_password)
                res = read_query(connection, q1)
                results = {}
                for row in res:
                    results[row['loginId']] = row['loginPassword']

                # Query to check admin login credentials
                q2 = ''' CALL admin_login_check('{u}', '{p}');'''.format(u=user_name, p=user_password)
                res_admin = read_query(connection, q2)
                results_admin = {}
                for row in res_admin:
                    results_admin[row['loginId']] = row['loginPassword']

                # Validate user login
                if user_name in results and results[user_name] == user_password:
                    validity = True
                    print("\nLogin Successful")
                    return 1, user_name

                # Validate admin login
                if user_name in results_admin and results_admin[user_name] == user_password:
                    validity = True
                    print("\nAdmin Login Successful")
                    return 2, user_name

                # Invalid login
                else:
                    print("\nInvalid Credentials or No Account Found")

        # Option for creating a new account
        elif option == '2':
            print("\nEnter A New User Name and Password")

            # Query to fetch existing usernames
            q3 = ''' Call user_names_list();'''
            result_user = read_query(connection, q3)
            user_login_ids = [*map(lambda d: next(iter(d.values())), result_user)]

            # Asking for a new username that hasn't been used
            user_name = user_login_ids[0]
            while user_name in user_login_ids:
                user_name = input("\nEnter User Name: ").upper()

                if user_name in user_login_ids:
                    print("User Name Already Exists")

            user_password = input("Enter Password: ")

            # Collecting additional user information
            first_name = input("Enter First Name: ").title()
            last_name = input("Enter Last Name: ").title()
            email = input("Enter Email Address: ").lower()

            # Creating new account through procedure call
            q4 = '''CALL create_user('{u}', '{p}', '{f}', '{l}', '{e}');'''.format(u=user_name, p=user_password,
                                                                                   f=first_name, l=last_name,
                                                                                   e=email)
            read_query(connection, q4)
            print("\nLogged into new account \n Welcome!")
            return 1, user_name

        # Option to quit the program
        elif option == '3':
            return 3, 'Quit'
