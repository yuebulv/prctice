#查找纬地项目文件prjpath中X文件路径，例FindXPathFromPrj(prjpath,3dr)
slopelevel_max = 8  # 默认边坡最大级数
# 数据表名称
tableName_of_slopeInGroup = 'slope_In_Group'
tableName_of_drainageDitchInGroup = 'drainage_Ditch_In_Group'
tableName_of_platformDrainInGroup = 'platform_Drain_In_Group'
tableName_of_rapidGutters = 'rapid_gutters_c'  # 'rapidGutters' C型急流槽数据表名称
# 急流槽配置参数
cutting_rapidGutter_spacing = 50  # 挖方边坡急流槽间距
embankment_rapidGutter_spacing = 25.3  # 初始值100
embankment_rapidGutter_spacing_sup = 25.3  # 超高侧填方边坡急流槽间距 初始值50
cuttingSlopeLevel_setInterceptingDitch = [1, 2, 3, 4, 5, 6, 7, 8]  # [2, 4, 6, 8]  # [1, 2, 3, 4, 5, 6, 7, 8]  # 边坡截水沟设置于第i级边坡
embankmentSlopeLevel_setInterceptingDitch = [1, 2, 3, 4, 5, 6, 7, 8]
tableName_of_rapidGutters_b = 'rapid_gutters_b'  # B型急流槽数据表名称
tableName_of_rapidGutters_a = 'rapid_gutters_a'  # B型急流槽数据表名称
rapid_gutter_b_slope_min = 1.5  # B型急流槽（填挖交界）最小坡度
embankment_slope_max = -1  # 路堤最大坡度，为负数（A型急流槽设置的最大坡度）

# 纬地tf文件格式
tfTitle_dic = {'桩号': 1, '挖方面积': 2, '填方面积': 3, '中桩填挖': 4, '路基左宽': 5, '路基右宽': 6, '基缘左高': 7, '基缘右高': 8,
               '左坡脚距': 9, '右坡脚距': 10, '左坡脚高': 11, '右坡脚高': 12, '左沟缘距': 13, '右沟缘距': 14, '左护坡道宽': 15,
               '右护坡道宽': 16, '左沟底高': 17, '右沟底高': 18, '左沟心距': 19, '右沟心距': 20, '左沟深度': 21, '右沟深度': 22,
               '左用地宽': 23, '右用地宽': 24, '清表面积': 25, '顶超面积': 26, '左超面积': 27, '右超面积': 28, '计排水沟': 29,
               '左沟面积填': 30, '左沟面积挖': 31, '右沟面积填': 32, '右沟面积挖': 33, '路槽面积填': 34, '路槽面积挖': 35,
               '清表宽度': 36, '清表厚度': 37, '挖1类面积': 38, '挖2类面积': 39, '挖3类面积': 40, '挖4类面积': 41, '挖5类面积': 42,
               '挖6类面积': 43, '左路槽B': 44, '右路槽B': 45, '左路槽': 46, '右路槽': 47, '左垫层': 48, '右垫层': 49, '左路床': 50,
               '右路床': 51, '左土肩培土': 52, '右土肩培土': 53, '左包边土': 54, '右包边土': 55, '左边沟回填': 56, '右边沟回填': 57,
               '左截沟填': 58, '左截沟挖': 59, '右截沟填': 60, '右截沟挖': 61, '挖台阶面积': 62}

# 纬地tf文件格式
ljTitle_dic = {'桩号': 1, '地面标高': 2, '设计标高': 3, '左侧土路肩宽度': 4, '左侧硬路肩宽度': 5, '左侧引用车道宽度': 6, '左侧行车道宽度': 7,
               '左半幅中分带宽度': 8, '右半幅中分带宽度': 9, '右侧行车道宽度': 10, '右侧引用车道宽度': 11, '右侧硬路肩宽度': 12,
               '右侧土路肩宽度': 13, '左侧土路肩高差': 14, '左侧硬路肩高差': 15, '左侧引用车道高差': 16, '左侧行车道高差': 17,
               '左半幅中分带高差': 18, '中心设计高差': 19, '右半幅中分带高差': 20, '右侧行车道高差': 21, '右侧引用车道高差': 22,
               '右侧硬路肩高差': 23, '右侧土路肩高差': 24}


