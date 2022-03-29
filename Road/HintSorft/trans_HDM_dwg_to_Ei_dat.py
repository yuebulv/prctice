'''
功能：
一、从横断面图dwg中提到到设计线坐标等数据；（lisp程序功能）
    1、将横断面图中路床、路面结构、占地线删除
    2、只保留设计线、边沟、挡墙、桥隧、中心线、分离式路基中心线
二、通过设计线坐标等数据得到EI数据的dat文件和are文件（本程序功能）
    一）、通过设计线坐标等数据得到EI数据的dat文件
        1、通过分离式路基线-中心线判断本路线与相交路线界线；
            分离式路基线-中心线重合时输出错误
        2、通过中心线分左右侧

        3、挡墙识别
            默认组成挡墙线条为闭合图形
            连续三条边类似形状：/-\、/-|、/-/、|-|，顶宽>=0.45m，两条边不能同时为直立边坡，（标识挡墙与墙背）
            与挡墙底边相连的图形为挡墙基座
            与挡墙基座相连的图形为挡墙基座
            输出的dat文件中挡墙以一条线代替，这条线的坡度、高度以/-\结构中的墙背为准
            默认断面左侧或者右侧只有一个挡墙
        4、水沟识别
            非挡墙

            连续三条边类似形状：\_/
            同一处有两条水沟线时，只留内沟线，舍弃衬砌线（标识水沟）
        5、中央分隔带、行车道、硬路肩、土路肩识别
            优先级：土路肩（0.25-0.75）、行车道（>=1.5m）、硬路肩、中央分隔带（第4段以后全为中央分隔带）
        6、填方边坡、挖方边坡识别
        7、去除平台截水沟
        8、按dat格式连接各部位
        9、输出dat


    1		        整幅路基
    1	中央分隔带	整幅路基
    1		        整幅路基
    1	路缘带	    整幅路基
    2	行车道	    整幅路基	桥梁
    3		        整幅路基	桥梁
    4		        整幅路基	桥梁
    5	土路肩	    整幅路基	桥梁
    6	填方边坡	    整幅路基
    7	边沟\排水沟	整幅路基
    8	挖方边坡	    整幅路基

顶点无分支，坡度相同，顶点坐标相同直线合并
    二）、通过设计线坐标等数据得到EI数据的are文件
公路BIM软件默认设置下出的横断面图特点：
    1、多段线：路面结构、路床、占地线；
    2、直线：中心线、分离式路基线、设计线、挡墙、水沟；
'''
import HintSorft.road as road
import HintSorft.roadglobal as roadglobal
import re
import operator
import copy
import numpy as np
import sys
import os
import tkinter as tk
from tkinter import filedialog


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
        msgbox = road.gui_filenotfine(f'{hdm_data_path}文件不存在')
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
        try:
            separated_x_2 = float(separated_x_tuple[1][0])
        except IndexError:
            symbol_2 = '!=-123456789'
        else:
            if separated_x_2 > zxx_x:
                symbol_2 = '<=' + str(separated_x_2)
            elif separated_x < zxx_x:
                symbol_2 = '>=' + str(separated_x_2)
            else:
                err_txt = 'hdm_separated_road_handle错误：分离式路基中心线X坐标与路基中心线X坐标相等，无法判断断面在分离式左侧还是右侧，请手动修改'
                err_list.append(err_txt)
                continue
        # 公路BIM V1.5版本生成的横断面文字注释格式与V1.2不同，引起hdm_lines[0]中含有设计高程的错误
        loc_debug_20210625 = hdm_lines[0].find('设计高程')
        hdm_lines[1] = hdm_lines[1] + hdm_lines[0][loc_debug_20210625:-1]
        hdm_lines[0] = hdm_lines[0][0:loc_debug_20210625]
        regx_chainage_dig = r'(?<!0)\d+\.*\d*'
        chainage_dig = re.findall(regx_chainage_dig, hdm_lines[0], re.MULTILINE)
        chainage_dig = float("".join(chainage_dig))
        # try:
        #     chainage_dig = float("".join(chainage_dig))
        # except ValueError:
        #     print(1)
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
                exp_2 = xyz_point[0] + symbol_2
                if eval(exp) and eval(exp_2):   # 过虑分离式路基
                    xyz_point = list(map(float, xyz_point))  # 转为数值形数据
                    # if float(xyz_point[0]) == zxx_x:  # 中间点  # 原代码
                    # 原代码存在问题：xyz_point[0]与zxx_x非常接近时，无法判断其属于左右还是右侧，左或右侧会漏掉此点
                    # 修改后代码将类似点同时加入左右侧，多余点通过后续代码删除。
                    if abs(float(xyz_point[0]) - zxx_x) <= 0.0005:  # 中间点 # 修改后代码20210707
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


def del_repeat_point_in_line(line):
    '''
    功能： 去除一条线中重叠线段
    方法：一条线中共有n个点，有m个重叠点，则非重叠点有n-m个，寻找n-m个连续点，并且其中无重叠点，则为所找点。
    :return:
    '''
    line_new = []
    [line_new.append(i) for i in line if not i in line_new]
    num = len(line_new)
    line_new = []
    if len(line) - len(line_new) > 0:
        for i in range(len(line)):
            line_num = line[i:(num+i)]
            [line_new.append(j) for j in line_num if not j in line_new]
            if len(line_new) == num:
                return line_num
            else:
                line_new = []


