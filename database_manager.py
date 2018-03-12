#This file contains a database manager and a api function caller
# Created on March 8th, 2018
# By Izak Fritz

import sqlite3
import wrapper
import time
import sched

# SQLite Database Manager
class db_manager():
    def __init__(self, db_name):
        # Connection to the sqlite database defined in db_name
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def create_table(self, name, fields={}, types={}):
        # Create the db_command by stating we are creating a table
        db_command = "CREATE TABLE IF NOT EXISTS " + name.strip(' ') + "("
        # For each field add that field to the command
        for i in range (0, len(fields)-1):
            db_command += (fields[i] + " " + types[i] + ", ")
        db_command += (fields[len(fields)-1] + " " + types[len(fields)-1]) + ")"

        self.c.execute(db_command)
        self.conn.commit()

    def insert_entry(self, table, data={}):
        # Create db_command by stating we are adding an entry to the table_command
        db_command = "INSERT INTO " + table + " VALUES ("
        for i in range (0, len(data)-1):
            db_command += "'" + data[i] + "', "
        db_command += (str(data[len(data)-1]) + " );")

        self.c.execute(db_command)
        self.conn.commit()

    def get_line_for_param(self, table, field={}):
        db_command = "SELECT * FROM " + table + " WHERE " + field[0] + " = " + field[1] + ";"
        self.c.execute(db_command)
        return c.fetchone()

    def delete_line_for_param(self, table, field={}):
        db_command = "DELETE FROM " + table + " WHERE " + field[0] + " = " + field[1] + ";"
        self.c.execute(db_command)
        self.conn.commit()

    def get_all(self, table):
        db_command = "SELECT * FROM " + table
        self.c.execute(db_command)
        return c.fetchall()

    def get_last_n_rows(self, table, period):
        db_command = "SELECT price FROM " + table + " ORDER BY rowid DESC LIMIT " + str(period) + ";"
        self.c.execute(db_command)
        return c.fetchall()
