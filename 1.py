import string
import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud

nltk.download('punkt')

st.title('网页分析工具')

st.sidebar.title('选择图表类型')

chart_type = st.sidebar.selectbox(
    '请选择图表类型', options=['柱形图', '折线图', '饼图', '词云图', '散点图', '热力图', '曲线图', '气泡图'])

url = st.text_input('请输入URL地址')

if url:
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text  # 获取网页的内容文本

    soup = BeautifulSoup(html_content, 'html.parser')  # 解析网页内容为BeautifulSoup对象
    soup.encode('utf-8')
    text = soup.get_text()  # 从BeautifulSoup对象中获取纯文本内容

    # 去除文本中的所有标点符号和引号
    text = text.translate(str.maketrans('', '', string.punctuation + '“”‘’'))

    tokens = nltk.word_tokenize(text)  # 分词处理
    word_count = Counter(tokens).most_common(10)  # 统计出现次数最多的10个单词及其出现次数

    if chart_type == '柱形图':
        fig = px.bar(word_count, x=[word[0] for word in word_count], y=[
                     word[1] for word in word_count])  # 创建柱状图数据集
        fig.update_layout(xaxis_title="统计", yaxis_title="出现次数",
                          title="单词出现次数柱形图")  # 设置图表标题和轴标签
        st.plotly_chart(fig)  # 显示柱状图

    elif chart_type == '折线图':
        fig = px.line(word_count, x=[word[0] for word in word_count], y=[
                      word[1] for word in word_count])  # 创建折线图数据集
        fig.update_layout(xaxis_title="统计", yaxis_title="出现次数",
                          title="单词出现次数折线图")
        st.plotly_chart(fig)

    elif chart_type == '饼图':
        fig = px.pie(word_count, values=[word[1] for word in word_count], names=[
                     word[0] for word in word_count])
        fig.update_layout(title="单词出现次数饼图")
        st.plotly_chart(fig)

    elif chart_type == '词云图':
        # 生成词云图并保存为PNG文件
        wordcloud = WordCloud(
            width=800, height=400, background_color='white', font_path='simhei.ttf').generate(f"{' '.join(word[0] + ': ' + str(word[1]) for word in word_count)}")  # 调整词云图尺寸和背景色，并添加词频信息到文本中
        output_filename = "wordcloud.png"
        wordcloud.to_file(output_filename)
        # 在Streamlit应用中显示该文件的图像
        st.image(open(output_filename, "rb").read())

    elif chart_type == '散点图':
        fig = px.scatter(word_count, x=[word[0] for word in word_count], y=[
                         word[1] for word in word_count], labels={'x': '单词', 'y': '出现次数'})
        fig.update_layout(title="单词出现次数散点图")
        st.plotly_chart(fig)

    elif chart_type == '热力图':
        fig = px.density_heatmap(word_count, x=[word[0] for word in word_count], y=[
                                 word[1] for word in word_count], nbinsx=20, nbinsy=20, labels={'x': '单词', 'y': '出现次数'})
        fig.update_layout(title="单词出现次数热力图")
        st.plotly_chart(fig)

    elif chart_type == '曲线图':
        fig = px.area(word_count, x=[word[0] for word in word_count], y=[
            word[1] for word in word_count], labels={'x': '单词', 'y': '出现次数'})
        fig.update_layout(title="单词出现次数曲线图")
        st.plotly_chart(fig)

    elif chart_type == '气泡图':
        fig = px.scatter(word_count, x=[word[0] for word in word_count], y=[word[1] for word in word_count], size=[
                         word[1] for word in word_count], labels={'x': '单词', 'y': '出现次数'}, color=[word[1] for word in word_count])
        fig.update_layout(title="单词出现次数气泡图")
        st.plotly_chart(fig)

    st.write("前10个单词和次数：")
    for word in word_count:
        st.write(f"{word[0]}: {word[1]}")
