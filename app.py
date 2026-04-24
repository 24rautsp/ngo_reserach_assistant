import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

import streamlit as st

st.write("Has OPENROUTER key:", "OPENROUTER_API_KEY" in st.secrets)
st.write("Has TAVILY key:", "TAVILY_API_KEY" in st.secrets)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

tavily = TavilyClient(
    api_key=st.secrets["TAVILY_API_KEY"]
)

st.title("🌍 NGO Research Assistant")

query = st.text_input("Ask anything about NGOs...")

if st.button("Search"):
    if query:
        # Step 1: Search
        search_result = tavily.search(query)

        # Step 2: Generate answer
        answer = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "user", "content": f"Answer clearly:\n{search_result}"}
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