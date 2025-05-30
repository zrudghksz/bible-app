import streamlit as st
import os
import difflib
import pandas as pd

# --- 파일 경로 설정 ---
audio_dir = "audio"
full_audio_file = os.path.join(audio_dir, "full_audio.wav")

# --- 성경 본문 로드 및 엑셀 저장 ---
lines = []
with open("verses.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            parts = line.split(" ", 1)
            if len(parts) == 2:
                verse_num = parts[0].replace("절", "")
                verse_text = parts[1]
                lines.append({"절": int(verse_num), "본문": verse_text})

df = pd.DataFrame(lines)

with open("verses.txt", "r", encoding="utf-8") as f:
    verse_texts = [line.strip().split(" ", 1)[1] for line in f if line.strip() and len(line.strip().split(" ", 1)) > 1]

def compare_texts(correct, user):
    correct_clean = correct.replace(" ", "")
    user_clean = user.replace(" ", "")
    ratio = difflib.SequenceMatcher(None, correct_clean, user_clean).ratio()
    return ratio >= 0.95

st.set_page_config(page_title="성경 암송", page_icon="📓", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-image: url("...");  /* 배경이미지는 기존 url 유지 */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .block-container {
        padding-top: 5px !important;
        padding-bottom: 0px !important;
        padding-left: 3vw !important;
        padding-right: 3vw !important;
        max-width: 100vw !important;
    }
    .stTextArea textarea, .stTextInput input {
        font-size: 20px !important;
        min-height: 60px !important;
        background: rgba(255,255,255,0.97) !important;
        border-radius: 16px !important;
    }
    .stRadio, .stToggle, .stSelectbox {
        background: rgba(255,255,255,0.94) !important;
        border-radius: 12px !important;
    }
    h1 { font-size: 27px !important; margin-bottom: 5px !important; }
    </style>
""", unsafe_allow_html=True)


# ✅ [복구] 전체 스타일을 한 번에!
st.markdown("""
    <style>
    textarea::placeholder {
        color: black !important;
        opacity: 1 !important;
    }
    /* 모든 입력/선택 박스 공통 스타일 */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"], .stRadio, .stToggle {
        background: rgba(255,255,255,0.93) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba(40,40,40,0.10);
        font-size: 17px;
        color: #222 !important;
        font-weight: 500;
    }
    /* 드롭다운 select 박스 배경 */
    [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.95) !important;
    }
    /* 라디오/토글 컨테이너 가독성 보정 */
    .stRadio, .stToggle {
        background: rgba(255,255,255,0.88) !important;
        border-radius: 10px !important;
        margin-bottom: 10px;
        padding: 4px 12px 2px 12px;
    }
    .stApp {
        background-image: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgjzYaPOcaFmVZ2eJCpNVGJwIAcAKcGymqLfDfPKhLSV57kk78TPv2QrlU3lfdpXf-ljtq_5BKhEN1cG0fXSgpGROVtlet27V31fo9-U5JFRvBTnfGOE4ST9p71uw5vgRHb2xiJKL-d8H0ad1xafK_BG3jh4iSHUAMn37GxEOY2roENSUJMeEnTRN3o1hSx/s320/ChatGPT%20Image%202025%EB%85%84%205%EC%9B%94%2029%EC%9D%BC%20%EC%98%A4%ED%9B%84%2003_05_44.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stButton > button {
        background-color: #4a7ebb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #3a6ea5;
    }
    .result-table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.15);
        border-radius: 10px;
        overflow: hidden;
    }
    .result-table th {
        background-color: #4a7ebb;
        color: white;
        padding: 12px;
        font-size: 16px;
    }
    .result-table td {
        padding: 12px;
        text-align: center;
        font-size: 15px;
        background-color: #f9f9f9;
    }
    .result-tag {
       font-weight: bold;
        margin-left: 8px;
        color: green;
    }
    .result-tag.wrong {
        color: red;
    }
    .verse-highlight {
        background-color: rgba(255, 255, 255, 0.85);
        color: #222;
        padding: 12px 18px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        margin-top: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 앱 제목  ---
st.markdown("""
<div style="text-align:center; margin-top:10px;">
    <h1 style="font-family: 'Arial'; color: navy; margin: 0; font-size: 36px;">
        📓 성경 암송
    </h1>
</div>
""", unsafe_allow_html=True)

# ✅ 기존 모드 선택 로직 복원
mode = st.radio("**🎧 모드를 선택하세요**", ["부분 듣기", "전체 듣기", "부분 암송 테스트", "전체 암송 테스트"], index=0)

# ✅ 듣기 처리 ---
if mode == "부분 듣기":
    # 기존 부분 듣기 코드...
    verse_num_label = st.selectbox("들을 절을 선택하세요.", [f"{i}절" for i in range(1, len(verse_texts)+1)])
    verse_num = int(verse_num_label.replace("절", ""))
    file_name = f"{verse_num:02d}_{verse_num}절.wav"
    path = os.path.join(audio_dir, file_name)
    st.markdown("---")
    if os.path.exists(path):
        st.audio(path, format='audio/wav')
        st.markdown(f"<div class='verse-highlight'><b>{verse_texts[verse_num-1]}</b></div>", unsafe_allow_html=True)
    else:
        st.error("오디오 파일을 찾을 수 없습니다.")

    # ⭐⭐ 구간 듣기 반복 기능 추가 ⭐⭐
    st.markdown("---")
    st.markdown("### 📢 구간 반복 듣기")
    start_verse = st.number_input("시작 절", min_value=1, max_value=len(verse_texts), value=1, key="repeat_start")
    end_verse = st.number_input("끝 절", min_value=start_verse, max_value=len(verse_texts), value=start_verse, key="repeat_end")
    repeat_count = st.number_input("반복 횟수", min_value=1, max_value=10, value=2, key="repeat_num")

    if st.button("구간 반복 듣기"):
        for _ in range(repeat_count):
            for i in range(start_verse, end_verse+1):
                rep_path = os.path.join(audio_dir, f"{i:02d}_{i}절.wav")
                if os.path.exists(rep_path):
                    st.audio(rep_path, format='audio/wav')
                else:
                    st.warning(f"{i}절 오디오가 없습니다.")


elif mode == "전체 듣기":
    st.subheader("전체 오디오 자동 재생")
    st.info("전체 오디오를 자동으로 재생합니다.")
    if os.path.exists(full_audio_file):
        st.audio(full_audio_file, format="audio/wav")
    else:
        st.error("full_audio.wav 파일을 audio 폴더 안에 넣어주세요.")

elif mode == "부분 암송 테스트":
    st.subheader("🧠 부분 암송 테스트 (5절)")
    start_label = st.selectbox("📝 시작 절을 선택하세요.", [f"{i}절" for i in range(1, len(verse_texts) - 4)])
    start_num = int(start_label.replace("절", ""))

    # --- 한 절씩 정답 공개 기능 ---
    if "reveal_idx" not in st.session_state or st.session_state["reset_trigger"] != start_num:
        st.session_state["reveal_idx"] = 0
        st.session_state["reset_trigger"] = start_num

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        show_answer = st.toggle("정답 보기", value=False)
    with col2:
        check_result = st.toggle("결과 보기", value=False)
    with col3:
        if st.button("정답 한 줄씩 공개"):
            st.session_state["reveal_idx"] += 1

    for i in range(start_num, start_num + 5):
        verse_index = i - 1
        correct_text = verse_texts[verse_index]
        key = f"input_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""
        input_text = st.text_area(
            f"{i}절",
            value=st.session_state[key],
            key=key,
            placeholder=correct_text if show_answer or (i - start_num) < st.session_state["reveal_idx"] else "",
            label_visibility="visible"
        )
        # 결과 표시 기존 그대로
        if check_result:
            is_correct = compare_texts(correct_text, input_text.strip()) if input_text.strip() else False
            st.markdown(
                f"<div style='color:{'green' if is_correct else 'red'}; font-weight:bold; font-size:16px;'>"
                f"{'✅ 정답' if is_correct else '❌ 오답'}</div>",
                unsafe_allow_html=True
            )

elif mode == "전체 암송 테스트":
    st.subheader("🧠 전체 암송 테스트 (29절)")
    col1, col2 = st.columns([1, 1])
    with col1:
        show_answer = st.toggle("정답 보기", value=False)
    with col2:
        show_result = st.toggle("결과 보기", value=False)
    st.markdown("""
        <style>
        textarea::placeholder {
            color: black !important;
            opacity: 1 !important;
        }
        .result-tag {
            font-weight: bold;
            margin-left: 6px;
            color: green;
            font-size: 15px;
        }
        .result-tag.wrong {
            color: red;
        }
        </style>
    """, unsafe_allow_html=True)
    user_inputs = []
    for i in range(len(verse_texts)):
        correct_text = verse_texts[i]
        key = f"full_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""
        input_text = st.text_area(
            f"{i+1}절",
            value=st.session_state[key],
            key=key,
            placeholder=correct_text if show_answer else "",
            label_visibility="visible"
        )
        user_inputs.append(input_text)
        if show_result:
            is_correct = compare_texts(correct_text, input_text.strip()) if input_text.strip() else False
            st.markdown(
                f"<div class='result-tag {'wrong' if not is_correct else ''}'>"
                f"{'✅ 정답' if is_correct else '❌ 오답'}</div>",
                unsafe_allow_html=True
            )
