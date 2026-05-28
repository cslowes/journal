import editor, sqlite3, sys

from datetime import datetime
from pathlib import Path, PosixPath


def main():

    # Database presence check    
    check_db()

    # Loads welcome page and gets user selection
    main_selection = welcome()   
    # Match case for user input
    match main_selection:
        # New entry
        case "n" | "N":
            new_entry()
        # Entry history
        case "h" | "H":
            #todo
            print("History!")
        # Exit
        case "e" | "E":
            print("Exit!")
            sys.exit()


def create_db(con, cur):
    # Creates new tables in database
    cur.execute(
        "CREATE TABLE entries (time DATETIME, content TEXT)"
    )
    con.commit()


def check_db():
    # Opens databse connection and checks table is present
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    res = cur.execute(
        "SELECT name FROM sqlite_master WHERE name='entries';"
    )

    # If table not found, database is created
    if res.fetchone() is None:
        print("Database not found!\nCreating database...")
        create_db(con, cur)
        print("Done!")
    else:
        print("Database found!")
    con.close()


def new_entry():

    print("New entry")

    # Confirms selection from user
    confirmation = input("Are you sure you want to create a new entry? (y / n)\n")
    if confirmation == "y" or confirmation == "Y":

        # Opens editor and adds header with current date and time
        message = editor.edit(contents=datetime.now().strftime('%A, %d %B %Y %H:%M').encode())

        # Writes closed file to storage
        write_file(message)
        print(str(message, 'utf-8'))
    else: 
        print("Exiting journal")
        sys.exit()


def welcome():
    # Prints welcome ASCII art
    print(r"""
    ___  ________  ___  ___  ________  ________   ________  ___          
   |\  \|\   __  \|\  \|\  \|\   __  \|\   ___  \|\   __  \|\  \         
   \ \  \ \  \|\  \ \  \\\  \ \  \|\  \ \  \\ \  \ \  \|\  \ \  \        
 __ \ \  \ \  \\\  \ \  \\\  \ \   _  _\ \  \\ \  \ \   __  \ \  \       
|\  \\_\  \ \  \\\  \ \  \\\  \ \  \\  \\ \  \\ \  \ \  \ \  \ \  \____  
\ \________\ \_______\ \_______\ \__\\ _\\ \__\\ \__\ \__\ \__\ \_______\
 \|________|\|_______|\|_______|\|__|\|__|\|__| \|__|\|__|\|__|\|_______|                    
                                                                         
                                                                         """)
    print("Welcome to journal\n\nWhat would you like to do?")

    # Function returns users choice from main menu
    return input("n: create new entry\nh: view entry history\ne: exit\n\n")


def write_file(message):
    # Create filepath
    p = PosixPath('~/journal').expanduser()

    # Check filepath exists and create if not
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

    # Create filename with current date
    filename = str(datetime.now().strftime('%d_%m_%Y')) + ".txt"
    # Create path to new file
    filepath = str(p) + "/" + filename

    # Open file and write message to it
    with open(filepath, "x") as f:
        f.write(str(message, 'utf-8'))   


# run main function
if __name__ == "__main__":
    main()

# CONVERT BYTE LIKE SEQUENCE TO STRING: 
#
# str(message, 'utf-8')