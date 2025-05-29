import streamlit as st
import random

# 色塊生成函式
def generate_color():
    r = random.randint(50, 200)
    g = random.randint(50, 200)
    b = random.randint(50, 200)
    return f"#{r:02x}{g:02x}{b:02x}", (r, g, b)

def adjust_brightness(rgb, factor=1.2):
    r, g, b = rgb
    r = min(max(int(r * factor), 0), 255)
    g = min(max(int(g * factor), 0), 255)
    b = min(max(int(b * factor), 0), 255)
    return f"#{r:02x}{g:02x}{b:02x}"

# 初始化狀態
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'round' not in st.session_state:
    st.session_state.round = 1
if 'grid_size' not in st.session_state:
    st.session_state.grid_size = 3
if 'correct_index' not in st.session_state:
    st.session_state.correct_index = 0

# 顯示標題
st.title("🎨 找出不同的色塊！")
st.write(f"第 {st.session_state.round} 回合")
st.write(f"目前分數：{st.session_state.score}")

# 設定網格
grid_size = st.session_state.grid_size
total_buttons = grid_size * grid_size

# 產生顏色
base_color, base_rgb = generate_color()
diff_color = adjust_brightness(base_rgb, 1.15)
correct_index = random.randint(0, total_buttons - 1)
st.session_state.correct_index = correct_index

# 建立按鈕網格
cols = st.columns(grid_size)
for i in range(total_buttons):
    color = diff_color if i == correct_index else base_color
    with cols[i % grid_size]:
        if st.button(" ", key=f"btn_{i}", help="點擊這個色塊", 
                     args=(i,), use_container_width=True):
            if i == st.session_state.correct_index:
                st.success("🎉 答對了！")
                st.session_state.score += 1
            else:
                st.error("😢 答錯了...")
            st.session_state.round += 1
            if st.session_state.round % 3 == 0:
                st.session_state.grid_size += 1  # 隨回合增加難度
            st.experimental_rerun()

# 重設按鈕
if st.button("🔁 重新開始"):
    st.session_state.score = 0
    st.session_state.round = 1
    st.session_state.grid_size = 3
    st.experimental_rerun()
