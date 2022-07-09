#!/usr/bin/env python
# encoding: utf-8
'''
Module Description

Created on Jul 22, 2019
@author: user
@change: Jul 22, 2019 user: initialization
'''
from lxml import etree  #将KML节点输出为字符串
from pykml import parser
import numpy as np
import re
import copy
from geopy.distance import geodesic
import math
from pathlib import Path
import os
import pandas as pd
import shutil


class Setting():
    maxDistance_picToLine = 10  # 线路所属照片与线路最大距离
    initialDistance = 10000
    regx_picDescription = "护栏"
    outputPath = r"D:\X项目\20220528大竹安保工程\W-外业成果\5组.txt"
    kmlPath = r"D:\X项目\20220528大竹安保工程\W-外业成果\5组.kml"
    path_group_excel = r"D:\X项目\20220528大竹安保工程\W-外业成果\20220614安全防护调查表（路侧护栏）汇总表-y.xlsx"
    sheetname = "Sheet1"


class Operation_kml():
    def __init__(self):
        pass

    def parse_kml(self, kml_file):
        '''
        @summary: parse single kml
        @param kml_file: the kml file
        @return: return gps data
        '''
        line_list = []
        with open(kml_file, 'r', encoding="utf-8") as f:
            doc = parser.parse(f).getroot()

            # find all the gps data
            try:
                latlng_list = str(doc.Placemark.LineString.coordinates).replace(' ', "\n").split("\n")
            except AttributeError:
                try:
                    line_all = doc.Document.Placemark.LineString.coordinates
                    for line in line_all:
                        latlng_list.append(line)
                    latlng_list = str(doc.Document.Placemark.LineString.coordinates).replace(' ', "\n").split("\n")
                except AttributeError:
                    latlng_list = str(doc.Folder.Placemark.LineString.coordinates).replace(' ', "\n").split("\n")
                except Exception:
                    return line_list
            except Exception:
                return line_list
            for item in latlng_list:
                latlng = item.split(',')

                # check the gps data is ok
                if len(latlng) == 3:
                    # remove the height and exchange the lat and lng
                    # change the str to float
                    tmp_latlng = [float(latlng[:2][::-1][0]), float(latlng[:2][::-1][1])]
                    line_list.append(tmp_latlng)

        return line_list


def point_distance_line(point, line_point1, line_point2):
    # 计算向量
    vec1 = line_point1 - point
    vec2 = line_point2 - point
    distance = np.abs(np .cross(vec1, vec2)) / np.linalg.norm(line_point1-line_point2)
    return distance
    # point = np.array ( [5,2])
    # line_point1 = np.array ( [2,2])
    # line_point2 = np.array ( [3,3])
    # print(get_distance_from_point_to_line(point,line_point1,line_point2))
    # print(point_distance_line(point,line_point1,line_point2))


def triangleAre(a: float, b: float, c: float):
    # 根据三边长度求面积
    if a + b > c and a + c > b and b + c > a:
        p = (a + b + c) / 2
        area = (p * (p - a) * (p - b) * (p - c))**0.5
        return area
    else:
        return 0


