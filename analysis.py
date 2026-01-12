import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def format_duration(seconds):
    """Formats seconds into MM:SS or HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def draw_gauge_chart(percentage, topic_name):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': topic_name, 'font': {'size': 18, 'color': 'white'}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#6366f1"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.1)"
        }
    ))
    fig.update_layout(
        height=220, 
        margin=dict(l=20, r=20, t=50, b=20), 
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Plus Jakarta Sans"}
    )
    return fig

def performance_analysis():
    if not st.session_state.quiz_history:
        st.info("No data available. Complete an assessment to see analytics.")
        return

    df = pd.DataFrame(st.session_state.quiz_history)
    
    # Force centering and bolding for the Profile Selection Heading
    st.markdown('<h3 style="text-align: center; font-weight: bold;">🔍 SELECT ANALYTICS PROFILE</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    selected_user = st.selectbox("Choose a student to view and export analytics", df["student"].unique(), label_visibility="collapsed")
    
    user_df = df[df["student"] == selected_user].copy()
    
    # --- PREPARE CLEAN EXPORT DATA ---
    export_df = user_df.copy()
    
    # 1. Mastery Level Formatting
    def calculate_mastery_plain(pct):
        if pct >= 90: return "Master"
        if pct >= 75: return "Proficient"
        if pct >= 50: return "Developing"
        return "Novice"
    export_df['Mastery Level'] = export_df['percentage'].apply(calculate_mastery_plain)
    
    # 2. Time Taken Formatting
    export_df['time_taken'] = export_df['time_taken'].apply(format_duration)

    # 3. Date Formatting (Convert to AM/PM)
    def format_to_ampm(date_str):
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            return dt.strftime("%Y-%m-%d %I:%M %p")
        except:
            return date_str # Return original if already formatted
    export_df['date'] = export_df['date'].apply(format_to_ampm)
    
    # 4. Capitalize Headers
    export_df.columns = [col.upper() for col in export_df.columns]

    csv = export_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label=f"📥 Export Full Analytics for {selected_user} (CSV)",
        data=csv,
        file_name=f"QuizLearn_Analytics_{selected_user}.csv",
        mime='text/csv',
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Analytics Visuals ---
    # Centered and Bold Performance Heading
    st.markdown(f'<h2 style="text-align: center; font-weight: bold;">PERFORMANCE METRICS FOR {selected_user.upper()}</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="text-align: center; font-weight: bold;">TOPIC MASTERY LEVEL</h4>', unsafe_allow_html=True)
    topic_summary = user_df.groupby("topic")["percentage"].mean().reset_index()
    gauge_cols = st.columns(len(topic_summary))
    
    for idx, row in topic_summary.iterrows():
        with gauge_cols[idx]:
            st.plotly_chart(draw_gauge_chart(row['percentage'], row['topic']), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="text-align: center; font-weight: bold;">SCORE PROGRESSION OVER TIME</h4>', unsafe_allow_html=True)
    
    # Use format_to_ampm on the visual chart as well
    user_df['date_display'] = user_df['date'].apply(format_to_ampm)
    
    line_fig = px.line(user_df, x="date_display", y="percentage", markers=True, template="plotly_dark")
    line_fig.update_traces(line_color='#a855f7', marker=dict(size=10))
    line_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Date and Time of Assessment",
        yaxis_title="Percentage Score"
    )
    st.plotly_chart(line_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)