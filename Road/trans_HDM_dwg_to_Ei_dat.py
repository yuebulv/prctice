'''
功能：
一、从横断面图dwg中提到到设计线坐标等数据；（lisp程序功能）
    1、将横断面图中路床、路面结构、占地线删除
    2、只保留设计线、边沟、挡墙、桥隧、中心线、分离式路基中心线
二、通过设计线坐标等数据得到EI数据的dat文件和are文件（本程序功能）
    一）、通过设计线坐标等数据得到EI数据的dat文件
        1、通过分离式路基线-中心线判断本路线与相交路线界线；
            分离式路基线-中心线重合时输出错误
        2、通过中心线分左右侧

        3、挡墙识别
            默认组成挡墙线条为闭合图形
            连续三条边类似形状：/-\，顶宽>=0.45m，两条边不能同时为直立边坡，（标识挡墙与墙背）
            与挡墙底边相连的图形为挡墙基座
            与挡墙基座相连的图形为挡墙基座
            输出的dat文件中挡墙以一条线代替，这条线的坡度、高度以/-\结构中的墙背为准
        4、水沟识别
            非挡墙

            连续三条边类似形状：\_/
            同一处有两条水沟线时，只留内沟线，舍弃衬砌线（标识水沟）
        5、中央分隔带、行车道、硬路肩、土路肩识别
            优先级：土路肩（0.25-0.75）、行车道（>=1.5m）、硬路肩、中央分隔带（第4段以后全为中央分隔带）
        6、填方边坡、挖方边坡识别
        7、去除平台截水沟
        8、按dat格式连接各部位
        9、输出dat


            1		        整幅路基
    1	中央分隔带	整幅路基
    1		        整幅路基
    1	路缘带	    整幅路基
    2	行车道	    整幅路基	桥梁
    3		        整幅路基	桥梁
    4		        整幅路基	桥梁
    5	土路肩	    整幅路基	桥梁
    6	填方边坡	    整幅路基
    7	边沟\排水沟	整幅路基
    8	挖方边坡	    整幅路基

顶点无分支，坡度相同，顶点坐标相同直线合并
    二）、通过设计线坐标等数据得到EI数据的are文件
公路BIM软件默认设置下出的横断面图特点：
    1、多段线：路面结构、路床、占地线；
    2、直线：中心线、分离式路基线、设计线、挡墙、水沟；
'''
import road
import roadglobal
import re
def hdm_separated_road_handle():
    # 1、通过分离式路基线-中心线判断本路线与相交路线界线；
    hdm_data_path = r'C:\Users\Administrator.DESKTOP-95R7ULF\Desktop\s.txt'
    layer_name = '图层分离式路基中心线'
    layer_name_zxx = '图层中心线'

    hdm_no_separated_road = []  # 去除分离式路基后的横断面坐标
    err_list = []
    try:
        file = open(hdm_data_path, 'r')
    except:
        msgbox=road.gui_filenotfine(f'{hdm_data_path}文件不存在')
        return ''
    filedata = file.read().lower()
    regx = roadglobal.regx_chainage_between_chainage
    hdms_xyz_list = re.findall(regx, filedata, re.MULTILINE)  #所有横断面的文件及文字标注
    file.close()
    print(f'len((hdms_xyz_list)):{len((hdms_xyz_list))}')
    for hdm_xyz_list in hdms_xyz_list:  # 每个断面
        xyz_lines_chainage = []
        xyz_line_chainage_dic = {}  # {chainage:K0+000,text:'左路基宽 = 3.35 左边距 = 3.35',left_lines:[left_line...],right_lines:[right_line...]}
        left_line = []  # left_line =[[x,y,z],[x,y,z]...]
        right_line = []  # right_line =[[x,y,z],[x,y,z]...]
        # regx_separated = f'.+{layer_name}.+'
        # separated_xyz = re.findall(regx_separated, hdm_xyz_list, re.MULTILINE)
        # print(f'separated_xyz:{separated_xyz}')
        # regx_x = r'x=(\d+\.?\d+)'
        # try:
        #     separated_x = re.findall(regx_x, separated_xyz[0], re.MULTILINE)  # 分离式路基中心线X坐标
        # except IndexError:
        #     # 无分离式路基
        #     pass
        # else:
        #     # 有分离式路基
        #     pass
        regx_x = f'{layer_name}.+X=(\d+\.?\d+)\s*Y=(\d+\.?\d+)\s*z=(\d+\.?\d+)'
        separated_x = re.findall(regx_x, hdm_xyz_list, re.MULTILINE)  # 分离式路基中心线X坐标

        regx_x = f'{layer_name_zxx}.+X=(\d+\.?\d+)\s*Y=(\d+\.?\d+)\s*z=(\d+\.?\d+)'
        zxx_x = re.findall(regx_x, hdm_xyz_list, re.MULTILINE)  # 路基中心线X坐标
        regx_line = r'.+'
        hdm_lines = re.findall(regx_line, hdm_xyz_list, re.MULTILINE)
        if len(zxx_x) == 0:
            err_txt = f'hdm_separated_road_handle错误：{hdm_lines[0]}无中心线，或者中心线特征字符{layer_name_zxx}不存在,请检查{hdm_data_path}文件。'
            err_list.append(err_txt)
            continue
        else:
            zxx_x[0] = float(zxx_x[0])
        try:
            separated_x[0] = float(separated_x[0])
        except IndexError:
            symbol = '!=-123456789'
        else:
            if separated_x[0] > zxx_x[0]:
                symbol = '<' + str(separated_x[0])
            elif separated_x[0] < zxx_x[0]:
                symbol = '>' + str(separated_x[0])
            else:
                err_txt = 'hdm_separated_road_handle错误：分离式路基中心线X坐标与路基中心线X坐标相等，无法判断断面在分离式左侧还是右侧，请手动修改'
                err_list.append(err_txt)
                continue
        xyz_line_chainage_dic['chainage'] = hdm_lines[0]
        xyz_line_chainage_dic['text'] = hdm_lines[1]
        for hdm_line in hdm_lines:  # 每条线
            regx_xyz = r'x=(\d+\.?\d+)\s*y=(\d+\.?\d+)\s*z=(\d+\.?\d+)'
            xyz_line_chainage = re.findall(regx_xyz, hdm_line, re.MULTILINE)
            print(hdm_line)
            print(f'xyz_line_chainage:{xyz_line_chainage}')
            print(f'len(xyz_line_chainage){len(xyz_line_chainage)}')
            # if len(xyz_line_chainage) == 0:
            #     if len(hdm_line.strip()) != 0:
            #         xyz_line_chainage_list.
            for xyz_point in xyz_line_chainage:  # 线中每个点
                print(f'xyz_point:{xyz_point}')

if __name__ == "__main__":
    s = hdm_separated_road_handle()
    # temp = '== True'
    # a = str(4) + temp #+ str(2)
    # te = eval(a)
    # print(te)
    #
    # if 1 == True:
    #     print(1)
    # else:
    #     print(2)