# 下（上）挡墙尺寸范围，通过横断图转dat文件是需要设置
min_width_top_wall = 0.45
max_width_top_wall = 2
max_gradient_side_wall = 0.55  # 墙顶两侧侧墙的最大坡度1：X，不分正负，重力式挡墙胸墙坡度可取到0.55
min_height_side_wall = 1  # 墙顶两侧侧墙最小高度

# # 云南院防护类型 含直立挡墙（注意：会和分离式混淆）
# # id chainagemin chainagemax 坡度min 坡度max 第i级min 第i级max 最大级数min 最大级数max 高度min 高度max 坡高min 坡高max 地质 防护类型
# protection_type = ((1, 0, 100000, -5, -1, 1, 1, 1, 10, -4, 0, -4, 0, '', '三维网植被网护坡'),
#                      (2, 0, 100000, -5, -1, 1, 10, 1, 10, -60, -0, -60, -4, '', '填方拱形骨架衬砌护坡'),
#                      (3, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 3, 0, 3, '', '挖方喷播植草护坡'),
#                      (4, 0, 100000, 0.5, 1.5, 1, 2, 1, 2, 0, 20, 4, 21, '', '现浇砼拱形骨架'),
#                      (5, 0, 100000, 0.1, 1.5, 1, 3, 3, 3, 0, 30, 20, 31, '', '锚杆框架梁植草防护'),
#                      (6, 0, 100000, 0.1, 1.5, 1, 10, 4, 10, 0, 100, 30, 100, '', '深挖路基'),
#                      (7, 0, 100000, 1.5, 9999, 1, 10, 1, 10, 0, 100, 0, 100, '', '特殊挖方边坡'),
#                      (8, 0, 100000, -0.3, 0, 1, 1, 0, 2, -15, -1, -15, 0, '', '路肩墙'),
#                      (9, 0, 100000, -0.3, 0, 1, 1, 0, 2, -1, 0, -1, -0, '', '护肩'),
#                      (10, 0, 100000, -0.3, 0, 2, 10, 2, 10, -14, -2, -34, 0, '', '路堤墙'),
#                      (11, 0, 100000, -0.3, 0, 2, 10, 2, 10, -2, -1, -100, -0, '', '护脚'))

# # 云南院防护类型
# protection_type = ((1, 0, 100000, -5, -1, 1, 1, 1, 10, -4, 0, -4, 0, '', '三维网植被网护坡'),
#                      (2, 0, 100000, -5, -1, 1, 10, 1, 10, -60, -0, -60, -4, '', '填方拱形骨架衬砌护坡'),
#                      (3, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 3, 0, 3, '', '挖方喷播植草护坡'),
#                      (4, 0, 100000, 0.5, 1.5, 1, 2, 1, 2, 0, 20, 4, 21, '', '现浇砼拱形骨架'),
#                      (5, 0, 100000, 0.1, 1.5, 1, 3, 3, 3, 0, 30, 20, 31, '', '锚杆框架梁植草防护'),
#                      (6, 0, 100000, 0.1, 1.5, 1, 10, 4, 10, 0, 100, 30, 100, '', '深挖路基'),
#                      (7, 0, 100000, 1.5, 9999, 1, 10, 1, 10, 0, 100, 0, 100, '', '特殊挖方边坡'),
#                      (8, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -15, -1, -15, -1, '', '路肩墙'),
#                      (9, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -1, 0, -1, -0, '', '护肩'),
#                      (10, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -14, -2, -34, 0, '', '路堤墙'),
#                      (11, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -2, -1, -100, -0, '', '护脚'))

