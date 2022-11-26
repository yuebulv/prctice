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


if __name__ == "__main__":
    str1 = "SZYS06010111 每公里土石方数量表汇总表"
    str2 = '路面，防护，排水，每公里'
    tem = getNumofCommonSubstr(str1, str2)
    print(tem)