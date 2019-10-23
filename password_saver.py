import pickle
import sys
import re
#The password list - We start with it populated for testing purposes
entries = [["yahoo", "XqffoZeo"], ["google", "CoIushujSetu"]]
#The password file name to store the data to
password_file_name = "samplePasswordFile.pickle"
#The encryption key for the caesar cypher
encryption_key = 16

menu_text = """
What would you like to do:
1. Open password file
2. Lookup a password
3. Add a password
4. Edit a password
5. Delete a password
6. Save password file
7. Print the encrypted password list (for testing)
8. Quit program
Please enter a number (1-6)"""


def password_encrypt(unencrypted_message, key):
    """Returns an encrypted message using a caesar cypher

    :param unencrypted_message (string)
    :param key (int) The offset to be used for the caesar cypher
    :return (string) The encrypted message
    """

    #Fill in your code here.
    # If you can't get it working, you may want to put some temporary code here
    # While working on other parts of the program

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


def load_password_file(file_name):
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


def save_password_file(file_name):
    """Saves a password file.  The file will be created if it doesn't exist.

    :param file_name (string) The file to save.
    """
    try:
        pickle.dump( (entries, encryption_key), open( file_name, "wb" ) )
    except:
        print("Could not save the file.")


def add_entry(website, password):
    """Adds an entry with a website and password

    Logic for function:

    Step 1: Use the password_encrypt() function to encrypt the password.
            The encryptionKey variable is defined already as 16, don't change this
    Step 2: create a list of size 2, first item the website name and the second
            item the password.
    Step 3: append the list from Step 2 to the password list


    :param website (string) The website for the entry
    :param password (string) The unencrypted password for the entry
    """
    encrypted_password = password_encrypt(password, encryption_key)
    new_entry = [website, encrypted_password]
    entries.append(new_entry)


def edit_entry(website, password):
    """Edits an existing entry's password

    :param website (string) The website for the entry edit
    :param password (string) The new password for the entry
    """
    encrypted_password = password_encrypt(password, encryption_key)
    for i, entry in enumerate(entries):
        if entry[0] == website:
            entries[i][1] = encrypted_password


def delete_entry(website):
    """Deletes an existing entry
    :param website (string) The website of the entry to delete
    """
    for i, entry in enumerate(entries):
        if entry[0] == website:
            entries.remove(entries[i])


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


def lookup_password(website):
    """Lookup the password for a given website

    Logic for function:
    1. Create a loop that goes through each item in the password list
     You can consult the reading on lists in Week 5 for ways to loop through a list

    2. Check if the name is found.  To index a list of lists you use 2 square backet sets
      So passwords[0][1] would mean for the first item in the list get it's 2nd item (remember, lists start at 0)
      So this would be 'XqffoZeo' in the password list given what is predefined at the top of the page.
      If you created a loop using the syntax described in step 1, then i is your 'iterator' in the list so you
      will want to use i in your first set of brackets.

    3. If the name is found then decrypt it.  Decrypting is that exact reverse operation from encrypting.  Take a look at the
    caesar cypher lecture as a reference.  You do not need to write your own decryption function, you can reuse passwordEncrypt

     Write the above one step at a time.  By this I mean, write step 1...  but in your loop print out every item in the list
     for testing purposes.  Then write step 2, and print out the password but not decrypted.  Then write step 3.  This way
     you can test easily along the way.

    :param website (string) The website for the entry to lookup
    :return: Returns an unencrypted password.  Returns None if no entry is found
    """
    website_in_entries = False
    index = 0
    for i, entry in enumerate(entries):
        if entry[0] == website:
            website_in_entries = True
            index = i
            break
    if website_in_entries:
        # return decrypted password
        return password_encrypt(entries[index][1], -(encryption_key))
    else:
        return None

"""
I changed the behavior of the program a bit, to avoid the condition where
there are multiple entries for the same website name. I made it so the user specifies
an integer as the position of the entry to edit or delete.


"""
while True:
    print(menu_text)
    choice = input()

    if(choice == '1'): # Load the password list from a file
        load_password_file(password_file_name)

    if(choice == '2'): # Lookup at password
        print("Which website do you want to lookup the password for?")
        # Print all Website entries accompanied with index + 1 (for readability),
        # then ask user to choose which index + 1 to edit
        for i, key_value in enumerate(entries):
            print(f"{i + 1}: {key_value[0]}")
        website_index = int(input(f"Please enter a number (1-{len(entries)}): ")) - 1
        website = entries[website_index][0]

        password = lookup_password(website)
        if password:
            print('The password is: ', password)
        else:
            print('Password not found')

    if(choice == '3'): # Add a new entry
        print("What website is this password for?")
        website = input()
        print("What is the password?")
        unencrypted_password = input()
        isPasswordComplex, returnString = check_complexity(unencrypted_password)
        if isPasswordComplex:
            add_entry(website, unencrypted_password)
        else:
            print(returnString)
    if (choice == '4'):  # Edit a password
        print("Which website's password do you want to edit? (Overwrite)")
        for i, key_value in enumerate(entries):
            print(f"{i + 1}: {key_value[0]}")
        website_index = int(input(f"Please enter a number (1-{len(entries)}): ")) - 1
        website = entries[website_index][0]

        password = lookup_password(website)
        if password:
            new_password = input("Enter the new password: ")
            isPasswordComplex, returnString = check_complexity(new_password)
            if isPasswordComplex:
                edit_entry(website, new_password)
            else:
                print(returnString)
        else:
            print("Website not found.")
    if (choice == '5'): # Delete an entry
        print("Which entry number do you wish to delete?")
        for i, key_value in enumerate(entries):
            print(f"{i+1}: {key_value[0]}")
        website_index = int(input(f"Please enter a number (1-{len(entries)}): ")) - 1
        website = entries[website_index][0]
        password = lookup_password(website)

        if password:
            delete_entry(website)
            print(f"Entry for {website} has been deleted.")
        else:
            print(f"Entry for {website} can't be deleted since it doesn't exist.")
    if(choice == '6'): #Save the passwords to a file
            save_password_file(password_file_name)

    if(choice == '7'): #print out the password list
        for key_value in entries:
            print(', '.join(key_value))

    if(choice == '8'):  #quit our program
        sys.exit()
