#!/usr/bin/env python

# Database imports
import sqlite3
from sqlite3 import Error
import os.path
from os.path import split, dirname, abspath, join


HOME = split(dirname(__file__))[0]
CSVDIR = abspath(join(HOME, 'csvs'))
SAVEDIR = abspath(join(HOME, 'model'))
DBDIR = abspath(join(HOME, 'sqlite'))
CONFIG_FILE = abspath(join(HOME, 'mlads.cfg'))
README_FILE = abspath(join(HOME, 'README.txt'))


def convert_tuple(values):
    """Convert a tuple to a string for use in the database.

    Convert a tuple or list of values into a string where each value is enclosed in quotes and separated by a comma.

    Parameters
    ----------
    values : (str), [str]
        The list or tuple of values
    """
    new_values = ""
    for i in values:
        new_values = new_values + "'" + str(i) + "',"

    return new_values[:-1]  # remove the last comma from the string and return it


def create_database(db_file):
    """Create a database.

    Create a database in the given file which has 3 tables based on schema designed in the final report.

    Parameters
    ----------
    db_file : str
        The file in which the new database should be stored
    """
    contact_table_query = """CREATE TABLE IF NOT EXISTS contacts (
                                    id integer UNIQUE NOT NULL PRIMARY KEY,
                                    forename text NOT NULL,
                                    surname text NOT NULL,
                                    email text NOT NULL,
                                    phone_number text NOT NULL
                            );"""

    group_table_query = """CREATE TABLE IF NOT EXISTS groups (
                                    id integer UNIQUE NOT NULL PRIMARY KEY,
                                    contact_id integer NOT NULL,
                                    alertable boolean NOT NULL CHECK (alertable IN (0,1)),
                                    FOREIGN KEY (contact_id) REFERENCES contacts (id)
                            );"""

    alert_table_query = """CREATE TABLE IF NOT EXISTS alerts (
                                    id integer UNIQUE NOT NULL PRIMARY KEY,
                                    group_id integer NOT NULL,
                                    flowid text,
                                    fwd_pkt_len_std real,
                                    bwd_pkt_len_std real,
                                    fwd_pkt_len_max integer,
                                    fwd_pkt_len_min integer,
                                    bwd_pkt_len_max integer,
                                    bwd_pkt_len_min integer,
                                    fwd_pkt_len_mean real,
                                    bwd_pkt_len_mean real,
                                    timestamp text,
                                    srcip text,
                                    dstip text,
                                    proto text,
                                    sport text,
                                    dport text,
                                    reason text,
                                    FOREIGN KEY (group_id) REFERENCES groups (id)
                                );"""

    insert_redacted_contact = "INSERT INTO contacts VALUES (0, 'Redacted', 'Redacted', 'Redacted', 'Redacted');"
    insert_unalertable_group = "INSERT INTO groups VALUES (0, 0, 0), (1, 0, 1);"

    try:
        conn = sqlite3.connect(db_file)  # connect to the file - creates new file if not exists
        c = conn.cursor()
        c.execute(contact_table_query)
        c.execute(group_table_query)
        c.execute(alert_table_query)
        c.execute(insert_redacted_contact)  # used when contacts are deleted
        c.execute(insert_unalertable_group)
        conn.commit()  # Save the database - changes are lost otherwise
    except Error as e:
        print(e)


