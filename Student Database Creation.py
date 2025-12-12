# Title: Student Database Creation
# Authors: Logan Gibson and Arianna Endres
# Date 12/12/2025

# This program creates the student database.

import sqlite3

def main():
    # Connect to the database.
    conn = sqlite3.connect('students.db')

    # Get the cursor.
    cur = conn.cursor()

    # Create the Students table if it doesn't already exist.

    cur.execute('''DROP TABLE IF EXISTS Students''')

    cur.execute('''CREATE TABLE Students (Student_ID PRIMARY KEY INTEGER NOT NULL, Name TEXT NOT NULL, Graduation_Year INTEGER, 
                Primary_Major TEXT, Hometown TEXT, Email TEXT, Student_Type TEXT, Campus_Status TEXT)''')

    # Call the populate_table function to add the student data to the table.
    populate_table(cur)

    # Commit the changes.
    conn.commit()

    # Close the database connection.
    conn.close()


# This function iterates through the list of student data and adds each entry to the database.
def populate_table(cur):
    # Create the list of student data.
    student_list = [[1, 'James Christian Gehrke', 2029, 'Biochemistry', 'Fargo ND', 'jcgehrke@students.unwsp.edu', 'PSEO', 'commuter'],
                    [2, 'Makayla Serenity Andersen', 2027, 'Mathematics Education', 'Duluth MN', 'msandersen@students.unwsp.edu', 'undergraduate', 'resident'],
                    [3, 'Ryan Jonathon Berkely', 2026, 'Master of Divinity', 'Denver CO', 'rjberkely@students.unwsp.edu', 'graduate', 'online'],
                    [4, 'Samantha Madison Buchanan', 2029, 'English', 'Madison WI', 'smbuchanan@students.unwsp.edu', 'Early College', 'online'],
                    [5, 'Emmanuel Santiago Martinez', 2028, 'Computer Science', 'Minneapolis MN', 'esmartinez@students.unwsp.edu', 'undergraduate', 'resident'],
                    [6, 'Gabriel Alexander Hanson', 2029, 'Undeclared', 'Phoenix AZ', 'gahanson@students.unwsp.edu', 'undergraduate', 'online'],
                    [7, 'Katherine Rose Owens', 2027, 'Associate of Arts', 'Rochester MN', 'krowens@students.unwsp.edu', 'PSEO', 'online'],
                    [8, 'Allan Anthony Green', 2026, 'Master of Business Administration', 'St. Paul MN', 'aagreen@students.unwsp.edu', 'graduate', 'resident'],
                    [9, 'Eliana Marie Thompson', 2028, 'Health Science', 'Des Moines IA', 'emthompson@students.unwsp.edu', 'undergraduate', 'commuter'],
                    [10, 'Sofia Mae King', 2027, 'Doctor of Philosophy', 'Detroit MI', 'smking@students.unwsp.edu', 'graduate', 'online']]

    # Add each entry into the database by iterating through the list of entries and adding each of their elements to the corresponding column.
    for entry in student_list:
        cur.execute('''INSERT INTO Students (Student_ID, Name, Graduation_Year, Primary_Major, Hometown, Email, Student_Type, Campus_Status)
                    Values (?, ?, ?, ?, ?, ?, ?, ?)''', (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7]))


# Call the main function.
if __name__ == '__main__':
    main()

