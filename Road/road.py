#road 常用函数
from tkinter import *
import tkinter as tk
import os
import pymysql
import road
def insertDataToTableDrainageDitchFrom3dr(pathOf3dr,chainage,prjname):
    #功能：将3dr中桩号为chainage边沟/排水沟信息插入到DrainageDitch表中
    # road.getCrossSectionOf3dr得到3dr中桩号chainagea横断面数据
    # findDrainageDitchFromLine找出边沟/排水沟信息
    # 将边沟/排水沟信息存到数据库prjname表drainageditch中
    threedrpath=pathOf3dr
    conn = pymysql.connect(user="root", passwd="sunday")  # ,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cross_sections=road.getCrossSectionOf3dr(threedrpath,chainage)
    for data in cross_sections:
        cross_section=re.split(r'\n',data)
        i=0
        for temp in cross_section:
            temp=temp.strip()
            if len(temp)>0:
                cross_section[i]=temp
                i=i+1
        for i_LOrR in [1,2]:
            drainage=road.findDrainageDitchFromLine(cross_section[i_LOrR])
            # print(i_LOrR,cross_section[0])
            # print(drainage)
            if drainage!=False:
                sql="insert into drainageditch(chainage,左右侧,3dr中起始位置,线段个数) values(%s,%s,%s,%s)"
                insert = cursor.execute(sql, (cross_section[0], i_LOrR, int(drainage[0]), int(drainage[1])))
                for i_drainage in range(int(drainage[1])):
                    sql = f'update drainageditch set 宽度{i_drainage}={float(drainage[i_drainage*3 + 2])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
                    update_drain = cursor.execute(sql)
                    sql = f'update drainageditch set 高度{i_drainage}={float(drainage[i_drainage*3 + 3])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
                    update_drain = cursor.execute(sql)
                    sql = f'update drainageditch set 坡度{i_drainage}={float(drainage[i_drainage*3 + 4])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
                    update_drain=cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    print("边沟/排水沟信息已存入drainageditch表")
def findDrainageDitchFromLine(linedata,drainageFilters='default'):
    #功能：根据给定的边沟/排水沟判定条件drainageFilters，从一条线linedata中找出边沟/排水沟，返回res=[6,3],表示linedata中第6段线开始为边沟/排水沟，边沟/排水沟由3条线段组成。
    #(linedata格式要像3dr左侧或右侧横断面格式，组数、平距、高差.....）
    #边沟/排水沟判定条件drainageFilters，格式应按程序默认值格式，width height gradient 为关键字，只接受小写；默认边沟/排水沟由3条线组成，每条线由width height gradient来判定
        #1.判定条件Filte
        #2.排除条件（目前未添加此功能）

    if drainageFilters=='default':
        drainageFilter1 = ['0<=width', 'height<0', '-1.5<=gradient<=0'] #第1条边判定条件
        drainageFilter2 = ['0<width', 'height<0.5', '5<abs(gradient)<=9999']    #第2条边判定条件
        drainageFilter3 = ['0<=width', '0<height', '0<=gradient<=1.5']  #第3条边判定条件
        Filter=[drainageFilter1,drainageFilter2,drainageFilter3]

    regx=r'-?\d*\.?\d+'
    pointsOfLinedata=re.findall(regx,linedata)
    # print(pointsOfLinedata)
    m=0
    i = 0
    res = []
    wlist={}
    hlist={}
    glist={}
    try:
        while i <float(pointsOfLinedata[0])-1:
            if abs(float(pointsOfLinedata[(i+2)*2-1]))-abs(float(pointsOfLinedata[(i+2-1)*2-1]))<0:
                print("挡墙")
                return False    #大概率是挡墙
            widthOfPoint=float(pointsOfLinedata[(i+2)*2-1])-float(pointsOfLinedata[(i+2-1)*2-1])
            widthOfPoint=abs(float('{:.3f}'.format(widthOfPoint)))
            heightOfPoint = float(pointsOfLinedata[(i + 2) * 2])-float(pointsOfLinedata[(i + 2-1) * 2])
            heightOfPoint=float('{:.3f}'.format(heightOfPoint))
            try:
                gradientOfPint=widthOfPoint/heightOfPoint
                gradientOfPint= float('{:.3f}'.format(gradientOfPint))
            except ZeroDivisionError:
                gradientOfPint=9999
            # print(widthOfPoint,heightOfPoint,gradientOfPint)
            wlist[i]=widthOfPoint
            hlist[i]=heightOfPoint
            glist[i]=gradientOfPint
            [width, height, gradient] = [widthOfPoint, heightOfPoint, gradientOfPint]
            if eval(Filter[m][0]):
                i_last=i
                if eval(Filter[m][1]):
                    if eval(Filter[m][2]):
                        m=m+1
                        if m == len(Filter):    #判定为边沟/排水沟条件
                            res.append(i-len(Filter)+1)
                            res.append(len(Filter))
                            j=res[0]
                            while j<=i:
                                res.append(wlist[j])
                                res.append(hlist[j])
                                res.append(glist[j])
                                # res.append(float(pointsOfLinedata[(j+2)*2-1]))
                                # res.append(float(pointsOfLinedata[(j + 2) * 2]))
                                j=j+1
                            m = 0
                    else:
                        if m != 0:
                            i = i_last - 1
                            m = 0
                else:
                    if m!=0:
                        i = i_last - 1
                        m=0
            else:
                m=0
            i=i+1
        if len(res)!=0:
            return res
        else:
            return False
    except:
        return False
