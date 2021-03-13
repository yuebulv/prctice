import pymysql
import road
import mysql
import re
import slope

db='长寿支线'
chainage=' a20.'
def insertDataFrom3drToTableSlope(pathOf3dr,chainage,prjname):
    #功能：将3dr中桩号为chainage边坡信息插入slope表中
    # road.getCrossSectionOf3dr得到3dr中桩号chainagea横断面数据
    #
    # 将边沟/排水沟信息存到数据库prjname表slope中
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
def findSlopeFromLine(linedata,i_slopeStart,i_slopeEnd,drainageFilters='default'):
    #功能：得到给定边坡范围边坡信息（i_slopeStart和i_slopeEnd表示边坡在linedata中的开始和结束的位置），，返回res=[6,3,宽度i,高度i,坡度i...],表示linedata中第6段线开始为边坡，边坡由3条线段组成,第i段边坡的宽度i,高度i,坡度i。
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
        for i in range(i_slopeStart,i_slopeEnd):
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

for i in range(2,10):
    print(i)


