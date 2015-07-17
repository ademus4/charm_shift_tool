# Functions for writing and readind to the charm shift database.
# The data base contains three different tables, one for user settings
# one containing reference values for the beam position detectors, and
# one for the beam intensity detectors.
# There are three user settings inserted into the settings table.
# They are:
# 1. Amout of time the beam is down before a message is sent in minutes,
# 2. Percentage increase/decrease in the intesity from the reference before a message is sent.
# 3. Percentage increase/decrease in the doserate per hour before a message is sent.

import sqlite3

database  = 'charm_shift.db'
set_table = 'settings'
user_table = 'User_info'
msg_table = 'messages'

default_pos = []

class db_commands:
    def __init__(self):
        '''
        Here I'm not sure if it's better to leave the database open and close manually after, or do
        as you are now and open and close within each function. Either way would work, and I guess
        closing it after each call is cleaner and potentially safer.
        :return:
        '''
        self.load_db()
        # Make sure that tables exist
        self.cur.execute('create table if not exists ' + set_table + ' (id INTEGER PRIMARY KEY, name text, setting int)')
        self.cur.execute('create table if not exists ' + user_table + ' (id integer priamry key, name text, email text, phone int)')
        self.cur.execute('create table if not exists ' + msg_table + ' (id INTEGER PRIMARY KEY, time text, msg text, status int)')
        self.con.commit()
        self.close_db()

    #def __del__(self):
    #  self._db_connection.close()
        
    def load_db(self):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()
    
    def close_db(self):
      self.con.close()

    def insert_user(self, data):
      if len(data) != 4:
        print("ERROR: A row in settings has 4 columns, not " + str(len(data)) + "!")
        return -1
      self.load_db()
      self.cur.execute("insert into " + user_table + " values(?,?,?)", data)
      self.con.commit()
      self.close_db()

    def insert_setting(self, data):
      if len(data) != 2:
        print("ERROR: A row in settings has 3 columns, not " + str(len(data)) + "!")
        return -1
      self.load_db()
      # Insert new setting if one with the same name does not exist
      # else update the setting
      # I am unsure if this is the best way of doing it 
      # Using insert or ingore might be a better method
      self.cur.execute("select rowid from settings where name = ?",(data[0],))
      row = self.cur.fetchone()
      if row is None:
        self.cur.execute("insert into " + set_table + "(name, setting)" " values(?,?)", data)
      else:
        self.cur.execute("update settings set setting=? where name=?",(data[1],data[0]))
      self.con.commit()
      self.close_db()

    def get_setting(self, settingname):
      if type(settingname) != str:
        print("ERROR: must supply setting name as a string")
        return -1
      self.load_db()
      self.cur.execute("select * from settings where name="+settingname)
      setting = self.cur.fetchone()
      return setting

    def insert_msg(self, data):
      if len(data) != 3:
        print("ERROR: A row in settings has 2 columns, not " + str(len(data)) + "!")
        return -1
      self.load_db()
      #data = [self.cur.lastrowid()+1]+data
      self.cur.execute("insert into " + msg_table + "(time,msg,status)" " values(?,?,?)", data)
      self.con.commit()
      self.close_db()

    def get_last_msg(self):
      self.load_db()
      self.cur.execute("select * from "+msg_table+" where id=(select max(id) from " + msg_table+")")
      msg = self.cur.fetchone() 
      return msg

    def print_tables(self):
      self.load_db()
      self.cur.execute("select * from messages")
      data = self.cur.fetchall()
      for d in data:
        print(d)
      self.close_db()

    def remove_all(self):
      self.load_db()
      self.cur.execute("delete from " + set_table)
      self.cur.execute("delete from " + msg_table)
      self.cur.execute("delete from " + user_table)
      self.con.commit()
      self.close_db()
