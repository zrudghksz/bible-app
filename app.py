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


st.markdown("""
<style>
/* ==== 전체 앱 배경 이미지 완전 적용 ==== */
html, body, .stApp {
    background-image: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgjzYaPOcaFmVZ2eJCpNVGJwIAcAKcGymqLfDfPKhLSV57kk78TPv2QrlU3lfdpXf-ljtq_5BKhEN1cG0fXSgpGROVtlet27V31fo9-U5JFRvBTnfGOE4ST9p71uw5vgRHb2xiJKL-d8H0ad1xafK_BG3jh4iSHUAMn37GxEOY2roENSUJMeEnTRN3o1hSx/s320/ChatGPT%20Image%202025%EB%85%84%205%EC%9B%94%2029%EC%9D%BC%20%EC%98%A4%ED%9B%84%2003_05_44.png");
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    background-repeat: no-repeat !important;
}

/* 라디오(모드 선택) 체크/동그라미 아이콘 숨김 */
[data-baseweb="radio"] label > span:first-child {
    display: none !important;
}

/* 라디오 항목 스타일(박스형) */
[data-baseweb="radio"] label {
    display: block !important;
    width: 100%;
    border-radius: 12px !important;
    padding: 7px 22px !important;
    margin-bottom: 8px !important;
    font-size: 1.14em !important;
    font-weight: 700 !important;
    color: #22537d !important;
    background: #f4f8ff !important;
    border: 2.5px solid #f4f8ff !important;
    box-shadow: 0 1.5px 7px #b9d4fa;
    cursor: pointer;
    transition: background 0.16s, color 0.16s, border 0.16s;
}

/* 마우스 오버 효과 */
[data-baseweb="radio"] label:hover {
    background: #e3eeff !important;
    border: 2.5px solid #5795ef !important;
    color: #103c79 !important;
}

/* 선택된 항목: 배경+글씨 강조 */
[data-baseweb="radio"] input:checked + div label {
    background: #3977d5 !important;
    border: 2.5px solid #3977d5 !important;
    color: #fff !important;
    font-weight: 900 !important;
    box-shadow: 0 2px 10px #a9ccff;
}

/* 전체 라디오 컨테이너(테두리+배경) */
.stRadio {
    background: linear-gradient(92deg, #e5f0fb 80%, #d2e3f8 100%) !important;
    border-radius: 16px !important;
    box-shadow: 0 6px 30px rgba(30,70,120,0.10), 0 1.5px 12px #aacdee;
    padding: 20px 28px 18px 22px !important;
    border: 2.5px solid #86b8ea !important;
    margin-bottom: 18px;
}
.markdown-highlight {
    background: rgba(255,255,255,0.96);
    border-radius: 8px;
    padding: 10px 16px 9px 16px;
    color: #193e73;
    font-size: 1.13em;
    font-weight: 700;
    margin: 8px 0 13px 0;
    box-shadow: 0 3px 16px rgba(60,80,120,0.10);
    letter-spacing: 0.01em;
    line-height: 1.7em;
    transition: background 0.18s;
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
    # 1. 안내문구(하얀색) 별도 출력
    st.markdown(
        "<span style='color:#fff; font-size:1.00em; font-weight:800; display:block; margin-bottom:-100px;'>들을 절을 선택하세요.</span>",
        unsafe_allow_html=True
    )
    # 2. selectbox 라벨은 빈 문자열
    verse_num_label = st.selectbox("", [f"{i}절" for i in range(1, len(verse_texts)+1)])
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
    st.markdown(
        "<span style='color:#fff; font-size:1.13em; font-weight:900;'>🎵 전체 오디오 자동 재생</span>",
        unsafe_allow_html=True
    )
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
        show_answer = st.toggle("전체 정답 보기", value=False, key="partial_show_answer")
    with col2:
        check_result = st.toggle("결과 보기", value=False, key="partial_show_result")

    for i in range(start_num, start_num + 5):
        verse_index = i - 1
        correct_text = verse_texts[verse_index]
        key = f"input_partial_{i}"

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

        # 정답 보기 켜진 경우
        if show_answer:
            st.markdown(
                f"""
                <div style="
                    background: #fff;
                    color: #222
                    border-radius: 7px;
                    padding: 9px 18px;
                    font-size: 1.10em;
                    font-weight: 400;
                    border: 2px solid #b3c9ee;
                    margin-bottom: 10px;">
                {correct_text}
                </div>
                """, unsafe_allow_html=True
            )
            # 입력창을 덮어쓰지 않음(세션 유지 X)
        else:
            input_text = st.text_area(
                "",
                value=st.session_state.get(key, ""),
                key=key,
                placeholder="직접 입력해 보세요.",
                label_visibility="collapsed"
            )

            # 결과 보기
            if check_result:
                if input_text.strip() == "":
                    st.markdown(
                        f"<div style='color:#d63e22; font-weight:900; font-size:16px;'>❌ 오답</div>",
                        unsafe_allow_html=True
                    )
                else:
                    is_correct = compare_texts(correct_text, input_text)
                    st.markdown(
                        f"<div style='color:{'green' if is_correct else '#d63e22'}; font-weight:900; font-size:16px;'>"
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

    for i in range(len(verse_texts)):    # ← 여기 들여쓰기 맞춰야 함
        correct_text = verse_texts[i]
        key = f"full_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""

        # ---- 절 번호 상자 라벨 추가 ----
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
            ">{i+1}절</span>
            """,
            unsafe_allow_html=True
        )

        input_text = st.text_area(
            "",
            value=st.session_state[key],
            key=key,
            placeholder=correct_text if show_answer else "",
            label_visibility="collapsed"
        )
        user_inputs.append(input_text)
        if show_result:
            is_correct = compare_texts(correct_text, input_text.strip()) if input_text.strip() else False
            st.markdown(
                f"<div class='result-tag {'wrong' if not is_correct else ''}'>"
                f"{'✅ 정답' if is_correct else '❌ 오답'}</div>",
                unsafe_allow_html=True
            )
