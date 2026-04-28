import streamlit as st
import pandas as pd
import numpy as np
import time

# -------- PAGE SETUP --------
st.set_page_config(page_title="Neuro Guru", layout="wide")
st.title("🧠 Neuro Guru - Live Focus Monitor")

# -------- FILE UPLOAD --------
uploaded_file = st.file_uploader("Upload EEG CSV", type=["csv"])

if uploaded_file is None:
    st.info("👋 Welcome! Please upload your EEG CSV file to begin your neuro-analysis.")
    st.stop()

# Load and Pre-calculate Data
df = pd.read_csv(uploaded_file)
df.columns = df.columns.str.strip().str.lower()

required_cols = ['alphalow', 'alphahigh', 'betalow', 'betahigh', 'theta']
missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"❌ Column mismatch! The CSV must have these headers: {required_cols}")
    st.stop()

# Brain State Math
# Alpha: Calm alertness | Beta: Active focus | Theta: Deep relaxation/Drowsiness
alpha = (0.6 * df['alphalow']) + (0.4 * df['alphahigh'])
beta = df['betalow'] + df['betahigh']
theta = df['theta']

df['focus'] = (beta / (alpha + theta + 1e-6)).rolling(10, min_periods=1).mean()
df['relax'] = (alpha / (beta + 1e-6)).rolling(10, min_periods=1).mean()
df['deep_relax'] = (df['alphalow'] / (beta + 1e-6)).rolling(10, min_periods=1).mean()

# -------- SESSION STATE --------
if "running" not in st.session_state: st.session_state.running = False
if "index" not in st.session_state: st.session_state.index = 0
if "messages" not in st.session_state: st.session_state.messages = []
if "last_state" not in st.session_state: st.session_state.last_state = {"f": 0, "r": 0, "d": 0}

# -------- UI CONTROLS --------
c1, c2 = st.columns(2)
with c1:
    if st.button("▶️ Start Session", use_container_width=True):
        st.session_state.running = True
with c2:
    if st.button("⏹ Stop & Reset", use_container_width=True):
        st.session_state.running = False
        st.session_state.index = 0
        st.rerun()

# Layout Placeholders
circle_placeholder = st.empty()
text_placeholder = st.empty()
metric_cols = st.columns(3)
chart_placeholder = st.empty()
progress_bar = st.progress(0)

# -------- CHATBOT SECTION --------
st.divider()
st.subheader("🤖 Ask Neuro Guru")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Ask: 'How is my focus?'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    cur = st.session_state.last_state
    
    if "status" in prompt.lower() or "how" in prompt.lower():
        reply = f"Current Focus: {cur['f']:.2f}. " + ("You're dialed in!" if cur['f'] > 1 else "Focus is dipping.")
    elif "stress" in prompt.lower():
        reply = "I'm monitoring your Alpha/Beta ratio. Try exhaling slowly to boost relaxation."
    else:
        reply = "I am your AI Brain Assistant. I interpret your live EEG data to help you optimize performance."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# -------- MAIN MONITORING & CONCLUSION LOOP --------
if st.session_state.running:
    i = st.session_state.index

    if i < len(df):
        f, r, d = df['focus'].iloc[i], df['relax'].iloc[i], df['deep_relax'].iloc[i]
        st.session_state.last_state = {"f": f, "r": r, "d": d}

        # Visual Feedback Logic
        if f > 1.2 and r > 1.0: color, msg = "#2ecc71", "🟢 Flow State Active"
        elif d > 1.1: color, msg = "#3498db", "🧘 Deeply Relaxed"
        elif f < 0.7: color, msg = "#e74c3c", "🔴 High Stress / Fatigue"
        else: color, msg = "#f1c40f", "🟡 Balanced State"

        circle_placeholder.markdown(f'''
            <div style="display: flex; justify-content: center;">
                <div style="width:160px; height:160px; border-radius:50%; background-color:{color}; 
                box-shadow: 0 0 40px {color}; transition: background-color 0.4s ease;"></div>
            </div>''', unsafe_allow_html=True)
        
        text_placeholder.markdown(f"<h3 style='text-align: center;'>{msg}</h3>", unsafe_allow_html=True)
        
        metric_cols[0].metric("Focus", f"{f:.2f}")
        metric_cols[1].metric("Relaxation", f"{r:.2f}")
        metric_cols[2].metric("Deep Relax", f"{d:.2f}")

        chart_placeholder.line_chart(df[['focus', 'relax']].iloc[:i+1])
        progress_bar.progress(min((i + 1) / len(df), 1.0))

        st.session_state.index += 1
        time.sleep(0.15) 
        st.rerun()
    
    else:
        # -------- FINAL REPORT SECTION --------
        st.session_state.running = False
        st.success("🏁 Session Analysis Complete!")
        st.markdown("---")
        st.header("📊 Final Neuro-Summary & Conclusion")
        
        avg_f = df['focus'].mean()
        avg_r = df['relax'].mean()
        
        rep1, rep2 = st.columns(2)
        with rep1:
            st.subheader("Your Profile")
            if avg_f > 1.1:
                st.write("🎯 **High Performer**: You maintained deep focus. Your Beta-to-Alpha ratio shows strong task engagement.")
            elif avg_f < 0.8:
                st.write("⚠️ **Scattered Attention**: Your data shows significant 'drift'. You were likely distracted or tired.")
            else:
                st.write("⚖️ **Steady Producer**: You maintained a consistent, sustainable effort without burning out.")

        with rep2:
            st.subheader("Guru's Advice")
            if avg_r < 0.9:
                st.write("🚨 **Urgent**: High stress markers. Take a 5-minute 'screen-free' break immediately.")
            else:
                st.write("✅ **Excellent**: You stayed calm while working. This is the 'Flow State'—the healthiest way to work.")

        st.info("💡 **Next Step:** To boost your scores, try 2 minutes of box-breathing before starting your next task.")
        if st.button("🔄 Analyze New Session"):
            st.session_state.index = 0
            st.rerun()