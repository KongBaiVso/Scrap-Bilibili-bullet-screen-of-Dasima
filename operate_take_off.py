import pandas as pd
import numpy as np
import re

df = pd.read_csv("take off.csv",engine="python",encoding="gb18030",header=None)
df.index = range(len(df))
df.columns = ["弹幕内容","发表时间","弹幕类型"]

# 数据统一归类。把带有 飞，起飞，飞飞飞字眼的内容都归为 起飞， 把可爱 字眼的内容都归为可爱
geng = ["飞","可爱","害怕","上当","不对劲","哈","？","?","倒霉蛋","啥b","啥比","经典","病","ICU","吃"
            "千层饼","双线程","被动触发","被动还就那个触发","好k","离谱","男同","男酮","肉蛋葱鸡","肉蛋充饥","芜湖","李在赣神魔","李在干什么","拖",
            "崩撤卖溜","泪目","谜语人","折磨王","贼眉鼠眼","饭","饱了","xswl","666","配合的不是很好",
            "skr","吸血怎么说","辅助杀手","神头鬼脸","胆小鬼","一枪不开","弱智墨菲特","一直可以的","量角器","角度","小法司","缪撒",
            "抹布吸","因为你不会","多捞哦","歪比巴卜","歪比歪比","加密通信","马来西亚","坠机","老","不亏","红皮鸭子"]
geng = np.array(geng)   # 这里job_list要变为ndarray格式的原因是列表不支持布尔索引，而ndarray可以。
def rename(x=None,geng=geng):
    index = [i in x for i in geng]
    # print(index)
    if sum(index) > 0:
        return geng[index][0]
    else:
        return x
df["弹幕内容"] = df["弹幕内容"].apply(rename)


# 数据统计、数据专员、数据分析统一归为数据分析
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("飞","起飞类词语",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("芜湖","起飞类词语",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("哈","哈哈哈哈哈",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("笑死我了","哈哈哈哈哈",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("肉蛋充饥","肉蛋葱鸡",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("肉蛋葱鸡","肉蛋葱鸡",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("老","老……的词语",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("病","发病类词语",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("ICU","发病类词语",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("拖","拖,就硬拖",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("李在赣神魔","李在赣神魔",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("李在干什么","李在赣神魔",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("你在干什么","李在赣神魔",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("一直可以的","……一直可以的",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("饭","下饭类词语",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("饱了","下饭类词语",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("吃","下饭类词语",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("？","问号",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("\?","问号",x))

df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("歪比歪比","加密通信",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("歪比巴卜","加密通信",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("加密通信","加密通信",x))
df["弹幕内容"] = df["弹幕内容"].apply(lambda x:re.sub("马来西亚","加密通信",x))
df1 = df["弹幕内容"].value_counts().reset_index()
df1 = pd.DataFrame(df1)
print(df1)
df1.to_csv("third_statistics.csv",header=None,index=None,encoding="gb18030")
