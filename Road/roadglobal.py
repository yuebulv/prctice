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
cuttingSlopeLevel_setInterceptingDitch = [2, 4, 6, 8]  #[2, 4, 6, 8]  # [1, 2, 3, 4, 5, 6, 7, 8]  # 边坡截水沟设置于第i级边坡
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

regx_chainage_between_chainage = r'^\w?[Kk]\d+\+\d+(?:.+[\n\r]){2}(?:.+(?:z=0\.0000\ *[\n\r]))+'
def regx_FindXPathFromPrj(typeOfFindX):
    # return f'\*\.{typeOfFindX}\).*=\s*(.*)\s*(?=\n)'
    return f'\*\.{typeOfFindX}\).*=(.*)(?=\n)'