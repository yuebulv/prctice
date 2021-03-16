import pymysql
import road
import mysql
import re
import slope

db='长寿支线'
chainage=' a20.'
def insertDataFrom3drToTableSlope(prjpath,chainage,prjname):
    '''
    功能：将3dr中桩号为chainage边坡信息插入slope表中
    :param prjpath: 项目路径
    :param chainage: 桩号
    :param prjname: 项目名称
    :return:

    '''

    try:
        chainage=road.getChainageFromChainagetable(prjname,chainage,True)[0]    #返回数据表chainage中等值桩号
    except:
        print(f'错误：数据表chainage中无桩号{chainage}')
        return ''

    # 一、得到TF数据
    tfpath = road.findXPathFromPrj(prjpath, 'tf')
    tfDatas = road.getDataFromTf(tfpath, chainage)
    for tfData_temp in tfDatas:
        regx = r'\w+.?\w+'
        tfData = re.findall(regx, tfData_temp, re.MULTILINE)
        print(tfData[0], tfData[4], tfData[5])
    # 二、得到边沟数据
    with mysql.UsingMysql(log_time=False,db=prjname) as um:
        um.cursor.execute(f"select chainage,左右侧,3dr中起始位置  from drainageditch where chainage='{chainage}'")
        data = um.cursor.fetchall()
        for dic in data:
            print(dic['左右侧'],dic['3dr中起始位置'])
        print(data)

    # 三、得到边坡数据
    threedrpath=road.findXPathFromPrj(prjpath, '3dr')
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


            regx=r'-?\d+.?\d+'
            drData_list=re.findall(regx,cross_section[i_LOrR],re.MULTILINE)
            print(drData_list)
            roadShoulderPosition=drData_list.index(tfData[i_LOrR+3]) #默认TF文件中第4、5列为路基左、右宽度
            print(roadShoulderPosition)
            for drainagePosition_dic in data:
                print(drainagePosition_dic['左右侧'])
                if drainagePosition_dic['左右侧']==i_LOrR:
                    drainagePosition=drainagePosition_dic['3dr中起始位置']






            # if drainage!=False:
            #     sql="insert into drainageditch(chainage,左右侧,3dr中起始位置,线段个数) values(%s,%s,%s,%s)"
            #     insert = cursor.execute(sql, (cross_section[0], i_LOrR, int(drainage[0]), int(drainage[1])))
            #     for i_drainage in range(int(drainage[1])):
            #         sql = f'update drainageditch set 宽度{i_drainage}={float(drainage[i_drainage*3 + 2])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
            #         update_drain = cursor.execute(sql)
            #         sql = f'update drainageditch set 高度{i_drainage}={float(drainage[i_drainage*3 + 3])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
            #         update_drain = cursor.execute(sql)
            #         sql = f'update drainageditch set 坡度{i_drainage}={float(drainage[i_drainage*3 + 4])} where chainage ="{cross_section[0]}" and 左右侧={i_LOrR}'
            #         update_drain=cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    print("边坡信息已存入drainageditch表")
def findSlopeFromLine(linedata,i_slopeStart,i_slopeEnd,platformFilters='default',slopeFilters='default'):
    #功能：得到给定边坡范围边坡信息（i_slopeStart和i_slopeEnd表示边坡在linedata中的开始和结束的位置），，返回res=[6,3,宽度i,高度i,坡度i...],表示linedata中第6段线开始为边坡，边坡由3条线段组成,第i段边坡的宽度i,高度i,坡度i。
    #(linedata格式要像3dr左侧或右侧横断面格式，组数、平距、高差.....）
    #边沟/排水沟判定条件drainageFilters，格式应按程序默认值格式，width height gradient 为关键字，只接受小写；默认边沟/排水沟由3条线组成，每条线由width height gradient来判定
        #1.判定条件Filte
        #2.排除条件（目前未添加此功能）

    if platformFilters=='default':
        drainageFilter1 = ['0<width', '10<abs(gradient)<=9999'] #第1条边判定条件
        platformFilter_list=[drainageFilter1]
    if slopeFilters=='default':
        drainageFilter1 = ['abs(height)>0', '0<abs(gradient)<=10'] #第1条边判定条件
        slopeFilter_list=[drainageFilter1]
    regx=r'-?\d*\.?\d+'
    pointsOfLinedata=re.findall(regx,linedata)
    # print(pointsOfLinedata)
    m=0
    i = 0
    res = []
    wlist={}
    hlist={}
    glist={}
    isSlope={}
    isPlatform={}
    slopeLevel=0
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
            if widthOfPoint==0 and widthOfPoint==0:
                continue
            else:
                wlist[i]=widthOfPoint
                hlist[i]=heightOfPoint
                glist[i]=gradientOfPint
                pointData = [widthOfPoint, heightOfPoint, gradientOfPint]

            for m in range(len(slopeFilter_list)):
                for n in range(len(slopeFilter_list[m])):
                    if eval(slopeFilter_list[m][n]):
                        isSlope[i]=True and isSlope[i]
                        print('this is slope')
            for m in range(len(platformFilter_list)):
                for n in range(len(platformFilter_list[m])):
                    if eval(platformFilter_list[m][n]):
                        isPlatform[i] = True and isPlatform[i]
                        print('this is platform')

            '''
                1先标记平台或者边坡，isSlope[i]
                2合并不同同一坡比边坡或平台
                3不同坡比边坡，边坡级数+1；不同坡比平台，级数不变
                4第一个pointdata存放一组边坡和平台数据（缺失部位用0补齐）
                
            '''
        for i in range(i_slopeStart, i_slopeEnd):

            pass
                    #     if isSlope[i-1]==True:
                    #         pointData.append(slopeLevel)
                    #         res.append(pointData)
                    #     else:
                    #         print('The last point is platform too,need join')
                    #
                    #         pass
                    #
                    # res.append(wlist[j])

        if len(res)!=0:
            return res
        else:
            return False
    except:
        return False



# for i in range(2,10):
#     if i ==5:
#         continue
#     print(i)
# a=True
# b=False
# c=True
# d=False
# print('a+b:',a and b)
# print('a+c',c and c)
# print('b+d',b and d)
# temp='1,2,3,4,2,6,7,2,9'
# c=temp.find('9',)
# print(c)
# print('{:g}'.format(2.012310000))
prjpath = r'F:\2020-10-14长寿支线\4-资料\王勇\K -12-16 - 副本\K.prj'
# prjpath = r'D:\Download\QQ文档\297358842\FileRecv\元蔓纬地设计文件\元蔓纬地设计文件\K27改移老路调坡上报\K27+400改移地方道路.prj'
prjname='长寿支线'
# #一、 生成数据表chainage
# road.setupChainageTable(prjname,prjpath)
# road.creatMysqlDrainageDitchTable(prjname)
chainages=['all']
chainage='a0'
insertDataFrom3drToTableSlope(prjpath,chainage,prjname)
