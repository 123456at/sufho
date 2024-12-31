import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import seaborn as sns
import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置matplotlib字体，以便正确显示中文
font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=14)  # Windows系统下的Microsoft YaHei字体路径
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置字体为Microsoft YaHei
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

# 创建词云图
def create_wordcloud(words, font):
    st.text_area("", value='词云图（Word Cloud）是一种图形化的文本数据可视化技术，它通过将文本中出现频率较高的词汇以不同大小和颜色显示出来，从而直观地展示文本数据中的关键信息和模式。')
    wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400).generate(' '.join(words))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

# 创建柱状图
def create_bar_chart(data, font):
    st.text_area("",value='柱状图（Bar Chart）是一种常用的数据可视化图表，它通过水平或垂直的条形来展示数据的比较和分布情况。')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='词语', y='频率', data=data, palette="viridis")
    ax.set_xlabel("词语", fontproperties=font)
    ax.set_ylabel("频率", fontproperties=font)
    ax.set_title("词频柱状图", fontproperties=font)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontproperties=font)
    return fig

# 创建饼图
def create_pie_chart(data, font):
    st.text_area("", value='饼图（Pie Chart）是一种圆形的统计图表，通过将圆形分割成扇形来展示数值比例。每个扇形的角度和面积表示该部分在整体中所占的比例。')
    if '词语' not in data.columns:
        raise ValueError("DataFrame must have a '词语' column")
    labels = data['词语']
    sizes = data['频率'].astype(float)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title("词频饼图", fontproperties=font)
    ax.axis('equal')
    return fig

# 创建折线图
def create_line_chart(data, font):
    st.text_area("", value='折线图（Line Chart）是一种以折线连接数据点来展示数据变化趋势的图表。')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['词语'], data['频率'], marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
    ax.set_xlabel("词语", fontproperties=font)
    ax.set_ylabel("频率", fontproperties=font)
    ax.set_title("词频折线图", fontproperties=font)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontproperties=font)
    return fig

# 创建热力图
def create_heatmap(data, font):
    st.text_area("", value='热力图（Heatmap）是一种数据可视化工具，它通过颜色的变化来表示数据值的大小或频率。')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(data, annot=True, cmap="coolwarm", cbar=True, ax=ax)
    ax.set_title("热力图", fontproperties=font)
    return fig

# 创建散点图
def create_scatter_plot(data, font):
    st.text_area("", value='散点图（Scatter Plot）是一种用于展示两个变量之间关系的图表，通过在坐标平面上绘制点来表示数据的分布情况。')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data['词语'], data['频率'], color='r')
    ax.set_xlabel("词语", fontproperties=font)
    ax.set_ylabel("频率", fontproperties=font)
    ax.set_title("词频散点图", fontproperties=font)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontproperties=font)
    return fig

# 创建条形图
def create_horizontal_bar_chart(data, font):
    st.text_area("", value='条形图（Bar Chart）是一种常用的数据可视化图表，它通过条形的长度来表示数据的大小。')
    if '词语' not in data.columns:
        raise ValueError("DataFrame must have a '词语' column")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='频率', y='词语', data=data, palette="muted", orient="h")
    ax.set_xlabel("频率", fontproperties=font)
    ax.set_ylabel("词语", fontproperties=font)
    ax.set_title("词频条形图", fontproperties=font)
    return fig

# 主函数
def main():
    st.title("词频分析")
    url = st.text_input("请输入URL:")
    if url:
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('div', class_='main')
        article_content = article.get_text(separator="\n", strip=True)
        st.write("### 全文展示")
        st.text_area("全文展示", value=article_content)
        words = jieba.cut(article_content)
        filtered_words = [word for word in words if len(word) > 1 and word.strip() not in ['\n', '...', ' ', '。', ',', '，', '！', '：', '；', '(', ')', '“', '”']]
        word_freq_counts = Counter(filtered_words)
        word_freq_df = pd.DataFrame(list(word_freq_counts.items()), columns=['词语', '频率']).sort_values(by='频率', ascending=False)
        top_20_word_freq_df = pd.DataFrame(list(word_freq_counts.most_common(20)), columns=['词语', '频率'])
        c1, c2 = st.columns(2)
        with c1:
            st.write("### 最高词频统计结果")
            st.dataframe(top_20_word_freq_df)
        with c2:
            st.write("### 词频统计结果")
            st.dataframe(word_freq_df)

        chart_type = st.selectbox(
            "选择图形类型",
            ["词云图", "柱状图", "饼图", "折线图", "热力图", "散点图", "条形图"]
        )
        top_n = 20
        if top_n > 0:
            top_n_word_freq_df = word_freq_df.head(top_n)
            if chart_type == "词云图":
                st.write("### 词云图")
                fig = create_wordcloud(top_n_word_freq_df['词语'].tolist(), font)
                st.pyplot(fig)
            elif chart_type == "柱状图":
                st.write("### 柱状图")
                fig = create_bar_chart(top_n_word_freq_df, font)
                st.pyplot(fig)
            elif chart_type == "饼图":
                st.write("### 词频饼图")
                fig = create_pie_chart(top_n_word_freq_df, font)
                st.pyplot(fig)
            elif chart_type == "折线图":
                st.write("### 折线图")
                fig = create_line_chart(top_n_word_freq_df, font)
                st.pyplot(fig)
            elif chart_type == "热力图":
                st.write("### 热力图")
                fig = create_heatmap(top_n_word_freq_df.set_index('词语').T, font)
                st.pyplot(fig)
            elif chart_type == "散点图":
                st.write("### 散点图")
                fig = create_scatter_plot(top_n_word_freq_df, font)
                st.pyplot(fig)
            elif chart_type == "条形图":
                st.write("### 条形图")
                fig = create_horizontal_bar_chart(top_n_word_freq_df, font)
                st.pyplot(fig)
    else:
        pass
if __name__ == "__main__":
    main()