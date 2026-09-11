import os
import re
import sys


def get_base_dir():
    """可写根目录：源码旁，或打包后 exe 所在目录。"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_resource_dir():
    """只读资源目录：开发时为项目根；打包后为 PyInstaller 的 _MEIPASS/_internal。"""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def resource_path(*parts):
    """拼接只读资源路径，如 resource_path('data', 'images', 'icon.png')。"""
    return os.path.join(get_resource_dir(), *parts)


def get_model_dir():
    """rembg 模型目录（可写）：exe/项目旁 data/model。"""
    return os.path.join(get_base_dir(), "data", "model")


def _has_model_files(root):
    if not os.path.isdir(root):
        return False
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".onnx") and os.path.getsize(os.path.join(dirpath, name)) > 1024:
                return True
    return False


def setup_model_home():
    """将 rembg 指向已有本地模型目录，避免重复下载/拷贝。

    优先使用已有模型：包内 _internal/data/model 或 exe/项目旁 data/model。
    仅在本地没有模型、需要下载时，才创建可写的 data/model。
    """
    writable = get_model_dir()
    bundled = resource_path("data", "model")

    # 打包后优先用包内模型，避免在 exe 旁多建空目录
    for candidate in (bundled, writable):
        if _has_model_files(candidate):
            os.environ["U2NET_HOME"] = candidate
            os.environ["REMBG_HOME"] = candidate
            print(f"使用本地模型目录: {candidate}")
            return candidate

    os.makedirs(writable, exist_ok=True)
    os.environ["U2NET_HOME"] = writable
    os.environ["REMBG_HOME"] = writable
    print(f"未找到本地模型，将下载到: {writable}")
    return writable


def ensure_download_proxy():
    """GitHub 模型下载走本机 VPN 代理（127.0.0.1:7890），代理未开则跳过。"""
    host, port = "127.0.0.1", 7890
    try:
        import socket
        with socket.create_connection((host, port), timeout=0.5):
            pass
    except OSError:
        return False
    proxy = f"http://{host}:{port}"
    for key in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        os.environ.setdefault(key, proxy)
    return True


def model_file_ready(model_name):
    """检查当前模型目录下是否已有该模型权重。"""
    model_name = (model_name or "").strip()
    home = os.environ.get("U2NET_HOME") or os.environ.get("REMBG_HOME") or get_model_dir()
    if not model_name:
        return _has_model_files(home)
    candidates = [
        os.path.join(home, "models", model_name, f"{model_name}.onnx"),
        os.path.join(home, f"{model_name}.onnx"),
        resource_path("data", "model", "models", model_name, f"{model_name}.onnx"),
        resource_path("data", "model", f"{model_name}.onnx"),
    ]
    return any(os.path.isfile(p) and os.path.getsize(p) > 1024 for p in candidates)


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

def _app_log(msg):
    print(msg, flush=True)
    try:
        path = os.path.join(get_base_dir(), "cwc.log")
        with open(path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def generate_mask(mask_ori,mask_only=False,model_name="silueta"):
    # 必须在 import onnxruntime/rembg 之前禁用 GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    model_name = (model_name or "silueta").strip()
    home = setup_model_home()
    ready = model_file_ready(model_name)
    if not ready:
        using_proxy = ensure_download_proxy()
        _app_log(
            f"模型 {model_name} 不存在于 {home}，开始下载"
            + ("（已启用 127.0.0.1:7890 代理）" if using_proxy else "（未检测到代理，直连 GitHub 可能很慢）")
        )
    else:
        _app_log(f"加载本地模型 {model_name} <- {home}")

    _app_log("import rembg/onnxruntime ...")
    from PIL import Image
    from rembg.session_factory import new_session
    from rembg import remove

    img = Image.open(mask_ori)
    _app_log(f"new_session({model_name}) providers=CPU ...")
    # 强制 CPU，避免打包环境下 CUDA provider 探测卡死
    custom_session = new_session(
        model_name=model_name,
        providers=["CPUExecutionProvider"],
    )
    _app_log(f"模型已加载，开始抠图: {mask_ori}")
    output = remove(
        img,
        session=custom_session,
        only_mask=mask_only,
        bgcolor=(255, 255, 255, 0),
        alpha_matting=False,
    )
    out_path = mask_ori + ".mask.png"
    output.save(out_path)
    _app_log(f"Mask 完成: {out_path}")
    return out_path, output




if __name__ == "__main__":
    # CharacterWordCloud(mask='stop.jpg').generate_wordcloud()
    from fontTools.ttLib import TTFont
    from matplotlib import font_manager
    font = TTFont("hysj.ttf")
    name_table = font["name"]
    print(name_table.getName(1,3,1))
    print(font_manager.FontProperties(fname="hysj.ttf").get_)