学习笔记

第一节：pandas(python 的 excel)
    常用测试数据集
        from sklearn import datasets
        aa = datasets.load_xxx()
        常用数据集: iris,boston,digits

    pandas 的底层就是 numpy，python 的数学计算库
    import matplotlib as plt

    pwd = os.path.dirname(os.path.realpath(__file__)
    path = os.path.join(pwd, 'book.txt')
        这种用法对交互模式不友好，因为交互模式的当前路径是语言的源目录如 /usr/local/bin/python3

    对每行判断是否 star 列为力荐
        df['star'] == '力荐'

    输出 star 列为力荐的行
        df[ df['star'] == '力荐' ]

    删除空行
        df.dropna()

    将 star 列进行聚合并求和，这个求和感觉是对所有数字列的求和吧，要验证下
        df.groupby('star').sum()

    将文字列按照字典映射成数字列
        df['new_star'] = df['star'].map(mapping_dict)


第二节: pandas 的两个数据类型
    pandas 中索引的意义： 提升查询性能
            1. 如果 index 唯一，pandas 会使用哈希表优化，查询性能为 0(1)
            2. 如果 index 有序不唯一，pandas 会使用二分查找算法，查询性能为 0(logN)
            3. 如果 index 完全随机，每次查询都要扫全表，查询性能为 0(N)

    pandas 最基础的两种数据类型 Series 和 DataFrame
    series
        跟 excel 的区别
            1. series 的列会有一个索引并且支持自定义
        s1 = pd.Series(['a', 'b', 'c'])
        s2 = pd.Series({'a':'A', 'b':'B'})
            等价于 s2 = pd.Series(['A', 'B'], index=['a', 'b'])
        s1.index 输出 s1 中的所有索引，类型是 obj
        s1.values 输出 s1 的所有值，类型是 numpy 定义的数组
        s1.values.tolist() 将 s1 的所有值转换成列表输出

    dataFrame(类似多行多列的 excel)
        跟 series 类似也有索引
        df1 = pd.DataFrame(['1', '2', '3'])
        df2 = pd.DataFrame([['a', 'b'], ['c', 'd']])
        df2.columns = ['aa', 'bb'] 自定义列索引
        df2.index = ['11', '22'] 自定义行索引

第三节：pandas 读取数据
    pandas 可以通过 read_xxx 系的方法读入外部数据源
    read_excel
        前置依赖 pip3 install xlrd
        excel1 = pd.read_excel(r'show.xlsx', sheet_name = 0) 读取 show.xlsx 中 sheet 名称为 0 的表格内容

    read_csv
        read_csv(r'file.csv', sep=' ', nrow=10, encoding='utf-8')

    read_table
        read_table(r'file.txt', sep=' ')

    read_sql
        import pymysql
        sql = 'select * from table';
        conn = pymysql.connect('ip', 'user', 'pwd', 'db', 'charset=utf-8')
        data1 = pd.read_sql(sql, conn) # 这一步才建立数据库连接

    其它通用方法
        d1.head(3) 获取前三行数据
        d1.shape 返回数据的行列信息，如 (3,4) 指三行四列
        d1.info() 详情
        d1.describe() 简单预统计信息

第四节：pandas 数据预处理
    1. 缺失值处理
    2. 重复值处理

    Series 操作
        x = pd.Series([1, 2, 5, pd.nan, 3, pd.nan])
        x.hasnans 检查是否有缺失值
        x.fillna(value = x.mean() 用平均值填充缺失值

    DataFrame 操作
        df = pd.DataFrame([
            [1, 2, 4, None],
            [1, None, 4, None],
            [1, 2, 4, 21]
        ])
        df.isnull() 以二维的形式展示每个值是否为空
        df.isnull().sum() 展示每行为空的值个数
        df.ffill() 空值以上一行值填充
        df.ffile(axis=1) 空值以前一列填充
            que: 那遇到连续两行为空，或者最后一行为空的时候怎么处理呢
            ext: 不是所有数据都可以无脑填充，如用户性别
        df.info() 输出信息
        df.dropna() 删除包含空值的行
        df.fillna('无') 以'无'填充所有空值
        df.drop_duplicates() 将完全重复的行删除
            ext: 部分重复的行删除需要通过 DataFrame 进一步处理

第五节：pandas 格式处理
    行列调整
        df[ ['A', 'B'] ] 获取 df 中的 A 列和 B 列
        df.iloc[:, [0,2]] 获取 df 中所有行的第1，3 列
        df.loc[ [0, 2] ] 获取第一行和第三行
        df.loc[0:2] 获取第一行到第三行

    比较过滤
        df[ (df['A'] < 5) & (df['D'] < 4) ] 获取 A 列值小于 5 且 D 列值小于 4 的行

    数据替换
        ndf = df['C'].replace(4, 44) 将 C 列中的 4 替换成 44
        ndf2 = df.replace(np.NaN, 0) 将空值替换成 0
        df.replace([4,5,6], 100) 将 4，5，6三个值替换成 100(456 三个值包括整型和浮点型)
        df.replace({'4':'100', '5':'200', '6':'300'}) 将 4 替换成 100，5 替换成 200，以此类推

    排序
        df.sort_values(by=['A'], ascending=True) 依据 A 列值从小到大排序
        df.sort_values(by=['A', 'B'], ascending=[True, False]) 依据 A 列升序，B 列降序排序

    删除
        df.drop('A', axis=1) 删除 A 列，axis 区分操作的是行或列
        df.drop(1, axis=0) 删除第二行
        df[ df['A'] < 4 ] 获取 A 列值小于 4 的行，也就是删除大于等于 4 的行(python 认为空值是大于 4 的)
            que: 空值应该是不管大于 4 或小于 4 都成立的吧，可以试一下

    行列互换
        df.T 行列互换
        df.T.T 互换两次，不变

    数据透视
        df = pd.DataFrame(
            [
                ['1', '2', '3'],
                ['4', '5', '6']
            ],
            columns=['one', 'two', 'three'],
            index=['A', 'B']
        )
        df.stack() 对行索引(index)进行数据透视，返回 DataFrame 对象
        df.unstack() 对列索引(columns)进行数据透视
        df.stack().reset_index() 对行索引进行数据透视，然后根据透视的条件填充空白


第八节：pandas 数据拼接
    横向拼接
        语法 pd.merge(data1, data2) 相当于 MySQL 的 join, 默认 inner join 模式
        参数解析：
            on 连接字段名
            left_on 跟 on 不能同时指定，左表字段名
            right_on 跟 on 不能同时指定，左表字段名
            how 连接方式 inner, left，right, outer

    纵向拼接
        pd.concat([data1, data2])

第九节：结果输出
    输出到文件
        to_excel
            excel_writer,columns,index,encoding,sheet_name,
            inf_rep = 0 无穷值以 0 替代
            na_rep = 0 空值以 0 替代
        to_csv
        to_pickle
        to_dict
        to_sql
    输出到图形
        import matplotlib as plt
        plt.plot(df.index, df['A']) 以 df.index, df['A'] 为横纵坐标绘制折线图
            属性
            color
            linewidth
            line
        plt.scatter 散点图
        plt.show() 展示图形

        import seaborn as sns
        丰富图表

第十节：自然语言处理-语义分析
    jieba 分词
        jieba.cut('asffsafsaf') 默认精确模式
        jieba.cut('xxxxxx', cut_all=True)另一种全模式会尽可能将所有词罗列出来
        jieba.cut_for_search('xxxxxx') 感觉是介乎精确和全模式的中间版本
        jieba.cut(text, HMM=False) 关闭自动计算词频

        词性标注
            import jieba.analyse 关键字提取
            基于 TF-IDF 算法
                jieba.analyse.extract_tags(text, topK=10, withWeight=True)
            基于 TextRank 算法
                jieba.analyse.textrank(text, topK=10, withWeight=True)

            屏蔽词
                jieba.analyse.set_stop_words(file)
                    设置算法的屏蔽词，不会认为他们是关键字，通过文件导入

            用户词典
                文件每行格式：关键词 权重 词性
                jieba.load_userdict(file) 要在 cut 前使用
                jieba.add_word
                jieba.del_word
                jieba.suggest_freq(('中', '将'), True) 正对算法总是认为是组合的词的情况，可以手动将其拆分

            词性表在 4c 分支
    情感分析