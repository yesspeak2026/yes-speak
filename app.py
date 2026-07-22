from google import genai
import streamlit as st
import random
from lessons import LESSONS
from missions import MISSIONS

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="YES Speak",
    page_icon="🗣️",
    layout="wide"
)

# Gemini Client
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# ---------------- SESSION STATE ---------------- #

if "selected_mission" not in st.session_state:
    st.session_state.selected_mission = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🗣️ YES Speak")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🎯 Missions",
        "💬 AI Chat",
        "📈 Progress"
    ]
)

# ---------------- HOME ---------------- #

if page == "🏠 Home":

    st.title("🗣️ YES Speak")

    st.markdown("## Welcome to your AI English Coach!")

    st.divider()

    st.subheader("🎯 Today's Mission")

    today_mission = random.choice(MISSIONS)

    st.success(today_mission["name"])

    if st.button("🚀 Start Today's Mission", use_container_width=True):

        # Save selected mission
        st.session_state.selected_mission = today_mission

        # Start a fresh chat
        st.session_state.messages = []

        st.success(f"Mission selected: {today_mission['name']}")

    st.write("")

    st.markdown("### OR")

    st.button("🔄 Choose Another Mission", use_container_width=True)

# ---------------- MISSIONS ---------------- #

elif page == "🎯 Missions":

    st.title("🎯 Mission Library")

    st.write("Choose any mission you want to practice.")

    st.button("🗣️ Daily Conversation", use_container_width=True)

    st.button("⚖️ Debate", use_container_width=True)

    st.button("💼 Job Interview", use_container_width=True)

    st.button("🎤 Presentation", use_container_width=True)

    st.button("🤝 Meeting New People", use_container_width=True)

# ---------------- AI CHAT ---------------- #

elif page == "💬 AI Chat":

    st.title("💬 AI Coach")

    if st.session_state.selected_mission:
        st.info(f"Current Mission: {st.session_state.selected_mission['name']}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Type your message...")

    if prompt:

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.write(prompt)

        conversation = ""

        for message in st.session_state.messages:
            role = "User" if message["role"] == "user" else "AI"
            conversation += f"{role}: {message['content']}\n"

        mission_name = (
            st.session_state.selected_mission["name"]
            if st.session_state.selected_mission
            else "General Conversation"
        )

        prompt_text = f"""
You are YES Speak, a friendly English-speaking coach.

Current Mission:
{mission_name}

Your job is to:
- Encourage the learner.
- Correct grammar politely.
- Explain mistakes simply.
- End every reply with one follow-up question.
- Keep responses short and motivating.

Conversation:

{conversation}
"""

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt_text
        )

        reply = response.text

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        with st.chat_message("assistant"):
            st.write(reply)

# ---------------- PROGRESS ---------------- #

elif page == "📈 Progress":

    st.title("📈 Progress")

    st.metric("🔥 Streak", "0 Days")

    st.metric("⭐ XP", "0")

    st.metric("🎯 Missions Completed", "0")

    st.info("Progress tracking will be added soon.")