# # 贵州院防护类型
# protection_type = ((1, 0, 100000, -5, -1, 1, 1, 1, 10, -3, 0, -3, 0, '', '填方喷播植草'),
#                     (2, 0, 100000, -5, -1, 1, 10, 1, 10, -8, -0, -8, -3, '', '填方挂三维网植草护坡'),
#                      (3, 0, 100000, -5, -1, 1, 10, 1, 10, -60, -0, -60, -8, '', '填方拱形骨架衬砌护坡'),
#                      (4, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 4, 0, 4, '', '挖方喷播植草护坡'),
#                      (5, 0, 100000, 0.5, 1.5, 1, 2, 1, 2, 0, 20, 4, 21, '', '挖方拱形骨架衬砌护坡'),
#                      (6, 0, 100000, 0.2, 1.5, 1, 3, 3, 3, 0, 30, 20, 31, '', '锚杆框架梁植草防护'),
#                      (7, 0, 100000, 0.1, 1.5, 1, 10, 4, 10, 0, 100, 30, 100, '', '深挖路基'),
#                      (8, 0, 100000, 1.5, 9999, 1, 10, 1, 10, 0, 100, 0, 100, '', '特殊挖方边坡'),
#                      (9, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -15, -1, -15, -1, '', '路肩墙'),
#                      (10, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -1, 0, -1, -0, '', '护肩'),
#                      (11, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -14, -2, -34, 0, '', '路堤墙'),
#                      (12, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -2, -1, -100, -0, '', '护脚'))

# # 中交二院四分院防护类型
# protection_type = ((1, 0, 100000, -5, -1, 1, 1, 1, 10, -3, 0, -3, 0, '', '填方喷播植草'),
#                     (2, 0, 100000, -5, -1, 1, 10, 1, 10, -6, -0, -6, -3, '', '填方挂三维网植草防护'),
#                      (3, 0, 100000, -5, -1, 1, 10, 1, 10, -60, -0, -60, -6, '', '人字形骨架植草防护'),
#                      (4, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 4, 0, 4, '', '挖方喷播植草护坡'),
#                      (5, 0, 100000, 0.5, 1.5, 1, 2, 1, 2, 0, 20, 4, 21, '', '挖方拱形骨架衬砌护坡'),
#                      (6, 0, 100000, 0.2, 1.5, 1, 3, 3, 3, 0, 30, 20, 31, '', '锚杆框架梁植草防护'),
#                      (7, 0, 100000, 0.1, 1.5, 1, 10, 4, 10, 0, 100, 30, 100, '', '深挖路基'),
#                      (8, 0, 100000, 1.5, 9999, 1, 10, 1, 10, 0, 100, 0, 100, '', '特殊挖方边坡'),
#                      (9, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -15, -1, -15, -1, '', '路肩墙'),
#                      (10, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -1, 0, -1, -0, '', '护肩'),
#                      (11, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -14, -2, -34, 0, '', '路堤墙'),
#                      (12, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -2, -1, -100, -0, '', '护脚'))

# 中铁长江交通设计集团防护类型
# # id chainagemin chainagemax 坡度min 坡度max 第i级min 第i级max 最大级数min 最大级数max 高度min 高度max 坡高min 坡高max 地质 防护类型
# protection_type = ((1, 0, 100000, -5, -1, 1, 1, 1, 10, -4, 0, -4, 0, '', '填方喷播植草'),
#                     (2, 0, 100000, -5, -1, 1, 10, 1, 10, -20, -0, -20, -4, '', '预制人字形骨架'),
#                      (3, 0, 100000, -5, -1, 1, 10, 1, 10, -60, -0, -60, -20, '', '高填方'),
#                      (4, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 8, 0, 8, '', '三维网植草防护'),
#                      (5, 0, 100000, 0.5, 1.5, 1, 2, 1, 2, 0, 20, 8, 21, '', '挖方拱形骨架防护'),
#                      (6, 0, 100000, 0.2, 1.5, 1, 3, 3, 3, 0, 30, 20, 31, '', '锚杆框架梁植草防护'),
#                      (7, 0, 100000, 0.1, 1.5, 1, 10, 4, 10, 0, 100, 30, 100, '', '深挖路基'),
#                      (8, 0, 100000, 1.5, 9999, 1, 10, 1, 10, 0, 100, 0, 100, '', '特殊挖方边坡'),
#                      (9, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -15, -1, -15, -1, '', '路肩墙'),
#                      (10, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -1, 0, -1, -0, '', '护肩'),
#                      (11, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -14, -2, -34, 0, '', '路堤墙'),
#                      (12, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -2, -1, -100, -0, '', '护脚'))

