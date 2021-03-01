#road 常用函数
from tkinter import *
import tkinter as tk
import os
import pymysql
import road
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
            data_file=file.read()
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
    path=road.FindXPathFromPrj(path,'3dr')

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
            insert = cursor.execute(sql,(i,i-1,key,''))
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
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `id_last` int(11) ,
          `chainage` varchar(255) NOT NULL,
          `chainage_noBreakChain` varchar(255) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
def creatMysqlDrainageDitchTable(databaseName):
    #在databaseName数据库中新建drainageDitch表
    # chainage    左右侧 3dr中起始位置     线段个数   平距  高差     平距  高差...
    prjname=databaseName
    conn = pymysql.connect(user = "root",passwd = "sunday")#,db = "mysql")
    cursor = conn.cursor()
    conn.select_db(prjname)
    cursor.execute('drop table if exists drainageDitch')
    sql = """CREATE TABLE IF NOT EXISTS `drainageDitch` (
          `chainage` varchar(255),
          `左右侧` varchar(255) NOT NULL ,
          `3dr中起始位置` int(11) ,
          `线段个数` int(11) ,
          PRIMARY KEY (`chainage`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
    cursor.execute(sql)
    for i in range(9):
        temp='平距'+str(i)
        sql=f'alter table drainageDitch add {temp}'
        cursor.execute(sql)
        temp='高差'+str(i)
        sql=f'alter table drainageDitch add {temp}'
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
        res.append(temp2[0])
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
