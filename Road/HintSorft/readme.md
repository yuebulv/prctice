## module widFile
### 功能目标：实现hintSoft对宽度文件的修改
### 实现思路
    已知：范围（中心桩号），渐变率（渐变长度），渐变方式（线性/二次抛物线等）change_style，左右侧，加宽宽度，加宽位置（车道/硬路肩/土路肩），在原基础加宽还是设置总宽度
    目标：修改wid文件
    例如：对护栏/错车道/位置加宽
    注：护栏段落护肩最小宽度75cm，不满足段落需要加宽；
    错车道范围加宽，
```python
def wid():
    pass
```
## module slope 
### 使用流程
  1. eicad数据中包含are（生横断面图后生成）/dat/hdx/dl(如有)/sqx/dmx/gzx/icd
  2. 运行TransEiDatToHint3dr生成3dr/tf文件
  3. 将icd/sqx/dmx/hdx/gzx转为纬地数据，并在纬地里格式化一下(需要重置为python版本)
  4. 使用数量表工具生成低填等数量表(需要重置为python版本)
  5. 不同路线数据要放到不同文件夹内，使用slope生成防护排水数据。(需要将结果存入excel表-xlwings)
## module bridgeTableToEIHint