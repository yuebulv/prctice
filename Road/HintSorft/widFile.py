from roadglobal import regx_wide
import re
import copy
from operator import itemgetter

'''
1.读入宽度文件
def read_wide_file():

2.定位加宽桩号

3.修改宽度

4.写入文件
'''


class HintWide:
    def __init__(self):
        self.lors = {
            '左侧': 0,
            '左': 0,
            '右侧': 1,
            '右': 1
        }
        self.postions = {
            '中间带': 1,
            '车行道': 2,
            '行车道': 2,
            '硬路肩': 3,
            '土路肩': 5,
        }


# 1.读入宽度文件
def read_wide_file(path):
    with open(path, 'r') as file:
        file_data = file.read()
    list_file_data = re.findall(regx_wide(), file_data, re.MULTILINE)
    return list_file_data


def wide_mile_range(start_mile, end_mile, changeWidth, changerate):
    try:
        gradul_change_start = start_mile - changeWidth/changerate
        gradul_change_end = end_mile + changeWidth/changerate
    except ZeroDivisionError:
        gradul_change_start = start_mile
        gradul_change_end = end_mile
    wide_mile_range_list = [gradul_change_start, start_mile, end_mile, gradul_change_end]
    return wide_mile_range_list


def mileage_clain_change(mileage):

    return mileage


def modify_wideFile_2(wide_mile_range_list: list, position: int, change_width, wide_file_data, change_style='line'):
    '''
    :param wide_mile_range_list: [渐变段起点桩号, 等加宽起点桩号, 等加宽止点桩号, 渐变段止点桩号]
    :param position: 加宽部位
    :param change_width: 加宽宽度
    :param wide_file_data: 加宽前的数据
    :param change_style: 加宽方式，默认为线性加宽
    :return: 加宽后的数据
    '''
    new_wide_date_list = []
    mileage_in_new_wide_date_list = []
    for i in range(len(wide_mile_range_list)):
        wide_mile_range_list[i] = float(wide_mile_range_list[i])
    wide_rows_list = re.findall('.+', wide_file_data)
    for wide_row in wide_rows_list:
        wide_row = re.sub('\t+', ' ', wide_row)
        wide_row = re.sub(' +', ' ', wide_row)
        wide_row_list = re.split(' ', wide_row.strip())
        # print("wide_row_list[0]", wide_row_list[0])
        # print("wide_row", wide_row)
        # wide_row_list[0] = float(wide_row_list[0])
        for j in range(len(wide_row_list)):
            try:
                wide_row_list[j] = float(wide_row_list[j])
            except:
                pass
        # print('wide_mile_range_list:', wide_mile_range_list)
        # print('wide_row_list[0]:', wide_row_list[0])
        if wide_mile_range_list[0] < wide_row_list[0] < wide_mile_range_list[1]:  # 前渐变段
            print('wide_row_list[0]:', wide_row_list[0])
            if wide_mile_range_list[0] in mileage_in_new_wide_date_list is False:
                add_row_wide_data = get_insert_wide_row(wide_mile_range_list[0], new_wide_date_list[-1], wide_row_list)
                new_wide_date_list.append(add_row_wide_data)
                new_wide_date_list.append(add_row_wide_data)
                mileage_in_new_wide_date_list.append(add_row_wide_data[0])
                print(1)
            print(2)
            widen_width = calculate_widen_width(wide_row_list[0], wide_mile_range_list[0], wide_mile_range_list[1],
                                                change_width)
            wide_row_list[position] += widen_width
            # new_wide_date_list.append(wide_row_list)
            # mileage_in_new_wide_date_list.append(wide_row_list[0])
        elif wide_mile_range_list[1] <= wide_row_list[0] <= wide_mile_range_list[2]:  # 加宽段
            wide_row_list[position] += change_width
            if wide_mile_range_list[1] in mileage_in_new_wide_date_list:
                pass
            else:
                print('222222')
                add_row_wide_data = get_insert_wide_row(wide_mile_range_list[1], new_wide_date_list[-1], wide_row_list)
                # add_row_wide_data[position] += change_width
                new_wide_date_list.append(add_row_wide_data)
                new_wide_date_list.append(add_row_wide_data)
                mileage_in_new_wide_date_list.append(add_row_wide_data[0])
            # new_wide_date_list.append(wide_row_list)
            # mileage_in_new_wide_date_list.append(wide_row_list[0])
        elif wide_mile_range_list[2] < wide_row_list[0] <= wide_mile_range_list[3]:  # 后渐变段
            if wide_mile_range_list[2] in mileage_in_new_wide_date_list:
                pass
            else:
                add_row_wide_data = get_insert_wide_row(wide_mile_range_list[2], new_wide_date_list[-1], wide_row_list)
                add_row_wide_data[position] += new_wide_date_list[-1][position]
                new_wide_date_list.append(add_row_wide_data)
                new_wide_date_list.append(add_row_wide_data)
                mileage_in_new_wide_date_list.append(add_row_wide_data[0])
            widen_width = calculate_widen_width(wide_row_list[0], wide_mile_range_list[2], wide_mile_range_list[3],
                                                change_width)
            wide_row_list[position] += widen_width
            # new_wide_date_list.append(wide_row_list)
            # mileage_in_new_wide_date_list.append(wide_row_list[0])
        elif wide_mile_range_list[3] < wide_row_list[0]:
            if wide_mile_range_list[3] in mileage_in_new_wide_date_list:
                pass
            else:
                add_row_wide_data = get_insert_wide_row(wide_mile_range_list[3], new_wide_date_list[-1], wide_row_list)
                add_row_wide_data[position] += wide_row_list[position]
                new_wide_date_list.append(add_row_wide_data)
                new_wide_date_list.append(add_row_wide_data)
                mileage_in_new_wide_date_list.append(add_row_wide_data[0])
            # new_wide_date_list.append(wide_row_list)
            # mileage_in_new_wide_date_list.append(wide_row_list[0])
        mileage_in_new_wide_date_list.append(wide_row_list[0])
        new_wide_date_list.append(wide_row_list)
    return new_wide_date_list