def tagging_wall_in_hdm_xyz(xyz_line, zxx_xyz, wall_filters='default'):
    # 已知直线或多段线各顶点坐标（坐标要按顶点前后顺序排列），如果判定为挡墙，返回墙背起止点坐标，
    '''
    直线或多段线坐标格式
    [
        [x y z]
        [x y z]
    ]
    :return:[[x y z], [x y z]] 或者 ’‘
    注意：水沟沟壁形状与挡墙形状有机会相同，只能通过改变水沟的尺寸来区分
    如果是路堑墙，返回''
    '''
    min_height_side_wall = abs(roadglobal.min_height_side_wall)
    max_gradient_side_wall = abs(roadglobal.max_gradient_side_wall)
    min_width_top_wall = abs(roadglobal.min_width_top_wall)
    max_width_top_wall = abs(roadglobal.max_width_top_wall)
    if wall_filters == 'default':   # 挡墙判定条件
        filter1 = [f'height1>{min_height_side_wall}', f'0<=gradient1<={max_gradient_side_wall}']  # 第1条边判定条件
        filter2 = [f'{min_width_top_wall}<=width2<={max_width_top_wall}', 'height2<0.5', '5<abs(gradient2)<=9999']  # 第2条边判定条件
        filter3 = [f'height3<{-abs(min_height_side_wall)}', f'{-abs(max_gradient_side_wall)}<=gradient3<=0']  # 第3条边判定条件
        filter4 = ['gradient1 != 0 or gradient3 != 0']   # 墙背和墙面坡比不能同时为0
        filter5 = ['width4>=width2']  # 墙顶宽度要小于等于底宽
        filters = [filter1, filter2, filter3, filter4, filter5]
    else:
        filters = wall_filters
    len_xyz_line = len(xyz_line)
    # try:
    #     len_xyz_line = len(xyz_line)
    # except TypeError:
    #     print(1)
    if len_xyz_line > 3:
        xyz_line.extend([xyz_line[0], xyz_line[1], xyz_line[2]])
        for i in range(len_xyz_line):
            width1 = abs(xyz_line[i + 1][0] - xyz_line[i][0])
            width2 = abs(xyz_line[i + 2][0] - xyz_line[i + 1][0])
            width3 = abs(xyz_line[i + 3][0] - xyz_line[i + 2][0])
            height1 = xyz_line[i + 1][1] - xyz_line[i][1]
            height2 = xyz_line[i + 2][1] - xyz_line[i + 1][1]
            height3 = xyz_line[i + 3][1] - xyz_line[i + 2][1]
            try:
                gradient1 = width1/height1
            except ZeroDivisionError:
                gradient1 = 9999
            try:
                gradient2 = width2 / height2
            except ZeroDivisionError:
                gradient2 = 9999
            try:
                gradient3 = width3 / height3
            except ZeroDivisionError:
                gradient3 = 9999
            width4 = abs(xyz_line[i + 0][0] - xyz_line[i + 3][0])
            is_wall = True
            for filter0 in filters:
                if not is_wall:
                    break
                for formula in filter0:
                    if eval(formula):
                        pass
                    else:
                        is_wall = False
                        break
            if is_wall:
                print(f'xyl_line:{xyz_line} is wall')
                if -1 <= zxx_xyz[1] - xyz_line[i + 1][1]:  # 路堤挡墙
                    if abs(zxx_xyz[0]-xyz_line[i + 1][0]) > abs(zxx_xyz[0]-xyz_line[i + 2][0]):
                        return [xyz_line[i], xyz_line[i+1]]
                    else:
                        return [xyz_line[i+2], xyz_line[i+3]]
                else:  # 路堑挡墙
                    return ''


def del_drainage_outside_frame(lines):
    # 删除断面中水沟衬砌线
    '''
    1、删除垫层，挡墙以下，X方向与挡墙存在交集
    2、边沟折线处理，边沟折线范围盖板删除
    3、识别边沟、盖板
        2.1如果有一线中，水沟设计线与衬砌线同时存在，那他们X值的单调性不同，一条线中含边坡，水沟内外框，利用X值单调性来删除水沟外框（内框底标高要高于外框）
            水沟衬砌线与边坡线直接相连（目前不支持）
            水沟内框线与边坡直接相连（支持）
            ++++++0---
            ---0++++++
            2.1.2内框、外框连到一起的水沟;
                ++++0---0++
                0++++++0---
                +++++
                起点在+-分界点时，保留，其它情况同两边+或-


        2.4内框、外框分开的水沟，多条线，利用X值单调性来判断内框和外框
                +++++++++++
            ++++
                    +++
    :return:
    '''
    res_lines = []
    err_list = []
    for line in lines:
        # 如果有一线中，水沟设计线与衬砌线同时存在，那他们X值的单调性不同，-2,2分别表示X值递减、递增；-1,1分别表示垂直递减、垂直递增。
        # 删除特殊形状
        print(f'l:{line}')
        line = correct_special_shape(line)
        print(f'c:{line}')
        if len(line) < 2:
            continue
        i_change_index_list = [[0, 0, 0]]  # [X值递减或递增，i_start,i_end]
        data_inner_outer_frame = [[0, 0, 0, 0], [0, 0, 0, 0]]  # [-2或2,i_start_in_line,i_end_in_line,min_y] 表示
        x_direction = 0
        for i in range(1, len(line)):
            if line[i][0] > line[i-1][0]:
                line[i][2] = 2
                if i_change_index_list[-1][0] != line[i][2]:
                    i_change_index_list[-1][-1] = i-2
                    i_change_index_list.append([line[i][2], i-1, 0])
                    if i > 1 and line[i][1] == line[i-1][1]:
                        if line[i-1][1]-line[i-2][1] > 0:
                            x_direction = line[i][2]
                        else:
                            x_direction = -line[i][2]
                    else:
                        pass
            elif line[i][0] < line[i-1][0]:
                line[i][2] = -2
                if i_change_index_list[-1][0] != line[i][2]:
                    i_change_index_list[-1][-1] = i - 2
                    i_change_index_list.append([line[i][2], i-1, 0])
                    if i > 1 and line[i][1] == line[i-1][1]:
                        if line[i-1][1]-line[i-2][1] > 0:
                            x_direction = line[i][2]
                        else:
                            x_direction = -line[i][2]
                    else:
                        pass
            elif line[i][1] > line[i-1][1]:
                line[i][2] = 1
            elif line[i][1] < line[i-1][1]:
                line[i][2] = -1
                # if x_direction[0] != -2 or x_direction != 2:
                #     x_direction[0] = i_change_index_list[-1][0]
        # try:
        #     i_change_index_list[-1][-1] = i
        # except UnboundLocalError:
        #     print(1)
        i_change_index_list[-1][-1] = i
        # print(f'line:{line}')
        # print(f'i_change_index_list:{i_change_index_list}')
        # print(f'x_direction:{x_direction}')
        # 以下区分水沟设计线与衬砌线。
        line_origin = copy.deepcopy(line)
        for i_change_index in i_change_index_list:
            if i_change_index[0] == x_direction and x_direction != 0:
                line = line[i_change_index[1]:(i_change_index[2]+1)]
                break
            if i_change_index == i_change_index_list[-1] and x_direction != 0:
                line = []
        print(f'line_origin:{line_origin}')
        print(f'line:{line}')
        print(f'i_change_index_list:{i_change_index_list}')
        print(f'x_direction:{x_direction}')
        if len(line)>0:
            res_lines.append(line)
    return [res_lines, err_list]


