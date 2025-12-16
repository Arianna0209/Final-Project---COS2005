# Title: Student Database CRUD
# Author: Logan Gibson and Arianna Endres
# Date: 12/--/2025

# This program allows users to read, update, and delete data from the student database in a GUI window.

import sqlite3

import tkinter

import tkinter.messagebox

# Connect to the database.
conn = sqlite3.connect('students.db')

# Create the cursor.
cursor = conn.cursor()

class StudentDatabaseGUI:
    def __init__(self):
        # Create and title the main window.
        self.main_window = tkinter.Tk()
        self.main_window.title('Students')

        # Add the user prompt.
        self.prompt = tkinter.Label(self.main_window, text='Select an entry to modify or delete it, '
                                                           'or click "add entry" to add a new entry. '
                                                           'Click "search" to search the database '
                                                           'using a certain criteria.')


        # Set up the database list:
        # Add column labels.
        self.column_labels = tkinter.Label(self.main_window, text=f'{'ID':<10}\t{'Name':<86}{'Grad':<17}{'Primary Major':<95}'
                                                                  f'{'Hometown':<41}{'Email':<89}{'Student Type':<42}{'Campus Status':21}')

        # Create the student list frame.
        self.students_listbox_frame = tkinter.Frame(self.main_window)

        # Create a listbox for the student data.
        self.students_listbox = tkinter.Listbox(self.students_listbox_frame, font='TkFixedFont', width=175, height=20)

        # Create a scrollbar for the listbox.
        self.scrollbar = tkinter.Scrollbar(self.students_listbox_frame, orient=tkinter.VERTICAL)

        # Pack the listbox and scrollbar.
        self.students_listbox.pack(side='left')
        self.scrollbar.pack(side='right', fill=tkinter.Y)

        # Configure the scrollbar and listbox.
        self.scrollbar.config(command=self.students_listbox.yview)
        self.students_listbox.config(yscrollcommand=self.scrollbar.set)


        # Fill the students listbox:
        # Select all the data from the Students table.
        cursor.execute('''SELECT * FROM Students''')

        # Fetch the data and assign it the "students" variable.
        self.students = cursor.fetchall()

        # Iterate through each row in the list of students and add it to the listbox.
        for row in self.students:
            self.students_listbox.insert(tkinter.END, f'{row[0]:<6}{row[1]:<35}{row[2]:<8}{row[3]:<40}'
                                                      f'{row[4]:<20}{row[5]:<35}{row[6]:<20}{row[7]:<20}')



        # Create the buttons:
        # Create a frame for the buttons that will manipulate the data.
        self.button_frame = tkinter.Frame(self.main_window)

        # Create the add, modify, and delete buttons, which redirect the program to their respective functions.
        self.add_button = tkinter.Button(self.button_frame, text='Add Entry', command=self.add_entry_window)
        self.modify_button = tkinter.Button(self.button_frame, text='Modify Entry', command=self.modify_entry_window)
        self.delete_button = tkinter.Button(self.button_frame, text='Delete Entry', command=self.deletion_confirmation)
        self.search_button = tkinter.Button(self.button_frame, text='Search Database', command=self.search_criteria_selection_window)

        # Pack the buttons.
        self.add_button.pack(side='left', padx=5)
        self.modify_button.pack(side='left', padx=5)
        self.delete_button.pack(side='left', padx=5)
        self.search_button.pack(side='left', padx=5)

        # Create the quit button.
        self.quit_button = tkinter.Button(self.main_window, text='Quit', command=self.end_program_confirmation)

        # Pack all the widgets.
        self.prompt.pack(pady=5)
        self.column_labels.pack()
        self.students_listbox_frame.pack(padx=15, pady=(0, 10))
        self.button_frame.pack(padx=5, pady=5)
        self.quit_button.pack(padx=5, pady=5)

        # Call the tkinter mainloop.
        tkinter.mainloop()

    # Define the function that will allow the user to search the database:
    # Define the function that will allow the user to select criteria to search by.
    def search_criteria_selection_window(self):
        # Define the function that will allow the user to enter the criteria they would like to search by.
        def search():
            # Define the function that will allow the user to search the database by their criteria and edit the results.
            def search_database():
                # Get the input values
                id = id_entry.get()
                name = name_entry.get()
                grad = grad_entry.get()
                major = major_entry.get()
                hometown = hometown_entry.get()
                email = email_entry.get()
                type = type_entry.get()
                campus_status = campus_status_entry.get()

                # Make a list of input values.
                input_list = [id, name, grad, major, hometown, email, type, campus_status]

                # Set the integer values to zero instead of none to avoid SQL expecting an integer and getting none.
                if input_list[0] is None:
                    input_list[0] = 0

                if input_list[2] is None:
                    input_list[2] = 0

                # Create a search database window.
                search_database_window = tkinter.Toplevel(search_window)

                # Show the user the criteria they entered:
                # Create a frame.
                criteria_entered_frame = tkinter.Frame(search_database_window)

                # Create a label.
                entries_containing_label = tkinter.Label(criteria_entered_frame, text='Entries containing: ')

                # Pack the label.
                entries_containing_label.pack(side='left')

                # Remind the user of the search criteria they entered.
                for input in input_list:
                    # Make sure the user entered something for that criteria.
                    if input is not None:
                        input_label = tkinter.Label(criteria_entered_frame, text=f'\"{input}\", ')

                        input_label.pack(side='left')

                # Create a label with instructions for editing their searched data.
                searched_data_instructions = tkinter.Label(criteria_entered_frame,
                                                           text='Click an entry to modify or delete it, '
                                                                'otherwise click cancel to return to the search window.')

                # Create a listbox containing the matching database entries:
                # Create a frame.
                matching_entries_frame = tkinter.Frame(search_database_window)

                # Create the listbox.
                matching_entries_listbox = tkinter.Listbox(matching_entries_frame)


                # Search the database for the input.
                cursor.execute('''SELECT * FROM Students WHERE (Student_ID == ?, Name LIKE ?, Graduation_Year == ?, Primary_Major LIKE ?, 
                                                                Hometown LIKE ?, Email LIKE ?, Student_Type LIKE ?, Campus_Status LIKE ?)''',
                               (input_list[0], f'%{input_list[1]}%', input_list[2], f'%{input_list[3]}%', f'%{input_list[4]}%',
                                f'%{input_list[5]}%', f'%{input_list[6]}%', f'%{input_list[7]}%'))

                # Get the matching entries.
                matching = cursor.fetchall()

                # Add the matching entries to the listbox.
                for row in matching:
                    matching_entries_listbox.insert(tkinter.END, f'{row[0]:<6}{row[1]:<35}{row[2]:<8}{row[3]:<40}'
                                                                 f'{row[4]:<20}{row[5]:<35}{row[6]:<20}{row[7]:<20}')

                # Create buttons that allow the user to edit the matching entries:
                # Create the frame.
                matching_entry_button_frame = tkinter.Frame(search_database_window)

                # Create the modify and delete buttons, which redirect the program to their respective functions.
                modify_button = tkinter.Button(matching_entry_button_frame, text='Modify Entry',
                                               command=self.modify_entry_window)
                delete_button = tkinter.Button(matching_entry_button_frame, text='Delete Entry',
                                               command=self.deletion_confirmation)

                # Create a cancel button.
                cancel_database_search_button = tkinter.Button(matching_entry_button_frame, text='Search Database',
                                                               command=search_database_window.destroy)

                # Pack the buttons.
                modify_button.pack(side='left', padx=5)
                delete_button.pack(side='left', padx=5)
                cancel_database_search_button.pack()

                # Pack the frames.
                criteria_entered_frame.pack()
                matching_entries_frame.pack()
                matching_entry_button_frame.pack()


            # Create the window that will allow the user to input data to search.
            search_window = tkinter.Toplevel(search_criteria_window)

            # Add instructions so the user knows what to do.
            search_instruction_label = tkinter.Label(search_window, text='Enter the information you would like to '
                                                                         'search in the boxes below.')
            # Pack the instruction label.
            search_instruction_label.pack()

            # Create the entry boxes based on the selected criteria:
            if id_var.get() == 1:
                # Create the ID entry:
                # Create a frame.
                id_entry_frame = tkinter.Frame(search_window)

                # Create a label.
                id_label = tkinter.Label(id_entry_frame, text='ID')

                # Create an entry widget.
                id_entry = tkinter.Entry(id_entry_frame)

                # Pack the widgets.
                id_label.pack(side='left')
                id_entry.pack(side='left')

                # Pack the frame.
                id_entry_frame.pack()


            if name_var.get() == 1:
                # Create the name entry:
                # Create a frame.
                name_entry_frame = tkinter.Frame(search_window)

                # Create a label.
                name_label = tkinter.Label(name_entry_frame, text='Name')

                # Create an entry widget.
                name_entry = tkinter.Entry(name_entry_frame)

                # Pack the widgets.
                name_label.pack(side='left')
                name_entry.pack(side='left')

                # Pack the frame.
                name_entry_frame.pack()


            if grad_var.get() == 1:
                # Create the graduation entry:
                # Create a frame.
                grad_entry_frame = tkinter.Frame(search_window)

                # Create a label.
                grad_label = tkinter.Label(grad_entry_frame, text='Graduation Year')

                # Create an entry widget.
                grad_entry = tkinter.Entry(grad_entry_frame)

                # Pack the widgets.
                grad_label.pack(side='left')
                grad_entry.pack(side='left')

                # Pack the frame.
                grad_entry_frame.pack()


            if major_var.get() == 1:
                # Create the primary major entry:
                # Create a frame.
                major_entry_frame = tkinter.Frame(search_window)

                # Create a label.
                major_label = tkinter.Label(major_entry_frame, text='Major')

                # Create an entry widget.
                major_entry = tkinter.Entry(major_entry_frame)

                # Pack the widgets.
                major_label.pack(side='left')
                major_entry.pack(side='left')

                # Pack the frame.
                major_entry_frame.pack()


            if hometown_var.get() == 1:
                # Create the hometown entry:
                # Create a frame.
                hometown_entry_frame = tkinter.Frame(search_window)

                # Create a label.
                hometown_label = tkinter.Label(hometown_entry_frame, text='Hometown')

                # Create an entry widget.
                hometown_entry = tkinter.Entry(hometown_entry_frame)

                # Pack the widgets.
                hometown_label.pack(side='left')
                hometown_entry.pack(side='left')

                # Pack the frame.
                hometown_entry_frame.pack()


            if email_var.get() == 1:
                # Create the email entry:
                # Create a frame.
                email_entry_frame = tkinter.Frame(search_window)

                # Create a label.
                email_label = tkinter.Label(email_entry_frame, text='Email')

                # Create an entry widget.
                email_entry = tkinter.Entry(email_entry_frame)

                # Pack the widgets.
                email_label.pack(side='left')
                email_entry.pack(side='left')

                # Pack the frame.
                email_entry_frame.pack()


            if type_var.get() == 1:
                # Create the student type entry:
                # Create a frame.
                type_entry_frame = tkinter.Frame(search_window)

                # Create a label.
                type_label = tkinter.Label(type_entry_frame, text='Student Type')

                # Create an entry widget.
                type_entry = tkinter.Entry(type_entry_frame)

                # Pack the widgets.
                type_label.pack(side='left')
                type_entry.pack(side='left')

                # Pack the frame.
                type_entry_frame.pack()


            if campus_status_var.get() == 1:
                # Create the campus status entry:
                # Create a frame.
                campus_status_entry_frame = tkinter.Frame(search_window)

                # Create a label.
                campus_status_label = tkinter.Label(campus_status_entry_frame, text='Campus Status')

                # Create an entry widget.
                campus_status_entry = tkinter.Entry(cmapus_status_entry_frame)

                # Pack the widgets.
                campus_status_label.pack(side='left')
                campus_status_entry.pack(side='left')

                # Pack the frame.
                campus_status_entry_frame.pack()


            else:
                # Create an error window since the user did not select a criteria.
                tkinter.messagebox.showerror('Error', 'Please select a criteria to search by.')

                # Close the search window.
                search_window.destroy()


            # Create the buttons:
            # Create the frame.
            search_button_frame = tkinter.Frame(search_window)

            # Create the continue to search button.
            search_database_button = tkinter.Button(search_button_frame, text='Search Database', command=search_database)

            # Create the cancel button.
            cancel_search_button = tkinter.Button(search_button_frame, text='Cancel', command=search_window.destroy)

            # Pack the buttons.
            search_database_button.pack(side='left', padx=5)
            cancel_search_button.pack(side='left', padx=5)

            # Pack the button frame.
            search_button_frame.pack()


        # Create the window that will allow the user to choose a search criteria.
        search_criteria_window = tkinter.Toplevel(self.main_window)

        # Create instructions so the user knows what to do.
        criteria_instruction_label = tkinter.Label(search_criteria_window, text='Select the criteria you would like to search by below.')

        # Create the search criteria options:
        # Create the search criteria frame.
        search_criteria_frame = tkinter.Frame(search_criteria_window)

        # Create the IntVar objects.
        id_var = tkinter.IntVar()
        name_var = tkinter.IntVar()
        grad_var = tkinter.IntVar()
        major_var = tkinter.IntVar()
        hometown_var = tkinter.IntVar()
        email_var = tkinter.IntVar()
        type_var = tkinter.IntVar()
        campus_status_var = tkinter.IntVar()

        # Set the IntVar objects to zero.
        id_var.set(0)
        name_var.set(0)
        grad_var.set(0)
        major_var.set(0)
        hometown_var.set(0)
        email_var.set(0)
        type_var.set(0)
        campus_status_var.set(0)

        # Create the checkbuttons.
        id_checkbutton = tkinter.Checkbutton(search_criteria_frame, text='ID', variable=id_var)
        name_checkbutton = tkinter.Checkbutton(search_criteria_frame, text='Name', variable=name_var)
        grad_checkbutton = tkinter.Checkbutton(search_criteria_frame, text='Graduation Year', variable=grad_var)
        major_checkbutton = tkinter.Checkbutton(search_criteria_frame, text='Primary Major', variable=major_var)
        hometown_checkbutton = tkinter.Checkbutton(search_criteria_frame, text='Hometown', variable=hometown_var)
        email_checkbutton = tkinter.Checkbutton(search_criteria_frame, text='Email', variable=email_var)
        type_checkbutton = tkinter.Checkbutton(search_criteria_frame, text= 'Student Type', variable=type_var)
        campus_status_checkbutton = tkinter.Checkbutton(search_criteria_frame, text='Campus Status', variable=campus_status_var)

        # Pack the checkbuttons.
        id_checkbutton.pack()
        name_checkbutton.pack()
        grad_checkbutton.pack()
        major_checkbutton.pack()
        hometown_checkbutton.pack()
        email_checkbutton.pack()
        type_checkbutton.pack()
        campus_status_checkbutton.pack()


        # Create the buttons:
        # Create the frame.
        button_frame = tkinter.Frame(search_criteria_window)

        # Create the continue to search button.
        continue_to_search_button = tkinter.Button(button_frame, text='Continue to search', command=search)

        # Create the cancel button.
        cancel_button = tkinter.Button(button_frame, text='Cancel', command=search_criteria_window.destroy)

        # Pack the buttons.
        continue_to_search_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)


        # Pack the frames and instruction widget.
        criteria_instruction_label.pack()
        search_criteria_frame.pack()
        button_frame.pack()




    def add_entry_window(self):
        # Define the function that uses that input to add data to the database.
        def add_entry():
            
            #Find the current maximum ID to make the new ID
            cursor.execute('''SELECT * FROM Students WHERE Student_ID = (SELECT MAX(Student_ID) FROM Students)''')

            # Fetch the entry.
            row = cursor.fetchone()
            max_id = row[0]

            # Get the student info input.
            name = name_entry.get()
            id = int(max_id) + 1
            graduation_year = graduation_year_entry.get()
            major = major_entry.get()
            hometown = hometown_entry.get()
            email = email_entry.get()
            student_type = student_type_entry.get()
            campus_status = campus_status_entry.get()

            

            # Make sure the user entered data in both fields before proceeding, if so:
            if name != '':
                # Insert the data into the database and commit the changes.
                cursor.execute('''INSERT INTO Students (Student_ID, Name, Graduation_Year, Primary_Major, Hometown, Email, Student_Type, Campus_Status) VALUES (?,?,?,?,?,?,?,?)''', 
                               (id, name, graduation_year, major, hometown, email, student_type, campus_status,))
                conn.commit()

                # Select the entry from the database to keep the formatting the same as the other items in the listbox.
                cursor.execute('''SELECT * FROM Students WHERE Student_ID = (SELECT MAX(Student_ID) FROM Students)''')

                # Fetch the entry.
                row = cursor.fetchone()

                # Insert the entry into the phonebook list and listbox.

                self.students_listbox.insert(tkinter.END, f'{row[0]:<6}{row[1]:<35}{row[2]:<8}{row[3]:<40}'
                                                      f'{row[4]:<20}{row[5]:<35}{row[6]:<20}{row[7]:<20}')
                self.students.append(row)

                # Provide a confirmation that the data was successfully entered.
                tkinter.messagebox.showinfo('Entry Added', 'Entry successfully added')

                # Close the add window.
                add_window.destroy()

            # If the user left one or both fields blank, show and error messagebox and ask them to re-enter.
            else:
                tkinter.messagebox.showerror('Error', 'Please enter a name and ID.')

        # Create the window that will ask for input.
        add_window = tkinter.Toplevel(self.main_window)

        # Provide an instruction label telling the user what to do.
        instructions = tkinter.Label(add_window, text='Add an entry by typing in student information in'
                                                      '\nthe corresponding boxes below.')
                                                      

        # Create the name input section:
        # Create the name entry frame.
        name_frame = tkinter.Frame(add_window)

        # Create the name entry label.
        name_label = tkinter.Label(name_frame, text='Name')

        # Create the input box.
        name_entry = tkinter.Entry(name_frame)

        # Pack the label and entry widgets.
        name_label.pack(side='left')
        name_entry.pack(side='left')

        # Create the name input section:
        # Create the name entry frame.
        # Create the phone number input section:
        # Create the frame.
        graduation_year_frame = tkinter.Frame(add_window)

        # Create the label for the entry box.
        graduation_year_label = tkinter.Label(graduation_year_frame, text='Graduation year')

        # Create the entry box.
        graduation_year_entry = tkinter.Entry(graduation_year_frame)

        # Pack the label and entry widgets.
        graduation_year_label.pack(side='left')
        graduation_year_entry.pack(side='left')

        major_frame = tkinter.Frame(add_window)

        # Create the label for the entry box.
        major_label = tkinter.Label(major_frame, text='Major')

        # Create the entry box.
        major_entry = tkinter.Entry(major_frame)

        # Pack the label and entry widgets.
        major_label.pack(side='left')
        major_entry.pack(side='left')

        hometown_frame = tkinter.Frame(add_window)

        # Create the label for the entry box.
        hometown_label = tkinter.Label(hometown_frame, text='Hometown')

        # Create the entry box.
        hometown_entry = tkinter.Entry(hometown_frame)

        # Pack the label and entry widgets.
        hometown_label.pack(side='left')
        hometown_entry.pack(side='left')

        email_frame = tkinter.Frame(add_window)

        # Create the label for the entry box.
        email_label = tkinter.Label(email_frame, text='Email')

        # Create the entry box.
        email_entry = tkinter.Entry(email_frame)

        # Pack the label and entry widgets.
        email_label.pack(side='left')
        email_entry.pack(side='left')

        student_type_frame = tkinter.Frame(add_window)

        # Create the label for the entry box.
        student_type_label = tkinter.Label(student_type_frame, text='Student Type')

        # Create the entry box.
        student_type_entry = tkinter.Entry(student_type_frame)

        # Pack the label and entry widgets.
        student_type_label.pack(side='left')
        student_type_entry.pack(side='left')

        campus_status_frame = tkinter.Frame(add_window)

        # Create the label for the entry box.
        campus_status_label = tkinter.Label(campus_status_frame, text='Campus Status')

        # Create the entry box.
        campus_status_entry = tkinter.Entry(campus_status_frame)

        # Pack the label and entry widgets.
        campus_status_label.pack(side='left')
        campus_status_entry.pack(side='left')



        # Create the button section:
        # Create a frame.
        button_frame = tkinter.Frame(add_window)

        # Create the add button, which redirects the program to the add_entry function,
        # which will add the entry to the database.
        add_button = tkinter.Button(button_frame, text='Add', command=add_entry)

        # Create the cancel button, which destroys the add window.
        cancel_button = tkinter.Button(button_frame, text='Cancel', command=add_window.destroy)

        # Pack the buttons.
        add_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)

        # Pack all the widgets.
        instructions.pack()
        name_frame.pack(padx=(0,20), pady=(5, 0))
        graduation_year_frame.pack(padx=(0,73), pady=(5, 0))
        major_frame.pack(padx=(0,20), pady=(5, 0))
        hometown_frame.pack(padx=(0,48),pady=(5, 0))
        email_frame.pack(padx=(0,16), pady=(5, 0))
        student_type_frame.pack(padx=(0,57), pady=(5, 0))
        campus_status_frame.pack(padx=(0,66), pady=(5, 0))
        
        button_frame.pack(pady=5)
        
    def modify_entry_window(self):
        # Define the function that performs the modification.
        def modify_entry():
            # Get the primary key (aka the index for the database) for the entry in the database
            # (index is defined in the modify_entry_window function).
            db_index = int((self.students_listbox.get(index)).split(' ')[0])

            # Get the name and phone number input.
            name = name_entry.get()
            graduation_year = graduation_year_entry.get()
            major = major_entry.get()
            hometown = hometown_entry.get()
            email = email_entry.get()
            student_type = student_type_entry.get()
            campus_status = campus_status_entry.get()
            

            # Update the name in the database entry if the user enters a name.
            entered = False

            if name != '':
                cursor.execute('''UPDATE Students SET Name=? WHERE Student_ID=?''', (name, db_index))
                entered = True

            # Update the phone number in the database entry if the user enters one.
            if graduation_year != '':
                cursor.execute('''UPDATE Students SET Graduation_Year=? WHERE Student_ID=?''', (graduation_year, db_index))
                entered = True

            if major != '':
                cursor.execute('''UPDATE Students SET Primary_Major=? WHERE Student_ID=?''', (major, db_index))
                entered = True

            if hometown != '':
                cursor.execute('''UPDATE Students SET Hometown=? WHERE Student_ID=?''', (hometown, db_index))
                entered = True

            if email != '':
                cursor.execute('''UPDATE Students SET Email=? WHERE Student_ID=?''', (email, db_index))
                entered = True

            if student_type != '':
                cursor.execute('''UPDATE Students SET Student_Type=? WHERE Student_ID=?''', (student_type, db_index))
                entered = True

            if campus_status != '':
                cursor.execute('''UPDATE Students SET Campus_Status=? WHERE Student_ID=?''', (campus_status, db_index))
                entered = True

            # If the user leaves all fields blank:
            if entered == False:
                # Show an error message asking them to fill in at least one of the fields.
                tkinter.messagebox.showerror('Error', 'Please enter information to change.')

                # Exit the modify_entry function to allow the user to try again.
                return

            # Commit the database changes.
            conn.commit()

            # Select the entry from the database to keep the formatting the same as the other items in the listbox.
            cursor.execute('''SELECT * FROM Students WHERE Student_ID = ?''', (db_index,))

            # Fetch the row.
            row = cursor.fetchone()

            # Delete the corresponding listbox and phonebook list item.
            self.students_listbox.delete(index)
            del self.students[index]

            # Replace the deleted listbox and phonebook list item with a new one containing the updated data.
            self.students_listbox.insert(index, f'{row[0]:<6}{row[1]:<35}{row[2]:<8}{row[3]:<40}'
                                                      f'{row[4]:<20}{row[5]:<35}{row[6]:<20}{row[7]:<20}')
            
            print(int(index))
            self.students.insert(index, row)

            # Provide a confirmation that the data was successfully entered.
            tkinter.messagebox.showinfo('Entry Modified', 'Entry successfully modified')

            # Close the modify window.
            modify_window.destroy()

        # Make sure the user chose an entry to modify, otherwise an error will occur:
        # Get the user's selection.
        selection = self.students_listbox.curselection()

        # Ensure the selection is not an empty tuple. If not:
        if selection != ():
            # Get the index of the selection - this will turn the curselection from a tuple to an integer.
            index = selection[0]

        # If the user did not make a selection:
        else:
            # Create an error messagebox asking the user to select an entry.
            tkinter.messagebox.showerror('Error', 'Please select an entry to modify.')

            # Exit the function so the user can make a selection.
            return

        # Create a window that will allow the user to enter a new name and/or phone number.
        modify_window = tkinter.Toplevel(self.main_window)

        # Add instructions to tell the user what to do.
        instructions = tkinter.Label(modify_window, text="Modify the student's info by typing"
                                                         '\nin the corresponding boxes below.')
                                                         

        # Show the current name and phone number to the user so they know what they're changing.
        current_info = tkinter.Label(modify_window, text=f'ID: {(self.students[index])[0]}\n'
                                                         f'Name: {(self.students[index])[1]}\n'
                                                         f'Class of: {(self.students[index])[2]}')

        # Create the name input section:
        # Create the frame.
        name_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        name_label = tkinter.Label(name_frame, text='New name')

        # Create the entry box.
        name_entry = tkinter.Entry(name_frame)

        # Pack the label and entry widgets.
        name_label.pack(side='left')
        name_entry.pack(side='left')

        # Create the graduation year input section:
        # Create the frame.
        graduation_year_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        graduation_year_label = tkinter.Label(graduation_year_frame, text='Graduation year')

        # Create the entry box.
        graduation_year_entry = tkinter.Entry(graduation_year_frame)

        # Pack the label and entry widgets.
        graduation_year_label.pack(side='left')
        graduation_year_entry.pack(side='left')

        major_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        major_label = tkinter.Label(major_frame, text='Major')

        # Create the entry box.
        major_entry = tkinter.Entry(major_frame)

        # Pack the label and entry widgets.
        major_label.pack(side='left')
        major_entry.pack(side='left')

        hometown_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        hometown_label = tkinter.Label(hometown_frame, text='Hometown')

        # Create the entry box.
        hometown_entry = tkinter.Entry(hometown_frame)

        # Pack the label and entry widgets.
        hometown_label.pack(side='left')
        hometown_entry.pack(side='left')

        email_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        email_label = tkinter.Label(email_frame, text='Email')

        # Create the entry box.
        email_entry = tkinter.Entry(email_frame)

        # Pack the label and entry widgets.
        email_label.pack(side='left')
        email_entry.pack(side='left')

        student_type_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        student_type_label = tkinter.Label(student_type_frame, text='Student Type')

        # Create the entry box.
        student_type_entry = tkinter.Entry(student_type_frame)

        # Pack the label and entry widgets.
        student_type_label.pack(side='left')
        student_type_entry.pack(side='left')

        campus_status_frame = tkinter.Frame(modify_window)

        # Create the label for the entry box.
        campus_status_label = tkinter.Label(campus_status_frame, text='Campus Status')

        # Create the entry box.
        campus_status_entry = tkinter.Entry(campus_status_frame)

        # Pack the label and entry widgets.
        campus_status_label.pack(side='left')
        campus_status_entry.pack(side='left')

        # Create the buttons:
        # Create a frame for the buttons.
        button_frame = tkinter.Frame(modify_window)

        # Create a modify button that redirects the program to the function that will modify the entry.
        modify_button = tkinter.Button(button_frame, text='Modify', command=modify_entry)

        # Create a cancel button that will close the modify window.
        cancel_button = tkinter.Button(button_frame, text='Cancel', command=modify_window.destroy)

        # Pack the buttons.
        modify_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)

        # Pack all the widgets.
        instructions.pack(padx=10, pady=5)
        current_info.pack(pady=5)
        # id_frame.pack(pady=(5, 0))
        name_frame.pack(padx=(0, 45), pady=(5, 0))
        graduation_year_frame.pack(padx=(0,73), pady=(5, 0))
        major_frame.pack(padx=(0,20), pady=(5, 0))
        hometown_frame.pack(padx=(0,48),pady=(5, 0))
        email_frame.pack(padx=(0,16), pady=(5, 0))
        student_type_frame.pack(padx=(0,57), pady=(5, 0))
        campus_status_frame.pack(padx=(0,66), pady=(5, 0))
        button_frame.pack(pady=5)

        
    # Define the function that allows the user to delete data in the database:
    # Define the confirmation window in case the user misclicks.
    def deletion_confirmation(self):
        # Define the function that removes the entry from the database and listbox.
        def delete_entry():
            # Get the primary key (aka the index for the database) for the entry in the database
            # (index is defined in the deletion_confirmation function).
            db_index = int((self.students_listbox.get(index)).split(' ')[0])

            # Delete the entry from the database and commit the change.
            cursor.execute('''DELETE FROM Students WHERE Student_ID=?''', (db_index,))
            conn.commit()

            # Delete the entry from the phonebook list and listbox.
            self.students_listbox.delete(index)
            del self.students[index]

            # Provide a confirmation that the data was successfully deleted.
            tkinter.messagebox.showinfo('Entry Deleted', 'Entry successfully deleted')

            # Close the deletion confirmation window.
            confirmation_window.destroy()


        # Make sure the user chose an entry to delete, otherwise an error will occur:
        # Get the user's selection.
        selection = self.students_listbox.curselection()

        # Ensure the selection is not an empty tuple. If not:
        if selection != ():
            # Get the index of the selection - this will turn the curselection from a tuple to an integer.
            index = selection[0]

        # If the user did not make a selection:
        else:
            # Create an error messagebox asking the user to select an entry.
            tkinter.messagebox.showerror('Error', 'Please select an entry to delete.')

            # Exit the function so the user can make a selection.
            return

        # Create a window for the user to confirm their deletion in.
        confirmation_window = tkinter.Toplevel(self.main_window)

        # Add the label asking the user if they're sure they'd like to delete the entry.
        confirmation = tkinter.Label(confirmation_window, text='Are you sure you want to delete'
                                                     f'\n{self.students[index]}')

        # Create the buttons for the user to select:
        # Create the button frame.
        button_frame = tkinter.Frame(confirmation_window)

        # Create a yes button, which will redirect the program to the delete_entry function.
        yes_button = tkinter.Button(button_frame, text='Yes', command=delete_entry)

        # Create a cancel button, which will close the confirmation window.
        cancel_button = tkinter.Button(button_frame, text='Cancel', command=confirmation_window.destroy)

        # Pack the buttons.
        yes_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)

        # Pack all the widgets.
        confirmation.pack(padx=5, pady=5)
        button_frame.pack(pady=5)

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ Needs Modifying Below -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    # Define the function that will end the program when the user clicks quit:
    # Define the confirmation in case the user misclicks.
    def end_program_confirmation(self):
        # Define the function that will end the program.
        def end_program():
            # Close the database.
            conn.close()

            # Close the confirmation window.
            confirmation_window.destroy()

            # Close the main window.
            self.main_window.destroy()

        # Create the confirmation window.
        confirmation_window = tkinter.Toplevel(self.main_window)

        # Add a label asking the user if they're sure they want to quit.
        confirmation = tkinter.Label(confirmation_window, text='Are you sure you want to quit?')


        # Create the buttons:
        # Create a button frame.
        button_frame = tkinter.Frame(confirmation_window)

        # Create a yes button that will redirect the program to the end_program function.
        yes_button = tkinter.Button(button_frame, text='Yes', command=end_program)

        # Create a cancel button that will close the confirmation window.
        cancel_button = tkinter.Button(button_frame, text='Cancel',
                                       command=confirmation_window.destroy)

        # Pack the buttons.
        yes_button.pack(side='left', padx=5)
        cancel_button.pack(side='left', padx=5)


        # Pack all the widgets:
        confirmation.pack(padx=5, pady=5)
        button_frame.pack(pady=5)


# Call the main function.
if __name__== '__main__':
    # Create an instance of the StudentDatabaseGUI class.
    student_database_gui = StudentDatabaseGUI()





