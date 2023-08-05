#!/usr/bin/env python

# UI imports
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
# ML + DB imports
from mlads_lukem_fyp.databaser import Databaser
from mlads_lukem_fyp.detector import Detector
from mlads_lukem_fyp import detector
# Other imports
import re
import os
from os.path import split, dirname, abspath, join
import numpy as np


HOME = split(dirname(__file__))[0]
CSVDIR = abspath(join(HOME, 'csvs'))
SAVEDIR = abspath(join(HOME, 'model'))
DBDIR = abspath(join(HOME, 'sqlite'))
CONFIG_FILE = abspath(join(HOME, 'mlads.cfg'))
README_FILE = abspath(join(HOME, 'README.txt'))


def coming_soon():
    """For use while a component is not in use.

    Print 'Coming Soon' to the console."""
    popup = tk.Tk()
    popup.wm_title("Coming Soon")
    label = ttk.Label(popup, text='Coming Soon!')
    label.pack()
    button = ttk.Button(popup, text="Okay", command=popup.destroy)
    button.pack()
    popup.mainloop()


class GUI:
    """A class used as the main interface between the user and the anomaly detection system

    Attributes
    ----------
    window : tkinter.Tk
        A Tkinter object to contain all widgets that are shown to the user
    db_file : str
        The file in which the database is stored
    db : databaser.Databaser
        A databaser object to interact with the backend database
    det : detector.Detector
        A detector object to interact with the machine learning aspects of the project

    Methods
    -------
     view_alerts_window()
        Select all alerts from the database and show them to the user
     view_alert_details(table, focus)
        Detailed view of an individual alert provided to the user
     analyse_window()
        Allows the user to upload new PCAPs or use existing files to access the machine learning detector
     populate_table_csv(table, filename)
        Populate a Treeview table with the information in a csv file with provided filename
     analyse_file(filename)
        Analyse a file using the machine learning anomaly detection algorithm
     upload_file_window()
        A window to select a file to upload to the MLADS project
     upload_file(inpcap, window)
        Open a pcap file and convert it to a csv stored in the MLADS project 'csv' folder
     contacts_window()
        Select all contacts from the database and show them to the user
     add_edit_contact(table, focus, cond)
        Allow the user to add or edit a contact in a new window
     remove_contact(table, focus)
        Remove a contact from the backend database
     populate_table_db(table, search_table, search_term, search_col)
        Populate a Treeview table with the information in a given table in the database
     create_menubar()
        Create the menu bar shown in every window
     main_menu()
        Setup the main menu that is shown when the program is launched
     reset()
        Reset the window by removing all previous widgets and creating a new menu bar
     quit()
        Quit the program
     valid_email(email, widget_name)
        Check an email address is in a valid format
     valid_phone(phone, widget_name)
        Check a phone number is in a valid format
     invalid(widget_name)
        Define actions to be taken if a field is invalid
    read_config()
        Read the configuration file.
    """

    def __init__(self):
        """Define initial values for various class attributes.

        Define the window, which widgets to display first and the database and detector attributes."""
        # Define the window
        self.window = tk.Tk()
        self.main_menu()

        # Read config
        self.db_file = None
        self.read_config()

        # Open database
        if self.db_file is None:
            self.db = Databaser()
        else:
            self.db = Databaser(self.db_file)

        # And the detector
        train_df = 'Xample_Training_Data.csv'
        train_df = abspath(join(CSVDIR, train_df))
        self.det = Detector(train_data_file=train_df)

        # Run the loop, showing the window
        tk.mainloop()

    def view_alerts_window(self):
        """Select all alerts from the database and show them to the user.

        A tkinter TreeView is used to hold the data in a table. Basic search functionality is provided.
        """
        # Reset the window to remove old widgets
        self.reset()
        self.window.title("MLADS - View Alerts")

        # Define attributes needed for the optionbox and treeview
        cols = ('ID', 'Summary', 'Source IP', 'Dest. IP', 'Protocol',
                'Source Port', 'Dest. Port', 'Timestamp')
        by_var = tk.StringVar(self.window)
        by_var.set('Summary')

        # Create the widgets that make the window
        search_lbl = tk.Label(self.window, text="Search:")
        search_lbl.grid(row=0, column=0, sticky=tk.E)
        input_textbox = tk.Entry(self.window, width=35)
        input_textbox.grid(row=0, column=1, columnspan=2, sticky=tk.W)
        by_lbl = tk.Label(self.window, text="By:")
        by_lbl.grid(row=0, column=3, sticky=tk.E)
        by_opbox = tk.OptionMenu(self.window, by_var, *cols)
        by_opbox.config(width=25)
        by_opbox.grid(row=0, column=4, sticky=tk.W)
        search_btn = tk.Button(self.window, text="Search", command=lambda: self.populate_table_db(alert_table,
                                                                                                  'alerts',
                                                                                                  input_textbox.get(),
                                                                                                  by_var.get()))
        search_btn.grid(row=0, column=5, sticky=tk.W)

        alert_table = ttk.Treeview(self.window, columns=cols, show='headings')
        # Set column headings and widths
        for col in cols:
            alert_table.heading(col, text=col)
            if col == "ID":
                alert_table.column(col, width=50)
            elif col == "Summary":
                alert_table.column(col, width=275)
            elif col == "Protocol":
                alert_table.column(col, width=75)
            else:
                alert_table.column(col, width=100)
        alert_table.grid(row=1, column=0, columnspan=6, sticky=tk.W)
        # Populate the table after the widget has been created
        alert_table = self.populate_table_db(alert_table, 'alerts', None, None)

        viewdetails_btn = tk.Button(self.window, text="Details",
                                    command=lambda: self.view_alert_details(alert_table, alert_table.focus()))
        viewdetails_btn.grid(row=2, column=5, sticky=tk.E)

    def view_alert_details(self, table, focus):
        """Detailed view of an individual alert provided to the user.

        Each property of the alert is shown to the user in a separate field.

        Parameters
        ----------
        table : tkinter.ttk.Treeview
            The table the initial data is kept in
        focus : str
            The ID of the object in focus in table
        """
        # Define initial values needed through the method, and get data from the database
        values = table.item(focus)['values']
        details_window = tk.Toplevel(self.window)
        colnames, data = self.db.select_all_alerts(values[0])
        boxes = []
        labels = []
        newrow = 1
        newcol = 0

        if data is not None:
            # For each column in the data, create a label and a textbox to put the values into
            for i in range(0, len(data)):
                # To place each item correctly in the window, i.e. 3 columns and x many rows
                if newcol >= 6:
                    newrow += 1
                    newcol = 0

                if colnames[i] == "id" and i > 1:
                    continue

                new_label = tk.Label(details_window, text=colnames[i])
                if colnames[i] == "summary":
                    new_label.grid(row=0, column=0, sticky=tk.W)
                else:
                    new_label.grid(row=newrow, column=newcol, sticky=tk.E)
                    newcol += 1

                new_entry = tk.Entry(details_window, width=30)
                # We want the summary of the alert to be on its own row
                if colnames[i] == "summary":
                    new_entry.grid(row=0, column=1, sticky=tk.W, columnspan=5)
                    new_entry.config(width=116)
                else:
                    new_entry.grid(row=newrow, column=newcol, sticky=tk.W)
                    newcol += 1
                new_entry.insert(tk.END, data[i])
                new_entry.config(state='disabled')

                boxes.append(new_entry)
                labels.append(new_label)

    def analyse_window(self):
        """Allows the user to upload new PCAPs or use existing files to access the machine learning detector.

        A tkinter TreeView is used to hold the file data. Options to use an existing file or upload a new file
        are provided.
        """
        # Reset the window to remove old widgets
        self.reset()
        self.window.title("MLADS - Analyse PCAP")

        cols = ('Flow ID', 'Fwd_pkt_len_std', 'Bwd_pkt_len_std', 'Fwd_pkt_len_max', 'Fwd_pkt_len_min',
                'Bwd_pkt_len_max', 'Bwd_pkt_len_min', 'Fwd_pkt_len_mean', 'Bwd_pkt_len_mean', 'Timestamp', 'Srcip',
                'Dstip', 'Proto', 'Sport', 'Dport')

        # Create the widgets that make the window
        load_existing_lbl = tk.Label(self.window, text='Load Existing File:')
        load_existing_lbl.grid(row=0, column=0, sticky=tk.E)

        # Create the variables needed for the optionbox
        existing_files = os.listdir(CSVDIR)
        file_var = tk.StringVar(self.window)
        file_var.set(existing_files[0])

        load_existing_opbox = tk.OptionMenu(self.window, file_var, *existing_files)
        load_existing_opbox.grid(row=0, column=1)
        analyse_btn = tk.Button(self.window, text="Analyse", command=lambda: self.analyse_file(file_var.get()))
        analyse_btn.grid(row=0, column=2)
        upload_file_btn = tk.Button(self.window, text="Upload New File", command=self.upload_file_window)
        upload_file_btn.grid(row=0, column=4)

        csv_table = ttk.Treeview(self.window, columns=cols, show='headings')
        # Set the column headings appropriately
        for col in cols:
            csv_table.heading(col, text=col)
            if col == "Flow ID":
                csv_table.column(col, width=250)
            elif col in ['Proto', 'Sport', 'Dport']:
                csv_table.column(col, width=75)
            else:
                csv_table.column(col, width=110)

        csv_vsb = tk.ttk.Scrollbar(self.window, orient='vertical', command=csv_table.yview)
        csv_vsb.grid(row=1, column=7, sticky=tk.W)
        csv_table.configure(xscrollcommand=csv_vsb.set)
        # set column headings and widths
        csv_table.grid(row=1, column=0, columnspan=6, sticky=tk.W)
        # Populate the treeview after it's created
        self.populate_table_csv(csv_table, file_var.get())

        # Send us to the alerts page when we want more info on malicious streams
        alerts_btn = tk.Button(self.window, text="View Alerts", command=self.view_alerts_window)
        alerts_btn.grid(row=2, column=5, sticky=tk.E)

    @staticmethod
    def populate_table_csv(table, filename):
        """Populate a Treeview table with the information in a csv file with provided filename.

        Open the file and read each line into the Treeview.

        Parameters
        ----------
        table : tkinter.ttk.Treeview
            The table to populate
        filename : str
            The filename of the file data is to be read from
        """
        # Read the csv
        data = detector.read_csv(filename)

        # Populate the table
        for i, (y) in enumerate(data):
            if i == 0:  # Don't include the first row (headings)
                continue
            table.insert("", "end", values=list(y))

        return table

    def analyse_file(self, filename):
        """Analyse a file using the machine learning anomaly detection algorithm.

        Read a csv file into an array which is passed through the machine learning algorithm.

        Parameters
        ----------
        filename : str
            The filename of the file to be read from
        """
        # Make sure we are reading the csv file
        csv_filename = abspath(join(CSVDIR, filename))
        try:
            # Check the csv exists, if it doesnt, convert the pcap to csv
            if not os.path.exists(csv_filename):
                detector.pcap_to_csv(filename)
            x = detector.read_csv(csv_filename)
            x = np.array(x)
            # Predict which streams are malicious
            self.det.predict(x)
        except IOError as e:
            # If we can't read the file, tell us and exit the program
            print(e)
            self.quit()

    def upload_file_window(self):
        """A window to select a file to upload to the MLADS project.

        Allow the user to browse the files on their computer and select one to upload.
        """
        upload_window = tk.Toplevel(self.window)
        # Create widgets shown in the window
        browse_lbl = tk.Label(upload_window, text='Upload New File:')
        browse_lbl.grid(row=0, column=0, sticky=tk.E)
        browse_entry = tk.Entry(upload_window, width=50)
        browse_entry.grid(row=0, column=1)
        browse_btn = tk.Button(upload_window, text='Browse',
                               command=lambda: [browse_entry.delete(0, 'end'),
                                                browse_entry.insert(tk.END,
                                                                    filedialog.askopenfilename(initialdir="/",
                                                                                               parent=upload_window,
                                                                                               filetype=(("PCAP Files",
                                                                                                          "*.pcap"),
                                                                                                         ("PCAP Files",
                                                                                                          "*.pcapng"),
                                                                                                         ("All Files",
                                                                                                          "*.*"))))])
        browse_btn.grid(row=0, column=2, sticky=tk.W)
        upload_btn = tk.Button(upload_window, text='Upload',
                               command=lambda: self.upload_file(browse_entry.get(), upload_window))
        upload_btn.grid(row=0, column=3, sticky=tk.W)

    @staticmethod
    def upload_file(inpcap, window):
        """Open a pcap file and convert it to a csv stored in the MLADS project 'csv' folder.

        Check the filename exists, before reading the file and passing it to a PCAP to CSV conversion method.

        Parameters
        ----------
        inpcap : str
            The filename of the file to be converted
        window : tkinter.TK
            The window error messages should be displayed on
        """
        # Check the file exists and isn't too big
        if os.path.exists(inpcap):
            if os.stat(inpcap).st_size > 500000000:
                warning_lbl = tk.Label(window, text="File size too large! Files must be < 0.5Gb", fg='red')
                warning_lbl.config(font=(warning_lbl.cget("font"), 15))
                warning_lbl.grid(row=1, column=0, columnspan=4)
            else:
                # Convert the pcap to csv then close the 'upload file' window
                detector.pcap_to_csv(inpcap)
                window.destroy()
                window.update()
        else:
            warning_lbl = tk.Label(window, text="File does not exist...", fg='red')
            warning_lbl.config(font=(warning_lbl.cget("font"), 15))
            warning_lbl.grid(row=1, column=0, columnspan=4)

    def contacts_window(self):
        """Select all contacts from the database and show them to the user.

        A tkinter TreeView is used to hold the data in a table. Basic search functionality is provided.
        """
        # Reset the window to remove old widgets
        self.reset()
        self.window.title("MLADS - Contacts")

        # Define values needed by the optionbox and treeview
        cols = ('ID', 'Forename', 'Surname', 'Email', 'Phone No.', 'Alertable')
        by_var = tk.StringVar(self.window)
        by_var.set('Forename')

        # Create the widgets that make the window
        search_lbl = tk.Label(self.window, text="Search:")
        search_lbl.grid(row=0, column=0, sticky=tk.E)
        input_textbox = tk.Entry(self.window)
        input_textbox.config(width=35)
        input_textbox.grid(row=0, column=1, columnspan=2, sticky=tk.W)
        by_lbl = tk.Label(self.window, text="By:")
        by_lbl.grid(row=0, column=3, sticky=tk.E)
        by_opbox = tk.OptionMenu(self.window, by_var, *cols)
        by_opbox.config(width=25)
        by_opbox.grid(row=0, column=4, sticky=tk.W)
        search_btn = tk.Button(self.window, text="Search", command=lambda: self.populate_table_db(contact_table,
                                                                                                  'contacts',
                                                                                                  input_textbox.get(),
                                                                                                  by_var.get()))
        search_btn.grid(row=0, column=5, sticky=tk.W)

        contact_table = ttk.Treeview(self.window, columns=cols, show='headings')
        # set column headings and widths
        for col in cols:
            contact_table.heading(col, text=col)
            if col == "ID":
                contact_table.column(col, width=50)
            elif col == "Email":
                contact_table.column(col, width=200)
            else:
                contact_table.column(col, width=125)
        contact_table.grid(row=1, column=0, columnspan=6, sticky=tk.W)
        # Populate the table after it is created
        contact_table = self.populate_table_db(contact_table, 'contacts', None, 'forename')

        add_btn = tk.Button(self.window, text="Add",
                            command=lambda: self.add_edit_contact(contact_table, None, 'add'))
        add_btn.grid(row=2, column=3, sticky=tk.E)
        edit_btn = tk.Button(self.window, text="Edit",
                             command=lambda: self.add_edit_contact(contact_table, contact_table.focus(), 'edit'))
        edit_btn.grid(row=2, column=4, sticky=tk.E)
        remove_btn = tk.Button(self.window, text="Remove",
                               command=lambda: self.remove_contact(contact_table, contact_table.focus()))
        remove_btn.grid(row=2, column=5, sticky=tk.E)

    def add_edit_contact(self, table, focus, cond):
        """Allow the user to add or edit a contact in a new window.

        Each property required is shown to the user in a separate field.

        Parameters
        ----------
        table : tkinter.ttk.Treeview
            The table the initial data is kept in
        focus : str, None
            The ID of the object in focus in table
        cond : str
            Condition to determine if we are editing or adding a contact
        """
        contact_window = tk.Toplevel(self.window)
        # Define verification of email and phone number fields
        vcmd_email = (self.window.register(self.valid_email), "%P", "%W")
        vcmd_phone = (self.window.register(self.valid_phone), "%P", "%W")
        invcmd = (self.window.register(self.invalid), "%W")

        # Define widgets that show in the window
        id_lbl = tk.Label(contact_window, text='ID:')
        id_lbl.grid(row=0, column=0, sticky=tk.W)
        id_entry = tk.Entry(contact_window, width=30)
        id_entry.grid(row=0, column=1, columnspan=2)
        forename_lbl = tk.Label(contact_window, text='Forename:')
        forename_lbl.grid(row=1, column=0, sticky=tk.W)
        forename_entry = tk.Entry(contact_window, width=30)
        forename_entry.grid(row=1, column=1, columnspan=2)
        surname_lbl = tk.Label(contact_window, text='Surname:')
        surname_lbl.grid(row=2, column=0, sticky=tk.W)
        surname_entry = tk.Entry(contact_window, width=30)
        surname_entry.grid(row=2, column=1, columnspan=2)
        email_lbl = tk.Label(contact_window, text='Email:')
        email_lbl.grid(row=3, column=0, sticky=tk.W)
        email_entry = tk.Entry(contact_window, width=30, validate="focusout", validatecommand=vcmd_email,
                               invalidcommand=invcmd)
        email_entry.grid(row=3, column=1, columnspan=2)
        phone_lbl = tk.Label(contact_window, text='Phone:')
        phone_lbl.grid(row=4, column=0, sticky=tk.W)
        phone_entry = tk.Entry(contact_window, width=30, validate="focusout", validatecommand=vcmd_phone,
                               invalidcommand=invcmd)
        phone_entry.grid(row=4, column=1, columnspan=2)
        alertable_lbl = tk.Label(contact_window, text='Alertable:')
        alertable_lbl.grid(row=5, column=0, sticky=tk.W)

        alertable_var = tk.IntVar(self.window)
        false_radio = tk.Radiobutton(contact_window, text='False', variable=alertable_var, value=0)
        false_radio.grid(row=5, column=1)
        true_radio = tk.Radiobutton(contact_window, text='True', variable=alertable_var, value=1)
        true_radio.grid(row=5, column=2)

        # Check if we are adding or editing a contact - each window behaves slightly differently but not by
        # enough to need a method for each
        if cond == 'edit':
            values = table.item(focus)['values']
            # Populate text boxes with existing values
            id_entry.insert(tk.END, values[0])
            id_entry.config(state='disabled')
            forename_entry.insert(tk.END, values[1])
            surname_entry.insert(tk.END, values[2])
            email_entry.insert(tk.END, values[3])
            phone_entry.insert(tk.END, values[4])
            alertable_var.set(convert_alertable(values[5]))

            edit_btn = tk.Button(contact_window, text='Edit',
                                 command=lambda: [self.db.update_row('contacts',
                                                                     ['forename', 'surname', 'email', 'phone_number',
                                                                      'alertable'],
                                                                     [forename_entry.get(),
                                                                      surname_entry.get(),
                                                                      email_entry.get(),
                                                                      phone_entry.get(),
                                                                      alertable_var.get()],
                                                                     values[0]),
                                                  contact_window.destroy(),
                                                  contact_window.update(),
                                                  self.populate_table_db(table, 'contacts', None, None)])
            edit_btn.grid(row=6, column=1, columnspan=2)
        elif cond == 'add':
            next_id = self.db.find_next_id('contacts')
            alertable_var.set(0)

            id_entry.insert(tk.END, next_id)
            id_entry.config(state='disabled')
            add_btn = tk.Button(contact_window, text='Add',
                                command=lambda: [self.db.insert_row('contacts',
                                                                    [next_id,
                                                                     forename_entry.get(),
                                                                     surname_entry.get(),
                                                                     email_entry.get(),
                                                                     phone_entry.get(),
                                                                     alertable_var.get()]),
                                                 contact_window.destroy(),
                                                 contact_window.update(),
                                                 self.populate_table_db(table, 'contacts', None, None)])
            add_btn.grid(row=6, column=1, columnspan=2)

    def remove_contact(self, table, focus):
        """Remove a contact from the backend database.

        A contact is removed from the database based on the highlighted item in the Treeview of the contacts window.

        Parameters
        ----------
        table : tkinter.ttk.Treeview
            The table the initial data is kept in
        focus : str
            The ID of the object in focus in table
        """
        # Find the ID of the contact to delete
        values = table.item(focus)['values']
        cid = values[0]
        self.db.delete_contact(cid)
        # Repopulate the treeview after deletion
        self.populate_table_db(table, 'contacts', None, None)

    def populate_table_db(self, table, search_table, search_term, search_col):
        """Populate a Treeview table with the information in a given table in the database.

        Open the database, search for the required information and read each line into the Treeview.

        Parameters
        ----------
        table : tkinter.ttk.Treeview
            The table to populate
        search_table : str, None
            The table in the database to search and read from
        search_term : str, None
            The term to look for while searching the database
        search_col : str, None
            The column the search_term should be looked for in
        """
        # Remove all values in the table before so we can repopulate when we search the database etc.
        table.delete(*table.get_children())
        data = None
        # Deal with input values appropriately, shame python doesn't have 'switch' functionality
        if search_term is None:
            search_term = ''
        if search_term.lower() in ['true', 'false']:
            search_term = convert_alertable(search_term)

        if search_col is not None:
            if search_col == 'Phone No.':
                search_col = 'phone_number'
            if search_col == 'Contact':
                search_col = 'contact_id'
            if search_col == 'Source IP':
                search_col = 'srcip'
            if search_col == 'Dest. IP':
                search_col = 'dstip'
            if search_col == 'Protocol':
                search_col = 'proto'
            if search_col == 'Source Port':
                search_col = 'sport'
            if search_col == 'Dest. Port':
                search_col = 'dport'
            if search_col == 'Summary':
                search_col = 'flowid'
            search_col = search_col.lower()
        elif search_col is None:
            search_col = 'id'

        # Query the database with the given table
        if search_table == "contacts":
            data = self.db.search_contacts(search_term, search_col.lower())
        elif search_table == "alerts":
            data = self.db.search_alerts(search_term, search_col.lower())

        # Populate the treeview with the data from the database
        if data is not None:
            if search_table == 'contacts':
                for i, (cid, forename, surname, email, phone, alertable) in enumerate(data):
                    if cid == 0:  # If the selected row is the 'redacted' row don't include it
                        continue
                    alertable = convert_alertable(alertable)
                    table.insert("", "end", values=(cid, forename, surname, email, phone, alertable))
            if search_table == 'alerts':
                for i, (aid, summary, srcip, dstip, proto, sport,
                        dport, timestamp) in enumerate(data):
                    table.insert("", "end",
                                 values=(aid, summary, srcip, dstip, proto, sport, dport, timestamp))

        return table

    def create_menubar(self):
        """Create the menu bar shown in every window.

        Add a menu bar showing options for File, Window and Help.
        """
        # Menu Bar
        menu_bar = tk.Menu(self.window)

        # File tab
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.analyse_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Window tab
        window_menu = tk.Menu(menu_bar, tearoff=0)
        window_menu.add_command(label="Main Menu", command=self.main_menu)
        window_menu.add_separator()
        window_menu.add_command(label="View Alerts", command=self.view_alerts_window)
        window_menu.add_command(label="Analyse PCAP", command=self.analyse_window)
        window_menu.add_command(label="Edit Contacts", command=self.contacts_window)
        menu_bar.add_cascade(label="Window", menu=window_menu)

        # Help tab
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About...", command=lambda: os.startfile(README_FILE))
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.window.config(menu=menu_bar)

    def main_menu(self):
        """Setup the main menu that is shown when the program is launched.

        Main menu items include 6 buttons and a menu bar.
        """
        self.reset()
        self.window.title("MLADS - Main Menu")

        # Welcome label
        welcome_lbl = tk.Label(self.window, text="Welcome to MLADS", font=("Arial Bold", 30))
        welcome_lbl.grid(row=0, column=0, columnspan=3)
        # Top row buttons
        view_alerts_btn = tk.Button(self.window, text="View Alerts", command=self.view_alerts_window, height=5,
                                    width=20)
        view_alerts_btn.grid(row=1, column=0, sticky=tk.W, padx=2, pady=2)
        upload_btn = tk.Button(self.window, text="Analyse PCAPs", command=self.analyse_window, height=5,
                               width=20)
        upload_btn.grid(row=1, column=1, sticky=tk.W, padx=2, pady=2)
        contact_btn = tk.Button(self.window, text="Edit Contacts", command=self.contacts_window, height=5, width=20)
        contact_btn.grid(row=1, column=2, sticky=tk.W, padx=2, pady=2)
        # Bottom row buttons
        live_capture_btn = tk.Button(self.window, text="Live Capture", command=coming_soon, height=5, width=20)
        live_capture_btn.grid(row=2, column=0, sticky=tk.W, padx=2, pady=2)
        col1row2_btn = tk.Button(self.window, text="Coming Soon", command=coming_soon, height=5, width=20)
        col1row2_btn.grid(row=2, column=1, sticky=tk.W, padx=2, pady=2)
        col2row2_btn = tk.Button(self.window, text="Coming Soon", command=coming_soon, height=5, width=20)
        col2row2_btn.grid(row=2, column=2, sticky=tk.W, padx=2, pady=2)

    def reset(self):
        """Reset the window by removing all previous widgets and creating a new menu bar."""
        # Remove each 'child' in the window (each widget)
        for child in self.window.winfo_children():
            child.destroy()
        self.create_menubar()

    def quit(self):
        """Quit the program."""
        self.window.quit()

    def valid_email(self, email, widget_name):
        """Check an email address is in a valid format.

        Using regular expressions, ensure the email provided is in a correct format.

        Parameters
        ----------
        email : str
            The email to be validated
        widget_name : str
            The name of the widget that called this method
        """
        if email == "" or re.match(r"[^@]+@[^@]+\.[^@]+", email):
            # If valid set the background of the textbox widget to default (white)
            default_colour = self.window.cget("background")
            self.window.nametowidget(widget_name).config(bg=default_colour)
            return True
        else:
            return False

    def valid_phone(self, phone, widget_name):
        """Check a phone number is in a valid format.

        Using regular expressions, ensure the phone number provided is in a correct format.

        Parameters
        ----------
        phone : str
            The phone number to be validated
        widget_name : str
            The name of the widget that called this method
        """
        if phone == "" or re.match(r"([0-9]{5}|\+[0-9]{1,2} ?[0-9]{4}) ?[0-9]{3} ?[0-9]{3}", phone):
            # If valid set the background of the textbox widget to default (white)
            default_colour = self.window.cget("background")
            self.window.nametowidget(widget_name).config(bg=default_colour)
            return True
        else:
            return False

    def invalid(self, widget_name):
        """Define actions to be taken if a field is invalid.

        Turn the background of the widget red if item is invalid.

        Parameters
        ----------
        widget_name : str
            The name of the widget that called this method"""
        # Set the background colour of the widget to red and keep it in focus
        new_colour = 'red'
        self.window.nametowidget(widget_name).config(bg=new_colour)
        self.window.nametowidget(widget_name).focus()

    def read_config(self):
        """Read the configuration file."""
        try:
            with open(CONFIG_FILE, 'r') as f:
                for line in f.readlines():
                    if line.startswith('#'):  # skip comments
                        continue
                    if 'database' in line:
                        self.db_file = join(DBDIR, line.split("=")[1].strip())
        except FileNotFoundError as err:
            print(err)
            print('Config file error')


def convert_alertable(a):
    """Convert the 'alertable' values from the groups table to/from human readable format.

    Convert the value based on the premise 1 is True and 0 is False.

    Parameters
    ----------
    a : bool, int
        The value to be converted
    """
    # 0 = False, 1 = True
    if a == 0:
        a = 'False'
    elif a == 1:
        a = 'True'
    elif a.lower() == 'false':
        a = 0
    elif a.lower() == 'true':
        a = 1
    return a
