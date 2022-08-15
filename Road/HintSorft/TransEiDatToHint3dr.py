#coding=utf-8
# 1 从dat文件中获取逐桩横断面三维数据get3DdataFromDatfile(path)
    # 1.1 用正则将每个横断面dat数据放入list res中
# 2 将逐桩横断面三维数据转为纬地3dr格式数据trans3DdataTo3drFile(get3DdataFromDatfile)
    # 2.1 用正则将每个横断面的dat数据中桩号、三维坐标放入list 中（key，HdmPoints_xyz）
    # 2.2 将list中的横断面三维数据转为3dr格式数据
    # 2.3 将list中的横断面三维数据转为tf格式数据
        #2.3.1 先转非填、挖面积、中桩填挖类数据
            #2.3.1.1 先将路基左侧数据存入list中
            #2.3.1.2 先将路基右侧数据存入list中
        #2.3.2 再将Ei are 中填挖面积、中桩填挖导入hint tf文件中
            # 2.3.2.1 先将Ei are 中填挖面积、中桩填挖数据存入list中
            # 2.3.2.2 将list数据存入tf文件
#注意事项
#使用说明：直接调用getfilepath('dat')函数，例resu=getfilepath('Dat'),即历所选文件夹内所有dat（e.dat）类型文件，指定文件夹内需包含e.are,e.dmx文件(dat,are,dmx文件名必须相同否则找不到对应文件)，
# 2.3-pro 已考虑TF中正负号的问题
# 暂不支持dat are dmx 中桩号有断链情况
'''
    1		        整幅路基
    1	中央分隔带	整幅路基
    1		        整幅路基
    1	路缘带	    整幅路基
    2	行车道	    整幅路基	桥梁
    3		        整幅路基	桥梁
    4	硬路肩       整幅路基	桥梁
    5	土路肩	    整幅路基	桥梁
    6	填方边坡	    整幅路基
    7	边沟\排水沟	整幅路基
    8	挖方边坡	    整幅路基
'''
import re
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import sys
import road as road
import roadglobal as roadglobal


def get3DdataFromDatfile(path): # 1 从dat文件中获取逐桩横断面三维数据
    DatFile=''
    with open(path, "r") as FData:
        DatFile = FData.read()
    regx = r'^\d+\.\d+[\r\n]+(?:(?:(?:\d+\.\d+ ?\d*){3}|\d+)[\r\n]+)+'
    res = re.findall(regx, DatFile, re.MULTILINE)   #1 用正则将每个横断面dat数据放入list res中
    FData.close()
    return res


