import os
import subprocess

from multiprocessing import Pool
import time

webhook = 'https://nyxserverbot.herokuapp.com'
datawebhook = webhook + '/data'
pwd = '1910'


def sendData(data, webhook=datawebhook):
    subprocess.call("curl -X POST -H 'Content-type: application/text' --data '\"{}\"' {}".format(data, webhook), shell=True)
    
def sshSend(url):
    print('\nSending Url..')
    sendData(url)

# -----------------------------------------

def startNgrok(port):
    print('\nStarting Ngrok....')
    url = subprocess.getoutput('./ngrokstart.sh {}').format(port).split('/')[-1]
    print('\nStart finish, url : ')
    print(url)
    return url

def killNgrokProcess():
    print('\nKilling Ngrok..')
    subprocess.call("killall ngrok", shell=True)

def sshStart(): #kill ngrok process, start ngrok, send ngrok link | every 8 hour
    print('\nKilling Ngrok..')
    killNgrokProcess()
    print('\nSending Ngrok link and starting it..')
    sendData(startNgrok(22))
    print('\nDone..')

# -----------------------------------------------

def rebootProcess():
    print('3 minutes..')
    sendData('3 minutes to reboot..')
    time.sleep(minuteTosecond(1))
    print('2 minutes..')
    time.sleep(minuteTosecond(1))
    print('1 minutes')
    time.sleep(minuteTosecond(1))
    sendData('rebooting server.')
    print('rebooting server..')
    subprocess.call('reboot', shell=True)


# -----------------------------------------------

def temp():
    temp = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, './tempCheck.sh'))
    return temp

def tempCheck():
    a = True
    while ( a == True ):
        temps = int(temp())
        if temps > 75:
            print('server is at > 75 degree')
            a = False
    print('Auto reboot in 3 minute...')
    rebootProcess()

#------------------------------------------------

def batStatus():
    status = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, './chargeStatus.sh'))
    return status

def checkBatStatus():
    status = batStatus()
    if status == 'Discharging':
        print('\nnot ok')
        return 'discharging'
    else:
        print('\nok')
        return 'charging'

def sendBatStatus():
    status = checkBatStatus()
    sendData(status)

# -----------------------------------

def checkNgrok(): # check if ngrok is up or not | run every 30 minute
    status = str(subprocess.getoutput('./ngrokStatus.sh'))
    if status == '0':
        print('\nok')
        return 'ok'
    elif status == '1':
        print('\nNgrok missing, starting it')
        sshStart()

def ngrok(): # every 8 hour
    sshStart()

def battery(): # every 15 minute
    status = checkBatStatus()
    if status == 'discharging':
        sendData("The server is {}, please plug it in.".format(status))

# --------------------------------------------



def time_looper(a):
    while True:
        print('\nstarting function {} in {} sec on {}'.format(str(a[1]).split(' ')[1], a[0], time.ctime()))
        time.sleep(a[0]) # in second
        print('\nstarting function {}'.format(str(a[1]).split(' ')[1]))
        a[1]()
        print('\nfinish at {}'.format(time.ctime()))

def minuteTosecond(minute):
    second = minute * 60
    print(int(second))
    return second

def hourToSecond(hour):
    second = minuteTosecond(hour * 60)
    print(int(second))
    return second

def test1():
    print('TEST 1 done..')

def test2():
    print('TEST 2 done...')

def test3():
    print('TEST 3 done....')

def process_start(b):
    print('\nStarting function {} at {}'.format(str(b).split(' ')[1], time.ctime()))
    b()

def run_process(p):
    p[0](p[1])

def pool_handler():
    # a = minuteTosecond(30) | check ngrok
    # b = hourToSecond(8) | start ngrok
    # c = minuteTosecond(15) | check battery
    a = 500
    b = 600
    c = 500

    process = ([time_looper, [a, checkNgrok]], [time_looper, [b, startNgrok]], [time_looper, [c, battery]], [process_start, tempCheck]) # in order = checkngrok, ngrok, battery 
    secondary_process = (tempCheck,)
    p = Pool(4)
    p.map(run_process, process)

if __name__ == "__main__":
    pool_handler()