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


def get_chat_content(response):
    try:
        return response.choices[0].message.content
    except Exception:
        try:
            return response["choices"][0]["message"]["content"]
        except Exception:
            return ""


st.title("🌍 NGO Research Assistant")

query = st.text_input("Ask anything about NGOs...")

if st.button("Search"):
    if query:
        # Step 1: Search
        search_result = tavily.search(query)

        # Step 2: Generate answer
        answer_resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
               {"role": "user", "content": f"Summarize:\n{search_result}"}
            ],
        )
        answer = get_chat_content(answer_resp)

        # Step 3: Judge (evaluation)
        evaluation_resp = client.chat.completions.create(
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
        )
        evaluation = get_chat_content(evaluation_resp)

        # UI output
        st.subheader("📊 Answer")
        st.write(answer)

        st.subheader("🧠 AI Evaluation")
        st.write(evaluation)