from tkinter import *

def getTheExitAndEntranceOfTunnelNearbyChainage(filepath, len, respath):
    '''
    功能：根据filepath内桩号，得到（filepath-len，filepath+len）内桩号，放入respath中
    :param filepath:
    :param len:
    :param respath:
    :return:
    '''
    file = open(filepath, 'r')
    filedata = file.read()
    regx = r'.+(?=[\n|\r])'
    filedata_list = re.findall(regx, filedata, re.MULTILINE)
    # print(filedata_list[0])
    file_save = open(respath, 'a')
    regx = r'\w+'
    for filedata_line in filedata_list:
        chainage = re.findall(regx, filedata_line, re.MULTILINE)
        chainage_start = int(chainage[0])
        chainage_end = int(chainage[1])
        if chainage_end >= chainage_start:
            chainage_res = list(range(chainage_start-50, chainage_start+50))
            file_save.write('\n')
            file_save.write(str(chainage_res).replace(',', '\n').replace('[', '').replace(']', ''))
            chainage_res = list(range(chainage_end-50, chainage_end+50))
            file_save.write('\n')
            file_save.write(str(chainage_res).replace(',', '\n').replace('[', '').replace(']', ''))
            # for resdata in chainage_res:
            #     file_save.write(str(resdata)+'\n')
        else:
            return ''
    file_save.close()
    file.close()

filepath = r'F:\1.txt'
len = 50
respath = r'F:\res.sta'
getTheExitAndEntranceOfTunnelNearbyChainage(filepath, len, respath)