import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="名字检测工具",
    page_icon="📝",
    layout="wide"
)

# 标题
st.title("📝 名字检测工具")
st.markdown("上传图片，自动检测哪些名字已出现、哪些未出现")

# 名字库（可根据需要修改）
DEFAULT_NAMES = ["徐锐", "田芸", "王忠", "文芮", "徐荣", "徐晓彬", "郑静"]

# 侧边栏设置
st.sidebar.header("⚙️ 设置")

# 允许用户修改名字库
use_default = st.sidebar.checkbox("使用默认名字库", value=True)

if use_default:
    name_list = DEFAULT_NAMES
else:
    name_input = st.sidebar.text_area(
        "请输入名字库（每行一个）",
        "\n".join(DEFAULT_NAMES)
    )
    name_list = [n.strip() for n in name_input.split("\n") if n.strip()]

st.sidebar.markdown("---")
st.sidebar.caption(f"当前名字库共 **{len(name_list)}** 人")

# 上传图片
uploaded_file = st.file_uploader(
    "选择图片",
    type=["jpg", "jpeg", "png", "bmp", "tiff"],
    help="支持 jpg、png、bmp 等常见格式"
)

# 检测按钮
if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="上传的图片", use_container_width=True)
    
    if st.button("🔍 开始检测", type="primary"):
        with st.spinner("正在识别图片中的文字，请稍候..."):
            try:
                # 初始化 OCR
                reader = easyocr.Reader(['ch_sim', 'en'])
                
                # 转换为 numpy 数组
                img_array = np.array(image)
                
                # 执行识别
                result = reader.readtext(img_array)
                
                # 提取识别到的文字
                detected_texts = []
                for (bbox, text, confidence) in result:
                    detected_texts.append(text.strip())
                    st.caption(f"识别到: {text} (置信度: {confidence:.2f})")
                
                # 匹配名字
                appeared = []
                missing = []
                
                for name in name_list:
                    matched = False
                    for detected in detected_texts:
                        if name == detected or name in detected or detected in name:
                            matched = True
                            break
                    
                    if matched:
                        appeared.append(name)
                    else:
                        missing.append(name)
                
                # 显示结果
                with col2:
                    st.success(f"✅ 已出现的名字（{len(appeared)} 个）")
                    if appeared:
                        for name in appeared:
                            st.write(f"  - {name}")
                    else:
                        st.info("未识别到任何名字")
                    
                    st.markdown("---")
                    
                    if missing:
                        st.error(f"❌ 未出现的名字（{len(missing)} 个）")
                        for name in missing:
                            st.write(f"  - {name}")
                    else:
                        st.success("🎉 所有名字都已出现！")
                
                # 显示识别到的所有文字（调试用）
                with st.expander("📋 识别到的所有文字"):
                    st.write(detected_texts)
                    
            except Exception as e:
                st.error(f"识别失败：{str(e)}")
                st.info("请尝试更换更清晰的图片")

else:
    st.info("👈 请先上传图片")

# 页脚
st.markdown("---")
st.caption("提示：图片越清晰，识别准确率越高。建议拍摄时保证光线充足、文字清晰可见。")