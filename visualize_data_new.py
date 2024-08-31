import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql
from wordcloud import WordCloud

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'myuser',
    'password': 'mypassword',
    'database': 'house_data',
    'charset': 'utf8mb4',
}

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 连接到数据库并查询数据
query = "SELECT * FROM houses"  # 根据需要修改查询语句
connection = pymysql.connect(**db_config)
df = pd.read_sql(query, con=connection)
connection.close()

# 总价分布的直方图
plt.figure(figsize=(10, 6))
sns.histplot(df['total_price'], bins=50, kde=True, color="skyblue")
plt.title('总价分布')
plt.xlabel('总价/万')
plt.ylabel('数量')
plt.savefig('total_price_distribution.png')
plt.close()

# 单位价格分布的直方图
plt.figure(figsize=(10, 6))
sns.histplot(df['unit_price'], bins=30, kde=True, color="salmon")
plt.title('单位价格分布')
plt.xlabel('单位价格/元')
plt.ylabel('数量')
plt.savefig('unit_price_distribution.png')
plt.close()

# 计算每种装修风格的房屋数量
decoration_counts = df['decoration_form'].value_counts()

# 绘制饼状图
plt.figure(figsize=(8, 8))
plt.pie(decoration_counts, labels=decoration_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('各装修风格的房屋数量分布')
plt.axis('equal')  # 确保饼状图是圆形
plt.savefig('decoration_form_distribution.png')
plt.close()

# 生成文字云
text = " ".join(df['house_title'])

# 生成文字云
wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400, background_color='white').generate(text)

# 显示并保存文字云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('房源标题中的高频关键字')
plt.savefig('wordcloud.png')
plt.close()
