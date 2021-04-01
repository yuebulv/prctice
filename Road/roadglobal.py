#查找纬地项目文件prjpath中X文件路径，例FindXPathFromPrj(prjpath,3dr)
def regx_FindXPathFromPrj(typeOfFindX):
    # return f'\*\.{typeOfFindX}\).*=\s*(.*)\s*(?=\n)'
    return f'\*\.{typeOfFindX}\).*=(.*)(?=\n)'