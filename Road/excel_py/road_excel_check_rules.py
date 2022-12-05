# 功能：道路excel数量表检查规则


class RoadExcelCheckRules():  # 与road_excel.py中RoadExcel类有耦合
    def __init__(self):
        # check_rule格式{'exp': '检查用的表达式', 'columns': [结果中输出的columns列], 'rexg': '如果columns为空[]时，刚用正则划分columns'}
        self.check_rules_exp_split_regx = r'[\+\-\*\/\=\!\'\"\s\&\|()]+'  # 将exp中的列名分出来
        self.check_rules = [
            {'exp': '止点<起点', 'columns': ['起点', '止点'], 'regx': r'[^\+\-*\/=\!\'\"\s]+'},
            {'exp': '长度!=(止点-起点)', 'columns': ['长度', '起点', '止点']},

        ]


class RoadTfExcelCheckRules(RoadExcelCheckRules):
    def __init__(self):
        super().__init__()
        self.check_rules.extend([
            {'exp': '挖方总数量!=(挖方松土+挖方普通土+挖方硬土+挖方软石+挖方次坚石+挖方坚石)', 'columns': [],
             'regx': self.check_rules_exp_split_regx},
            {'exp': '填方总数量!=(填方土方+填方石方)', 'columns': ['填方总数量', '填方土方', '填方石方']},
            {'exp': '起讫桩号=="合计" & (挖方松土+挖方普通土+挖方硬土+借方土方)!=(填方土方+废方土方)', 'columns': [], 'regx': self.check_rules_exp_split_regx},

        ])


class RoadProtectExcelCheckRules(RoadExcelCheckRules):
    def __init__(self):
        super().__init__()
        self.check_rules.extend([
            {'exp': '挖方总数量!=挖方土方松土+挖方土方普通土+挖方土方硬土+挖方石方软石+挖方石方次坚石+挖方石方坚石', 'columns': [],
             'regx': r'[\+\-\*\/\=\!\'\"\s]+'},
            {'exp': '填方总数量!=填方土方+填方石方', 'columns': ['填方总数量', '填方土方', '填方石方']},

        ])


class RoadDrainExcelCheckRules(RoadExcelCheckRules):
    def __init__(self):
        super().__init__()
        self.check_rules.extend([
            {'exp': '挖方总数量!=挖方土方松土+挖方土方普通土+挖方土方硬土+挖方石方软石+挖方石方次坚石+挖方石方坚石', 'columns': [],
             'regx': r'[\+\-\*\/\=\!\'\"\s]+'},
            {'exp': '填方总数量!=填方土方+填方石方', 'columns': ['填方总数量', '填方土方', '填方石方']},

        ])


class RoadPavingExcelCheckRules(RoadExcelCheckRules):
    def __init__(self):
        super().__init__()
        self.check_rules.extend([
            {'exp': '挖方总数量!=挖方土方松土+挖方土方普通土+挖方土方硬土+挖方石方软石+挖方石方次坚石+挖方石方坚石', 'columns': [],
             'regx': r'[\+\-\*\/\=\!\'\"\s]+'},
            {'exp': '填方总数量!=填方土方+填方石方', 'columns': ['填方总数量', '填方土方', '填方石方']},

        ])