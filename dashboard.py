import streamlit as st
from kafka import KafkaConsumer
import json
from collections import defaultdict
import pandas as pd

st.set_page_config(page_title="Live Poll Dashboard", layout="wide")
st.title("📊 Live Poll Response Dashboard")

consumer = KafkaConsumer(
    'livepoll',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='dashboard-group',
    enable_auto_commit=True
)

question_short_labels = {
    'How was the Conference overall? (Rate between 1 - 5)': 'Q1',
    'How would you rate the keynote speaker? (Rate between Very Bad - Very Good)': 'Q2',
    'Did you find the breakout sessions informative?': 'Q3'
}

aggregated = defaultdict(lambda: defaultdict(int))
response_data = pd.DataFrame()

placeholder_counts = st.empty()
placeholder_charts = st.empty()
placeholder_table = st.empty()
placeholder_footer = st.empty()

for msg in consumer:
    try:
        data = json.loads(msg.value.decode('utf-8'))
        answer_id = data['answer_id']
        row = {'answer_id': answer_id}

        for item in data['answer_array']:
            for question, answer in item.items():
                aggregated[question][answer] += 1
                short_label = question_short_labels.get(question, question)
                row[short_label] = answer

        response_data = pd.concat([response_data, pd.DataFrame([row])], ignore_index=True)

        with placeholder_counts.container():
            st.subheader("🔢 Count Summary")
            for question, answers in aggregated.items():
                st.markdown(f"**{question}**")
                cols = st.columns(len(answers))
                for i, (answer, count) in enumerate(answers.items()):
                    cols[i].metric(label=answer, value=count)

        with placeholder_charts.container():
            st.subheader("📈 Poll Results (Bar Charts)")
            for question, answers in aggregated.items():
                st.subheader(question)
                df_chart = pd.DataFrame({
                    'Answer': list(answers.keys()),
                    'Count': list(answers.values())
                })
                st.bar_chart(df_chart.set_index('Answer'))

        with placeholder_table.container():
            st.subheader("🧾 All Poll Responses (Table)")
            st.dataframe(response_data.set_index('answer_id'), use_container_width=True)

        with placeholder_footer.container():
            st.markdown("---")
            st.markdown(
                "<p style='text-align: center; font-size: 14px;'>Created by <b>Syed Muhammad Mudassir Naqvi</b></p>",
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Error processing message: {e}")
