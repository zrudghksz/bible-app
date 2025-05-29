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

st.set_page_config(page_title="골로새서 암송 도우미", page_icon="📓", layout="centered")
st.markdown("""
    <style>
    textarea::placeholder {
        color: black !important;
        opacity: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)


# ✅ UI 고도화 스타일 패키지 적용
st.markdown("""
    <style>
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
        📓 성경 암송 도우미
    </h1>
</div>
""", unsafe_allow_html=True)

# ✅ 기존 모드 선택 로직 복원
mode = st.radio("**🎧 모드를 선택하세요**", ["부분 듣기", "전체 듣기", "부분 암송 테스트", "전체 암송 테스트"], index=0)

# ✅ 분기 처리 ---
if mode == "부분 듣기":
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

    # 👉 정답 보기 / 결과 보기 토글 나란히
    col1, col2 = st.columns(2)
    with col1:
        show_answer = st.toggle("정답 보기", value=False)
    with col2:
        check_result = st.toggle("결과 보기", value=False)

    # ✅ 입력값과 결과 따로 저장
    user_inputs = []
    correctness = []

    for i in range(start_num, start_num + 5):
        verse_index = i - 1
        correct_text = verse_texts[verse_index]

        # 사용자의 기존 입력 유지 (세션 상태 저장용)
        key = f"input_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""

        # 입력창 표시
        input_text = st.text_area(
            f"{i}절",
            value=st.session_state[key],
            key=key,
            placeholder=correct_text if show_answer else "",
            label_visibility="visible"
        )

        user_inputs.append(input_text)

        # 결과 보기일 때만 정답 비교
        if check_result:
            is_correct = compare_texts(correct_text, input_text.strip()) if input_text.strip() else False
            correctness.append(is_correct)

            st.markdown(
                f"<div style='color:{'green' if is_correct else 'red'}; font-weight:bold; font-size:16px;'>"
                f"{'✅ 정답' if is_correct else '❌ 오답'}</div>",
                unsafe_allow_html=True
            )




elif mode == "전체 암송 테스트":
    st.subheader("🧠 전체 암송 테스트 (29절)")

    # 👉 정답 보기 / 결과 보기 토글 나란히 표시
    col1, col2 = st.columns([1, 1])
    with col1:
        show_answer = st.toggle("정답 보기", value=False)
    with col2:
        show_result = st.toggle("결과 보기", value=False)

    # ✅ placeholder 색상 검정으로 설정
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

        # 기존 입력 유지
        if key not in st.session_state:
            st.session_state[key] = ""

        # 입력창
        input_text = st.text_area(
            f"{i+1}절",
            value=st.session_state[key],
            key=key,
            placeholder=correct_text if show_answer else "",
            label_visibility="visible"
        )

        user_inputs.append(input_text)

        # 결과 보기 시 정답 비교
        if show_result:
            is_correct = compare_texts(correct_text, input_text.strip()) if input_text.strip() else False
            st.markdown(
                f"<div class='result-tag {'wrong' if not is_correct else ''}'>"
                f"{'✅ 정답' if is_correct else '❌ 오답'}</div>",
                unsafe_allow_html=True
            )