def distinguish_a_shape_in_a_line(line_origin, is_closed=True, shape_filters='default'):
    '''
    功能：识别直线line_origin中，形状为shape_filters线段，返回[[1, 8], [err_list]]
    :param line_origin:
    :param is_closed:True时，对直线起止点相接进行循环判断
    :param shape_filters:
    :return:[[1, 8], [err_list]]
            或者
            [[[3, 8], [0, 1]], [err_list]] （闭合线段有可能）
    '''
    err_list = []
    if shape_filters == 'default':  # 带盖板边沟内框判定条件
        filter1 = ['height[1]<0', 'width[1]==0']
        filter2 = ['width[2]!=0', 'height[2]==0']
        filter3 = ['height[3]<0', '0<=abs(gradient[3])<=5']
        filter4 = ['width[4]!=0', '5<=abs(gradient[4])<=9999']
        filter5 = ['height[5]>0', '0<=abs(gradient[5])<=5']
        filter6 = ['width[6]*width[2]>0', 'height[6]==0']
        filter7 = ['height[7]>0', 'width[7]==0']
        filters = [filter1, filter2, filter3, filter4, filter5, filter6, filter7]
    else:
        filters = shape_filters
    line = copy.deepcopy(line_origin)
    len_origin_line = len(line_origin)
    if is_closed:
        line.extend(line_origin[0:len(filters)])
    height = {}
    width = {}
    gradient = {}
    if len_origin_line > len(filters):
        for j in range(0, len_origin_line-len(filters)):
            m = 1
            for i in range(j+1, len(filters)+j+1):
                height[m] = line[i][1] - line[i-1][1]
                width[m] = line[i][0] - line[i-1][0]
                try:
                    gradient[m] = width[m]/height[m]
                except ZeroDivisionError:
                    gradient[m] = 9999
                m += 1
            is_shape = True
            for filter0 in filters:
                if not is_shape:
                    break
                for formula in filter0:
                    if eval(formula):
                        pass
                    else:
                        is_shape = False
                        break
            if is_shape:
                if j+len(filters)+1 <= len_origin_line:
                    return [[j, j+len(filters)], err_list]
                else:
                    return [[[j, len_origin_line-1], [0, j + len(filters) - len_origin_line]], err_list]
    return [[], err_list]


def is_line_x_in_x1_to_x2(line, x1, x2):
    # 功能：判断line的x坐标是不是全部在x1和x2之间
    if len(line) > 0:
        for point_xyz in line:
            try:
                x_min = min(x_min, point_xyz[0])
                x_max = max(x_max, point_xyz[0])
            except NameError:
                x_min = point_xyz[0]
                x_max = point_xyz[0]
        if x_min >= min(x1, x2) and x_max <= max(x1, x2):
            return True
        else:
            return False
    else:
        return True


