# nalanda_neuroguru
An AI-powered EEG analysis dashboard that monitors live focus and relaxation states using Streamlit. Features real-time visual biofeedback and a post-session cognitive health report
# 🧠 Neuro Guru - Live EEG Focus Monitor

Neuro Guru is a real-time neurofeedback application built with Streamlit. It processes raw EEG frequency data to visualize a user's cognitive state, providing actionable insights into focus, stress, and deep relaxation.

## 🚀 Features
- **Live State Visualization**: A dynamic "Glow Orb" that changes color based on Beta/Alpha/Theta ratios.
- **AI Neuro-Assistant**: A chatbot that provides real-time status updates and stress-management advice.
- **Automatic Session Conclusion**: Generates a post-session summary with a "Brain Profile" (e.g., Flow State, Mental Fatigue).
- **Interactive Metrics**: Live line charts and progress tracking.

## 📊 How it Works
The app calculates brain states using standard BCI ratios:
- **Focus Score**: $\frac{\text{Beta}}{\text{Alpha} + \text{Theta}}$
- **Relaxation Score**: $\frac{\text{Alpha}}{\text{Beta}}$
- **Rolling Averages**: 10-period smoothing to eliminate signal noise.

## 🛠️ Installation
1. Clone the repo: `git clone https://github.com/your-username/neuro-guru.git`
2. Install dependencies: `pip install streamlit pandas numpy`
3. Run the app: `streamlit run app.py`

## 📂 Data Format
The app expects a CSV with the following headers:
`alphalow, alphahigh, betalow, betahigh, theta`