class Databaser:
    """A class used to interact with a database used for the MLADS program.

    Attributes
    ----------
    conn : sqlite3.Connection
        A connection to a database file
    c : sqlite3.Cursor
        A cursor on the connection object

    Methods
    -------
    __init__(self)
        Define initial values for various class attributes.
    create_connection(self, db_file)
        Create a connection to the database.
    insert_row(self, table, values)
        Insert rows into the database.
    update_row(self, table, cols, values, row_id)
        Update rows in the database.
    delete_contact(self, contact_id)
        Delete a row from the contacts table.
    select_all_alerts(self, aid)
        Select all columns from the alerts table given an alert ID.
    find_next_id(self, table)
        Find the next unique ID in a table.
    search_contacts(self, term, col)
        Search the contacts table.
    search_alerts(self, term, col)
        Search the alerts table.
    """
    def __init__(self, database_file=abspath(join(DBDIR, 'mlads_db.db'))):
        """Define initial values for various class attributes.

        Define the database connection object and then define the cursor."""
        # define a connection
        self.conn = None
        self.create_connection(database_file)
        try:
            # create the cursor
            self.c = self.conn.cursor()
        except Error as e:
            print(e)

    def create_connection(self, db_file):
        """Create a connection to the database.

        Given a database file, we create an SQLite connection.

        Parameters
        ----------
        db_file : str
            The file in which the SQLite database is kept
        """
        connection = None
        if not os.path.exists(db_file):
            # if the database file doesn't exist, create a new one
            create_database(db_file)

        try:
            # connect
            connection = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        self.conn = connection

    def insert_row(self, table, values):
        """Insert rows into the database.

        Given a table and the appropriate values, insert a row into the database.

        Parameters
        ----------
        table : str
            The name of the table to insert values to
        values : [str]
            The tuple of values to be inserted
        """
        query = []
        if table == 'contacts':
            c_values = convert_tuple(values[:-1])
            g_values = convert_tuple((str(self.find_next_id('groups')), values[0], values[-1]))
            query.append(str("INSERT INTO contacts VALUES (" + c_values + ");"))
            query.append(str("INSERT INTO groups VALUES (" + g_values + ");"))
        if table == 'alerts':
            # Format the values so the database accepts them
            values = str(self.find_next_id(table)) + "," + convert_tuple(values)
            query.append("INSERT INTO " + table + " VALUES (" + values + ");")

        try:
            for q in query:
                self.c.execute(q)
            self.conn.commit()  # Save to the database - changes are lost otherwise
        except Error as e:
            print(e)

    def update_row(self, table, cols, values, row_id):
        """Update rows in the database.

        Given a table and the appropriate values, update a row into the database.

        Parameters
        ----------
        table : str
           The name of the table to be updated
        cols : [str]
            The names of columns that will be updated
        values : [str]
           The tuple of values to be updated to
        row_id : int
            The ID of the row that will be updated
        """
        set_vals = ''
        g_set_vals = ''
        query = []
        # Check the parameters given are valid, then form the query
        if len(cols) > 0 and len(cols) == len(values):
            if table == 'contacts':
                for i, col in enumerate(cols):
                    if col == 'alertable':
                        g_set_vals = str(col) + " = '" + str(values[i]) + "'"
                    else:
                        set_vals = set_vals + str(col) + " = '" + str(values[i]) + "',"
                query.append(str("UPDATE contacts SET " + set_vals[:-1] + " WHERE id = " + str(row_id) + ";"))
                query.append(str("UPDATE groups SET " + g_set_vals + " WHERE contact_id = " + str(row_id) + ";"))
            else:
                for i, col in cols:
                    set_vals = set_vals + str(col) + " = '" + str(values[i]) + "',"
                query.append(str("UPDATE " + table + " SET " + set_vals[:-1] + " WHERE id = " + str(row_id) + ";"))
        else:
            # If not valid, return from the method without touching the database
            print("Invalid details")
            return

        try:
            for q in query:
                self.c.execute(q)
            self.conn.commit()  # Save to the database - changes are lost otherwise
        except Error as e:
            print(e)

    def delete_contact(self, contact_id):
        """Delete a row from the contacts table.

        Given a contact ID, delete the corresponding row from the contacts table and update other tables as required.

        Parameters
        ----------
        contact_id : int
            The ID of the contact to be deleted
        """
        delete_contact_query = "DELETE FROM contacts WHERE id = " + str(contact_id) + ";"
        delete_group_query = "DELETE FROM groups where contact_id = " + str(contact_id) + ";"

        try:
            self.c.execute(delete_contact_query)
            self.c.execute(delete_group_query)
            self.conn.commit()  # Save to the database - changes are lost otherwise
        except Error as e:
            print(e)

    def select_all_alerts(self, aid):
        """Select all columns from the alerts table given an alert ID.

        Given an alert ID select all columns from the alerts table and return the data.

        Parameters
        ----------
        aid : int
            The alert ID to be selected
        """
        data = None
        col_names = []
        query = "SELECT alerts.*, contacts.forename, contacts.surname, contacts.email " \
                "FROM alerts JOIN groups ON alerts.group_id = groups.id " + \
                "JOIN contacts ON groups.contact_id = contacts.id " + \
                "WHERE alerts.id = " + str(aid) + ";"
        try:
            self.c.execute(query)
            data = self.c.fetchone()  # Fetch the data
            desc = self.c.description  # Fetch the column names
            for i in desc:
                col_names.append(i[0])
        except Error as e:
            print(e)

        return col_names, data

    def find_next_id(self, table):
        """Find the next unique ID in a table.

        Given a table, find the next possible unique ID.

        Parameters
        ----------
        table : str
            The table to find the next ID in
        """
        current_id = None
        if table in ('contacts', 'groups', 'alerts'):
            try:
                # Execute a query to select only the largest id currently in the table
                self.c.execute('SELECT id FROM ' + table + ' ORDER BY id DESC LIMIT 1;')
                current_id = self.c.fetchone()
            except Error as e:
                print(e)
        else:
            print('Invalid table name')

        if current_id is None:  # If the table was empty, next id = 0
            current_id = 0
        else:  # Otherwise add 1 to the current largest id
            current_id = current_id[0] + 1
        return current_id

    def search_contacts(self, term, col):
        """Search the contact table.

        Given a search term and column, search the contact table.

        Parameters
        ----------
        term : str
            The term to search for
        col : str
            The column to search through
        """
        data = None
        if 'alert' in col:
            query = "SELECT contacts.id, contacts.forename, contacts.surname, contacts.email, contacts.phone_number, " \
                "groups.alertable FROM contacts INNER JOIN groups ON groups.contact_id = contacts.id " \
                "WHERE groups.alertable LIKE '%" + str(term) + "%';"
        else:
            query = "SELECT contacts.id, contacts.forename, contacts.surname, contacts.email, contacts.phone_number, " \
                "groups.alertable FROM contacts INNER JOIN groups ON groups.contact_id = contacts.id " \
                "WHERE contacts." + col + " LIKE '%" + str(term) + "%';"
        try:
            self.c.execute(query)
            data = self.c.fetchall()
        except Error as e:
            print(e)
        return data

    def get_alertable_contacts(self):
        """Get all contacts in the alertable group.

        Get the contact details for any contact that is a part of the alertable group.
        """
        data = None
        query = "SELECT contacts.email, contacts.phone_number FROM contacts " \
                "INNER JOIN groups ON contacts.id = groups.contact_id WHERE groups.alertable = 1;"
        try:
            self.c.execute(query)
            data = self.c.fetchall()
        except Error as e:
            print(e)
        return data

    def search_groups(self, term, col):
        """Search the group table.

        Given a search term and column, search the group table.

        Parameters
        ----------
        term : str
            The term to search for
        col : str
            The column to search through
        """
        data = None
        query = "SELECT * FROM groups WHERE " + col + " LIKE '%" + str(term) + "%';"
        try:
            self.c.execute(query)
            data = self.c.fetchall()
        except Error as e:
            print(e)
        return data

    def search_alerts(self, term, col):
        """Search the alert table.

        Given a search term and column, search the alert table.

        Parameters
        ----------
        term : str
            The term to search for
        col : str
            The column to search through
        """
        data = None
        # Select only the columns that will be shown to the user
        query = "SELECT id, flowid, srcip, dstip, proto, sport, dport, timestamp " + \
                "FROM alerts WHERE " + col + " LIKE '%" + str(term) + "%' ORDER BY id DESC;"
        try:
            self.c.execute(query)
            data = self.c.fetchall()
        except Error as e:
            print(e)
        return data
