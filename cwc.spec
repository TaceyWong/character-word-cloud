# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Character Word Cloud GUI."""

import os
from PyInstaller.utils.hooks import (
    collect_all,
    collect_data_files,
    collect_dynamic_libs,
    copy_metadata,
)

block_cipher = None

# 只打必要资源；模型默认仅含 u2net（约 168MB）。其它模型首次选用时再下载。
datas = [
    ("data/images", "data/images"),
    ("data/fonts", "data/fonts"),
    ("data/demo", "data/demo"),
    ("data/stop", "data/stop"),
    ("data/model/models/u2net", "data/model/models/u2net"),
]
binaries = []
hiddenimports = [
    "jieba",
    "jieba.posseg",
    "wordcloud",
    "rembg",
    "rembg.session_factory",
    "rembg.sessions",
    "rembg.sessions.u2net",
    "rembg.sessions.silueta",
    "rembg.sessions.u2net_human_seg",
    "rembg.sessions.u2net_cloth_seg",
    "rembg.sessions.dis_general_use",
    "rembg.sessions.dis_anime",
    "pymatting",
    "numba",
    "llvmlite",
    "matplotlib",
    "matplotlib.font_manager",
    "fontTools",
    "fontTools.ttLib",
    "PIL",
    "numpy",
    "onnxruntime",
    "onnxruntime.capi",
    "onnxruntime.capi.onnxruntime_pybind11_state",
    "pooch",
    "wx",
    "wx.adv",
    "wx.lib.dialogs",
]

# 不要 collect_all(onnxruntime)：CUDA/transformers 会撑爆体积并导致卡死
# pymatting 依赖 numba/llvmlite，必须打进包
for pkg in ("jieba", "rembg", "wordcloud", "matplotlib", "pymatting", "numba", "llvmlite"):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

for pkg in ("pymatting", "rembg", "pooch", "onnxruntime", "numpy", "Pillow", "scipy", "numba", "llvmlite"):
    try:
        datas += copy_metadata(pkg)
    except Exception:
        pass

try:
    binaries += collect_dynamic_libs("onnxruntime")
except Exception:
    pass

try:
    datas += collect_data_files("jieba")
except Exception:
    pass


def _is_windows_system_dll(dest_name: str) -> bool:
    name = os.path.basename(dest_name).lower()
    if name.startswith("api-ms-win-") or name.startswith("ext-ms-"):
        return True
    exclude = {
        "ucrtbase.dll",
        "ucrtbased.dll",
        "vcruntime140.dll",
        "vcruntime140_1.dll",
        "msvcp140.dll",
        "msvcp140_1.dll",
        "msvcp140_2.dll",
        "concrt140.dll",
        "vcomp140.dll",
        "msvcr120.dll",
        "msvcp120.dll",
    }
    return name in exclude


def _is_gpu_ort_binary(dest_name: str) -> bool:
    """排除 ORT GPU/加速库，强制只用 CPU，避免打包后探测 CUDA 卡死。"""
    n = dest_name.lower().replace("\\", "/")
    needles = (
        "cuda",
        "cudnn",
        "cublas",
        "cufft",
        "curand",
        "cusolver",
        "cusparse",
        "nvrtc",
        "nvidia",
        "tensorrt",
        "nvinfer",
        "openvino",
        "dnnl",
        "mklml",
        "tvm",
        "providers_cuda",
        "providers_tensorrt",
        "providers_openvino",
        "providers_dnnl",
    )
    return any(x in n for x in needles)


def _is_bloat_path(dest_name: str) -> bool:
    """去掉非默认模型、测试/示例数据等大块（保留 numba/llvmlite）。"""
    n = dest_name.lower().replace("\\", "/")
    if n.endswith(".onnx"):
        parts = n.split("/")
        if "u2net" in parts and parts[-1] == "u2net.onnx":
            return False
        return True
    bloat_dirs = (
        "/matplotlib/mpl-data/sample_data/",
        "/matplotlib/tests/",
        "/scipy/tests/",
        "/skimage/data/",
        "/tk/",
        "/_tk_data/",
        "/tcl/",
        "/_tcl_data/",
    )
    return any(x in n for x in bloat_dirs)


a = Analysis(
    ["cwc_gui.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["rthook_ort_cpu.py"],
    excludes=[
        "onnxruntime.transformers",
        "torch",
        "torchvision",
        "tensorflow",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.binaries = [
    b
    for b in a.binaries
    if (not _is_windows_system_dll(b[0]))
    and (not _is_gpu_ort_binary(b[0]))
    and (not _is_bloat_path(b[0]))
]
a.datas = [d for d in a.datas if not _is_bloat_path(d[0])]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CharacterWordCloud",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="data/images/icon.png",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="CharacterWordCloud",
)