def getCrossSectionOf3dr(pathof3dr,chainage='all'):
    #查找pathof3dr中给定桩号的横断面信息cross_section，桩号缺省时查找全部桩号
    prjpath=pathof3dr
    chainage=chainage.strip()
    if os.path.exists(prjpath):
        if chainage.lower()=='all':
            regx=r'^[\t\f ]*[a-zA-Z]?(?:\d+|\d+\.\d+)[\t\f ]*[\n](?:.+[\n\r])+'   #提取3dr中横断面信息
        elif len(chainage)==0:
            pass
        else:
            temp=road.cutInvalidWords_chainage(chainage)
            try:
                chainage=temp[0]+temp[1]
            except:
                pass
            if chainage.find('.')==-1:
                regx = f'^[\t\f ]*[a-zA-Z]?(?:{chainage}(?:\.0+)?)[\t\f ]*[\n](?:.+[\n\r])+'
            else:
                regx =f'^[\t\f ]*[a-zA-Z]?(?:{chainage}0*)[\t\f ]*[\n](?:.+[\n\r])+'
        if len(chainage)==0:
            return ''
        else:
            file=open(prjpath,'r')
            data_file=file.read().upper()
            cross_sections=re.findall(regx,data_file,re.MULTILINE)
            file.close()
            return cross_sections
    else:
        temp=road.gui_filenotfine(prjpath)
def setupChainageTable(prjname,prjpath):
    #功能：建立chainage表
    #步骤：
        # 1 查找纬地项目文件prj中3dr文件路径
        # 2 提取3dr文件中桩号
        # 3 将3dr中的桩号，存入数据表chainage中
    path=prjpath
    prjname=prjname

    # 1 查找纬地项目文件prj中3dr文件路径
    path=road.findXPathFromPrj(path,'3dr')

    # 2 提取3dr文件中桩号
    try:
        file=open(path,'r')
    except:
        msgbox=road.gui_filenotfine(path)
    else:
        filedata = file.read()
        regx = r'^\s*(\w{0,1}\d+\.\d+|\w{0,1}\d+)\s*\n' #提取3dr中桩号的正则表达式
        keyslist = re.findall(regx, filedata, re.MULTILINE)
        file.close()
    # res=TransEiDatToHint3dr.whetherContainTheKeyInDmxfile(34676.4,path)
    # print(res)
        temp=road.creatMysqlChainageTable(prjname)
        conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
        cursor = conn.cursor()
        conn.select_db(prjname)
        sql='insert into chainage values(%s,%s,%s,%s)'
        i=1
        # 3 装3dr中的桩号，存入数据表key中
        for key in keyslist:
            insert = cursor.execute(sql,(i,i-1,key,0))
            i=i+1
        cursor.close()
        conn.commit()
        conn.close()
        print('chainage数据导入成功')
