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


# 문자 및 상자 ---
st.markdown("""
<style>
/* ================== 앱 배경 ================== */
.stApp {
    background-image: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgjzYaPOcaFmVZ2eJCpNVGJwIAcAKcGymqLfDfPKhLSV57kk78TPv2QrlU3lfdpXf-ljtq_5BKhEN1cG0fXSgpGROVtlet27V31fo9-U5JFRvBTnfGOE4ST9p71uw5vgRHb2xiJKL-d8H0ad1xafK_BG3jh4iSHUAMn37GxEOY2roENSUJMeEnTRN3o1hSx/s320/ChatGPT%20Image%202025%EB%85%84%205%EC%9B%94%2029%EC%9D%BC%20%EC%98%A4%ED%9B%84%2003_05_44.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* ========== 타이틀/섹션(상단) 하늘색 박스 ========== */
h1, h2, h3, .section-title {
    color: #193e73 !important;
    background: linear-gradient(92deg, #e0f3ff 80%, #c9e9fa 100%) !important;
    border-radius: 10px !important;
    padding: 13px 18px !important;
    font-weight: 900 !important;
    font-size: 1.35em !important;
    box-shadow: 0 2px 10px rgba(60,70,90,0.10);
    margin-bottom: 18px !important;
    text-shadow: 0 2px 8px #fff, 0 1px 7px #b5e0fc !important;
}

/* ========== 라디오(원) 선택 진하게 ========== */
[data-baseweb="radio"] label > span:first-child {
    border: 3px solid #103477 !important;
    background: #fff !important;
    border-radius: 50% !important;
    width: 24px !important;
    height: 24px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-right: 10px !important;
}
[data-baseweb="radio"] label > span:first-child > div {
    background: #103477 !important;
    width: 12px !important;
    height: 12px !important;
    border-radius: 50% !important;
    box-shadow: 0 0 5px #b2c8fa;
}
[data-baseweb="radio"] label {
    font-weight: 800 !important;
    font-size: 1.08em !important;
    color: #22336b !important;
}

/* ========== (하단) 라벨: 정답/결과/절번호 등 ========== */
.stRadio label, .stToggle label, .stCheckbox label, .stSelectbox label, label,
.stTextInput > label, .stTextArea > label, .st-b8, .css-1c7y2kd {
    color: #fff !important;
    font-weight: 800 !important;
    font-size: 1.10em !important;
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ========== 라디오 박스(메뉴 전체 박스) ========== */
.stRadio {
    background: linear-gradient(92deg, #e3f2fd 60%, #f5faff 100%) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 20px rgba(65,125,185,0.08), 0 1.5px 12px #b4dbfb;
    padding: 10px 18px 10px 16px;
    border: 1.5px solid #aed7fa !important;
    margin-bottom: 13px;
}

/* ========== 체크박스/토글 라벨(진한 파랑, 필요한 경우) ========== */
.stCheckbox label, .stToggle label {
    color: #2274ad !important;
    font-weight: 900 !important;
    font-size: 1.09em !important;
    background: none !important;
}

/* ========== 드롭다운 옵션 ========== */
[data-baseweb="select"] > div {
    color: #2350aa !important;
    font-weight: 800 !important;
}

/* ========== 안내/강조문 ========== */
.markdown-highlight {
    background: rgba(255,255,255,0.95);
    border-radius: 8px;
    padding: 10px 14px;
    color: #1a377b;
    font-size: 1.08em;
    font-weight: 700;
    margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(160,170,210,0.13);
}

/* ========== 전체 폰트 ========== */
body, .stApp, .stMarkdown {
    color: #23272f !important;
    font-weight: 500 !important;
    font-size: 1.04em !important;
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
    verse_num_label = st.selectbox("들을 절을 선택하세요.", [f"{i}절" for i in range(1, len(verse_texts)+1)])
    verse_num = int(verse_num_label.replace("절", ""))
    file_name = f"{verse_num:02d}_{verse_num}절.wav"
    path = os.path.join(audio_dir, file_name)
    st.markdown("---")
    if os.path.exists(path):
        st.audio(path, format='audio/wav')
        st.markdown(
    f"<div class='markdown-highlight'>{verse_texts[verse_num-1]}</div>",
    unsafe_allow_html=True
)

    else:
        st.error("오디오 파일을 찾을 수 없습니다.")


elif mode == "전체 듣기":
    st.markdown("🎵  전체 오디오 자동 재생", unsafe_allow_html=True)
    st.markdown(
    "<div class='markdown-highlight'>전체 오디오를 자동으로 재생합니다.</div>",
    unsafe_allow_html=True
)
    if os.path.exists(full_audio_file):
        st.audio(full_audio_file, format="audio/wav")
    else:
        st.error("full_audio.wav 파일을 audio 폴더 안에 넣어주세요.")

elif mode == "부분 암송 테스트":
    st.subheader("🧠 부분 암송 테스트 (5절씩)")
    start_label = st.selectbox("📝 시작 절을 선택하세요.", [f"{i}절" for i in range(1, len(verse_texts) - 4)])
    start_num = int(start_label.replace("절", ""))

    col1, col2 = st.columns(2)
    with col1:
        show_answer = st.toggle("전체 정답 보기", value=False)
    with col2:
        check_result = st.toggle("결과 보기", value=False)

    user_inputs = []
    correctness = []

    for i in range(start_num, start_num + 5):
        verse_index = i - 1
        correct_text = verse_texts[verse_index]
        key = f"input_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""

        # --- 각 절 라벨 스타일 강조 ---
        st.markdown(
            f"""
            <span style="
                display: inline-block;
                background: rgba(255,255,255,0.94);
                color: #14428c;
                font-size: 1.15em;
                font-weight: 800;
                padding: 4px 13px 4px 10px;
                border-radius: 7px;
                margin-bottom: 6px;
                box-shadow: 0 2px 12px rgba(70,70,120,0.13);
            ">{i}절</span>
            """,
            unsafe_allow_html=True
        )


        # --- 입력창 (정답 보기 시 정답 표시, 아니면 입력값) ---
        if show_answer:
            display_value = correct_text
        else:
            display_value = st.session_state[key]

        input_text = st.text_area(
            "",
            value=display_value,
            key=key,
            placeholder="직접 입력해 보세요.",
            label_visibility="collapsed"
        )

        user_inputs.append(input_text)

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