def isPicBelongLine(point: list, line_start: list, line_end: list, toleranceRadius=0):
    '''
    # 判断奥维中某个照片是否属于该线段
    :param point:[经度 纬度]
    :param line_start:[经度 纬度]
    :param line_end:[经度 纬度]
    :param toleranceRadius:单位：米，与线段距离小于等于toleranceRadius时，判断为True；
    线段两个端点半径toleranceRadius范围内，无论夹角多少度都判断为True;
    方法：
    1、point与线段端点夹角小于等于90，point与线段距离小于toleranceRadius时判断为True
    '''
    lenA = abs(geodesic(line_start[::-1], point[::-1]).m)
    lenB = abs(geodesic(line_end[::-1], line_start[::-1]).m)
    lenC = abs(geodesic(line_end[::-1], point[::-1]).m)
    triangle_Are = triangleAre(lenC, lenA, lenB)
    if lenA <= toleranceRadius or lenC <= toleranceRadius:
        return True
    try:
        distance = triangle_Are / lenB
    except ZeroDivisionError:
        return False
    else:
        if distance <= toleranceRadius:
            angle_a = math.acos((lenA**2+lenB**2-lenC**2)/(2*lenA*lenB))*180/math.pi
            angle_c = math.acos((lenC**2+lenB**2-lenA**2)/(2*lenC*lenB))*180/math.pi
            # print(f"angle_c:{angle_c}", f"angle_a:{angle_a}")
            if angle_a <= 90 and angle_c <= 90:
                return True
            else:
                return False
        else:
            return False

    # if distance < distance_min and distance < Setting().maxDistance_picToLine:
    #     lenH = (lenC ** 2 - distance ** 2) ** 0.5
    #     chainAge = lineLen - lenH
    #     distance_min = distance


def findDataFromExcel(path_excel, sheetname, key="路线编号", col="all") -> pd.Series:
    # key不区分大小写
    data = pd.read_excel(path_excel, sheet_name=sheetname)
    key = key.upper()
    try:
        res = data.loc[data["路线编号"] == key].iloc[0, :4]  # data[key=="C043511724", :]
    except IndexError:
        key = key.lower()
        try:
            res = data.loc[data["路线编号"] == key].iloc[0, :4]
        except IndexError:
            res = pd.Series([], dtype="float64")
    return res


def move_file(target_path, source_path):
    pass


def getTargetPathFromList(pic_inf_list):
    # 功能：从list中得到目标path ,list 格式如main中res_picName_description_lineId_list
    len_of_line_number = len(pic_inf_list[2])
    new_line_number = "C000511724"
    if len_of_line_number == 2:  # ********************************************************需要精减
        new_line_number = "C0" + str(pic_inf_list[2]) + "511724"
    elif len_of_line_number == 3:
        new_line_number = "C" + str(pic_inf_list[2]) + "511724"
    elif len_of_line_number == 6:
        pass
    else:
        return None
    target_path_series = findDataFromExcel(Setting.path_group_excel, sheetname=Setting.sheetname, key=new_line_number)
    target_path = "\\".join(target_path_series.astype(str).tolist())
    target_path = Path(Setting.kmlPath).parent.joinpath(target_path).joinpath(pic_inf_list[4])
    return target_path


