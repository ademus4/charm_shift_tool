from archive.database_call_v0 import lgdb_tools
from data_retriver import Timber_detectors
from datetime import datetime 
from matplotlib.dates import date2num
from matplotlib.pyplot import plot_date, show, title, grid, legend, xlabel, ylabel, savefig, xticks, tight_layout
from time import sleep
import subprocess
import zipfile

def sec_screens():
    variable_name = 'MSC01.ZT8.107:COUNTS'
    filename = 'sec_screen_data'
    timeformat = '%Y-%m-%d %H:%M:%S.%f'
    headers = ['Time [local]','Counts']
    deltahours = 3.00

    sec = Timber_detectors()

    sec.fetch_from_timber(variable_name, filename, deltahours)

    f = open('data/'+filename+'.CSV', 'r')
    for i in range(7):
      f.readline() # read first 7 header lines
    
    times = []
    counts = []
    for line in f:
      l = line.split(',')
      times.append(datetime.strptime(l[0], timeformat))
      counts.append(l[1])
    
    dates = date2num(times)
    plot_date(dates,counts,'r-',label=variable_name)
    try:
        title(str(times[0])[0:19] + ' to ' + str(times[-1])[0:19]) # [0:19] removes the microseconds to avoid too long title
    except IndexError:
      title(str(datetime.now()))
    legend([variable_name])
    grid(True)
    xlabel('LOCAL_TIME')
    ylabel('count')
    xticks(rotation=70)
    tight_layout()

    savefig('//cern.ch/dfs/Websites/t/test-charmShiftTool/screens/sec.png', dpi=220)

def web_screens():
  p = subprocess.Popen('./phantomjs.exe ./auto_logger.js', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == "__main__":
  directory = '//cern.ch/dfs/Websites/t/test-charmShiftTool/screens/'
  while True:
    sec_screens()
    web_screens()
    print('Creating zip file')
    zf = zipfile.ZipFile(directory+'all_screens.zip', mode = 'w')
    try:
      print('Adding bpm1.png')
      zf.write(directory+'bpm1.png',arcname='bpm1.png')
      print('Adding bpm_all.png')
      zf.write(directory+'bpm_all.png',arcname='bpm_all.png')
      print('Adding sec.png')
      zf.write(directory+'sec.png',arcname='sec.png')
      print('Adding mwpc.png')
      zf.write(directory+'mwpc.png',arcname='mwpc.png')
      print('Adding op.png')
      zf.write(directory+'op.png',arcname='op.png')
    finally:
      print('closing')
      zf.close()
    print('DONE: Sleeping for 5 minutes')
    sleep(300) #sleep 900 seconds aka 15 min
