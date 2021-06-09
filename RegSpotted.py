from datetime import datetime


def CameraReg(name):
    with open('Spotted.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%D %H:%M:%S')#%H:%M:%S'
            f.writelines(f'\n{name},{dtString}')
