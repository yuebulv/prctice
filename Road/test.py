import TransEiDatToHint3dr
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import os
import road
import pymysql
import math
import mysql
import copy
import glob
import roadglobal
import gui_confirm
from tkinter import filedialog
# import filedialog
class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        qfile_stats = QFile("../ui/main.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)
        self.ui.action_openprj.triggered.connect(self.openPrjFile)
        self.ui.pushButton_quit.clicked.connect(self.quitSoftware)
        # self.ui.button.clicked.connect(self.handleCalc)

    def openPrjFile(self):
        root = tk.Tk()
        root.withdraw()
        folderpath = tkinter.filedialog.askdirectory(title='请选择prj文件所在文件夹')
        os.chdir(folderpath)
        for prjfile in glob.glob('*.prj'):
            prjpath = folderpath + '\\' + prjfile
            if os.path.exists(prjpath) == False:
                msgbox = road.gui_filenotfine(f'{prjpath} path:不在存在')
                continue
            prjpath = prjpath.replace('/', '\\')
            slopefilepath_list = prjpath.split('\\')
            regx = r'(.+)(?=\.\w+)'
            prjname = re.findall(regx, slopefilepath_list[-1])[0]
            prjname = prjname.replace('+', '')

            self.ui.lineEdit_prjname_1.setText(prjname)
            self.ui.lineEdit_prjpath_1.setText(prjpath)
            i = 2
            uiWidget = f"lineEdit_prjname_{i}"
            # self.ui.uiWidget.setText(prjname)
            # self.ui.setAttribute(uiWidget, prjname)
            # setattr(self.ui, uiWidget, prjname)
            # print(self.ui.lineEdit_prjname_2.text)

            obj = self.ui
            print(self.ui.__getattribute__('lineEdit_prjpath_1'))
            print(dir(obj))
            # obj.lineEdit_prjname_3.setText(prjname)
            setattr(obj, 'lineEdit_prjname_2', prjname)
            print(obj)
            print(getattr(obj, 'lineEdit_prjpath_1'))

    def quitSoftware(self):
        sys.exit()

    def handleCalc(self):
        info = self.ui.textEdit.toPlainText()

        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')

            parts = [p for p in parts if p]
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.ui,
                          '统计结果',
                          f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}'''
                          )

def grop_hdms_lines(hdm_data_path, layer_name_zxx='图层中心线', layer_name='图层分离式路基中心线'):
    '''
    1、功能：通过分离式路基线-中心线，筛选出本断面的直线、多段线坐标；
    :param hdm_data_path: 横断面设计线坐标文件路径，格式有限制
    :param layer_name_zxx: 中心图所在图层名
    :param layer_name: 分离式路基中心线所在图层
    :return: res_xyz_lines_chainage_and_err
    [
        [K0+000:{chainage:
                text:
                zxx_xyz:
                left_lines:
                right_lines
                }
        ...
        ],
        err
    ]
    例如：res_xyz_lines_chainage_and_err[0]['bk0+130']['right_lines']可得到BK0+130右侧断面设计线坐标
        res_xyz_lines_chainage_and_err[1]为捕获的错误
    '''
    # 1、通过分离式路基线-中心线，筛选出本断面的直线、多段线坐标；
    res_xyz_lines_chainage_and_err = []  # 去除分离式路基后,左右侧横断面坐标
    err_list = []
    try:
        file = open(hdm_data_path, 'r')
    except:
        msgbox=road.gui_filenotfine(f'{hdm_data_path}文件不存在')
        return ''
    filedata = file.read().lower()
    regx = roadglobal.regx_chainage_between_chainage
    hdms_xyz_list = re.findall(regx, filedata, re.MULTILINE)  # 所有横断面的文件及文字标注
    file.close()
    print(f'len((hdms_xyz_list)):{len((hdms_xyz_list))}')
    res_xyz_lines_chainage = {}  # {chainage:xyz_line_chainage_dic}
    for hdm_xyz_list in hdms_xyz_list:  # 每个断面
        xyz_line_chainage_dic = {}  # {chainage:K0+000,text:'左路基宽 = 3.35 左边距 = 3.35',left_lines:[left_line...],right_lines:[right_line...]}
        left_line = []  # left_line =[[x,y,z],[x,y,z]...]
        right_line = []  # right_line =[[x,y,z],[x,y,z]...]
        regx_x = f'{layer_name}.+x=(\d+\.?\d+)\s*y=(\d+\.?\d+)\s*z=(\d+\.?\d+)'
        separated_x_tuple = re.findall(regx_x, hdm_xyz_list, re.MULTILINE)  # 分离式路基中心线X坐标
        regx_x = f'{layer_name_zxx}.+x=(\d+\.?\d+)\s*y=(\d+\.?\d+)\s*z=(\d+\.?\d+)'
        zxx_x_tuple = re.findall(regx_x, hdm_xyz_list, re.MULTILINE)  # 路基中心线X坐标
        regx_line = roadglobal.regx_exclude_str(layer_name_zxx, layer_name)
        hdm_lines = re.findall(regx_line, hdm_xyz_list, re.MULTILINE)
        if len(zxx_x_tuple) == 0:
            err_txt = f'hdm_separated_road_handle错误：{hdm_lines[0]}无中心线，或者中心线特征字符{layer_name_zxx}不存在,请检查{hdm_data_path}文件。'
            err_list.append(err_txt)
            continue
        else:
            zxx_x = float(zxx_x_tuple[0][0])

        try:
            separated_x = float(separated_x_tuple[0][0])
        except IndexError:
            symbol = '!=-123456789'
        else:

            if separated_x > zxx_x:
                symbol = '<=' + str(separated_x)
            elif separated_x < zxx_x:
                symbol = '>=' + str(separated_x)
            else:
                err_txt = 'hdm_separated_road_handle错误：分离式路基中心线X坐标与路基中心线X坐标相等，无法判断断面在分离式左侧还是右侧，请手动修改'
                err_list.append(err_txt)
                continue
        regx_chainage_dig = r'(?<!0)\d+\.*\d*'
        chainage_dig = re.findall(regx_chainage_dig, hdm_lines[0], re.MULTILINE)
        chainage_dig = float("".join(chainage_dig))
        xyz_line_chainage_dic['chainage'] = chainage_dig
        # xyz_line_chainage_dic['chainage'] = hdm_lines[0]
        xyz_line_chainage_dic['text'] = hdm_lines[1]
        for hdm_line in hdm_lines:  # 每条线
            regx_xyz = r'x=(\d+\.?\d+)\s*y=(\d+\.?\d+)\s*z=(\d+\.?\d+)'
            xyz_line_chainage = re.findall(regx_xyz, hdm_line, re.MULTILINE)
            print(hdm_line)
            print(f'xyz_line_chainage:{xyz_line_chainage}')
            print(f'len(xyz_line_chainage){len(xyz_line_chainage)}')
            # if len(xyz_line_chainage) == 0:
            #     if len(hdm_line.strip()) != 0:
            #         xyz_line_chainage_list.
            left_line_points = []
            right_line_points = []
            for xyz_point in xyz_line_chainage:  # 线中每个点
                print(f'xyz_point:{xyz_point}')
                exp = xyz_point[0] + symbol
                if eval(exp):   # 过虑分离式路基
                    xyz_point = list(map(float, xyz_point))  # 转为数值形数据
                    if float(xyz_point[0]) == zxx_x:  # 中间点
                        left_line_points.append(list(xyz_point))
                        right_line_points.append(list(xyz_point))
                        xyz_line_chainage_dic['zxx_xyz'] = xyz_point
                    elif float(xyz_point[0]) <= zxx_x:  # 左侧断面
                        left_line_points.append(list(xyz_point))
                    else:
                        right_line_points.append(list(xyz_point))
            if len(left_line_points) > 1:
                left_line.append(left_line_points)
            if len(right_line_points) > 1:
                right_line.append(right_line_points)
        xyz_line_chainage_dic['left_lines'] = left_line
        xyz_line_chainage_dic['right_lines'] = right_line
        res_xyz_lines_chainage[chainage_dig] = xyz_line_chainage_dic
    res_xyz_lines_chainage_and_err.append(res_xyz_lines_chainage)
    res_xyz_lines_chainage_and_err.append(err_list)
    return res_xyz_lines_chainage_and_err


if __name__ == "__main__":
    a=[1,2]
    b=[1,2,3]
    if a == b:
        print(1)