# 中交二院
protection_type = ((1, 0, 100000, -5, -1, 1, 1, 1, 10, -3, 0, -3, 0, '', '三维网植被网护坡'),
                     (2, 0, 100000, -5, -1, 1, 10, 1, 10, -60, -0, -60, -3, '', '填方拱形骨架衬砌护坡'),
                     (3, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 4, 0, 4, '', '挖方喷播植草护坡'),
                     (4, 0, 100000, 0.5, 1.5, 1, 2, 1, 2, 0, 20, 4, 21, '', '现浇砼拱形骨架'),
                     (5, 0, 100000, 0.1, 1.5, 1, 3, 3, 3, 0, 30, 20, 31, '', '锚杆框架梁植草防护'),
                     (6, 0, 100000, 0.1, 1.5, 1, 10, 4, 10, 0, 100, 30, 100, '', '深挖路基'),
                     (7, 0, 100000, 1.5, 9999, 1, 10, 1, 10, 0, 100, 0, 100, '', '特殊挖方边坡'),
                     (8, 0, 100000, -0.3, 0, 1, 1, 0, 2, -15, -1, -15, 0, '', '路肩墙'),
                     (9, 0, 100000, -0.3, 0, 1, 1, 0, 2, -1, 0, -1, -0, '', '护肩'),
                     (10, 0, 100000, -0.3, 0, 2, 10, 2, 10, -14, -2, -34, 0, '', '路堤墙'),
                     (11, 0, 100000, -0.3, 0, 2, 10, 2, 10, -2, -1, -100, -0, '', '护脚'))

# 过虑器
# 1 水沟过虑器
drainageFilter1 = ['height[1]<0', '0<=abs(gradient[1])<=2']  # 第1条边判定条件
drainageFilter2 = ['width[2]!=0', '5<=abs(gradient[2])<=9999', 'width[1]*width[2]>=0',]  # 第2条边判定条件
drainageFilter3 = ['0<height[3]', '0<=abs(gradient[3])<=2', 'width[2]*width[3]>=0']  # 第3条边判定条件
drain_filter = [drainageFilter1, drainageFilter2, drainageFilter3]  # 必须一条线一个元素

# regx_chainage_between_chainage = r'^\w?[Kk]\d+\+\d+(?:.+[\n\r]){2}(?:.+(?:z=0\.0000\ *[\n\r]))+'
# debug_20250112 上式中regx_chainage_between_chainage桩号前缀多于1个 如LZK时，无法划分
regx_chainage_between_chainage = r'^\w?\w?[Kk]\d+\+\d+(?:.+[\n\r]){2}(?:.+(?:z=0\.0000\ *[\n\r]))+'
regx_get_filename_from_path = r'.+/(\w+(?:\w*\.*)*)\.\w+$'  # 提取路径中文件名

def regx_FindXPathFromPrj(typeOfFindX):
    # return f'\*\.{typeOfFindX}\).*=\s*(.*)\s*(?=\n)'
    return f'\*\.{typeOfFindX}\).*=(.*)(?=\n)'


def regx_exclude_str(str1, str2):
    # 按行分组，且此行中不含str1,str2字符，str1,str2顺序可换
    return f'^(?:(?!{str1}).(?!{str2}))*$'


# 纬地dmx文件中查找桩号是否存在
def regx_is_key_in_dmx(key):
    if key.find('.') == -1:  # 判断是整桩号还是含小数桩号
        regx = f'^(?<!\w)\s*({key}(?:\.0+)?)(?!\w)'
    else:
        regx = f'^(?<!\w)\s*({key}0*)(?!\w)'
    return regx


# 纬地wid文件中查找加宽数据，自动分左右
def regx_wide():
    regx = f'\]([\d.\s]+[^\[\]]+)'
    return regx


# EI dat文件中分组提取断面信息
def regx_eiDat_hdmData():
    regx = r'^\d+\.\d+[\r\n]+(?:(?:(?:-?\d+\.\d+ ?\d*){3}|\d+)[\r\n]+)+'
    return regx