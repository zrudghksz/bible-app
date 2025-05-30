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

# --- 문자 스타일 ---
st.markdown("""
<style>
.stRadio label {
    color: #29519d !important;  /* 파랑, 진하게 */
    font-weight: 600 !important;
    font-size: 1.10em !important;
}

h1 {
    color: #203a5e !important;
    background: rgba(255,255,255,0.85);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 2rem !important;
    font-weight: 700 !important;
    margin-bottom: 18px !important;
    box-shadow: 0 1px 8px rgba(80,90,100,0.08);
}

/* 소제목(섹션 제목 등)은 살짝만 강조 */
h2, h3 {
    color: #29519d !important;
    background: rgba(255,255,255,0.80);
    border-radius: 7px;
    padding: 7px 13px 7px 12px;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    margin-bottom: 14px !important;
}

/* ------ 강조 안내문, 자막용 박스 스타일 추가 ------ */
.markdown-highlight {
    background: rgba(255,255,255,0.98);
    border-radius: 8px;
    padding: 8px 12px;
    color: #16366a;
    font-size: 1.07em;
    font-weight: 600;
    margin-bottom: 8px;
    box-shadow: 0 1px 7px rgba(180,180,200,0.09);
}

/* 전체 폰트: 더 진하게, 약간 어두운 색 */
body, .stApp, .stMarkdown, .stRadio label, .stToggle label, .stSelectbox label, label, .st-b8, .css-1c7y2kd {
    color: #23272f !important;
    font-weight: 500 !important;
    font-size: 1.04em !important;
}

/* 안내/강조문: 진한 글씨+연한 흰 배경 */
.markdown-highlight {
    background: rgba(255,255,255,0.90);
    border-radius: 8px;
    padding: 8px 12px;
    color: #16366a;
    font-size: 1.07em;
    font-weight: 600;
    margin-bottom: 8px;
    box-shadow: 0 1px 7px rgba(180,180,200,0.09);
}

/* 입력창, 셀렉트, 라디오 등은 기본 Streamlit 스타일 최대한 유지 */
.stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,0.96) !important;
    border-radius: 10px !important;
    box-shadow: 0 3px 10px rgba(60,60,70,0.08);
    font-size: 1em !important;
    color: #23272f !important;
    font-weight: 500 !important;
}

/* 앱 배경은 기존 사진 유지 */
.stApp {
    background-image: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgjzYaPOcaFmVZ2eJCpNVGJwIAcAKcGymqLfDfPKhLSV57kk78TPv2QrlU3lfdpXf-ljtq_5BKhEN1cG0fXSgpGROVtlet27V31fo9-U5JFRvBTnfGOE4ST9p71uw5vgRHb2xiJKL-d8H0ad1xafK_BG3jh4iSHUAMn37GxEOY2roENSUJMeEnTRN3o1hSx/s320/ChatGPT%20Image%202025%EB%85%84%205%EC%9B%94%2029%EC%9D%BC%20%EC%98%A4%ED%9B%84%2003_05_44.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
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
    st.subheader("🧠 부분 암송 테스트 (5절)")
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

        # 각 절별로 정답보기 체크박스
        show_this_answer = st.checkbox(f"{i}절 정답보기", key=f"show_answer_{i}")

        # --- 개선(정답을 value에 넣어 진하게 보임) ---
        # (입력값 대신 정답을 표시, 전체/절별 정답보기일 때만)
        if show_answer or show_this_answer:
            display_value = correct_text
        else:
            display_value = st.session_state[key]

        input_text = st.text_area(
            f"{i}절",
            value=display_value,
            key=key,
            placeholder="",   # placeholder 사용 안함!
            label_visibility="visible"
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
