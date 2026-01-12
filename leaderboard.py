import streamlit as st
import pandas as pd

def leaderboard():
    st.markdown("## Leaderboard")

    if not st.session_state.quiz_history:
        st.info("No data available.")
        return

    df = pd.DataFrame(st.session_state.quiz_history)
    leaderboard_df = (df.groupby("student")
                      .agg(Average_Percentage=("percentage","mean"), Quizzes_Taken=("student","count"))
                      .reset_index()
                      .sort_values("Average_Percentage", ascending=False))
    leaderboard_df["Average_Percentage"] = leaderboard_df["Average_Percentage"].round(1)
    leaderboard_df = leaderboard_df.rename(columns={
        "student":"Student", "Average_Percentage":"Average Percentage", "Quizzes_Taken":"Quizzes Taken"
    })

    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
        st.dataframe(leaderboard_df[["Student","Average Percentage","Quizzes Taken"]],
                     use_container_width=True)
    with col2:
        st.bar_chart(leaderboard_df.set_index("Student")["Average Percentage"])
    st.markdown('</div>', unsafe_allow_html=True)
