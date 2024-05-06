import re


def clean_text(text):
    # 清洗掉HTML标签
    return re.sub(r'<[^>]+>', '', text, flags=re.S)


def generate_stopwords(stopwords_paths=None):
    from wordcloud import STOPWORDS
    stopwords = set(STOPWORDS)
    stopwords.add("said")
    if not stopwords_paths:
        return stopwords
    for stopwords_path in stopwords_paths:
        if not stopwords_path:continue
        with open(stopwords_path,encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("------"): continue
                stopwords.add(line.strip())
    return stopwords

def word_cut(text_paths):

    # 判断是否需要分词
    import os
    
    # jieba.enable_parallel(os.cpu_count()) # parallel mode only supports posix system
    # userdict_list =["MIUI","小米"]
    # (jieba.add_word(i) for i in userdict_list)
    text = []
    for text_path in text_paths:
        with open(text_path,encoding='utf-8') as f: 
            text.append(f.read())
    text = " ".join(text)
    if re.match(r'[\u4e00-\u9fa5]',text):
        print("包含中文,进行分词")
        import jieba
        seg = jieba.cut(text)
        # seg = [i for i in seg if i.strip() not in stopwords and i != ""]
        seg = " ".join(seg)
    else:
        print("不包含中文,不进行分词")
        seg = text
    return seg

def generate_wordcloud(text,mask_path,colored=False,**kwargs):
    """
    kwargs:font_path、backgroud_color、max_words、stopwords、max_font_size、random_state、repeat、margin
    """
    from PIL import Image
    from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator
    import numpy as np
    import os
    os.environ["U2NET_HOME"] = os.path.join(os.path.dirname(__file__), "data/model")
    
    if mask_path:
        kwargs["mask"] = np.array(Image.open(mask_path))
    wc = WordCloud(**kwargs)
    wc.generate(text)
    out_path = mask_path+".wordcloud.png"
    # wc.to_file("小米创业思考.png")
    if colored and mask_path:
        wc = wc.recolor(color_func=ImageColorGenerator(kwargs["mask"]))
    wc.to_file(out_path)
    return out_path,wc

def generate_mask(mask_ori,mask_only=False,model_name="silueta"):
    from PIL import Image
    from rembg.session_factory import new_session
    from rembg import remove

    input = Image.open(mask_ori)
    custom_session = new_session(model_name=model_name)
    output = remove(input,session=custom_session,only_mask=mask_only,bgcolor=(255,255,255,0),alpha_matting=False)
    out_path = mask_ori+".mask.png"
    output.save(out_path)
    return out_path,output




if __name__ == "__main__":
    # CharacterWordCloud(mask='stop.jpg').generate_wordcloud()
    from fontTools.ttLib import TTFont
    from matplotlib import font_manager
    font = TTFont("hysj.ttf")
    name_table = font["name"]
    print(name_table.getName(1,3,1))
    print(font_manager.FontProperties(fname="hysj.ttf").get_)