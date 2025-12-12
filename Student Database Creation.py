# Program to create the student database. We still have to add the table and data, I'm just
# making the program to share through GitHub to make sure that works on my end as well.

#Logan Gibson was virtually here

import sqlite3

def main():
    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cur.execute('''CREATE TABLE Students'''

    student_list = []

    conn.commit()

    conn.close()


if __name__ == '__main__':
    main()

