#查找纬地项目文件prjpath中X文件路径，例FindXPathFromPrj(prjpath,3dr)
slopelevel_max = 8  # 默认边坡最大级数
# 数据表名称
tableName_of_slopeInGroup = 'slope_In_Group'
tableName_of_drainageDitchInGroup = 'drainage_Ditch_In_Group'
tableName_of_platformDrainInGroup = 'platform_Drain_In_Group'
tableName_of_rapidGutters = 'rapid_gutters_c'  # 'rapidGutters' C型急流槽数据表名称
# 急流槽配置参数
cutting_rapidGutter_spacing = 50  # 挖方边坡急流槽间距
embankment_rapidGutter_spacing = 100
embankment_rapidGutter_spacing_sup = 50  # 超高侧填方边坡急流槽间距
cuttingSlopeLevel_setInterceptingDitch =[1, 2, 3, 4, 5, 6, 7, 8]  # [2, 4, 6, 8]  # [1, 2, 3, 4, 5, 6, 7, 8]  # 边坡截水沟设置于第i级边坡
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

# 下（上）挡墙尺寸范围，通过横断图转dat文件是需要设置
min_width_top_wall = 0.45
max_width_top_wall = 2
max_gradient_side_wall = 0.5  # 墙顶两侧侧墙的最大坡度1：X，不分正负
min_height_side_wall = 1  # 墙顶两侧侧墙最小高度

# 云南院防护类型
protection_type = ((1, 0, 100000, -5, -1, 1, 1, 1, 10, -4, 0, -4, 0, '', '三维网植被网护坡'),
                     (2, 0, 100000, -5, -1, 1, 10, 1, 10, -60, -0, -60, -4, '', '填方拱形骨架衬砌护坡'),
                     (3, 0, 100000, 0.5, 1.5, 1, 10, 1, 10, 0, 3, 0, 3, '', '挖方喷播植草护坡'),
                     (4, 0, 100000, 0.5, 1.5, 1, 2, 1, 2, 0, 20, 4, 21, '', '现浇砼拱形骨架'),
                     (5, 0, 100000, 0.1, 1.5, 1, 3, 3, 3, 0, 30, 20, 31, '', '锚杆框架梁植草防护'),
                     (6, 0, 100000, 0.1, 1.5, 1, 10, 4, 10, 0, 100, 30, 100, '', '深挖路基'),
                     (7, 0, 100000, 1.5, 9999, 1, 10, 1, 10, 0, 100, 0, 100, '', '特殊挖方边坡'),
                     (8, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -15, -1, -15, -1, '', '路肩墙'),
                     (9, 0, 100000, -0.3, -0.01, 1, 1, 1, 2, -1, 0, -1, -0, '', '护肩'),
                     (10, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -14, -2, -34, 0, '', '路堤墙'),
                     (11, 0, 100000, -0.3, -0.01, 2, 10, 2, 10, -2, -1, -100, -0, '', '护脚'))

regx_chainage_between_chainage = r'^\w?[Kk]\d+\+\d+(?:.+[\n\r]){2}(?:.+(?:z=0\.0000\ *[\n\r]))+'


def regx_FindXPathFromPrj(typeOfFindX):
    # return f'\*\.{typeOfFindX}\).*=\s*(.*)\s*(?=\n)'
    return f'\*\.{typeOfFindX}\).*=(.*)(?=\n)'


def regx_exclude_str(str1, str2):
    # 按行分组，且此行中不含str1,str2字符，str1,str2顺序可换
    return f'^(?:(?!{str1}).(?!{str2}))*$'