def main():
    """
    1得到所有路线（name,坐标）
    2得到含关键字照片（name,坐标,description,OvAttaItem）
    3判断照片桩号，分析description内容
    4生成表格
    5图片分组
    """
    kmlPath = Setting.kmlPath
    with open(kmlPath, 'r', encoding="utf-8") as f:
        placeMark_all = parser.parse(f).getroot().Document.Placemark

        # step1:得到所有路线（name,坐标）--------------------
        lines_dic = {}
        for placeMark in placeMark_all:
            # print(placeMark)
            try:
                latlng_list = str(placeMark.LineString.coordinates).replace(' ', "\n").split("\n")
            except AttributeError:
                pass
            else:
                lines_dic[placeMark.name] = latlng_list
        # print(len(lines_dic))
        # print(lines_dic.keys())-----------------------
        print("step1:得到所有路线（name,坐标）,Done!")

        # step2:得到含关键字照片（name,坐标,description,OvAttaItem）-------------------
        picPlaceMarkIndex_list = []
        regx = Setting.regx_picDescription
        for index, placeMark in enumerate(placeMark_all):
            try:
                descr = placeMark[index].description.text
            except AttributeError:
                pass
            else:
                try:
                    re.findall(regx, descr, re.MULTILINE)[0]
                except IndexError:
                    pass
                else:
                    picPlaceMarkIndex_list.append(index)
                # print(placeMark[index].name)
                # print(placeMark[index].Point.coordinates)
                # for item in placeMark[index].OvAttr.OvAttaList.OvAttaItem:
                #     print(item)
        print("step2:得到含关键字照片（name,坐标,description,OvAttaItem）,Done!")

        # step3:判断照片桩号，分析description内容---------------------------------------
        res_picName_description_lineId_list = [["照片标签名称", "描述", "所属路线名字", "照片标签与路线距离", "照片桩号", "照片路径"]]
        for index in picPlaceMarkIndex_list:
            picName_description_lineId_list = []
            temp = placeMark[index].Point.coordinates.text.split(",")[:2]
            pointCoord_array = np.array([float(temp[0]), float(temp[1])])
            lineId_distance_chainAge_list = []
            for lineKey in lines_dic:
                # print(lines_dic[lineKey])
                lineLen = 0
                distance_list = []
                distance_min = Setting().initialDistance
                chainAge = ""
                try:
                    del lineCoord_pre_list
                except:
                    pass
                for lineCoord_str in lines_dic[lineKey]:
                    if lineCoord_str == "":
                        continue
                    lineCoord_list = lineCoord_str.split(",")[:2]
                    # print(lineCoord_list)
                    lineCoord_list = [float(lineCoord_list[0]), float(lineCoord_list[1])]
                    try:
                        lineLen += abs(geodesic(lineCoord_list[::-1], lineCoord_pre_list[::-1]).m)
                    except NameError:
                        pass
                    else:
                        lenA = abs(geodesic(lineCoord_pre_list[::-1], pointCoord_array[::-1]).m)
                        lenB = abs(geodesic(lineCoord_list[::-1], lineCoord_pre_list[::-1]).m)
                        lenC = abs(geodesic(lineCoord_list[::-1], pointCoord_array[::-1]).m)
                        triangle_Are = triangleAre(lenC, lenA, lenB)
                        try:
                            distance = triangle_Are/lenB
                        except ZeroDivisionError:
                            distance = lenC
                        if isPicBelongLine(pointCoord_array.tolist(), lineCoord_pre_list, lineCoord_list, Setting().maxDistance_picToLine):
                            if distance < distance_min:
                                lenH = (lenC**2 - distance**2)**0.5
                                chainAge = lineLen - lenH
                                distance_min = distance
                    lineCoord_pre_list = copy.deepcopy(lineCoord_list)
                    # print(f"lineLen:{lineLen}")
                lineId_distance_chainAge_list.append([lineKey, distance_min, chainAge])
            print(placeMark[index].name)
            print(placeMark[index].description.text)
            # print(len(lineId_distance_chainAge_list))
            lineId_distance_chainAge_list = sorted(lineId_distance_chainAge_list, key=lambda x: x[1])
            # print(lineId_distance_chainAge_list)
            print(lineId_distance_chainAge_list[0])
            # for item in lineId_distance_chainAge_list:
            #     print(item)
            ovatta_list = [item for item in placeMark[index].OvAttr.OvAttaList.OvAttaItem]
            picName_description_lineId_list = [placeMark[index].name, placeMark[index].description.text,
                                               lineId_distance_chainAge_list[0], ovatta_list]
            res_picName_description_lineId_list.append(picName_description_lineId_list)
        print("step3:判断照片桩号，分析description内容,Done!")

        # step4:生成表格--------------------
        with open(Setting.outputPath, 'w', encoding="utf-8") as outfile:
            outfile.write(str(res_picName_description_lineId_list).replace("], [", "\n").replace('[', "").replace("]", ""))
        print("step4:生成表格,Done!")

        # step5:照片分组整理
        for pic_inf_list in res_picName_description_lineId_list:
            target_path = getTargetPathFromList(pic_inf_list)
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            for source_path in pic_inf_list[-1]:
                source_path = Path(Setting.kmlPath).parent.joinpath(source_path)
                if os.path.exists(source_path):
                    shutil.copy(source_path, target_path)
        print("step5:照片分组整理,Done!")


if __name__ == '__main__':
    main()