# 功能：统一道路项目表格表头
# 要求：可方便扩展表格，公共属性，提供映射函数
#


class RoadExcelFormatColumns():  # 与road_excel.py中RoadExcel类有耦合
    def __init__(self):
        # {‘列标签（统一访问接口）'：[('1原标签中关键字1','1原标签中关键字2'),('2原标签中关键字2','2原标签中关键字2')] }
        # 解释：即将含有（'1原标签中关键字1','原标签中关键字2'）或者('2原标签中关键字2','2原标签中关键字2')的文本替换为‘列标签（统一访问接口）'
        # 元组中只有一个元素中时后面要加个逗号，如('桩号',)，才能保证'桩号'是个整体，否则遍历时会拆成桩、号
        self.columns = {
            '起讫桩号': [('起止桩号',)],
            '起点桩号': [('起点',), ('qd',)],
            '止点桩号': [('止点',), ('zd',)],
            '位置左幅': [('位置', '左'), ],
            '位置右幅': [('位置', '右'), ],
            '位置': [('位置', ), ],
            '长度': [('长度',)],
        }  # ('桩号',),


class TfExcelFormatColumns(RoadExcelFormatColumns):
    def __init__(self):
        super().__init__()
        self.columns_add = {
            '挖方总数量': [('挖', '总数量')],
            '挖方松土': [('挖', '软土'), ('挖', 'I'), ('挖', '松土')],
            '挖方普通土': [('挖', '普通'), ('挖', 'Ⅱ')],
            '挖方硬土': [('挖', '硬土'), ('挖', 'Ⅲ')],
            '挖方软石': [('挖', '软石'), ('挖', 'Ⅳ')],
            '挖方次坚石': [('挖', '次坚石'), ('挖', 'Ⅴ')],
            '挖方坚石': [('挖', '坚石'), ('挖', 'Ⅵ')],
            '填方总数量': [('填', '总数量')],
            '填方土方': [('填', '土')],
            '填方石方': [('填', '石')],
            '借方土方': [('借', '土')],
            '借方石方': [('借', '石')],
            '废方总数量': [('废', '总数量'), ('弃', '总数量')],
            '废方软土方': [('废', '软土'), ('弃', 'I')],
            '废方土方': [('废', '土'), ('弃', '土')],
            '废方石方': [('废', '石'), ('弃', '石')],
            '清表回填': [('清表', '回填')],
            }
        self.columns.update(self.columns_add)


class PsExcelFormatColumns(RoadExcelFormatColumns):
    def __init__(self):
        super().__init__()
        self.columns_add = {
            '工程名称': [('工程', '名称')],
            '类型': [('类型',), ('型式',)],
            '挖基': [('挖基',)],
            }
        self.columns.update(self.columns_add)


class FhExcelFormatColumns(RoadExcelFormatColumns):
    def __init__(self):
        super().__init__()
        self.columns_add = {
            '人字型挖基': [('人字型', '挖基')],
            '人字型C20砼': [('人字型', 'C20', '砼'), ('人字型', 'C20', '混凝土')],
            '人字型M7.5水泥砂浆': [('人字型', 'M7.5', '砂浆')],
            }
        self.columns.update(self.columns_add)


class QbExcelFormatColumns(RoadExcelFormatColumns):
    def __init__(self):
        super().__init__()
        self.columns_add = {
            '清表土': [('清表', '土')],
            '回填土': [('回填', '土')],
            }
        self.columns.update(self.columns_add)


class QtExcelFormatColumns(RoadExcelFormatColumns):
    def __init__(self):
        super().__init__()
        self.columns_add = {
            '中心桩号': [('中心', '桩号')],
            '回填碎石': [('回填', '碎石')],
            '碎石垫层': [('垫层', '碎石')],
            '回填石屑': [('回填', '石屑')],
            }
        self.columns.update(self.columns_add)


class XjExcelFormatColumns(RoadExcelFormatColumns):
    def __init__(self):
        super().__init__()
        self.columns_add = {
            '边坡清表': [('边坡', '清表')],
            '台阶挖土方': [('台阶', '挖', '土')],
            '回填土方': [('回填', '土')],
            }
        self.columns.update(self.columns_add)


class QlExcelFormatColumns(RoadExcelFormatColumns):
    def __init__(self):
        super().__init__()
        self.columns_add = {
            '中心桩号': [('中心', '桩号')],
            '桥名': [('桥名', )],
            '孔径': [('孔径', )],
            '交角': [('交角',)],
            '桥梁长度': [('桥梁', '全长'), ('桥梁', '长度')],
            '上部结构': [('上部结构',)],
            '桥墩': [('墩', '下部结构')],
            '桥台': [('台', '下部结构')],
            '基础': [('基础', '下部结构')],
            }
        self.columns.update(self.columns_add)