#Date: 12/##/25
#Authors: Logan Gibson & Arianna Endres
#Title: "Student Database CRUD" 

import sqlite3

conn = sqlite3.connect('students.db')

#add the cursor object
cur = conn.cursor()

MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5

#create the main function that controls menu navigation
def main():
    
    choice = 0
    
    while choice != EXIT:
        
        display_menu()
        choice = get_menu_choice()
   
        if choice == CREATE:
            create()
        elif choice == READ:
            read()
        elif choice == UPDATE:
            update()
        elif choice == DELETE:
            delete()

#show the menu's display
def display_menu():
    
    print('\n------- Student Profile Database -------')
    print('1. Create a new student profile')
    print('2. Read a student profile')
    print('3. Update a student profile')
    print('4. Delete a student profile')
    print('5. Exit the database')



#get the user's menu navigation choice
def get_menu_choice():
    choice = 0
    choice = int(input('Enter your choice:'))

    #make sure choice is valid
    while choice < MIN_CHOICE or choice > MAX_CHOICE:
        print(f'Valid choices are {MIN_CHOICE} through {MAX_CHOICE}.')
        choice = int(input('Enter your choice: '))

    return choice

#add a new entry to the Entries table
#note the insert_row() function


#Student_ID INTEGER NOT NULL, Name TEXT NOT NULL, Graduation_Year INTEGER, 
#Primary_Major TEXT, Hometown TEXT, Email TEXT, Student_Type TEXT, Campus_Status TEXT

def create():
    print('Create New Student Profile')
    id = input('Student ID: ')
    name = input('Student Name: ')
    grad_year = input('Graduation Year: ')
    major = input('Primary Major: ')
    hometown = input('Hometown: ')
    email = input('Email: ')
    type = input('Student Type: ')
    status = input('Campus Status (online, resident, commuter): ')
    insert_row(id, name, grad_year, major, hometown, email, type, status)

#display an existing entry
#note the display_item() function
def read():
    name = input("Enter a student name to search for: ")
    num_found = display_profile(name)
    print(f'{num_found} row(s) found.')

#update an existing entry
#note the update_row() function
def update():
    
    #display existing entry so user can make an informed decision
    read()

    #change info
    selected_id = int(input("Select a student ID: "))
    name = input("Enter the new person's name: ")
    grad_year = input("Enter the new phone number: ")
    major = input("Enter their new major: ")
    hometown = input("Enter their new hometown: ")
    email = input("Enter their new email: ")
    type = input("Enter the student's type of study: ")
    status = input("Enter the student's campus_status: ")

    num_updated = update_row(selected_id, name, grad_year, major, hometown, email, type, status)
    print(f'{num_updated} row(s) updated.')

#delete an existing entry
#note the delete_row() function
def delete():
    selected_id = int(input('Select a student ID to delete: '))
    sure = input('Are you sure you want to delete this student profile? (y/n): ')
    if sure.lower() == 'y':
        num_deleted = delete_row(selected_id)
        print(f'{num_deleted} row(s) deleted')

#logic to insert a new row in the Students table
#this is referened by create()
def insert_row(id, name, grad_year, major, hometown, email, type, status):
    
    conn = None
    try:
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO Students
        (Student_ID, Name, Graduation_Year, 
                Primary_Major, Hometown, Email, Student_Type, Campus_Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (name, id, name, grad_year, major, hometown, email, type, status)) 
        conn.commit()

    except sqlite3.Error as err:
        print('Database Error', err)

    finally:
        if conn != None:
            conn.close()



#----------------------------------------------------------------------------------

#THE REST OF THIS CODE NEEDS TO BE UPDATED 

#----------------------------------------------------------------------------------



#logic to display an existing entry
#this is referenced by read()
def display_profile(name):
    conn = None
    results = []
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute(''' SELECT * FROM Entries
                    WHERE lower(Name) == ?''',
                    (name.lower(),))
        results = cur.fetchall()
        for row in results:
            print(f'ID: {row[0]:<3}\n'
                  f'Name: {row[1]:<15}\n' 
                  f'Phone Number: {row[2]:<6}')
    except sqlite3.Error as err:
        print('Database Error, err')
    finally:
        if conn != None:
            conn.close()

    return len(results)


#logic to update an existing entry
#this is referenced by update()
def update_row(id, name, phone_number):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''UPDATE Entries SET Name = ?, PhoneNumber = ?
                    WHERE EntryID == ?''',
                    (name, phone_number, id))
        conn.commit()
        num_updated = cur.rowcount
    except sqlite3.Error as err:
        print('Database Error', err)
    
    finally:
        if conn != None:
            conn.close()

    return num_updated

#logic to delete a row
#this is referenced by delete()
def delete_row(id):
    conn = None
    num_deleted = 0
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM Entries
                    WHERE EntryID == ?''', 
                    (id,))
        conn.commit()
        num_deleted = cur.rowcount

    except sqlite3.Error as err:
        print('Database Error', err)

    finally:
        if conn != None:
            conn.close
    
    return num_deleted


#call the main function

if __name__ == '__main__':
    main()