def trans3DdataTo3drFile(get3DdataFromDatfile,path_3drsaved):   # 2 将逐桩横断面三维数据转为纬地3dr格式数据
    # 2.1 用正则将每个横断面的dat数据中桩号、三维坐标放入list 中（key，HdmPoints_xyz）
    for res in get3DdataFromDatfile:
        regx=r'^(\d+\.\d+)[\n\r]'
        key = re.findall(regx,res,re.MULTILINE) #桩号
        #<以下功能过滤Tflist中桩号 不在dmxfile中数据>
        pathregx = r'(.+\\?\/?\S+\.)\w+$'
        path_list = re.findall(pathregx, path_3drsaved, re.MULTILINE)
        path_dmx = path_list[0] + 'dmx'
        path_errfile = path_list[0] + 'err.txt'
        whetherExitKeyInDmxfile = whetherContainTheKeyInDmxfile(key=key[0], path_Dmxfile=path_dmx)
        if len(whetherExitKeyInDmxfile) == 0:
            errfile = open(path_errfile, 'a')
            errfile.write(f'{path_dmx}中未找到桩号：{key[0]}，3dr文件中不显示该桩号数据\n')
            errfile.close()
        else:
        #</>
            file_3dr = open(path_3drsaved, 'a')
            file_3dr.write(key[0] + '\n')
            regx = r'((?:\d+\.\d+ ?){3})[\n\r]'
            key_design_xyz = re.findall(regx, res, re.MULTILINE)  #中桩三维坐标
            key_design_xyz = key_design_xyz[0].split( )
            key_design_xyz = list(map(float, key_design_xyz))
            regx = r'^(\d+)[\n\r]'
            TollNum_HdmPoints = re.findall(regx, res, re.MULTILINE)
            regx = r'(?:(?:\d+\.\d+ ){3}\d[\n\r]?)+'
            HdmPoints_xyz=re.findall(regx, res, re.MULTILINE)   #左右侧横断面三维坐标
            # 2.2 将list中的横断面三维数据转为3dr格式数据
                #1 左右侧
                #2 切成每个点
                #3 切成每个点的坐标
            for j in range(0,2):
                file_3dr.write(TollNum_HdmPoints[j]+'\t')
                regx = r'((?:\d+\.\d+ ){3}\d)[\n\r]?'
                if float(TollNum_HdmPoints[j]) == 0:  # 解决左侧或右侧没有横断面坐标的情况
                    HdmPoint_xyz = ''
                else:
                    try:
                        HdmPoint_xyz = re.findall(regx, HdmPoints_xyz[j], re.MULTILINE)  # 左右侧横断面三维坐标
                    except IndexError:
                        HdmPoint_xyz = re.findall(regx, HdmPoints_xyz[0], re.MULTILINE)  # 左右侧横断面三维坐标
                # HdmPoint_xyz = re.findall(regx, HdmPoints_xyz[j], re.MULTILINE)  # 左右侧横断面三维坐标
                for Hdmlist in HdmPoint_xyz:
                    Hdmlist=Hdmlist.split( )
                    Hdmlist=list(map(float,Hdmlist))
                    dist_3dr=((Hdmlist[0]-key_design_xyz[0])**2+(Hdmlist[1]-key_design_xyz[1])**2)**0.5
                    dist_3dr = round(dist_3dr, 3)
                    if j ==0:
                        dist_3dr = -dist_3dr
                    file_3dr.write(str(dist_3dr) + '\t'+str(Hdmlist[2])+'\t')
                file_3dr.write('\n')
            file_3dr.write('\n')
            file_3dr.close()


