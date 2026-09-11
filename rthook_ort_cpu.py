# PyInstaller runtime hook: 必须在 import onnxruntime 之前生效
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ.setdefault("OMP_NUM_THREADS", "4")
# 减少 ORT 初始化时的额外探测
os.environ.setdefault("ORT_TENSORRT_UNAVAILABLE", "1")
