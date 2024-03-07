from MangaAppHelpers_PrettyTable import user_menu, read_query, create_server_connection, prettytable
from MangaAppUserLoginValidation import validate_user_login
from MangaAppAdmin import admin_menu


def main():
    # Create a server connection
    connection = create_server_connection()

    # Check if the connection is open
    if connection.open:
        # Validate user login
        account_type, username = validate_user_login(connection)

        # User interaction
        if account_type == 1:
            user_menu(connection, username)

        # Admin interaction
        elif account_type == 2:
            admin_menu(connection, username)

        # Quit
        elif account_type == 3:
            print("Quitting")

        # Close the connection
        connection.close()


if __name__ == "__main__":
    main()
