import pickle
import sys

#The password list - We start with it populated for testing purposes
entries = {'yahoo':{'username':'johndoe', 'password':'XqffoZeo', 'url':'https://www.yahoo.com'},
            'google':{'username':'johndoe', 'password':'CoIushujSetu', 'url':'https://www.google.com'}}

#The password file name to store the data to
password_file_name = "PasswordFile.pickle"
#The encryption key for the caesar cypher
encryption_key = 16

menu_text = """
What would you like to do:
1. Open password file
2. Add an entry
3. Lookup an entry
4. Save password file
5. Quit program
Please enter a number (1-6)"""

def password_encrypt (unencrypted_message, key):
    """Returns an encrypted message using a caesar cypher

    :param unencrypted_message (string)
    :param key (int) The offset to be used for the caesar cypher
    :return (string) The encrypted message
    """

    #Fill in your code here.
    # #If you can't get it working, you may want to put some temporary code here
    # #While working on other parts of the program
    pass

def load_password_file():
    """Loads a password file.  The file must be in the same directory as the .py file

    :param file_name (string) The file to load.  Must be a pickle file in the correct format
    """
    entries, encryption_key = pickle.load(open(file_name, "rb"))

def save_password_file():
    """Saves a password file.  The file will be created if it doesn't exist.

    :param file_name (string) The file to save.
    """
    pickle.dump( (entries, encryption_key), open( password_file_name, "wb" ) )

def add_entry():
    """Adds an entry with an entry title, username, password and url

    Includes all user interface interactions to get the necessary information from the user
    """
    website = input("Enter the website to pair with the password: ")
    username = input("Enter the username: ")
    url = input("Enter the URL: ")
    password = input("Enter the password: ")
    # Password complexity check here
    entries[website] ={'username':username, 'password':password, 'url':url}

def print_entry():
    """Asks the user for the name of the entry and prints all related information in a pretty format
    """
    print("Which entry do you want to lookup the information for?")
    for key in entries:
        print(key)
    entry = input()

    if entry in entries:
        print(f"Website: {entry}\n"
              f"URL: {entries[entry]['url']}\n"
              f"Username: {entries[entry]['username']}\n"
              f"Password: {entries[entry]['password']}") # Don't forget to decrypt
    else:
        print("Invalid entry.")
def end_program():
    sys.exit()

menu_dict = {'1': load_password_file,
             '2': add_entry,
             '3': print_entry,
             '4': save_password_file,
             '5': end_program}

while True:
    user_choice = input(menu_text)
    if user_choice in menu_dict and menu_dict[user_choice]:
        menu_dict[user_choice]()
    else:
        print('Not a valid choice')