def modify_a_shape_in_a_line(line_origin, is_closed=True, shape_filters='default'):
    '''
    功能：修改带盖板边沟|_  _| 为 | |，以便转为dat数据
                      |_|     |_|
    :param line_origin:
    :param is_closed:True时，对直线起止点相接进行循环判断
    :param shape_filters:
    :return:[[1, 8], [err_list]]
    '''
    err_list = []
    if shape_filters == 'default':  # 带盖板边沟内框判定条件
        filter1 = ['height[1]<0', 'width[1]==0']
        filter2 = ['width[2]!=0', 'height[2]==0']
        filter3 = ['height[3]<0', '0<=abs(gradient[3])<=5']
        filter4 = ['width[4]!=0', '5<=abs(gradient[4])<=9999']
        filter5 = ['height[5]>0', '0<=abs(gradient[5])<=5']
        filter6 = ['width[6]*width[2]>0', 'height[6]==0']
        filter7 = ['height[7]>0', 'width[7]==0']
        filters = [filter1, filter2, filter3, filter4, filter5, filter6, filter7]
    else:
        filters = shape_filters
    line = copy.deepcopy(line_origin)
    len_origin_line = len(line_origin)
    if is_closed:
        line.extend(line_origin[0:len(filters)])
    height = {}
    width = {}
    gradient = {}
    if len_origin_line > len(filters):
        for j in range(0, len_origin_line-len(filters)):
            m = 1
            for i in range(j+1, len(filters)+j+1):
                height[m] = line[i][1] - line[i-1][1]
                width[m] = line[i][0] - line[i-1][0]
                try:
                    gradient[m] = width[m]/height[m]
                except ZeroDivisionError:
                    gradient[m] = 9999
                m += 1
            is_shape = True
            for filter0 in filters:
                if not is_shape:
                    break
                for formula in filter0:
                    if eval(formula):
                        pass
                    else:
                        is_shape = False
                        break
            if is_shape:
                if j+len(filters)+1 <= len_origin_line:
                    index_list = list(range(j, j+len(filters)+1))
                    # return [[j, j+len(filters)], err_list]
                else:
                    index_list = list(range(j, len_origin_line-1))
                    index_list.extend(list(range(0, j + len(filters) - len_origin_line)))
                    # return [[[j, len_origin_line-1], [0, j + len(filters) - len_origin_line]], err_list]
                line_origin[index_list[2]][1] = line_origin[index_list[0]][1]
                line_origin[index_list[-3]][1] = line_origin[index_list[-1]][1]
                index_remove = index_list[0:2]
                index_remove.extend(index_list[-2:])
                index_remove.sort(reverse=True)
                # print(f'修改前line:{line}')
                for index_temp in index_remove:
                    del line_origin[index_temp]
                # print(f'修改后line:{line}')
                return [line_origin, err_list]
                # line[index_list[2]][1] = line[index_list[0]][1]
                # line[index_list[-3]][1] = line[index_list[-1]][1]
                # index_remove = index_list[0:2]
                # index_remove.extend(index_list[-2:])
                # index_remove.sort(reverse=True)
                # # print(f'修改前line:{line}')
                # for index_temp in index_remove:
                #     del line[index_temp]
                # # print(f'修改后line:{line}')
                # return [line, err_list]
    return [line_origin, err_list]


def del_point_of_dif_direction_in_line(line):
    # 功能：删除一条线中，不同方向的点，例如：当前点与前一点X方向不同时，删除当前点
    if len(line) > 2:
        j = 1
        while line[j][0] - line[j-1][0] == 0:
            j += 1
            if j > len(line)-1:
                return []
        # 修改原因：水沟起始线为垂直时，会全部过虑。修改后目标：水沟起始线为垂直时，保留一条垂直沟壁20210630
        temp = max(0, j-2)
        new_line = line[temp:(j+1)]
        # new_line = line[(j-1):(j+1)] 修改前代码
        for i in range(j+1, len(line)):
            if (line[i][0] - new_line[-1][0])*(new_line[-1][0] - new_line[-2][0]) > 0:
                new_line.append(line[i])
            elif (line[i][0] - new_line[-1][0])*(new_line[-1][0] - new_line[-2][0]) == 0:
                if line[i][1] != new_line[-1][1] or line[i][0] != new_line[-1][0]:
                    new_line.append(line[i])
    else:
        new_line = line
    return new_line


def del_coincide_point_in_line(line_origin, tolerance=0.01):
    # 功能：删除一条线中重合的点，距离在tolerance内的为重合点
    new_line = []
    if len(line_origin) > 1:
        new_line.append(line_origin[0])
        for i in range(1, len(line_origin)):
            distance = ((line_origin[i][0] - new_line[-1][0]) ** 2 + (line_origin[i][1] - new_line[-1][1]) ** 2) ** 0.5
            if distance > tolerance:
                new_line.append(line_origin[i])
    else:
        new_line = line_origin
    return new_line


