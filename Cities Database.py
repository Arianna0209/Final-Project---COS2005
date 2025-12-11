#This program was written by Logan Gibson on 12/6/25
#Its name is "Cities Database Viewer"

import sqlite3

def main():
    # Connect to the database.
    conn = sqlite3.connect('cities.db')

    # Get a database cursor.
    cur = conn.cursor()
    
    # Add the Cities table.
    add_cities_table(cur)
    
    # Add rows to the Cities table.
    add_cities(cur)

    # Commit the changes.
    conn.commit()

    # Close the connection.
    conn.close()

# The add_cities_table adds the Cities table to the database.
def add_cities_table(cur):
    # If the table already exists, drop it.
    cur.execute('DROP TABLE IF EXISTS Cities')

    # Create the table.
    cur.execute('''CREATE TABLE Cities (CityID INTEGER PRIMARY KEY NOT NULL,
                                        CityName TEXT,
                                        Population REAL)''')

# The add_cities function adds 20 rows to the Cities table.
def add_cities(cur):
    cities_pop = [(1,'Tokyo',38001000),
                  (2,'Delhi',25703168),
                  (3,'Shanghai',23740778),
                  (4,'Sao Paulo',21066245),
                  (5,'Mumbai',21042538),
                  (6,'Mexico City',20998543),
                  (7,'Beijing',20383994),
                  (8,'Osaka',20237645),
                  (9,'Cairo',18771769),
                  (10,'New York',18593220),
                  (11,'Dhaka',17598228),
                  (12,'Karachi',16617644),
                  (13,'Buenos Aires',15180176),
                  (14,'Kolkata',14864919),
                  (15,'Istanbul',14163989),
                  (16,'Chongqing',13331579),
                  (17,'Lagos',13122829),
                  (18,'Manila',12946263),
                  (19,'Rio de Janeiro',12902306),
                  (20,'Guangzhou',12458130)]
    
    for row in cities_pop:
        cur.execute('''INSERT INTO Cities (CityID, CityName, Population)
                       VALUES (?, ?, ?)''', (row[0], row[1], row[2]))


def make_cities_list():
    conn = sqlite3.connect('cities.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Cities')
    database_list = cur.fetchall()
    cities_list = []
    for city in database_list:
         cities_list.append(city[1])
    return cities_list

CITIES_LIST = make_cities_list()

def sort_alpha(CITIES_LIST):
    CITIES_LIST.sort()
    alpha_list = str(CITIES_LIST)
    alpha_list = alpha_list.lstrip("[")
    alpha_list = alpha_list.rstrip("]")
    return alpha_list

ALPHA_LIST = sort_alpha(CITIES_LIST)

def make_pop_list():
    conn = sqlite3.connect('cities.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Cities')
    database_list = cur.fetchall()
    pop_list = []
    for city in database_list:
         pop_list.append([city[2],city[1]])
    return pop_list

POP_LIST = make_pop_list()

def sort_pop_a(POP_LIST):
    POP_LIST.sort()
    pop_a_list = []
    for city in POP_LIST:
        pop_a_list.append(city[1])
    pop_a_list = str(pop_a_list)
    pop_a_list = pop_a_list.rstrip("]")
    pop_a_list = pop_a_list.lstrip("[")
    return pop_a_list
    
POP_A_LIST = sort_pop_a(POP_LIST)

def sort_pop_d(POP_LIST):
    POP_LIST.sort()
    POP_LIST.reverse()
    pop_d_list = []
    for city in POP_LIST:
        pop_d_list.append(city[1])
    pop_d_list = str(pop_d_list)
    pop_d_list = pop_d_list.lstrip("[")
    pop_d_list = pop_d_list.rstrip("]")
    return pop_d_list

POP_D_LIST = sort_pop_d(POP_LIST)

def calculate_average():
    conn = sqlite3.connect('cities.db')
    cur = conn.cursor() 
    total = 0
    average = 0
    num_rows = 0
    for row in cur.execute('SELECT * FROM Cities'):
        pop = int(row[2])
        total += pop
        num_rows += 1
    average = int(total / num_rows)
    conn.close()
    return average

    
def calculate_total():
    conn = sqlite3.connect('cities.db')
    cur = conn.cursor() 
    total = 0
    for row in cur.execute('SELECT * FROM Cities'):
        pop = int(row[2])
        total += pop
    conn.close()
    return total
    