def TransEiDatToHintTf(get3DdataFromDatfile, path_tfsaved, path_EiAre):
    # 2.1 用正则将每个横断面的dat数据中桩号、三维坐标放入list 中（key，HdmPoints_xyz）
    for res in get3DdataFromDatfile:
        regx=r'^(\d+\.\d+)[\n\r]'
        key = re.findall(regx,res,re.MULTILINE)  # 桩号
        file_3dr = open(path_tfsaved, 'a')
        # file_3dr.write(key[0] + ' ')
        regx=r'((?:\d+\.\d+ ?){3})[\n\r]'
        key_design_xyz = re.findall(regx,res,re.MULTILINE)  # 中桩三维坐标
        key_design_xyz=key_design_xyz[0].split( )
        key_design_xyz=list(map(float,key_design_xyz))
        regx = r'^(\d+)[\n\r]'
        TollNum_HdmPoints=re.findall(regx, res, re.MULTILINE)
        regx = r'(?:(?:\d+\.\d+ ){3}\d[\n\r]?)+'
        HdmPoints_xyz=re.findall(regx, res, re.MULTILINE)   # 左右侧横断面三维坐标
        # 2.3 将list中的横断面三维数据转为tf格式数据
            #2.3-pro 暂时不考虑TF中正负号的问题
            #2.3.1 先转非填、挖面积、中桩填挖类数据
                #2.3.1.1 先将路基左侧数据存入list中
                #2.3.1.2 先将路基右侧数据存入list中
            #2.3.2 再将Ei are 中填挖面积、中桩填挖导入hint tf文件中
                # 2.3.2.1 先将Ei are 中填挖面积、中桩填挖数据存入list中
                # 2.3.2.2 将list数据存入tf文件
        Tflist=[]
        for temp in range(1,63):
            Tflist.append(0)
        # 2.3.1 先转非填、挖面积、中桩填挖类数据
        Tflist[0] = key[0]
        for j in range(0, 2):
            regx = r'((?:\d+\.\d+ ){3}\d)[\n\r]?'
            if float(TollNum_HdmPoints[j]) == 0:  # 解决左侧或右侧没有横断面坐标的情况
                HdmPoint_xyz = ''
            else:
                try:
                    HdmPoint_xyz = re.findall(regx, HdmPoints_xyz[j], re.MULTILINE)  # 左右侧横断面三维坐标
                except IndexError:
                    HdmPoint_xyz = re.findall(regx, HdmPoints_xyz[0], re.MULTILINE)  # 左右侧横断面三维坐标
            # HdmPoint_xyz = re.findall(regx, HdmPoints_xyz[j], re.MULTILINE)  # 左右侧横断面三维坐标
            UpSlopeStatus = 0
            list_dist_3dr = []
            list_high = []
            Hdmlist_last = []
            for Hdmlist in HdmPoint_xyz:
                Hdmlist = Hdmlist.split( )
                Hdmlist=list(map(float, Hdmlist))
                dist_3dr=((Hdmlist[0]-key_design_xyz[0])**2+(Hdmlist[1]-key_design_xyz[1])**2)**0.5 #平距
                dist_3dr = round(dist_3dr, 3)
                # 判断当前Hdmlist在横断面中处于哪个部位#2.3.1.1 先将路基左/右侧数据存入list中
                try:
                    Hdmlist_last[0]
                except IndexError:
                    Hdmlist_last = Hdmlist[:]
                if Hdmlist[-1]==1:  #中央分隔带
                    pass
                elif Hdmlist[-1]==2:    #行车道
                    pass
                elif Hdmlist[-1]==3:    #
                    pass
                elif Hdmlist[-1]==4:    #
                    pass
                elif Hdmlist[-1]==5:    #土路肩
                    Tflist[4+j] =round(dist_3dr,3)   #路基宽度
                    Tflist[6+j] = round(Hdmlist[2],2)    #路基高程
                    Tflist[8 + j] = round(dist_3dr,3)  # 坡脚距
                    Tflist[10 + j] = round(Hdmlist[2],3)
                elif Hdmlist[-1]==6:    #填方边坡
                    Tflist[8+j] =round(dist_3dr,3)   #坡脚距
                    Tflist[10+j] = round(Hdmlist[2],3)
                elif Hdmlist[-1]==7:    #边沟\排水沟
                    try:    # 识别填方护坡道
                        dist_AdjacentPoints = ((Hdmlist_last[0]-Hdmlist_last_last[0])**2+(Hdmlist_last[1]-Hdmlist_last_last[1])**2)**0.5  # 相邻两点间距离
                        high_AdjacentPoints = abs(Hdmlist_last[2]-Hdmlist_last_last[2])  # 相邻两点间高差
                        slope_AdjacentPoints = dist_AdjacentPoints/high_AdjacentPoints
                    except IndexError:
                        pass
                    except ZeroDivisionError:
                        if Hdmlist_last[3] == 6:
                            Tflist[14+j] = round(dist_AdjacentPoints, 3)
                            Tflist[8 + j] = round(Tflist[8 + j]-dist_AdjacentPoints, 3)  # 坡脚距
                    else:
                        if slope_AdjacentPoints >= 24 and Hdmlist_last[3] == 6:  # 最后一级边坡坡度缓于1:24判断为填方护坡道
                            Tflist[14+j] = round(dist_AdjacentPoints, 3)
                            Tflist[8 + j] = round(Tflist[8 + j] - dist_AdjacentPoints, 3)  # 坡脚距
                            Tflist[10 + j] = round(Hdmlist_last_last[2], 3)
                    Tflist[12+j] = round(dist_3dr, 3)  # 沟缘距
                    list_dist_3dr.append(dist_3dr)
                    list_dist_3dr.sort()
                    min_dist_3dr=list_dist_3dr[0]
                    max_dist_3dr=list_dist_3dr[-1]
                    Tflist[18+j]=round((min_dist_3dr+max_dist_3dr)/2,3) #沟心距
                    list_high.append(Hdmlist[2])
                    list_high.sort()
                    min_high=list_high[0]
                    max_high=list_high[-1]
                    Tflist[16 + j] =round(min_high,3)
                    Tflist[20+j]=round(max_high-min_high,3)  #沟深
                elif Hdmlist[-1]==8:    #挖方边坡
                    try:    #识别挖方碎落台
                        dist_AdjacentPoints=round(((Hdmlist[0]-Hdmlist_last[0])**2+(Hdmlist[1]-Hdmlist_last[1])**2)**0.5,3) #相邻两点间距离
                        high_AdjacentPoints=abs(Hdmlist[2]-Hdmlist_last[2]) #相邻两点间高差
                        slope_AdjacentPoints=dist_AdjacentPoints/high_AdjacentPoints
                    except ZeroDivisionError:
                        Tflist[14+j]=dist_AdjacentPoints
                    except IndexError:
                        print(1)
                    else:
                        if slope_AdjacentPoints>=24 and UpSlopeStatus==0: #第一级边坡坡度缓于1:24判断为碎落台
                            Tflist[14+j]=dist_AdjacentPoints
                    UpSlopeStatus=UpSlopeStatus+1
                    Tflist[8+j] =-round(dist_3dr,3) #坡脚距
                    Tflist[10+j] = round(Hdmlist[2],3)
                    #<>挖方边坡对应的路基宽度、沟缘距、护坡道均、沟心距、沟深都为负值
                    Tflist[4 + j] = -abs(Tflist[4 + j])
                    Tflist[12 + j]=-abs(Tflist[12+j])
                    Tflist[14 + j] = -abs(Tflist[14 + j])
                    Tflist[18 + j] = -abs(Tflist[18 + j])
                    Tflist[20 + j] = -abs(Tflist[20 + j])
                    #</>
                elif Hdmlist[-1]==9:    #
                    pass
                Hdmlist_last_last=Hdmlist_last[:]
                Hdmlist_last=Hdmlist[:]
                # dist_3dr = round(dist_3dr, 3)
                # if j ==0:
                #     dist_3dr=-dist_3dr
        # 2.3.2 再将Ei are 中填挖面积、中桩填挖导入hint tf文件中
        # 2.3.2.1 先将Ei are 中填挖面积、中桩填挖数据存入list中
        # 2.3.2.2 将list数据存入tf文件
        EiAreData=getHdmAreFromEIarefile(key[0],path_EiAre)
        if EiAreData is not None:
            EiAreData=EiAreData[0].split( )
            EiAreData=list(EiAreData)
            Tflist[1]=round(float(EiAreData[4]),0)
            Tflist[2]=round(float(EiAreData[3]),2)
            Tflist[3]=round(float(EiAreData[2]),0)
        #<以下功能过滤Tflist中桩号 不在dmxfile中数据>
        pathregx = r'(.+\\?\/?\S+\.)\w+$'
        path_list = re.findall(pathregx, path_tfsaved, re.MULTILINE)
        path_dmx = path_list[0] + 'dmx'
        path_errfile =path_list[0] + 'err.txt'
        whetherExitKeyInDmxfile = whetherContainTheKeyInDmxfile(key=key[0], path_Dmxfile=path_dmx)
        if len(whetherExitKeyInDmxfile) == 0:
            errfile = open(path_errfile, 'a')
            errfile.write(f'{path_dmx}中未找到桩号：{key[0]}，tf文件中不显示该桩号数据\n')
            errfile.close()
        else:
            file_3dr.write(str(Tflist).replace(',','\t').replace('[','').replace(']','').replace('\'',''))
            file_3dr.write('\n')
        #</>
        file_3dr.close()
