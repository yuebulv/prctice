# coding:utf-8


def getNumofCommonSubstr(str1, str2):
    '''
    求两个字符串的最长公共子串
    思想：建立一个二维数组，保存连续位相同与否的状态
    :return (最长公共子串，长度)
    '''
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位
    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return str1[p - maxNum:p], maxNum


def intersect(string1, string2):
    common = []
    for char in set(string1):
        common.extend(char * min(string1.count(char), string2.count(char)))
    return common


def str_map_factory(map_str, map_dic: dict) -> str:
    '''
    :功能：如果map_str中包含条件中的关键字时，返回关键字对应Key值
    :param map_dic: {'map到的值': [('map_str中要包含的关键字1', 'map_str中要包含的关键字2'), ('或者map_str中要包含的关键字1', 'I')],}
    :param map_str:
    :return:
    :例:{
            '挖方总数量': [('挖', '总数量')],
            '挖土方软土': [('挖', '软土'), ('挖', 'I')],
        }
    '''
    is_this_column_port = False
    for column_port in map_dic:
        # print(column_port)
        for column_key_words in map_dic[column_port]:
            for column_key_word in column_key_words:
                # if column_key_word not in column_str:
                if map_str.find(column_key_word) == -1:
                    is_this_column_port = False
                    break
                else:
                    is_this_column_port = True
                # print(f'{column_key_word},是否在{map_str}中：{is_this_column_port}')
            if is_this_column_port:
                return column_port
    return map_str


def alias_of_file(file_name_str) -> str:
    # 给文件取别名
    # 效率比较低
    alias_str = '排水工程，防护，路面，每公里,涵洞，特殊，新旧，夯实，用地，护栏，标志，青苗，砍树，技术指标'
    alias = getNumofCommonSubstr(file_name_str, alias_str)
    return alias[0]


def value_to_numeric(value, num_type='float'):
    exp = f'{num_type}({value})'
    try:
        # value = float(value)
        value = round(eval(exp), 3)
    except:
        pass
    return value


if __name__ == "__main__":
    # str1 = "SZYS06010111 每公里土石方数量表汇总表"
    # str2 = '路面，防护，排水，每公里'
    # tem = getNumofCommonSubstr(str1, str2)
    # print(tem)

    tem = '1.2a'
    tem = value_to_numeric(tem)
    print(tem)