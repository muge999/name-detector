import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="名字检测工具", page_icon="📝")

st.title("📝 名字检测工具")

# 名字库
DEFAULT_NAMES = ["徐锐", "田芸", "王忠", "文芮", "徐荣", "徐晓彬", "郑静"]

# 侧边栏
with st.sidebar:
    st.header("设置")
    use_default = st.checkbox("使用默认名字库", value=True)
    if use_default:
        name_list = DEFAULT_NAMES
    else:
        name_input = st.text_area("名字库（每行一个）", "\n".join(DEFAULT_NAMES))
        name_list = [n.strip() for n in name_input.split("\n") if n.strip()]
    st.write(f"共 {len(name_list)} 人")

# 上传
uploaded_file = st.file_uploader("上传图片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=300)
    
    if st.button("开始检测"):
        with st.spinner("识别中..."):
            try:
                reader = easyocr.Reader(['ch_sim', 'en'])
                result = reader.readtext(np.array(image))
                detected = [text for (_, text, _) in result]
                
                appeared = [n for n in name_list if any(n in d or d in n for d in detected)]
                missing = [n for n in name_list if n not in appeared]
                
                st.success(f"✅ 已出现: {appeared}")
                if missing:
                    st.error(f"❌ 未出现: {missing}")
                else:
                    st.success("🎉 全部出现！")
            except Exception as e:
                st.error(f"错误: {e}")