def getHdmAreFromEIarefile(key,EiarefilePath):
    # 功能通过已知桩号key，查找EiarefilePath中桩号key对应行的数据
    try:
        key='{:.1f}'.format(int(float(key)*10)/10)
    except:
        print(key)
        print(type(key))
    else:
        pass
    pathregx=r'(.+\\?\/?\S+\.)\w+$'
    path_errfile=re.findall(pathregx,EiarefilePath, re.MULTILINE)
    path_errfile=path_errfile[0]+'err.txt'
    file_are = open(EiarefilePath, 'r')
    DataOfEiare = file_are.read()
    regx =f'^{key}\d*\\t.+(?=\\n)'
    res = re.findall(regx, DataOfEiare, re.MULTILINE)  # 1 用正则将每个横断面dat数据放入list res中
    if len(res) ==0:
        errfile=open(path_errfile,'a')
        errfile.write(f'{EiarefilePath}中未找到桩号：{key}\n')
        errfile.close()
    else:
        return res
    file_are.close()
def initFunction(path_EiDat):
    path=path_EiDat
    data_dat=get3DdataFromDatfile(path)
    pathregx = r'(.+\\?\/?\S+\.)\w+$'
    path_list = re.findall(pathregx,path, re.MULTILINE)
    path_3drsaved =path_list[0]+'3dr'
    path_tfsaved = path_list[0]+'tf'
    path_Eiare =path_list[0]+'are'
    if os.path.isfile(path_Eiare) is False:
        rootb = tk.Tk()
        # 创建一个文本Label对象
        textLabel = Label(rootb,  # 将内容绑定在  root 初始框上面
                          text=f"{path_Eiare}文件不存在",
                          justify=LEFT,  # 用于 指明文本的 位置
                          padx=10)  # 限制 文本的 位置 , padx 是 x轴的意思 .
        textLabel.pack(side=LEFT)  # 致命 textlabel 在初识框 中的位置
        mainloop()
        sys.exit()
    # path_Eiare = "C:\\Users\\Administrator.DESKTOP-95R7ULF\\Desktop\\E.are"
    try:
        tempfile=open(path_3drsaved,'a')
        tempfile.truncate(0)
        tempfile.write('HINTCAD5.83_HDM_SHUJU'+'\n')
        tempfile.close()
        tempfile=open(path_tfsaved,'a')
        tempfile.truncate(0)
        tempfile.write('HINTCAD6.00_TF_SHUJU'+'\n')
        tempfile.write('//[	桩	号	]	[挖方面积]	[填方面积]	[中桩填挖]	[路基左宽]	[路基右宽]	[基缘左高]	[基缘右高]	[左坡脚距]	[右坡脚距]	[左坡脚高]	[右坡脚高]	[左沟缘距]	[右沟缘距][左护坡道宽][右护坡道宽][左沟底高][右沟底高]	[左沟心距]	[右沟心距]	[左沟深度]	[右沟深度]	[左用地宽]	[右用地宽]	[清表面积]	[顶超面积]	[左超面积]	[右超面积]	[计排水沟][左沟面积填][左沟面积挖][右沟面积填][右沟面积挖][路槽面积填][路槽面积挖][清表宽度][清表厚度][挖1类面积][挖2类面积][挖3类面积][挖4类面积][挖5类面积][挖6类面积][左路槽B]	[右路槽B]	[左路槽C]	[右路槽C]	[左垫层]	[右垫层]	[左路床]	[右路床][左土肩培土][右土肩培土][左包边土]	[右包边土][左边沟回填][右边沟回填][左截沟填][左截沟挖][右截沟填][右截沟挖][挖台阶面积][填1类面积][填2类面积][填3类面积][填4类面积][填5类面积][填6类面积][弃1类面积][弃2类面积][弃3类面积][弃4类面积][弃5类面积][弃6类面积]' + '\n')
        tempfile.close()
    except FileNotFoundError:
        print("打开文件错误")
    else:
        pass
    result1=trans3DdataTo3drFile(data_dat,path_3drsaved)
    result2 = TransEiDatToHintTf(data_dat, path_tfsaved,path_Eiare)
    print('运行结束')
