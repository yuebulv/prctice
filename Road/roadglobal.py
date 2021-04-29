#查找纬地项目文件prjpath中X文件路径，例FindXPathFromPrj(prjpath,3dr)
slopelevel_max = 8 # 默认边坡最大级数
tableName_of_slopeInGroup = 'slopeInGroup'
tableName_of_platformDrainInGroup = 'platformDrainInGroup'
# 急流槽配置参数
cutting_rapidGutter_spacing = 40  # 挖方边坡急流槽间距
embankment_rapidGutter_spacing = 50
cuttingSlopeLevel_setInterceptingDitch = [1, 2, 3, 4, 5, 6, 7, 8]  # 边坡截水沟设置于第i级边坡
embankmentSlopeLevel_setInterceptingDitch = [1, 2, 3, 4, 5, 6, 7, 8]


def regx_FindXPathFromPrj(typeOfFindX):
    # return f'\*\.{typeOfFindX}\).*=\s*(.*)\s*(?=\n)'
    return f'\*\.{typeOfFindX}\).*=(.*)(?=\n)'