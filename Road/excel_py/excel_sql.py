"""
目标：实现excel <--> mysql 双向便捷交互

# 1。1 excel_to_excel
  - get_tf_km_age(项目名称，路线，data_source=[excel_name,mysql], axis="返回值轴向") -> [DataFrame,Series]
  - get_tf_km_data(项目名称，路线，起点，止点，data_source=[excel_name,mysql], axis="返回值轴向") -> [DataFrame,Series]
    - return:挖方 【土方（1，2，3类），石方（4,5,6类）】；填方 【土方（1，2，3类），石方（4,5,6类）】
            本桩利用
            远运利用
            借方
            废方
    class sheet_road():
        sheet_tf_km
        sheet_bridgehead_roadbed
        sheet_mud_base
        sheet_protect
        sheet_drain
        sheet_
    class road()
    起点、止点、左幅、右幅、整幅、长度
  - tf.wf.tff.ptt
  - tf.wf.total
## 1.2 mysql_to_excel
# 2.to_mysql

"""


class tf():
    def __init__(self):
        self.wf = "wf"
        self.wf = "t"
    def wf(self):
        pass
        def tff(self):
            pass
            def ptt(self):
                pass