def mark_road_item_in_line(line_origin, subgrade_width):
    # 功能：路基设计线line，标注line中的中央分隔带、行车道、路肩、边沟、边坡等，例如[[x, y ,z, 标注]]
    # line 格式[[x,y,z], [x,y,z]...]
    # line 中各点从中心线到坡脚排序
    line = copy.deepcopy(line_origin)
    err_list_mark = []
    tolerance = 0.01  # 容差范围
    subgrade_width = abs(subgrade_width)
    if abs(line[0][0]-line[-1][0])-subgrade_width < -tolerance:
        err_text = f'mark_road_item_in_line-line:{line},总宽度小于路基宽度：{subgrade_width}'
        err_list_mark.append(err_text)
        return {'line': [], 'err_list': err_list_mark}  # [[], err_list_mark]
    width_to_centre_line = 0
    road_item_priority = [5, 2, 2, 1, 1, 1, 1, 1]
    i_platform_omit_type_list = []
    for i in range(1, len(line)):
        width_to_centre_line += abs(line[i][0]-line[i-1][0])
        if abs(width_to_centre_line - subgrade_width) <= tolerance and len(line[i-1]) == 3:  # 中央分隔带、行车道、路肩标注
            j = i
            while j != 0:
                line[j].append(road_item_priority[0])
                del road_item_priority[0]
                j -= 1
            line[0].append(line[1][-1])
        elif width_to_centre_line - subgrade_width >= -tolerance:  # 边沟、边坡等标注
            try:
                temp = line[i][3]
            except IndexError:
                line_3points = line[i-1:(i+3)]
                is_drain_list = distinguish_a_shape_in_a_line(line_3points, is_closed=False, shape_filters=roadglobal.drain_filter)
                # 识别边沟7
                try:
                    for i_drain in range(is_drain_list[0][0]+1, is_drain_list[0][1]+1):
                        line[i-1+i_drain].append(7)
                except TypeError:
                    pass
                except IndexError:
                    pass
                try:
                    temp = line[i][3]
                except IndexError:  # 识别边坡6 8
                    width = line[i][0] - line[i-1][0]
                    height = line[i][1] - line[i-1][1]
                    try:
                        gradient = width/height
                    except ZeroDivisionError:
                        gradient = 9999
                    if height > 0 and 0 <= abs(gradient) <= 5:
                        line[i].append(8)
                        platform_type = 8
                    elif height < 0 <= abs(gradient) <= 5:
                        line[i].append(6)
                        platform_type = 6
                    else:  # 平台类型与前一边坡类型一致
                        try:
                            line[i].append(platform_type)
                        except NameError:
                            i_platform_omit_type_list.append(i)  # 类型未标记的平台
    for i in i_platform_omit_type_list:
        j = i+1
        while j <= len(line):
            try:
                line[i].append(line[j][3])
            except IndexError:
                pass
            else:
                break
            j += 1
        try:
            temp = line[i][3]
        except IndexError:
            line[i].append(8)
    try:
        line[0][3]
    except IndexError:
        line[0].append(line[1][-1])
    # 删除平台截水沟，水沟两侧最近边坡（非平台）坡度一致时判定为平台截水沟
    i_drain_list = []
    switch = True
    item_and_slope_of_last_point = [0, 9999]  # [6, 坡度]
    item_and_slope_of_next_point = [0, 9999]
    for i in range(1, len(line)):
        print(f'line:{line}.i:{i}')
        if line[i][3] == 7:
            i_drain_list.append(i)
        elif len(i_drain_list) > 0:
            for j in range(i+1, len(line)):
                width = line[j][0] - line[j - 1][0]
                height = line[j][1] - line[j - 1][1]
                try:
                    slope = width / height
                except ZeroDivisionError:
                    slope = 9999
                if line[j][3] > 5 and slope != 9999:
                    item_and_slope_of_next_point = [line[j][3], slope]
                    break
            if item_and_slope_of_last_point[0] == item_and_slope_of_next_point[0] > 5:  # 判定为平台截水沟
                for i_drain_del in i_drain_list:
                    line[i_drain_del] = []
            i_drain_list = []
            item_and_slope_of_last_point = [0, 9999]  # [6, 坡度]
            item_and_slope_of_next_point = [0, 9999]
        else:
            width = line[i][0]-line[i-1][0]
            height = line[i][1]-line[i-1][1]
            try:
                slope = width/height
            except ZeroDivisionError:
                slope = 9999
            if line[i][3] > 5 and slope != 9999:
                item_and_slope_of_last_point = [line[i][3], slope]
    line_new = []
    for point in line:
        if len(point) > 0:
            line_new.append(point)
    # 填方水沟外侧衬砌线
    if line_new[-2][3] == 7:
        height = line_new[-1][1] - line_new[-2][1]
        if height == 0:
            del line_new[-1]
    return line_new


def calculate_height_of_point(line_origin, known_point_xyz, known_point_design_height):
    '''
    # 功能：已知A/B两点相对高差，已知A点设计标高，求B点设计标高
    :param line_origin: [[x, y, z], [x, y, z,]...]
    :param known_point_xyz: [x, y, z]
    :param known_point_design_height: float
    :return:line
    '''
    line = copy.deepcopy(line_origin)
    for i in range(len(line)):
        relative_height = line[i][1] - known_point_xyz[1]
        height = known_point_design_height + relative_height
        line[i][2] = '%.4f' % height  # float('%.4f' % height)
        line[i][1] = '0.0000'
        line[i][0] = '%.4f' % line[i][0]  # float('%.4f' % line[i][0])
    return line


def check_hdm_line(line_origin):
    # 检查6 8同时存在，只有一组7,X单调，只有一个5
    '''
    :param line_origin: [[x, y, z, num], [[x, y, z, num]]...]
    :return:{‘line’:line_new, 'err_list':err_list}
    '''
    # line中num=7有多组时，保留y值最小的一组，意图删除坡顶截水沟
    line = copy.deepcopy(line_origin)
    num_7_dic = {}
    i_num_is_7 = []
    err_list_check = []
    j = 1
    for i in range(len(line)):
        if line[i][3] == 7:
            i_num_is_7.append(i)
            try:
                y_min = min(y_min, line[i][1])
            except NameError:
                y_min = line[i][1]
            num_7_dic[j] = {'i_list': i_num_is_7, 'y_min': y_min}
            try:
                y_min_min = min(y_min, y_min_min)
            except NameError:
                y_min_min = y_min
        else:
            if len(i_num_is_7) > 0:
                num_7_dic[j] = {'i_list': i_num_is_7, 'y_min': y_min}
                j += 1
                i_num_is_7 = []
                del y_min
    i_del = []
    if len(num_7_dic) > 1:
        for key in num_7_dic:
            if num_7_dic[key]['y_min'] > y_min_min:
                i_del.extend(num_7_dic[key]['i_list'])
        i_del = sorted(i_del, reverse=True)
        for i in i_del:
            del line[i]
    return {'line': line, 'err_list': err_list_check}


