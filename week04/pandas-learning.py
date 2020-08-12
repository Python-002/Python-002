#!/usr/bin/env python3

"""
这期作业看了第一个视频有个大概其的，就可以做了感觉，所以先做作业了，当然需要对照相关文档
"""

# 抄袭的pandas.cn 上的tutorial里面用的别名
import numpy as np
import pandas as pd

size = 1500
data = pd.DataFrame({
  'id':np.array(list(range(size))),
  'age':np.random.random_integers(15,50,size)
})

# 返回所有数据就是直接引用DataFrame类型的变量就可以了
# expr本来是为了输出的更好看点，不过最后放弃了，不如写点注释完事了，那天看pep8说特么的不让写中文注释么还是我理解错了
print('1. SELECT * FROM data;')
expr = 'data'
print(expr)
print("output: ",eval(expr))

print('\n',"*"*20,'\n')


# 头部的十个么，想想limit 10，10？难道是head(10+10).tail(10)？
print('2. SELECT * FROM data LIMIT 10;')
print(data.head(10))

print('\n',"*"*20,'\n')


# https://www.pypandas.cn/docs/getting_started/comparison.html#select，注意select 多列怎么写 
print('3. SELECT id FROM data;  //id 是 data 表的特定一列')
print(data['id'])

print('\n',"*"*20,'\n')


# 选出一列其实返回的是个Series, 如果用双中括号（例如select多列），那返回还是个DataFrame，是二维结构，size不等同于表的记录数
print('4. SELECT COUNT(id) FROM data')
print(data['id'].size)

print('\n',"*"*20,'\n')


# 发现两个写法，还是query表达式清楚吧，底下那个是文档SQL对应章节的，好啰嗦的感觉；不知道效率上有没差别，心里感觉上一样
print('5. SELECT * FROM data WHERE id<1000 AND age>30')
print(data.query('id<1000 and age>30'))
print(data[(data['id'] < 1000 )& (data['age'] > 30)])

print('\n',"*"*20,'\n')


# 这个上网搜了，参考的[这个](https://www.cnblogs.com/onemorepoint/p/10613953.html)，其实哪个方法我感觉都没看懂
print('6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;')
size_of_table1 = 20
table1 = pd.DataFrame({
  'id':np.random.random_integers(1,3,size_of_table1),
  'order_id':np.random.random_integers(10,15,size_of_table1)
})

print(table1)
print(table1.groupby(['id']).agg({'order_id': pd.Series.nunique}))

print('\n',"*"*20,'\n')


# 直接[参考](https://www.pypandas.cn/docs/getting_started/comparison.html#inner-join)
print("7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;")
table2 = pd.DataFrame({
  'id':[1,5],'name':['pete','michael']
})
print(pd.merge(table1,table2,on='id'))

print('\n',"*"*20,'\n')


# 也是直接[参考](https://www.pypandas.cn/docs/getting_started/comparison.html#union)
print("8. SELECT * FROM table1 UNION SELECT * FROM table2;")
print(pd.concat([table1,table2]).drop_duplicates())

# 上面数据准备不太好，看不出drop_duplicates效果来，下面这个自己union自己就能看出来了，而且万一table1自己里面数据有重复的也会清除掉
# 当然人家文档里写的也很清楚
print(pd.concat([table1,table1]))
print("="*20)
table1_union = pd.concat([table1,table1]).drop_duplicates()
print(table1_union,table1)
print("="*20)
print(table1_union.size)

print('\n',"*"*20,'\n')


# 我改了一下因为我的数据准备没有10
# 这个感觉应该就没有直接删的，因为找到的drop的方法都是基于所谓index或者label的，这俩概念好像这么并列描述也不准，稍后细看
# 所以还是得先按条件查出来，然后找到对应的index然后删除之
print('9. DELETE FROM table1 WHERE id=10;')
print(table1.drop(table1.query('id==2').index,axis=0))

print('\n',"*"*20,'\n')

# 这个似乎更直接一点，没看出有什么坑，改列名也很简单，文档里直接有栗子
print('10. ALTER TABLE table1 DROP COLUMN column_name;')
print(table1.drop(['id'],axis=1))

