import logging
import time
import os
import datetime as dt
import shutil

def moveFile(fromFile, toDir, dir):  # Move FROM:fromFile, TO: toDir
    print('Start MOVE FILE')
    if os.path.isdir(fromFile):
        clearDir = fromFile[len(dir):]
        try:
            os.makedirs(toDir + clearDir)
            print('NewFolder: '+ fromFile + ' ===> '+(toDir + fromFile[len(dir):]))
        except:
            print('NewFolder-PASS:'+ fromFile)
            return
    else:
        clearDir = os.path.dirname(fromFile)[len(dir):]
        if not os.path.isdir(toDir + clearDir):
            os.makedirs(toDir + clearDir)
        try:
            time.sleep(0.2)
            shutil.move(fromFile, toDir + fromFile[len(dir):])
            print('MoveFile: '+ fromFile + ' ===> '+(toDir + fromFile[len(dir):]))
        except Exception as e: 
            print(e)
            print('MoveFile-PASS:'+ fromFile)
            print(toDir + fromFile[len(dir):])
            return

    return
    
def pre_filter_day_backup(mins,in_dir,movepath):
    now = dt.datetime.now()
    ago = now-dt.timedelta(minutes=mins)
    for root, dirs,files in os.walk(in_dir):  
        for fname in files:
            path = os.path.join(root, fname)
            st = os.stat(path)    
            mtime = dt.datetime.fromtimestamp(st.st_mtime)
            if ago > mtime:
                print('%s modified %s'%(path, mtime))
                moveFile(path, movepath,in_dir)