def calculate_highest():
    conn = sqlite3.connect('cities.db')
    cur = conn.cursor()
    
    num_row = 0
    high = 0
    for row in cur.execute('SELECT * FROM Cities'):
        current_pop = int(row[2])
        if num_row > 0:
            if high > current_pop:
                high = high
            elif high < current_pop:
                high = current_pop
        else:
            high = current_pop

        num_row += 1
    for row in cur.execute('SELECT * FROM Cities'):
        if row[2] == high:
            high_city = row[1]
        else:
            pass
    city_phrase = (f'Highest Population: {high_city} with {high:,} people.')
    conn.close
    return city_phrase



def calculate_lowest():
    conn = sqlite3.connect('cities.db')
    cur = conn.cursor()
    num_row = 0
    low = 0
    for row in cur.execute('SELECT * FROM Cities'):
        current_pop = int(row[2])
        if num_row > 0:
            if low < current_pop:
                low = low
            elif low > current_pop:
                low = current_pop
        else:
            low = current_pop

        num_row += 1

    for row in cur.execute('SELECT * FROM Cities'):
        if row[2] == low:
            low_city = row[1]
        else:
            pass
    city_phrase = (f'Lowest Population: {low_city} with {low:,} people.')
    conn.close
    return city_phrase 

# Execute the main function.
if __name__ == '__main__':
    main()

#Begin the GUI!

import tkinter

class Cities_GUI:
    def __init__(self):
    
        self.main_window = tkinter.Tk()
        self.main_window.title('Cities Database Interface')

        self.top_frame = tkinter.Frame(self.main_window)
        self.database_frame = tkinter.Frame(self.main_window)
        self.stats_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)

        self.info_label = tkinter.Label(self.top_frame, 
        text = 'Welcome to the cities database interface!' \
        ' Click buttons to show the data you want to see.\n' \
        'Use the Clear button to reset your selections.')

        self.name_button = tkinter.Button(self.top_frame,
         text='Sort Alphabetically', command=self.alphabetically)

        self.pop_a_button = tkinter.Button(self.top_frame,
         text='Sort by Population (Ascending Left to Right)', command=self.pop_a)
        
        self.pop_d_button = tkinter.Button(self.top_frame,
         text='Sort by Population (Descending Left to Right)', command=self.pop_d)
        
        #now for the output field labels

        #string variables

        self.database_var = tkinter.StringVar()

        self.stats_var = tkinter.StringVar()


        #the chart label
        self.database_label = tkinter.Label(self.database_frame,
                            textvariable = self.database_var)
        
        self.stats_label = tkinter.Label(self.stats_frame, 
                            textvariable = self.stats_var)
        
        
        #creating integer variable for the radio buttons to come
        self.radio_var = tkinter.IntVar()
        self.radio_var.set(0)

        #make the radio buttons
        self.average_button = tkinter.Radiobutton(self.bottom_frame,
        text = 'Average City Population', variable = self.radio_var, value = 1,
        command = self.average)

        self.total_button = tkinter.Radiobutton(self.bottom_frame,
        text = 'Total City Population', variable = self.radio_var, value = 2,
        command = self.total)

        self.highest_button = tkinter.Radiobutton(self.bottom_frame,
        text = 'City With Highest Population', variable = self.radio_var, value = 3,
        command = self.highest)

        self.lowest_button = tkinter.Radiobutton(self.bottom_frame,
        text = 'City With Lowest Population', variable = self.radio_var, value = 4,
        command = self.lowest)

        #write the clear button

        self.clear_button = tkinter.Button(self.bottom_frame,
        text = 'Clear', command = self.clear)

        self.top_frame.pack(pady = 10)
        self.database_frame.pack(pady = 10)
        self.stats_frame.pack(pady = 10)
        self.bottom_frame.pack(pady= 10)

        self.info_label.pack()
        self.stats_label.pack()
        self.database_label.pack()

        self.name_button.pack()
        self.pop_a_button.pack()
        self.pop_d_button.pack()
        
        self.average_button.pack()
        self.total_button.pack()
        self.highest_button.pack()
        self.lowest_button.pack()
        self.clear_button.pack()

        
        tkinter.mainloop()
        
#These are the call-to functions for the various buttons

    def alphabetically(self):
        self.database_var.set(str(ALPHA_LIST))

    def pop_a(self):
        self.database_var.set(str(POP_A_LIST))

    def pop_d(self):
        self.database_var.set(str(POP_D_LIST))
    
    def lowest(self):
        self.stats_var.set(calculate_lowest())
    
    def highest(self):
        self.stats_var.set(calculate_highest())

    def total(self):
        self.stats_var.set(f'Total Population: {calculate_total():,} people.')
        
    def average(self):
        self.stats_var.set(f'Average Population: {calculate_average():,} people.')
    
    def clear(self):
        self.database_var.set('')
        self.stats_var.set('')
        self.radio_var.set(0)
        

my_database = Cities_GUI()
        
