# Functions for interacting with the sqltie3 database

import sqlite3
from itertools import chain

database  = '//cern.ch/dfs/Websites/t/test-charmShiftTool/data/charm_shift.db'
#database = './charm_shift.db'
set_table = 'settings'
msg_table = 'messages'
#status_table 'status'
response_table = 'response'
shifter_table = 'shifter'

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
        self.cur.execute('create table if not exists ' + msg_table + ' (id INTEGER PRIMARY KEY, time text, msg text, status int, fwhm int, centre int)')
        #self.cur.execute('create table if not exists ' + status_table + ' (id INTEGER PRIMARY KEY, text, msg text, status int)')
        self.cur.execute('create table if not exists ' + response_table + ' (id INTEGER PRIMARY KEY, name text, status int)')
        self.cur.execute('create table if not exists ' + shifter_table + ' (id INTEGER PRIMARY KEY, name text, email text, phone int, current int, alert int)')
        self.con.commit()
        self.close_db()

    #def __del__(self):
    #  self._db_connection.close()
        
    def load_db(self):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()
    
    def close_db(self):
      self.con.close()

    def insert_setting(self, data):
      if len(data) != 2:
        print("ERROR: A row in settings has 2 columns, not " + str(len(data)) + "!")
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

    def insert_shifter(self, data):
      if len(data) != 5:
        print("ERROR: shifter data must have length 4!")
        return -1
      self.load_db()
      self.cur.execute("select rowid from " + shifter_table + " where name = ?",[data['name'],])
      row = self.cur.fetchone()
      if row is None:
        self.cur.execute("insert into " + shifter_table + "(name, email, phone, current, alert)" " values(?,?,?,?,?)", [data['name'],data['email'],data['phone'],data['current'],data['alert']])
      else:
        self.cur.execute("update " + shifter_table + " set email=?, phone=?, current=?, alert=? where name=?",[data['email'],data['phone'],data['current'],data['alert'],data['name']])
      self.con.commit()
      self.close_db()

    def set_shifter_email(self, data):
      if len(data) !=2:
        print("ERROR: shifter data must have length 4!")
        return -1
      self.load_db()
      self.cur.execute("select rowid from " + shifter_table + " where name = ?",(data[0],))
      row = self.cur.fetchone()
      if row is None:
        data += (0,0,0)
        self.cur.execute("insert into " + shifter_table + "(name, email, phone, current, alert)" " values(?,?,?,?,?)", data)
      else:
        self.cur.execute("update " + shifter_table + " set email=? where name=?",(data[1],data[0]))
      self.con.commit()
      self.close_db()

    def set_shifter_phone(self, data):
      if len(data) !=2:
        print("ERROR: shifter data must have length 4!")
        return -1
      self.load_db()
      self.cur.execute("select rowid from " + shifter_table + " where name = ?",(data[0],))
      row = self.cur.fetchone()
      if row is None:
        data = (data[0],"",data[1],0,0)
        self.cur.execute("insert into " + shifter_table + "(name, email, phone, current, alert)" " values(?,?,?,?,?)", data)
      else:
        self.cur.execute("update " + shifter_table + " set phone=? where name=?",(data[1],data[0]))
      self.con.commit()
      self.close_db()

    def set_current_shifter(self, name):
      self.load_db()
      self.cur.execute("select rowid from " + shifter_table + " where name = ?",[name])
      row = self.cur.fetchone()
      if row is None:
        # Shifter does not exist in database, so create him
        # This wont send emails to them, but will allow displaying their name in the web interface
        data = {'name':name,'email':'','phone':'','current':0,'alert':0}
        self.insert_shifter(data)
      current = self.get_current_shifter()
      self.load_db()
      if current == None:
        self.cur.execute("update " + shifter_table + " set current=1 where name='"+name+"'")
      elif current != name:
        self.cur.execute("update " + shifter_table + " set current=0 where name='"+current+"'")
        self.cur.execute("update " + shifter_table + " set current=1 where name='"+name+"'")
      self.con.commit()
      self.close_db()

    def get_current_shifter(self):
      self.load_db()
      self.cur.execute("select name from " + shifter_table + " where current = 1")
      shifter = self.cur.fetchone()
      if shifter != None:
        shifter = shifter[0]
      self.close_db()
      return shifter

    def get_all_shifters(self):
      self.load_db()
      self.cur.execute("select name from " + shifter_table)
      shifters = self.cur.fetchall()
      self.close_db()
      shifters = list(chain.from_iterable(shifters))
      return shifters

    def get_alerts(self):
      self.load_db()
      self.cur.execute("select name from " + shifter_table + " where alert=1")
      alertees = self.cur.fetchall()
      # Tested two methods of flatting lists
      #$ python -mtimeit -s'l=[[1,2,3],[4,5,6], [7], [8,9]]*99' '[item for sublist in l for item in sublist]'
      #10000 loops, best of 3: 62.6 usec per loop
      #
      #$ python -mtimeit -s 'l=[[1,2,3],[4,5,6], [7], [8,9]]*99' 'list(itertools.chain.from_iterable(l))'
      #10000 loops, best of 3: 34.8 usec per loop
      alertees = list(chain.from_iterable(alertees))
      self.close_db()
      return alertees

    def set_alert(self,data):
      if len(data) !=2:
        print("ERROR: set_alert must have length 2!")
        return -1
      self.load_db()
      self.cur.execute("select rowid from " + shifter_table + " where name = ?",(data[0],))
      row = self.cur.fetchone()
      if row is None:
        data = (data[0],"","",0,data[1])
        self.cur.execute("insert into " + shifter_table + "(name, email, phone, current, alert)" " values(?,?,?,?,?)", data)
      else:
        self.cur.execute("update " + shifter_table + " set alert=? where name=?",[data[1],data[0]])
      self.con.commit()
      self.close_db()

    def get_shifter_info(self, name):
      self.load_db()
      self.cur.execute("select * from " + shifter_table + " where name='" + name + "'")
      shifter = self.cur.fetchone()
      self.close_db()
      shifter_dict = {}
      if shifter != None:
        shifter_dict['name'] = shifter[1]
        shifter_dict['email'] = shifter[2]
        shifter_dict['phone'] = shifter[3]
        shifter_dict['current'] = shifter[4]
        shifter_dict['alert'] = shifter[5]
      else:
        shifter_dict['name']    = ""  
        shifter_dict['email']   = ""  
        shifter_dict['phone']   = ""  
        shifter_dict['current'] = "" 
        shifter_dict['alert']   = "" 
      return shifter_dict

    def get_setting(self, settingname):
      if type(settingname) != str:
        print("ERROR: must supply setting name as a string")
        return -1
      self.load_db()
      self.cur.execute("select * from settings where name='"+settingname+"'")
      setting = self.cur.fetchone()
      try:
        setting = int(setting[2])
      except NoneType:
          return None
      return setting

    def insert_msg(self, data):
      if len(data) != 5:
        print("ERROR: A row in settings has 5 columns, not " + str(len(data)) + "!")
        return -1
      self.load_db()
      #data = [self.cur.lastrowid()+1]+data
      self.cur.execute("insert into " + msg_table + "(time,msg,status,fwhm,centre)" " values(?,?,?,?,?)", data)
      self.con.commit()
      self.close_db()

    def get_last_msg(self):
      self.load_db()
      self.cur.execute("select * from "+msg_table+" where id=(select max(id) from " + msg_table+")")
      msg = self.cur.fetchone() 
      self.close_db()
      return msg

    def get_last_x_msgs(self, x):
      self.load_db()
      self.cur.execute("select * from "+msg_table+" order by id DESC limit " + str(x))
      msg = self.cur.fetchall() 
      self.close_db()
      return msg

    def get_beam_status(self):
      self.load_db()
      self.cur.execute("select * from "+msg_table+" where id=(select max(id) from " + msg_table+")")
      msg = self.cur.fetchone() 
      beam = msg[3]
      fwhm = msg[4]
      centre = msg[5]
      return beam, fwhm, centre

    def get_response(self):
      self.load_db()
      self.cur.execute("select status from "+response_table+" where name='beam'")
      beam = self.cur.fetchone()
      # Will return None if there is no response in database
      return beam

    def respond(self, x):
      if type(x) != int:
        print("ERROR: first argument must be a string and second argument an int")
        return -1
      self.load_db()
      self.cur.execute("select rowid from "+response_table+" where name='beam'")
      data = ('beam',x)
      row = self.cur.fetchone()
      if row is None:
        self.cur.execute("insert into " + response_table + "(name, status)" " values(?,?)", data)
      else:
        self.cur.execute("update "+response_table+" set status=? where name='beam'",(x,))
      self.con.commit()
      self.close_db()

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
      self.con.commit()
      self.close_db()
