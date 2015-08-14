import subprocess
import os

class lgdb_tools(object):
    def __init__(self):
        self.java    = self.get_java_install_location()#r'C:\Program Files (x86)\Java\jre7\bin\java.exe'
        #self.java    = r'C:\Program Files\Java\jre7\bin\java.exe'
        self.jarfile = r'accsoft-cals-extr-client-nodep.jar'
        self.j_api_str = '{} -jar {} -M DS -vs {} -t1 "{}" -t2 "{}" -N {} -F CSV -MD'

    def get_java_install_location(self):
      osname = os.name
      if osname == "nt":
        # Unfortunatley this does not work when running 32-bit python on 64-bit windows
        # because "where java" returns C:\Windows\system32\java.exe, however windows
        # will redirect 32-bit applications from system32 to WoW64, thus python will
        # try to run C:\Windows\WoW64\java.exe which does not exist... Thus it is assumed
        # that java is installed to the default location instead
        #retstr = subprocess.check_output(["java", "-version"],stderr=subprocess.STDOUT,shell=True)
        #retstr = retstr[:-2] # remove the \r\n, or java wont run
        #retstr = retstr.decode("utf-8")
        retstr = "C:\Program Files\Java\jre7\\bin\java.exe" 
        if not os.path.isfile(retstr):
          print("Error: Please install Java to " + "C:\Program Files\Java\jre7\\bin\java.exe")
          exit(-1)
      elif osname == "posix":
        retstr = subprocess.check_output(["which", "java"])
        retstr = retstr.decode("utf-8")
        retstr = retstr.replace('\n','')
        if not os.path.isfile(retstr):
          print("Error: Please install Java!")
          exit(-1)
      else:
        print ("ERROR: your OS is not supported!\nSupported OSes are Windows 7 or higher and posix compliant OSes like Linux and OS X.")
        exit(-1)
      return retstr

    def get_data(self, variable_name, t1, t2, filename):
        self.j_api_command = self.j_api_str.format(self.java, self.jarfile, variable_name, t1, t2, filename)
        print (self.j_api_command)
        self.p_call()
        return self.p.communicate()

    def p_call(self):
        self.p = subprocess.Popen(self.j_api_command,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
