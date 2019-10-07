import os
import threading
from local import run_local
from pacserver import run_pacserver

def enable_proxy():
    os.system('''REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "AutoConfigURL" /t "REG_SZ" /d "http://127.0.0.1:9998/proxy_pac.js" /f''')
def disable_proxy():
    os.system('''REG DELETE "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "AutoConfigURL" /f''')

t1=threading.Thread(target=run_local,name='local_server')
t2=threading.Thread(target=run_pacserver,name='pac_server')

t1.start()
t1.join()
t2.start()
t2.join()


# def tmp():
#     f1 = open('data/wpss.log', 'w')
#     f2 = open('data/wpss_start.log', 'w')
#     p1 = subprocess.Popen(['python', 'local.py'], stdout=f1)
#     p2 = subprocess.Popen(['python', 'pacserver.py'], stdout=f2)
#     enable_proxy()
#
#     def stop(signal, frame):
#         p1.kill()
#         p2.kill()
#         disable_proxy()
#         print('wpss stoped.')
#         exit(0)
#
#     signal.signal(signal.SIGINT, stop)
#     while True:
#         pass