def correct_special_shape(line_origin):
    # 修正指定形状line
    # 连续三点A/B/C，坐标Y值相同，X-B 不在X-A X-C之间，则删除B点，如果A/B两点距离小于tolerate时，删除与B点距离较近点
    line = copy.deepcopy(line_origin)
    i_line_del = []
    tolerance = 0.05
    if len(line) > 2:
        for i in range(2, len(line)):
            if line[i][1] == line[i-1][1] == line[i-2][1]:
                if line[i-1][0] < min(line[i][0], line[i-2][0]) or line[i-1][0] > max(line[i][0], line[i-2][0]):
                    i_line_del.append(i-1)
                    if abs(line[i][0]-line[i-2][0]) <= tolerance:
                        if abs(line[i-1][0]-line[i-2][0]) > abs(line[i-1][0]-line[i][0]):
                            i_line_del.append(i)
                        else:
                            i_line_del.append(i - 2)
        i_line_del = sorted(i_line_del, reverse=True)
        for i in i_line_del:
            del line[i]
    # 连续三个点A/B/C，坐标X值相同，Y-B 不在Y-A Y-C之间，则删除B点
    i_line_del = []
    if len(line) > 2:
        for i in range(2, len(line)):
            if line[i][0] == line[i-1][0] == line[i-2][0]:
                if line[i-1][1] < min(line[i][1], line[i-2][1]) or line[i-1][1] > max(line[i][1], line[i-2][1]):
                    i_line_del.append(i-1)
        i_line_del = sorted(i_line_del, reverse=True)
        for i in i_line_del:
            del line[i]
    # 连续6个点，中间4个点Y值相等，两端Y值高于中间4点，则删除中间4点
    i_line_del = []
    if len(line) > 5 and len(line) != 11:
        for i in range(5, len(line)):
            if line[i-4][1] == line[i-3][1] == line[i-2][1] == line[i-1][1]:
                if line[i-5][1] > line[i-4][1] and line[i][1] > line[i-4][1]:
                    for temp in [i-4, i-3, i-3, i-1]:
                        i_line_del.append(temp)
        i_line_del = sorted(i_line_del, reverse=True)
        for i in i_line_del:
            del line[i]
    return line


