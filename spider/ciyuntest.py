import jieba
import wordcloud
import imageio

# 导入imageio库中的imread函数，并用这个函数读取本地图片，作为词云形状图片
py = imageio.imread(r"E:\MyStudy\cpitest\spider\beijing.png")
f = open(r'ci.txt', encoding='utf-8')
txt = f.read()
# print(txt)
# jiabe 分词 分割词汇
txt_list = jieba.lcut(txt)
string = ' '.join(txt_list)
# 词云图设置
wc = wordcloud.WordCloud(
    width=1000,  # 图片的宽
    height=700,  # 图片的高
    background_color='white',  # 图片背景颜色
    font_path='msyh.ttc',  # 词云字体
    mask=py,  # 所使用的词云图片
    scale=15,
    stopwords={'关于', '不要'},
    # contour_width=5,
    # contour_color='red'  # 轮廓颜色
)
# 给词云输入文字
wc.generate(string)
wc.to_file(r's.png')