def getfilepath(filetype):
    #打开文件夹对话框，获得该文件夹下指定类型文件的绝对路径,例：filetype=exe
    filetype = filetype.lower()
    root = tk.Tk()
    root.withdraw()
    Folderpath = filedialog.askdirectory(title="选择EI dat are dmx 所在文件夹")  # 获得选择好的文件夹
    # Filepath = filedialog.askopenfilename()  # 获得选择好的文件
    rootdir = os.path.join(Folderpath)
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() =='.'+filetype:
                temp = Folderpath + '/' + filename
                res = initFunction(temp)
    '''打开选择文件夹对话框'''
def whetherContainTheKeyInDmxfile_prevesion(key, path_Dmxfile): #上一版
    #判断桩号key是否在文件path_Dmxfile中
    key = '{:.1f}'.format(int(float(key) * 10) / 10)
    try:
        dmxfile = open(path_Dmxfile,'r')
        data_dmx = dmxfile.read()
    except:
        rootb = tk.Tk()
        # 创建一个文本Label对象
        textLabel = Label(rootb,  # 将内容绑定在  root 初始框上面
                          text=f"{path_Dmxfile}文件不存在",
                          justify=LEFT,  # 用于 指明文本的 位置
                          padx=10)  # 限制 文本的 位置 , padx 是 x轴的意思 .
        textLabel.pack(side=LEFT)  # 致命 textlabel 在初识框 中的位置
        mainloop()
        sys.exit()
    else:
        # f'^{key}\d*\\t.+(?=\\n)'
        key = key.replace('.', '\.')
        regex = f'(?<!\d){key}\\d*[\t| ]'
        data_dmx = re.findall(regex, data_dmx, re.MULTILINE)
        dmxfile.close()
        return data_dmx