def modify_wideFile(wide_mile_range_list: list, position: int, change_width, wide_file_data, change_style='line'):
    '''
    :param wide_mile_range_list: [渐变段起点桩号, 等加宽起点桩号, 等加宽止点桩号, 渐变段止点桩号]
    :param position: 加宽部位
    :param change_width: 加宽宽度
    :param wide_file_data: 加宽前的数据
    :param change_style: 加宽方式，默认为线性加宽
    :return: 加宽后的数据
    '''
    new_wide_date_list = []
    mileage_in_new_wide_date_list = []
    add_wide_rows_list = []
    for i in range(len(wide_mile_range_list)):
        wide_mile_range_list[i] = float(wide_mile_range_list[i])
    wide_rows_list = re.findall('.+', wide_file_data)
    # 1.将节点桩号数据和wid文件中数据加入到new_wide_date_list
    for wide_row in wide_rows_list:
        wide_row = re.sub('\t+', ' ', wide_row)
        wide_row = re.sub(' +', ' ', wide_row)
        wide_row_list = re.split(' ', wide_row.strip())
        for j in range(len(wide_row_list)):
            try:
                wide_row_list[j] = float(wide_row_list[j])
            except:
                pass
        mileage_in_new_wide_date_list.append(wide_row_list[0])
        new_wide_date_list.append(wide_row_list)
    for mileage_add in wide_mile_range_list:
        if mileage_add in mileage_in_new_wide_date_list:
            pass
        else:
            add_wide_row_list = copy.deepcopy(new_wide_date_list[0])
            add_wide_row_list[0] = mileage_add
            new_wide_date_list.append(add_wide_row_list)
            add_wide_rows_list.append(add_wide_row_list)
    new_wide_date_list = sorted(new_wide_date_list, key=itemgetter(0))
    # print('mileage_in_new_wide_date_list:', mileage_in_new_wide_date_list)
    for tem in new_wide_date_list:
        print(tem)
    # 2.对new_wide_date_list进行加宽处理
    for add_wide_row_list in add_wide_rows_list:

        print(new_wide_date_list.index(add_wide_row_list))
    return new_wide_date_list


