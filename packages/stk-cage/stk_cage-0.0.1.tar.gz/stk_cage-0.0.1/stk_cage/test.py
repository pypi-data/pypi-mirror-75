from cage import *

# 创建block
b1=block("NC1CCCCC1N",[group["-NH2"]()]) #CHDNH2
b2=block("O=Cc1cc(C=O)cc(C=O)c1",[group["-CHO"]()])  # BTMCHO
# 根据cage的拓扑和block创建framework, 然后用MMFF力场初步优化
test=cage("2+3",(b1,b2),opt=True)
# 写分子
test.write("cage.xyz")

