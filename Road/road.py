#road 常用函数
from tkinter import *
import tkinter as tk
import os
import pymysql
import road
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
def FindXPathFromPrj(prjpath,typeOfFindX):
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
        prjfile.close()
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
