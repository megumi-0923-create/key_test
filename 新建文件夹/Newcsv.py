import pandas as pd

# 读取 CSV
df = pd.read_csv("result_test2.csv", header=None, names=['first','second'])

# 找到第二列唯一值作为新表头
unique_second = df['second'].unique()

# 用字典存放每个第二列对应的第一列列表
data_dict = {val: df.loc[df['second'] == val, 'first'].tolist() for val in unique_second}

# 找出最长的列长度
max_len = max(len(lst) for lst in data_dict.values())

# 补齐每列，保证长度一致
for key in data_dict:
    lst = data_dict[key]
    if len(lst) < max_len:
        lst.extend([''] * (max_len - len(lst)))

# 转换成 DataFrame
new_df = pd.DataFrame(data_dict)

# 保存到新 CSV
new_df.to_csv("transformed.csv", index=False, header=True, encoding='utf-8')
