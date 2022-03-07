# Tasks app - Oct 23/2021 - IG: @osm3rr

#****** part 1:  *******
# Libraries necesary
from os import remove
from tkinter import *
import sqlite3

# principal window
root = Tk()

# title window
root.title('Gestor de tareas Adakademy')

# Size window
root.geometry('500x500')


## ****** Data base ******
# We open the connection with database
con = sqlite3.connect( 'hw.db' )

# We create the cursor for exucute SQL commands
cur = con.cursor()

# We create data base
cur.execute( ''' 
         CREATE TABLE if not exists hw(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
             description TEXT NOT NULL,
             completed BOOLEAN NOT NULL
         );  
            ''' )
# Save the change
con.commit()



# Label for "task"
lbl_hw = Label( root, text='Task: ', padx=5, pady=20 )
lbl_hw.grid( row=0, column=0, padx= 20 )

# Data Entry
entry_hw = Entry( root,width=40, bd=5 )
entry_hw.grid( row=0, column=1, pady=20 )
#entry_hw.insert(0, 'Entry homework')

# Focus on data entry
entry_hw.focus()

# We create a remove function
def remove_task(id_task):
    def _remove_task():
        cur.execute( ''' DELETE FROM hw WHERE id = ? ''', ( id_task,  ) )
        con.commit()
        render_hw()
    return _remove_task
        

# This secuence is known as currying
# Completed id function
def completed( id_task ):
    # we wrap the complete function
    def _completed():
        # Logic
        # we get the task id
        task = cur.execute( '''SELECT * from hw WHERE id = ?''', ( id_task,  ) ).fetchone()
        
        cur.execute( ''' 
                    UPDATE hw
                    SET completed = ?
                    WHERE id = ?
                    ''',
                    ( not task[ 3 ], id_task )
                    )
        con.commit()
        # we show the homeworks
        render_hw()
        #print( id_task )
    return _completed

# Function to render the homeworks
def render_hw():
    # Query the database
    row_hw = cur.execute( ''' SELECT * FROM hw ''' ).fetchall()
    
    # loop for erase the task
    for widget in lbl_frame_hw.winfo_children():
        widget.destroy()
    
    
    # View the answer in row_hw
    #print( row_hw )
    
    # Access to task completed and description
    for item in range( 0, len( row_hw ) ):
        completed_task = row_hw[item][ 3 ] # It read like at boolean
        description_task = row_hw[item][ 2 ]
        
        # Color variable to view 
        # 
        color_hw = '#555555' if completed_task else '#0000ff' 
        
        
        # Get the id for identify completed task
        id_task = row_hw[item][ 0 ]
        
        # the anchor parameter is to move to the left
        check_btn = Checkbutton( lbl_frame_hw, text=description_task, width=42, anchor='w',
                                 command= completed( id_task ), fg=color_hw )
        check_btn.grid( row=item, column=0, sticky='W' )
        
        # Button for delete the tasks
        btn_del = Button( lbl_frame_hw, text='Delete', command= remove_task( id_task ) )
        btn_del.grid( row=item, column= 1 )
        
        # for show the checkbutton
        check_btn.select() if completed_task else check_btn.deselect()


# Homework function
def add_hw():
    # Get the tasks
    tasks = entry_hw.get()
    
    ## check if the task exists
    if tasks:
        # Save the tasks in db
        # We define "tasks" in False by default
        cur.execute( 
                    ''' 
                    INSERT INTO hw ( description, completed ) VALUES( ?, ? )
                    ''', ( tasks, False )
                    )
        con.commit()

        entry_hw.delete(0, END)

        # Add the render_hw function
        render_hw()
    else:
        pass

# Add button
btn_add = Button( root, text='ADD', command= add_hw )
btn_add.grid( row=0, column= 2, padx=20 )

# Frame for tasks
lbl_frame_hw = LabelFrame( root, text='Things to do' )
lbl_frame_hw.grid( row=1, columnspan=3, column=0,
                  padx=5, sticky='NSWE' )
# sticky='NWES'

### Mark Label 
#lbl_mark = Label( lbl_frame_hw, text='Homeworks here' )
#lbl_mark.grid( row=1, column=1 )
# , padx=150, pady=10


# Entry homework with enter
# listen to the return event for call
# the function add_hw
root.bind( '<Return>', lambda x: add_hw() )

# Show the render function
render_hw()

# Infinite loop
root.mainloop()