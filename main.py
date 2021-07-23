import subprocess
import time
import os
import time
#from tendo import singleton
#me = singleton.SingleInstance()  # will sys.exit(-1) if other instance is running

threshold = 95
dataDisks = ["/mnt/gdrive"]



def remountRclone():
    subprocess.Popen(["touch", "./lockFile"]).wait()
    subprocess.Popen(["systemctl", "stop", "rclone"]).wait()
    subprocess.Popen(["umount", "/mnt/gdrive"]).wait()
    subprocess.Popen(["cp", "/root/rclone.log", "./rclone.copy.log"]).wait()
    subprocess.Popen(["systemctl", "start", "rclone"]).wait()

def verifyDisksMounted():
    validDisks = 0
    errorString = ""
    for disk in dataDisks:
        if not os.path.exists('./lockFile') and not os.path.exists(os.path.join(disk, 'finderFile')):
            print("Error! Drive not mounted, tring to remount...")
            args = ['pushbullet', 'Error! Titanium - gdrive not mounted, tring to remount...']
            subprocess.Popen(args)
            remountRclone()
            errorString += 'Titanium - re-checking...'
            print(errorString)
            time.sleep(10)
        if os.path.exists('./lockFile') and not os.path.exists(os.path.join(disk, 'finderFile')):
            errorString += 'Titanium - Failed remount, rclone drive not detected.'
        elif os.path.exists('./lockFile') and os.path.exists(os.path.join(disk, 'finderFile')):
            errorString += 'Titanium - Successfully re-mounted drive, check saved log for an error'
            subprocess.Popen(['rm', 'lockFile'])
        if not errorString == "":
            subprocess.Popen(['pushbullet', errorString])
    return 0

if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    print(str(cwd))
    os.chdir(cwd)
    verifyDisksMounted()
