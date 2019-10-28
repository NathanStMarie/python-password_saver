import pickle
import sys
import re
#The password list - We start with it populated for testing purposes
entries = {'yahoo':{'username':'johndoe', 'password':'XqffoZeo', 'url':'https://www.yahoo.com'},
            'google':{'username':'johndoe', 'password':'CoIushujSetu', 'url':'https://www.google.com'}}
#The name of the file to save/load by default
file_name = "samplePasswordListFile.pickle"
#The password file name to store the data to
password_file_name = "PasswordFile.pickle"
#The encryption key for the caesar cypher
encryption_key = 16


def password_encrypt (unencrypted_message, key):
    """Returns an encrypted message using a caesar cypher

    :param unencrypted_message (string)
    :param key (int) The offset to be used for the caesar cypher
    :return (string) The encrypted message
    """
    encrypted_message = ""
    ord_list = []
    for char in unencrypted_message:
        new_ord = ord(char) + key
        if new_ord > 126:
            ord_list.append(32 + (new_ord - 126))
        elif new_ord < 32:
            ord_list.append(126 - (32 - new_ord))
        else:
            ord_list.append(ord(char) + key)
    for o in ord_list:
        encrypted_message += chr(o)
    return encrypted_message


def check_complexity(password):
    """Checks if the password meets complexity requirements.
    :param password (string) The password being checked for complexity requirements.
    :return: contstraint_string (string, empty if password is complex, descriptor if not)
             isPasswordComplex (Boolean, self-explanatory)

    Complexity requirements: password must be 12 char minimum length, must contain
    at least one capital letter, at least one lowercase letter, at least two numbers, and at
    least one special character (!@#$%^&*()_+).

    This function requires "import re" (Regular Expression)
    """
    constraint_string = ""
    isPasswordComplex = True

    if (len(password) < 12):
        constraint_string = "Password is not long enough. (min length is 12)."
        isPasswordComplex = False
    elif not re.search("\d{2}", password):
        constraint_string = "Password has one or no digits (min. 2)."
        isPasswordComplex = False
    elif not re.search("[A-Z]", password):
        constraint_string = "Password doesn't have any capital letters."
        isPasswordComplex = False
    elif not re.search("[a-z]", password):
        constraint_string = "Password doesn't have any lowercase letters."
        isPasswordComplex = False
    elif not re.search("[!@#$%^&*()\-+]", password):
        constraint_string = "Password has no special character (!@#$%^&*()_+)."
        isPasswordComplex = False
    return isPasswordComplex, constraint_string


def load_password_file():
    """Loads a password file.  The file must be in the same directory as the .py file

    :param file_name (string) The file to load.  Must be a pickle file in the correct format
    """
    try:
        with open(file_name, 'rb') as f:
            loaded_entries, loaded_encryption_key = pickle.load(f)
        global entries, encryption_key
        entries = loaded_entries
        encryption_key = loaded_encryption_key
    except:
        print(f"Could not load the password file. Make sure the filename is {file_name}")

def save_password_file():
    """Saves a password file.  The file will be created if it doesn't exist.

    :param file_name (string) The file to save.
    """
    try:
        pickle.dump( (entries, encryption_key), open( file_name, "wb" ) )
    except:
        print("Could not save the file.")

def add_entry():
    """Adds an entry with an entry title, username, password and url

    Includes all user interface interactions to get the necessary information from the user
    """
    website = input("Enter the website to pair with the password: ")
    username = input("Enter the username: ")
    url = input("Enter the URL: ")
    password = input("Enter the password: ")
    # Password complexity check here
    isPasswordComplex, constraint_string = check_complexity(password)
    if isPasswordComplex:
        entries[website] ={'username':username, 'password':password_encrypt(password, encryption_key), 'url':url}
    else:
        print(constraint_string)
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
              f"Password: {password_encrypt(entries[entry]['password'], -encryption_key)}")
    else:
        print("Invalid entry.")


def edit_entry():
    """Edits one of an existing entry's values.
    """
    for key in entries:
        print(key)
    entry = input("Enter the website to edit one of its attributes: ")
    if entry in entries:
        print(f"URL: {entries[entry]['url']}\n"
              f"Username: {entries[entry]['username']}\n"
              f"Password: {password_encrypt(entries[entry]['password'], -encryption_key)}")
        key = input("Enter the attribute you wish to edit: ")
        if key in entries[entry]:
            new_value = input(f"Enter the value to change the {key} to: ")
            if key == "password":
                isPasswordComplex, constraint_string = check_complexity(new_value)
                if isPasswordComplex:
                    entries[entry][key] = password_encrypt(new_value, encryption_key)
                else:
                    print(constraint_string)
            else:
                entries[entry][key] = new_value
            print(f"The {key} value in the {entry} entry has been changed to {new_value}.")
        else:
            print("Invalid choice.")
    else:
        print("Invalid entry.")


def delete_entry():
    """Deletes an existing entry by name"""
    for key in entries:
        print(key)
    entry = input("Enter the entry to delete: ")
    if entry in entries:
        entries.pop(entry)
        print(f"The {entry} entry has been removed.")
    else:
        print("Invalid entry.")


def end_program():
    sys.exit()

menu_text = """
What would you like to do:
1. Open password file
2. Add an entry
3. Edit an entry
4. Delete an entry
5. Lookup an entry
6. Save password file
7. Quit program
Please enter a number (1-6)"""

menu_dict = {'1': load_password_file,
             '2': add_entry,
             '3': edit_entry,
             '4': delete_entry,
             '5': print_entry,
             '6': save_password_file,
             '7': end_program}

while True:
    user_choice = input(menu_text)
    if user_choice in menu_dict and menu_dict[user_choice]:
        menu_dict[user_choice]()
    else:
        print('Not a valid choice')