def main(hdm_data_path):
    # 注意：横断面图中桩号一般无断链信息，所以转为的dat, are文件中桩号也无断链信息，后续需要优化
    # hdm_data_path = r'C:\Users\29735\Desktop\s.txt'
    # res_path = r'C:\Users\29735\Desktop\res.txt'
    if os.path.exists(hdm_data_path):
        hdm_data_path = hdm_data_path.replace('\\', '/')
        regEx = roadglobal.regx_get_filename_from_path
        file_name = re.findall(regEx, hdm_data_path, re.MULTILINE)[0]
        regEx = r"(.+/).+$"
        file_path = re.findall(regEx, hdm_data_path, re.MULTILINE)[0]
    else:
        return []
    res_path = file_path + 'res.txt'
    res_file = open(res_path, 'w')
    path_dat_saved = file_path + file_name + '.dat'
    dat_file = open(path_dat_saved, 'w')
    path_are_saved = file_path + file_name + '.are'
    are_file = open(path_are_saved, 'w')

    layer_name = '图层分离式路基中心线'
    layer_name_zxx = '图层中心线'
    err_list_main = []
    hdms_lines = grop_hdms_lines(hdm_data_path, layer_name_zxx, layer_name)
    # 1 墙背线替代挡墙，删除垫层
    for hdm in hdms_lines[0]:   # 每个桩号
        print(f'hdm:{hdm}')
        for key_left_Or_right in ['left_lines', 'right_lines']:
            # for i in range(len(hdms_lines[0][hdm][key_left_Or_right])):
            i = 0
            while i <= len(hdms_lines[0][hdm][key_left_Or_right]):
                try:
                    hdms_lines[0][hdm][key_left_Or_right][i]
                except IndexError:
                    break
                else:
                    hdms_lines[0][hdm][key_left_Or_right][i] = del_coincide_point_in_line(
                        hdms_lines[0][hdm][key_left_Or_right][i], tolerance=0.01)
                    hdms_lines[0][hdm][key_left_Or_right][i] = del_repeat_point_in_line(hdms_lines[0][hdm][key_left_Or_right][i])
                    if hdms_lines[0][hdm][key_left_Or_right][i] is None:
                        del hdms_lines[0][hdm][key_left_Or_right][i]
                        continue
                line_xyz = copy.deepcopy(hdms_lines[0][hdm][key_left_Or_right][i])  # 每条设计线
                if line_xyz is None:
                    wall_line = ''
                else:
                    wall_line = tagging_wall_in_hdm_xyz(line_xyz, hdms_lines[0][hdm]['zxx_xyz'])
                if wall_line:
                    print('原：', hdms_lines[0][hdm][key_left_Or_right][i])
                    hdms_lines[0][hdm][key_left_Or_right][i] = wall_line  # 用墙背线替换挡墙线
                    print(f'wall_line:{wall_line}')
                    # 删除垫层
                    j_correct = 0
                    for j in range(len(hdms_lines[0][hdm][key_left_Or_right])):
                        min_x_line = None
                        max_x_line = None
                        max_y_line = None
                        line_temp = hdms_lines[0][hdm][key_left_Or_right][j_correct]
                        for point_xyz in line_temp:
                            try:
                                min_x_line = min(min_x_line, point_xyz[0])
                            except TypeError:
                                min_x_line = point_xyz[0]
                            try:
                                max_x_line = max(max_x_line, point_xyz[0])
                            except TypeError:
                                max_x_line = point_xyz[0]
                            try:
                                max_y_line = max(max_y_line, point_xyz[1])
                            except TypeError:
                                max_y_line = point_xyz[1]
                        if not operator.eq(wall_line, line_temp):
                            if min_x_line >= max(wall_line[0][0], wall_line[1][0]):
                                pass
                            elif max_x_line <= min(wall_line[0][0], wall_line[1][0]):
                                pass
                            else:  # 与挡墙相交
                                if min(wall_line[0][1], wall_line[1][1]) >= max_y_line:  # 并在挡墙下方的线判断为垫层
                                    print(f'{hdm}:{key_left_Or_right}，多段线{line_temp}为垫层')
                                    del hdms_lines[0][hdm][key_left_Or_right][j_correct]
                                    j_correct -= 1
                        j_correct += 1
                    break  # 默认断面左侧或者右侧只有一个挡墙
                i += 1
    # 2 修改带盖板边沟|_  _| 为 | |，以便转为dat数据
    #                |_|     |_|
    for hdm in hdms_lines[0]:  # 每个桩号
        for key_left_Or_right in ['left_lines', 'right_lines']:
            for index_line in range(len(hdms_lines[0][hdm][key_left_Or_right])):
                line_xyz = copy.deepcopy(hdms_lines[0][hdm][key_left_Or_right][index_line])  # 每条设计线
                index_drain = distinguish_a_shape_in_a_line(line_xyz, is_closed=True, shape_filters='default')

                if len(index_drain[0]) == 2:  # 判定为带盖板边沟
                    try:
                        start_x_drain = min(line_xyz[index_drain[0][0][0]][0], line_xyz[index_drain[0][0][1]][0],
                                            line_xyz[index_drain[0][1][0]][0], line_xyz[index_drain[0][1][1]][0])
                        end_x_drain = max(line_xyz[index_drain[0][0][0]][0], line_xyz[index_drain[0][0][1]][0],
                                            line_xyz[index_drain[0][1][0]][0], line_xyz[index_drain[0][1][1]][0])
                    except TypeError:
                        start_x_drain = min(line_xyz[index_drain[0][0]][0], line_xyz[index_drain[0][1]][0])
                        end_x_drain = max(line_xyz[index_drain[0][0]][0], line_xyz[index_drain[0][1]][0])
                    print(f'index_drain:{index_drain}')
                    print(f'start_x_drain:{start_x_drain}')
                    print(f'end_x_drain:{end_x_drain}')
                    # 删除边沟盖板
                    for index_line_del_cover in range(len(hdms_lines[0][hdm][key_left_Or_right])):
                        if index_line_del_cover != index_line:
                            is_in = is_line_x_in_x1_to_x2(hdms_lines[0][hdm][key_left_Or_right][index_line_del_cover],
                                                          start_x_drain, end_x_drain)
                            if is_in:
                                # print('y', hdms_lines[0][hdm][key_left_Or_right][index_line_del_cover])
                                hdms_lines[0][hdm][key_left_Or_right][index_line_del_cover] = []
                                # print('h', hdms_lines[0][hdm][key_left_Or_right][index_line_del_cover])
                    # 2 修改带盖板边沟|_  _| 为 | |，以便转为dat数据
                    #                |_|     |_|
                    line_xyz = copy.deepcopy(hdms_lines[0][hdm][key_left_Or_right][index_line])  # 每条设计线
                    print(f'line_xyz:{line_xyz}')
                    line_new = modify_a_shape_in_a_line(line_xyz, is_closed=True, shape_filters='default')
                    hdms_lines[0][hdm][key_left_Or_right][index_line] = line_new[0]
                    print('修改后line_xyz：', hdms_lines[0][hdm][key_left_Or_right][index_line])

    # 3 删除断面中水沟衬砌线
    for hdm in hdms_lines[0]:  # 每个桩号
        for key_left_Or_right in ['left_lines', 'right_lines']:
            hdms_lines[0][hdm][key_left_Or_right] = del_drainage_outside_frame(hdms_lines[0][hdm][key_left_Or_right])[0]
            print(f'hdms_lines[0][hdm]:{hdms_lines[0][hdm][key_left_Or_right]}')
            # 4 给线段各顶点调整起止顺序，排序，
            if key_left_Or_right == 'left_lines':
                x_direction = -2
            else:
                x_direction = 2
            i_x_lines = []
            sorted_line = []
            for i_line_sort in range(len(hdms_lines[0][hdm][key_left_Or_right])):
                # print(f'line-{key_left_Or_right}:{hdms_lines[0][hdm][key_left_Or_right][i_line_sort]}')
                for point_line_direction in hdms_lines[0][hdm][key_left_Or_right][i_line_sort]:
                    # print(f'line_direction:{point_line_direction}')
                    if abs(point_line_direction[-1]) == 2:
                        if point_line_direction[-1] != x_direction:
                            hdms_lines[0][hdm][key_left_Or_right][i_line_sort].reverse()
                        break
                print(f'line-reverse{key_left_Or_right}:{hdms_lines[0][hdm][key_left_Or_right][i_line_sort]}')
                i_x_lines.append([i_line_sort, hdms_lines[0][hdm][key_left_Or_right][i_line_sort][0][0]])
            # 排序
            if key_left_Or_right == 'left_lines':
                i_x_lines = sorted(i_x_lines, key=(lambda x: x[1]), reverse=True)
            else:
                i_x_lines = sorted(i_x_lines, key=(lambda x: x[1]), reverse=False)
            print(f'i_x_lines:{i_x_lines}')
            i_sorted_list = [i_sorted[0] for i_sorted in i_x_lines]
            print(f'{hdm}{key_left_Or_right}:{hdms_lines[0][hdm][key_left_Or_right]}')
            # 合并为一条线
            for i_temp in i_sorted_list:
                sorted_line.extend(hdms_lines[0][hdm][key_left_Or_right][i_temp])
            # print(f'sorted_line:{sorted_line}')
            # 接点处理,根据x的单调性，
            sorted_line = del_point_of_dif_direction_in_line(sorted_line)
            # 删除重复点
            sorted_line = del_coincide_point_in_line(sorted_line, tolerance=0.01)
            sorted_line = correct_special_shape(sorted_line)
            print(f'sorted_line:{sorted_line}')
            if key_left_Or_right == 'left_lines':
                regx = f'左路基宽\s*=\s*(\d+\.?\d*)'
            else:
                regx = f'右路基宽\s*=\s*(\d+\.?\d*)'
            width_subgrade = re.findall(regx, hdms_lines[0][hdm]['text'], re.MULTILINE)
            width_subgrade = float(width_subgrade[0])
            print(f'width_subgrade:{width_subgrade}')
            # 5 中央分隔带，行车道，路肩，水沟，边坡标注
            if len(sorted_line) > 1:
                marked_line = mark_road_item_in_line(sorted_line, width_subgrade)
            else:
                err_txt = f'桩号：{hdm},{key_left_Or_right},断面错误'
                err_list_main.append(err_txt)
                hdms_lines[0][hdm][key_left_Or_right] = [[]]
                continue
            print(f'marked_line:{marked_line}')
            try:
                err_list_main.append(marked_line['err_list'])
            except TypeError:
                pass
            else:
                print(f'err_list:{err_list_main}')
                err_list_main[-1].append([{'hdm': hdm, 'key_left_Or_right': key_left_Or_right}])
                hdms_lines[0][hdm][key_left_Or_right] = [[]]
                continue
            #  检查6 8同时存在，只有一组7,X单调，只有一个5
            checked_line = check_hdm_line(marked_line)
            if len(checked_line['err_list']) > 0:
                err_list_main.append(checked_line['err_list'])
                err_list_main[-1].append([{'hdm': hdm, 'key_left_Or_right': key_left_Or_right}])
            temp_xyz = np.array(checked_line['line'])[:, 0:3].tolist()
            res_file.write('3q '+str(temp_xyz))
            res_file.write('\n')
            temp_xyz = np.array(checked_line['line'])[:, -1].tolist()
            res_file.write(str(temp_xyz))
            res_file.write('\n')
            # 5 计算坐标Z值
            regx = f'设计高程\s*=\s*(\d+\.?\d*)'
            design_height = re.findall(regx, hdms_lines[0][hdm]['text'], re.MULTILINE)
            design_height = float(design_height[0])
            corrected_z_line = calculate_height_of_point(checked_line['line'], hdms_lines[0][hdm]['zxx_xyz'], design_height)  # 修改Z坐标
            hdms_lines[0][hdm][key_left_Or_right] = [corrected_z_line]
        try:
            hdms_lines[0][hdm]['zxx_xyz'][1] = hdms_lines[0][hdm][key_left_Or_right][0][0][1]
            hdms_lines[0][hdm]['zxx_xyz'][2] = hdms_lines[0][hdm][key_left_Or_right][0][0][2]
        except IndexError:
            try:
                hdms_lines[0][hdm]['zxx_xyz'][1] = hdms_lines[0][hdm]['left_lines'][0][0][1]
                hdms_lines[0][hdm]['zxx_xyz'][2] = hdms_lines[0][hdm]['left_lines'][0][0][2]
            except IndexError:
                continue

    hdm_chainages = sorted(hdms_lines[0].keys())
    print(f'hdm_chainages:{hdm_chainages}')
    for hdm in hdm_chainages:  # 每个桩号
        # 6 生成dat文件
        dat_text = hdms_lines[0][hdm]['chainage']
        dat_file.write(str(dat_text))
        dat_file.write('\n')
        dat_text = ' '.join(map(str, hdms_lines[0][hdm]['zxx_xyz']))
        dat_file.write(dat_text)
        dat_file.write('\n')
        dat_text = str(len(hdms_lines[0][hdm]['left_lines'][0]))
        dat_file.write(dat_text)
        dat_file.write('\n')
        dat_text = "\n".join(map(str, hdms_lines[0][hdm]['left_lines'][0])).replace(',', '').replace('[', '').replace(']', '').replace("'", '')
        dat_file.write(dat_text)
        dat_file.write('\n')
        dat_text = str(len(hdms_lines[0][hdm]['right_lines'][0]))
        dat_file.write(dat_text)
        dat_file.write('\n')
        dat_text = "\n".join(map(str, hdms_lines[0][hdm]['right_lines'][0])).replace(',', '').replace('[', '').replace(']', '').replace("'", '')
        dat_file.write(dat_text)
        dat_file.write('\n')
        # 7 生成are文件
        are_text_list = [0]*12
        are_text_list[0] = float(hdm)
        pra_list = ['设计高程', '[填|挖]方[高|深]', '填方面积', '挖方面积']
        i = 1
        for pra in pra_list:
            regx = f'{pra}\s*=\s*(\d+\.?\d*)'
            are_text_list[i] = re.findall(regx, hdms_lines[0][hdm]['text'], re.MULTILINE)[0]
            if i == 2 and hdms_lines[0][hdm]['text'].find('挖方深') > -1:
                are_text_list[i] = -float(are_text_list[i])
            i += 1
        are_text = '\t'.join(map(str, are_text_list))
        are_file.write(are_text)
        are_file.write('\n')
    are_file.close()
    dat_file.close()
    res_file.close()
    return {'err_list': err_list_main}


if __name__ == "__main__":
    err_list = []
    root = tk.Tk()
    root.withdraw()
    my_filetypes = [('text files', '.txt'), ('all files', '.*')]
    answer_file = filedialog.askopenfilename(parent=root, title="Please select a file_public:", filetypes=my_filetypes)
    if os.path.exists(answer_file):
        err_list = main(answer_file)['err_list']
        hdm_data_path = answer_file.replace('\\', '/')
        regEx = r"(.+/).+$"
        file_path = re.findall(regEx, hdm_data_path, re.MULTILINE)[0]
        file_path = file_path + 'err_trans_hdm_dwg_to_ei_dat.txt'
        err_file = open(file_path, 'w')
        for err in err_list:
            # err_text = ' '.join(map(str, err))
            err_file.write(str(err))
            err_file.write('\n')
        err_file.close()
    print('dat_are文件转换完成')