def whetherContainTheKeyInDmxfile(key, path_Dmxfile):
    #判断桩号key是否在文件path_Dmxfile中
    key_list = road.cutInvalidWords_chainage(key)
    key = ''.join(key_list)
    print(f'whetherContainTheKeyInDmxfile key:{key}')
    try:
        dmxfile = open(path_Dmxfile,'r')
        data_dmx = dmxfile.read()
    except:
        rootb = tk.Tk()
        # 创建一个文本Label对象
        textLabel = Label(rootb,  # 将内容绑定在  root 初始框上面
                          text=f"{path_Dmxfile}文件不存在",
                          justify=LEFT,  # 用于 指明文本的 位置
                          padx=10)  # 限制 文本的 位置 , padx 是 x轴的意思 .
        textLabel.pack(side=LEFT)  # 致命 textlabel 在初识框 中的位置
        mainloop()
        sys.exit()
    else:
        key = key.replace('.', '\.')
        regx = roadglobal.regx_is_key_in_dmx(key)
        # if key.find('.') == -1:  # 判断是整桩号还是含小数桩号
        #     regx = f'^(?<!\w)({key}(?:\.0+)?)(?!\w)'  # 将tf中桩号chainage信息提取
        # else:
        #     regx = f'^(?<!\w)({key}0*)(?!\w)'
        data_dmx = re.findall(regx, data_dmx, re.MULTILINE)
        print(f'regx:{regx}')
        print(f'data_dmx:{data_dmx}')
        dmxfile.close()
        return data_dmx
if __name__ == "__main__":
    resu = getfilepath('Dat')
    rootb = tk.Tk()
    # 创建一个文本Label对象
    rootb.geometry('200x80+200+200')
    # textLabel = Label(rootb,  # 将内容绑定在  root 初始框上面
    #                   text="3dr,tf数据已生成",
    #                   justify=LEFT,  # 用于 指明文本的 位置
    #                   padx=10)  # 限制 文本的 位置 , padx 是 x轴的意思 .
    # textLabel.pack(side=LEFT)  # 致命 textlabel 在初识框 中的位置
    rootb.confirmbutton = Button(rootb, text='运行结束', width=10, command=rootb.quit)
    rootb.confirmbutton.grid(row=1, column=1)
    mainloop()


