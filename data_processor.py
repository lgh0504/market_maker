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

    def delete_first_row(self, table):
        db_command = "DELETE FROM " + table + " WHERE rowid= (SELECT rowid FROM " + table + " order by rowid limit 1);"
        self.c.execute(db_command)
        self.conn.commit()

    def get_line(self, table, field={}):
        db_command = "SELECT * FROM " + table + " WHERE " + field[0] + "=(?)"
        self.c.execute(table_command, (field[1],))

    def get_all(self, table):
        db_command = "SELECT * FROM " + table
        self.c.execute(db_command)

    def get_last_n_rows(self, table, period):
        db_command = "SELECT price FROM " + table + " ORDER BY rowid DESC LIMIT " + str(period) + ";"
        self.c.execute(db_command)

class api_calls():
    def __init__():
        # List of all possible commands
        self.wrapper = wrapper.bittrex_wrapper()
        command_list = ["getticker", "getmarketsummaries", "getmarketsummary",
                        "getorderbook", "buylimit", "selllimit", "cancel",
                        "getopenorders", "getbalances", "getbalance", "getorder"]

    # Define functions for each command
    def getticker(self, pair):
        return self.wrapper.process_command("getticker", "public",
                                            {'market': str(pair)})

    def getmarketsummaries(self):
        return self.wrapper.process_command("getmarketsummaries", "public")

    def getmarketsummary(self, pair):
        return self.wrapper.process_command("getmarketsummary", "public",
                                            {'market': str(pair)})

    # Booktype must be 'sell', 'buy', or 'both'
    def getorderbook(self, pair, booktype):
        return self.wrapper.process_command("getorderbook", "public",
                                            {'market': str(pair),
                                             'type': booktype})

    def buylimit(self, pair, quantity, rate):
        return self.wrapper.process_command("buylimit", "market",
                                            {'market': str(pair),
                                             'quantity': quantity,
                                             'rate': rate})

    def selllimit(self, pair, quantity, rate):
        return self.wrapper.process_command("selllimit", "market",
                                            {'market': str(pair),
                                             'quantity': quantity,
                                             'rate': rate})

    def cancel(self, order_id):
        return self.wrapper.process_command("cancel", "market",
                                            {'uuid': order_id})

    def getopenorders(self, pair):
        return self.wrapper.process_command("getopenorders", "market",
                                            {'market': str(pair)})

    def getbalances(self):
        return self.wrapper.process_command("getbalances", "account")

    def getbalance(self, pair):
        return self.wrapper.process_command("getbalance", "account",
                                            {'currency': str(pair)})

    def getorder(self, order_id):
        return self.wrapper.process_command("getorder", "account",
                                            {'uuid': order_id})
