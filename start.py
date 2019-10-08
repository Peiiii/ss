import os
import threading
from local import run_local
from pacserver import run_pacserver
import signal
# import sys

def enable_proxy():
    os.system('''REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "AutoConfigURL" /t "REG_SZ" /d "http://127.0.0.1:9998/proxy_pac.js" /f''')
def disable_proxy():
    os.system('''REG DELETE "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "AutoConfigURL" /f''')

t1=threading.Thread(target=run_local,name='local_server')
t2=threading.Thread(target=run_pacserver,name='pac_server')

def stop(signal,frame):
    disable_proxy()
    print('Exiting...')
    os._exit(0)
signal.signal(signal.SIGINT,stop)
enable_proxy()
t1.setDaemon(True)
t2.setDaemon(True)
t2.start()
t1.start()
while True:
    pass




