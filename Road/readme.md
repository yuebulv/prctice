## Function

### excel

1. inquiry_excel_data：查询表格中数据，查询语句：dataframe语法
2. check_dataframe_data：检查表格中数据是否正确，检查规则存放于road_excel_check_rules.py中
3. 表格联合检查，如，填方边坡、挖方边坡，支挡（路肩）、大-小鼻端、桥梁、隧道桩号连续
4. 路基宽度查询功能，EI可借助生成KD.csv来查询
5. 设计标高查询功能，中心标高、路基边缘设计标高
5. 根据坐标算面积，可提高精度

#### set

1. road_excel_columns_port.py

   - ```
     self.columns
     ```

2. road_excel.py

   - ```
     self.format_columns_class_and_excel_name_keys_dic
     ```

   - ```
     self.check_rules_function_and_excel_name_map_dic
     ```

3. road_excel_settings.py

   - ```
     format_abbreviation_and_excel_name_keys_dic
     ```

### common_function

1. str_map_factory(map_str, map_dic: dict)：字符映射

