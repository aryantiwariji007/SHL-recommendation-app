import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/recommend"

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
st.title("🔍 SHL Assessment Recommendation Engine")

st.markdown("Enter a job description or natural language query to get SHL assessment recommendations:")

user_query = st.text_area(
    "Job Description / Query",
    "Looking for an adaptive, remote numerical reasoning test for tech roles"
)

if st.button("Get Recommendations"):
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Talking to the backend..."):
            response = requests.post(API_URL, json={"input_query": user_query})
        
        if response.status_code == 200:
            results = response.json()["recommended_assessments"]
            if results:
                st.subheader("✅ Top Recommendations")
                st.markdown(
                    """
                    <style>
                        table, th, td {
                            border: none;
                            padding: 8px 16px;
                            text-align: left;
                        }
                        th { font-weight: bold; }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("<table><tr><th>Name</th><th>Remote</th><th>Adaptive</th><th>Duration</th><th>Type</th></tr>", unsafe_allow_html=True)
                for item in results:
                    st.markdown(f"""
                    <tr>
                        <td><a href="{item['url']}" target="_blank">{item['name']}</a></td>
                        <td>{item['remote_testing']}</td>
                        <td>{item['adaptive_irt']}</td>
                        <td>{item['duration_mins']} min</td>
                        <td>{item['type']}</td>
                    </tr>
                    """, unsafe_allow_html=True)
                st.markdown("</table>", unsafe_allow_html=True)
            else:
                st.warning("No matching assessments found.")
        else:
            st.error(f"API Error: {response.status_code}")