def creatMysqlChainageTable(databaseName):
    #在databaseName数据库中新建chainage表
    prjname=databaseName
    conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
    cursor = conn.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {prjname} DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')
    conn.select_db(prjname)
    cursor.execute('drop table if exists chainage')
    sql = """CREATE TABLE IF NOT EXISTS `chainage` (
          `id` int(6) NOT NULL AUTO_INCREMENT,
          `id_last` int(6) ,
          `chainage` varchar(50) NOT NULL,
          `chainage_noBreakChain` int(50) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
def creatMysqlDrainageDitchTable(databaseName):
    #在databaseName数据库中新建drainageDitch表
    # chainage    左右侧 3dr中起始位置     线段个数   宽度1    高度1  坡度1  宽度2    高度2  坡度2...
    prjname=databaseName
    conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cursor.execute('drop table if exists drainageDitch')
    sql = """CREATE TABLE IF NOT EXISTS `drainageDitch` (
          `id` int(6) NOT NULL AUTO_INCREMENT,
          `chainage` varchar(50),
          `左右侧` int(1) NOT NULL ,
          `3dr中起始位置` int(3) ,
          `线段个数` int(3),
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    for i in range(9):
        temp='宽度'+str(i)
        sql=f'alter table drainageDitch add {temp} float(10)'
        cursor.execute(sql)
        temp='高度'+str(i)
        sql=f'alter table drainageDitch add {temp} float(10)'
        cursor.execute(sql)
        temp='坡度'+str(i)
        sql=f'alter table drainageDitch add {temp} float(10)'
        cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
def findXPathFromPrj(prjpath,typeOfFindX):
    #查找纬地项目文件prjpath中X文件路径，例FindXPathFromPrj(prjpath,3dr)
    path_Dmxfile=prjpath
    typeOfFindX=typeOfFindX.lower()
    try:
        prjfile=open(path_Dmxfile,'r')
    except:#except FileNotFoundError:
        msgbox = gui_filenotfine(path_Dmxfile)
        sys.exit()
    else:
        data_prj=prjfile.read()
        prjfile.close()
        data_prj=data_prj.lower()
        regx = f'\*\.{typeOfFindX}\).*=\s*(\S*)\s*(?=\n)'
        res = re.findall(regx, data_prj, re.MULTILINE)
        if len(res[0])>0:
            if os.path.exists(res[0]):
                return res[0]
            else:
                regx=r'\w+\.\w+'
                temp=re.findall(regx,res[0],re.MULTILINE)
                regx=r'(.+\\)\w+\.\w+$'
                temppath=re.findall(regx,path_Dmxfile,re.MULTILINE)
                xpath=temppath[0]+temp[0]
                if os.path.exists(xpath):
                    return xpath
                else:
                    msgbox=gui_filenotfine(xpath)
                    return ""
        else:
            return res[0]
def cutInvalidWords_chainage(chainage):
    #去除桩中无效数字或者字母，如输入A20.010 ，输出res  (res[0]=A,res[1]=20.01)
    res=[]
    chainage=chainage.strip()
    regx=r'(?<!\S)[a-zA-Z]?(\d+(?:\.\d+)?)(?!\S)'
    temp1=re.findall(regx,chainage,re.MULTILINE)
    try:
        temp1[0]='{:g}'.format(float(temp1[0]))
    except:
        return res
    else:
        regx = r'(?<!\S)([a-zA-Z]?)\d+(?:\.\d+)?(?!\S)'
        temp2 = re.findall(regx, chainage, re.MULTILINE)
        res.append(temp2[0].upper())
        res.append(temp1[0])
        return res
def gui_filenotfine(path):
    # 功能：path文件不存在提示框
    rootb = tk.Tk()
    # 创建一个文本Label对象
    textLabel = Label(rootb,  # 将内容绑定在  root 初始框上面
                      text=f"{path}文件不存在",
                      justify=LEFT,  # 用于 指明文本的 位置
                      padx=10)  # 限制 文本的 位置 , padx 是 x轴的意思 .
    textLabel.pack(side=LEFT)  # 致命 textlabel 在初识框 中的位置
    mainloop()
