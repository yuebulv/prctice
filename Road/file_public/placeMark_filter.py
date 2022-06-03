from file_public import getData_list
import re
import os


def placeNameFilter_kml(placeNameFilter: list, path_kml, reg: str, en="UTF-8") -> str:
    regx = reg
    path = path_kml
    if not os.path.exists(path):
        return f"{path}文件不存在"
    with open(path, 'r', encoding=en) as file:
        fileData = file.read()
    fileData_list = re.findall(regx, fileData, re.MULTILINE)
    newName_list = []
    tem_list = []
    for data_name in fileData_list:
        for filter in placeNameFilter:
            if filter.replace(" ", "").replace(r"\t", "") in data_name.replace(" ", "").replace(r"\t", ""):
                tem_list.append(re.findall(r"<name>(.+)</name>", data_name, re.MULTILINE)[0])
                newName_list.append(data_name)
                break
        # if placeNameFilter in data_name:
        #     newName_list.append(data_name)
    print(newName_list)
    print(len(newName_list))
    # print(set(placeNameFilter).symmetric_difference(set(tem_list)))
    # with open(r"F:\20220524大竹县农村公路安全生命防护工程\O-奥维\new.kml", "a", encoding="UTF-8") as file:
    #     file.write("\n".join(tem_list))
    result = "\n".join(newName_list)
    return result


def diff_list():
    path = r"F:\20220524大竹县农村公路安全生命防护工程\O-奥维\countryName_all.kml"
    with open(path, 'r', encoding="UTF-8") as file:
        fileData = file.read()
    fileData_list = re.findall(r"<name>(.+)</name>", fileData, re.MULTILINE)

    filterNamePath_txt = r"F:\20220524大竹县农村公路安全生命防护工程\O-奥维\countryName.txt"
    if not os.path.exists(filterNamePath_txt):
        print(f"{filterNamePath_txt}文件不存在")
        exit()
    with open(filterNamePath_txt, 'r', encoding="UTF-8") as file:
        fileData = file.read()
    placeName_filter = re.findall(".+[村|乡|镇]", fileData, re.MULTILINE)

    print(set(placeName_filter).symmetric_difference(set(fileData_list)))


if __name__ == '__main__':
    # filterNamePath_txt = r"F:\20220524大竹县农村公路安全生命防护工程\O-奥维\countryName.txt"
    # if not os.path.exists(filterNamePath_txt):
    #     print(f"{filterNamePath_txt}文件不存在")
    #     exit()
    # with open(filterNamePath_txt, 'r', encoding="UTF-8") as file:
    #     fileData = file.read()
    # placeName_filter = re.findall(".+[村|乡|镇]", fileData, re.MULTILINE)
    # print(placeName_filter)
    # print(len(placeName_filter))
    # # placeName_filter = ["大竹县", "互助村"]
    # path_kml = r"F:\20220524大竹县农村公路安全生命防护工程\O-奥维\countryName_all.kml"
    # reg = r"<Placemark>(?:.*\s*){3}</Placemark>"
    # text = placeNameFilter_kml(placeName_filter, path_kml, reg)
    # newKmlPath = r"F:\20220524大竹县农村公路安全生命防护工程\O-奥维\new.kml"
    # with open(newKmlPath, "a", encoding="UTF-8") as file:
    #     file.write(text)
    diff_list()