def get_insert_wide_row(insert_mileage, last_wide_row: list, next_wide_row: list):
    insert_wide_row = copy.deepcopy(last_wide_row)
    insert_wide_row[0] = float(insert_mileage)
    for j in range(1, len(last_wide_row)):
        try:  # 线性插值
            insert_wide_row[j] = (float(insert_wide_row[0]) - float(last_wide_row[0])) / (
                    float(next_wide_row[0]) - float(last_wide_row[0])) * (
                                         float(next_wide_row[j]) - float(last_wide_row[j]))+float(last_wide_row[j])
            insert_wide_row[j] = round(insert_wide_row[j], 3)
        except TypeError:  # 宽度引用情况
            insert_wide_row[j] = 0
        except ZeroDivisionError:
            pass
        except IndexError:
            print('有可能是new_wide_date_list错误')
            pass
    return insert_wide_row


def calculate_widen_width(mileage, start_mileage, end_mileage, change_width, change_style='line'):
    widen_width = 0
    if change_style == 'line':
        try:
            widen_width = (mileage-start_mileage)/(end_mileage-start_mileage)*change_width
        except ZeroDivisionError:
            widen_width = 0
    return widen_width


def error_log(err_str):
    with open('err_log.txt', 'a', encoding='utf-8') as file:
        file.write(err_str)


def main():
    wide_file_path = '踏石路.WID'
    widen_range_file_path = '护栏.txt'
    new_wide_file_path = 'new' + wide_file_path

    wide_model = HintWide()
    list_file_data = read_wide_file(wide_file_path)
    # for wide_data in list_file_data:
    #     print('------------------------')
    #     print(wide_data)

    with open(widen_range_file_path, encoding='utf-8') as widen_file:
        widen_file_data = widen_file.read()
    widen_file_data = widen_file_data.split('\n')
    for widen_str in widen_file_data:
        widen_str = re.sub('\t+', ' ', widen_str)
        widen_str = re.sub(' +', ' ', widen_str)
        widen_list = re.split('[ \t]', widen_str)
        try:
            widen_dic = {
                'start_mile': float(widen_list[0]),
                'end_mile': float(widen_list[1]),
                'LOR': wide_model.lors[widen_list[2]],
                'position': wide_model.postions[widen_list[3]],
                'changeWidth': float(widen_list[4]),
                'change_rate': eval(str(widen_list[5])),
            }
        except Exception as e:
            err_str = widen_str+'\t'+str(e)+'\n'
            error_log(err_str)
            continue

        wide_mile_range_list = wide_mile_range(widen_dic['start_mile'], widen_dic['end_mile'], widen_dic['changeWidth'], widen_dic['change_rate'])
        # print(wide_mile_range_list)
        # print(widen_dic['change_rate'])
        new_wide_date_list = modify_wideFile(wide_mile_range_list, position=widen_dic['position'], change_width=widen_dic['changeWidth'], wide_file_data=list_file_data[widen_dic['LOR']])
        list_file_data[widen_dic['LOR']] = new_wide_date_list
        # print(new_wide_date_list)

    with open(new_wide_file_path, 'w') as new_file:
        head_text = 'HINTCAD6.00_WID_SHUJU'
        new_file.write(head_text + '\n' + '[LEFT]\n')
        new_file.write(str(list_file_data[0]).replace(']', '\n').replace('[', '').replace(',', '\t'))
        new_file.write('[RIGHT]\n')
        new_file.write(str(list_file_data[1]).replace(']', '\n').replace('[', '').replace(',', '\t'))


if __name__ == "__main__":
    main()
    # a = list(range(5))
    # print(a)
    # if 1 in a is False:
    #     print(1)
    # else:
    #     print(2)

    # students = [[3, 'Jack', 12], [2, 'Rose', 13], [1, 'Tom', 10], [5, 'Sam', 12], [4, 'Joy', 8]]
    # t = sorted(students, key=itemgetter(2))
    # print(t)