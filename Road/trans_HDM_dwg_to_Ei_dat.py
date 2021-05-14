'''
功能：
一、从横断面图dwg中提到到设计线坐标等数据；（lisp程序功能）
二、通过设计线坐标等数据得到EI数据的dat文件和are文件（本程序功能）
    一）、通过设计线坐标等数据得到EI数据的dat文件
        1、通过分离式路基线-中心线判断本路线与相交路线界线；
        2、通过中心线分左右侧
        顶点无分支，坡度相同，顶点坐标相同直线合并
        闭合多边形，挡墙
        3、识别四边形
            1）、可能是挡墙基础，边沟盖板，水沟
        识别三边形（口向上）
            1）、可能是水沟
        识别三边形（口向下）
            1）、可能是挡墙
        特殊图形内的所有直线、多段线都不输出
        第一个X只对应一个Y

    二）、通过设计线坐标等数据得到EI数据的are文件
'''