import streamlit as st
import random
from datetime import datetime

def take_quiz():
    # Retrieve the dynamic accent color from session state (defined in app.py)
    accent_color = st.session_state.get('active_accent', '#4f46e5')
    text_color = "#ffffff" # Default to white, or link to state if needed

    # --- STEP 1: LOGIN LOGIC ---
    if "active_student" not in st.session_state:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        name_input = st.text_input("Enter Student Name", placeholder="Type your name here")
        st.markdown('</div>', unsafe_allow_html=True)

        if not name_input:
            # Emoji-free Dynamic Themed Box
            st.markdown(
                f"""
                <div style="
                    background-color: {accent_color}1a; 
                    border: 1px solid {accent_color}4d; 
                    border-left: 5px solid {accent_color};
                    color: inherit; 
                    padding: 1rem 1.25rem; 
                    border-radius: 8px; 
                    margin-bottom: 20px;
                ">
                    <div style="font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px; color: {accent_color}; margin-bottom: 4px;">
                        System Notice
                    </div>
                    <div style="font-weight: 500; opacity: 0.9;">
                        Welcome. Please identify yourself to access the assessments.
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            return
        
        st.session_state.active_student = name_input
        
        all_greetings = ["Welcome", "Great to see you", "Greetings", "Good luck today", "Ready to learn"]
        if "greeting_pool" not in st.session_state or not st.session_state.greeting_pool:
            st.session_state.greeting_pool = all_greetings.copy()
            random.shuffle(st.session_state.greeting_pool)
        
        st.session_state.current_greeting = st.session_state.greeting_pool.pop(0)
        
        if not any(s["name"] == name_input for s in st.session_state.students):
            st.session_state.students.append({"id": len(st.session_state.students)+1, "name": name_input})
        
        st.rerun()

    # --- STEP 2: DISPLAY LOCKED NAME ---
    name = st.session_state.active_student.title()
    greeting = st.session_state.current_greeting
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"### {greeting}, **{name}**!")
    with c2:
        if st.button("Logout", use_container_width=True):
            del st.session_state.active_student
            st.session_state.current_quiz = None 
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- STEP 3: QUIZ LOGIC ---
    quiz = st.session_state.get("current_quiz", None)

    if quiz is None:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### Configure Session")
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            topic = st.selectbox("Select Subject", sorted(st.session_state.questions.keys()))
        with c2:
            diff = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
        with c3:
            count = st.select_slider("Question Count", options=[1, 3, 5, 10])
            
        if st.button("Initialize Assessment"):
            pool = st.session_state.questions[topic][diff.lower()]
            selected = random.sample(pool, min(count, len(pool)))
            st.session_state.current_quiz = {
                "student": name,
                "topic": topic,
                "difficulty": diff,
                "questions": selected,
                "answers": {},
                "start_time": datetime.now(),
                "is_completed": False,
                "show_results": False 
            }
            for i in range(len(selected)):
                st.session_state[f"q_idx_{i}"] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # --- ACTIVE QUIZ MODE ---
    if not quiz["is_completed"]:
        st.markdown(f"### {quiz['topic']} Assessment")
        
        # 1. Map dynamic colors
        diff_map = {"Easy": "#00C851", "Medium": "#FFBB33", "Hard": "#FF4444"}
        diff_accent = diff_map.get(quiz['difficulty'], "#ffffff")
        
        # 2. RESPONSIVE COUNTER
        total_questions = len(quiz["questions"])
        answered_count = sum(1 for i in range(total_questions) if st.session_state.get(f"q_idx_{i}") is not None)
        
        st.markdown(
            f'<p style="font-size: 1.4rem; font-weight: 700; margin-top: -15px; margin-bottom: 10px; letter-spacing: -0.5px;">'
            f'<span style="color: {diff_accent};">{quiz["difficulty"]} Mode</span>, '
            f'<span style="opacity: 0.9;">{answered_count}/{total_questions}</span>'
            f'</p>', 
            unsafe_allow_html=True
        )
        
        st.markdown(f"""
            <style>
                div[data-testid="stProgress"] > div > div > div > div {{
                    background-color: {diff_accent} !important;
                    height: 12px !important;
                }}
            </style>
            """, unsafe_allow_html=True)
        
        progress = answered_count / total_questions
        st.progress(progress)
        
        for i, q in enumerate(quiz["questions"]):
            user_ans = st.session_state.get(f"q_idx_{i}")
            quiz["answers"][i] = user_ans
            
            anim_class = ""
            if quiz["show_results"]:
                correct_ans = q.get("correct_answer") or q.get("correct")
                anim_class = "correct-pulse" if user_ans == correct_ans else "wrong-shake"
            
            st.markdown(f'<div class="custom-card {anim_class}">', unsafe_allow_html=True)
            st.markdown(f"**Question {i+1}**")
            
            # Use the global active_accent for radio buttons to avoid red
            st.markdown(f"""
                <style>
                div[role="radiogroup"] > label > div:first-child {{
                    border-color: {accent_color} !important;
                }}
                div[role="radiogroup"] > label > div:first-child > div {{
                    background-color: {accent_color} !important;
                }}
                </style>
            """, unsafe_allow_html=True)

            st.radio(
                q["question"], 
                q["options"], 
                key=f"q_idx_{i}", 
                index=None, 
                disabled=quiz["show_results"]
            )
            
            if quiz["show_results"]:
                correct_ans = q.get("correct_answer") or q.get("correct")
                if user_ans == correct_ans:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The right answer was: {correct_ans}")
            st.markdown('</div>', unsafe_allow_html=True)

        if not quiz["show_results"]:
            if st.button("Validate Answers"):
                quiz["show_results"] = True
                st.rerun()
        else:
            if st.button("Submit to Hall of Fame"):
                score = sum(1 for i, q in enumerate(quiz["questions"]) if quiz["answers"].get(i) == (q.get("correct_answer") or q.get("correct")))
                total = len(quiz["questions"])
                result = {
                    "student": quiz["student"],
                    "topic": quiz["topic"],
                    "difficulty": quiz["difficulty"],
                    "score": score,
                    "total": total,
                    "percentage": round((score/total)*100),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "time_taken": (datetime.now() - quiz["start_time"]).seconds
                }
                st.session_state.quiz_history.append(result)
                quiz["is_completed"] = True
                st.rerun()
    
    # Result Summary
    else:
        res = st.session_state.quiz_history[-1]
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### Assessment Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Final Score", f"{res['score']} / {res['total']}")
        col2.metric("Accuracy", f"{res['percentage']}%")
        col3.metric("Duration", f"{res['time_taken']} seconds")
        
        if res['percentage'] >= 60:
            st.success("Status: Passed")
        else:
            st.error("Status: Failed")
            
        if st.button("Start New Session"):
            for key in list(st.session_state.keys()):
                if key.startswith("q_idx_"):
                    del st.session_state[key]
            st.session_state.current_quiz = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)