import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

openrouter_key = st.secrets.get("OPENROUTER_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")

if not openrouter_key or not tavily_key:
    st.error("Missing OPENROUTER_API_KEY or TAVILY_API_KEY in Streamlit secrets.")
    st.info("Add them under Manage app → Secrets before running the app.")
    st.stop()

st.write("Has OPENROUTER key:", bool(openrouter_key))
st.write("Has TAVILY key:", bool(tavily_key))

client = OpenAI(
    base_url="https://openrouter.ai/v1",
    api_key=openrouter_key,
)

tavily = TavilyClient(
    api_key=tavily_key
)

st.title("🌍 NGO Research Assistant")

query = st.text_input("Ask anything about NGOs...")

if st.button("Search"):
    if query:
        # Step 1: Search
        search_result = tavily.search(query)

        # Step 2: Generate answer
        answer = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
               {"role": "user", "content": f"Summarize:\n{search_result}"}
            ],
        ).choices[0].message.content

        # Step 3: Judge (evaluation)
        evaluation = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Evaluate this answer on:
- Accuracy
- Clarity
- Usefulness

Give score out of 10 and short feedback.

Answer:
{answer}
"""
                }
            ],
        ).choices[0].message.content

        # UI output
        st.subheader("📊 Answer")
        st.write(answer)

        st.subheader("🧠 AI Evaluation")
        st.write(evaluation)