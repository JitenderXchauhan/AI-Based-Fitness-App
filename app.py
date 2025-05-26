import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import time
import base64
import importlib
from pathlib import Path
from chatbot import get_fitbee_response
from diet import get_full_day_diet_plan_llm
from exercise import get_exercise_plan_llm
from xhtml2pdf import pisa
import tempfile
import base64


# Load YOLOv11 model
@st.cache_resource
def load_model():
    return YOLO("yolo11n-pose.pt")

def generate_pdf_from_html(html_content):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(temp_file.name, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    if pisa_status.err:
        return None
    return temp_file.name

def play_audio():
    if Path("beep.wav").exists():
        audio_bytes = Path("beep.wav").read_bytes()
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"


def main():
    st.set_page_config(page_title="FitBee", layout="wide")

    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "diet_data" not in st.session_state:
        st.session_state.diet_data = {}
    if "exercise_data" not in st.session_state:
        st.session_state.exercise_data = {}
    if "reps" not in st.session_state:
        st.session_state.reps = 0
    if "state" not in st.session_state:
        st.session_state.state = "up"

    with st.sidebar:
        st.title("FitBee")
        option = st.radio(" ", ["Home", "Diet Planner", "Tutorials", "Real-Time Monitoring", "Exercise Planner", "Chat With FitBee"],
                          index=["Home", "Diet Planner", "Tutorials", "Real-Time Monitoring", "Exercise Planner", "Chat With FitBee"].index(st.session_state.page))

        if option != st.session_state.page:
            st.session_state.page = option
            st.rerun()

    if st.session_state.page == "Home":
      bg_image = get_base64_image("home_bg.png")  

      st.markdown(f"""
          <style>
          .home-container {{
              background-image: url("{bg_image}");
              background-size: cover;
              background-position: center;
            #   background-color:rgba(199,0,57,0.2);
              height:auto;
              min-height:100vh:
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              color: #C70039;
              text-align: center;
              padding: 60px 20px;
              text-shadow: 2px 2px 4px #000;
              border-radius:7px;
          }}
          .home-button .stButton button {{
              background-color: #C70039;
              color: #C70039;
              font-size: 18px;
              padding: 12px 24px;
              border-radius: 8px;
              border: none;
              box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.5);
          }}
          </style>
          <div class="home-container">
              <h1 style="background-color:rgba(255,87,51,0.2);">Welcome to Your AI Fitness Coach</h1>
              <p style="background-color:rgba(255,87,51,0.2);color:#DAF7A6 ">"Your only limit is you. Push yourself because no one else is going to do it for you."</p>
          </div>
      """, unsafe_allow_html=True)

      st.markdown('<div class="home-button">', unsafe_allow_html=True)
      if st.button("Start Training"):
          st.session_state.page = "Diet Planner"
          st.rerun()
      st.markdown('</div>', unsafe_allow_html=True)

        

    elif st.session_state.page == "Diet Planner":
        st.title("Diet Planner")
        st.write("Get a personalized full-day meal plan.")

        if "diet_data" not in st.session_state:
            st.session_state.diet_data = ""

        weight = st.number_input("Enter your weight (kg)", min_value=30.0, max_value=250.0, step=0.1)
        height = st.number_input("Enter your height (cm)", min_value=30.0, max_value=250.0, step=0.1)

        if weight and height:
            bmi = weight / ((height / 100) ** 2)
            st.write(f"Your BMI: {bmi:.2f}")

            diet_type = st.selectbox("Select your diet preference", ["Veg", "Non-Veg", "Semi-Veg"])
            disease = st.text_area("Any Disease ? (Specify if applicable)")
            Goal = st.selectbox("Diet Goal", ["Fat Loss", "Muscle Gain", "weight control"])

            if st.button("Generated Diet Plan"):
                with st.spinner("Generating diet plan."):
                    diet_plan = get_full_day_diet_plan_llm(bmi, diet_type, disease, Goal)
                    st.session_state.diet_data = diet_plan
                    st.success("Full-day diet plan generated!")


            if st.session_state.diet_data:
             st.markdown("### Suggested Full-Day Diet Plan (in Tables)")
             st.markdown(st.session_state.diet_data, unsafe_allow_html=True)

             pdf_file_path = generate_pdf_from_html(st.session_state.diet_data)

             if pdf_file_path:
                 with open(pdf_file_path, "rb") as f:
                     st.download_button(
                         label="📄 Download Diet Plan as PDF",
                         data=f,
                         file_name="diet_plan.pdf",
                                  mime="application/pdf"
                    )
          

           

    elif st.session_state.page == "Tutorials":
        st.title("Workout Tutorials")
        st.write("Search for a muscle group or an exercise.")

        muscle_groups = {
            "Legs": {
                "Squats": "https://www.youtube.com/embed/aclHkVaku9U",
                "Lunges": "https://www.youtube.com/embed/QOVaHwm-Q6U",
                "Leg Press": "https://www.youtube.com/embed/IZxyjW7MPJQ"
            },
            "Biceps": {
                "Bicep Curls": "https://www.youtube.com/embed/ykJmrZ5v0Oo",
                "Hammer Curls": "https://www.youtube.com/embed/zC3nLlEvin4",
                "Preacher Curls": "https://www.youtube.com/embed/wgSHaPZWe5o"
            },
            "Triceps": {
                "Tricep Dips": "https://www.youtube.com/embed/0326dy_-CzM",
                "Skull Crushers": "https://www.youtube.com/embed/d_KZxkY_0cM",
                "Close-Grip Bench Press": "https://www.youtube.com/embed/6G3kQyq8yts"
            },
            "Shoulders": {
                "Shoulder Press": "https://www.youtube.com/embed/B-aVuyhvLHU",
                "Lateral Raises": "https://www.youtube.com/embed/3VcKaXpzqRo",
                "Front Raises": "https://www.youtube.com/embed/-t7fuZ0KhDA"
            }
        }

        search_query = st.text_input("Search for an exercise", "").lower()
        found_exercises = []

        for muscle, exercises in muscle_groups.items():
            for exercise, video_url in exercises.items():
                if search_query in exercise.lower() or search_query in muscle.lower():
                    found_exercises.append((exercise, video_url))

        if found_exercises:
            for exercise, video_url in found_exercises:
                st.subheader(exercise)
                st.video(video_url)
        else:
            st.write("No exercises found. Try searching for a different term.")

    elif st.session_state.page == "Exercise Planner":
      st.title("Personalized Exercise Planner")
      st.write("Get a workout plan based on your body type, age, and fitness level.")

      age = st.number_input("Enter your age", min_value=12, max_value=100, step=1)
      height = st.number_input("Enter your height (cm)", min_value=100.0, max_value=250.0, step=0.1)
      weight = st.number_input("Enter your weight (kg)", min_value=30.0, max_value=200.0, step=0.1)
      body_type = st.selectbox("Select your body type", ["Endomorph", "Ectomorph", "Mesomorph"])
      goal = st.selectbox("Select your goal", ["Weight Loss", "Muscle Gain", "Endurance"])
      injury = st.text_area("Any past injuries? (Specify if applicable)")

      if st.button("Generate Plan"):
          with st.spinner("Generating your exercise plan..."):
              plan_output = get_exercise_plan_llm(goal, body_type, injury, height, weight, age)
              st.session_state.exercise_data = {"plan": plan_output}
              st.success("Exercise plan generated!")

      if st.session_state.get("exercise_data"):
          st.markdown("### Suggested Full-Day Exercise Plan (in Tables)")
          st.markdown(st.session_state.exercise_data["plan"], unsafe_allow_html=True)

          pdf_file_path = generate_pdf_from_html(st.session_state.exercise_data["plan"])

          if pdf_file_path:
              with open(pdf_file_path, "rb") as f:
                  st.download_button(
                      label="📄 Download Exercise Plan as PDF",
                      data=f,
                      file_name="Exercise_plan.pdf",
                      mime="application/pdf"
                  )


    elif st.session_state.page == "Chat With FitBee":
        st.title("Chat with FitBee")
        st.write("Ask me anything about diet, workouts, or your fitness goals!")

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        with st.form("chat_form"):
            user_input = st.text_input("You:")
            submitted = st.form_submit_button("Send")

        if submitted and user_input:
            response = get_fitbee_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("FitBee", response))

        for sender, message in st.session_state.chat_history:
            st.markdown(f"**{sender}:** {message}")

        if st.button("Clear Chat History"):
            st.session_state.chat_history = []

    elif st.session_state.page == "Real-Time Monitoring":
        st.title("📹 Real-Time Exercise Detection")
        exercise_options = sorted([f.stem for f in Path("Exercise").glob("*.py") if f.stem != "__init__"])
        selected_exercise = st.selectbox("Select Exercise to Monitor", exercise_options)

        if st.button("Reset Reps"):
            st.session_state.reps = 0
            st.session_state.state = "up"

        run = st.toggle("Start Webcam")

        FRAME_WINDOW = st.image([])

        if run:
            cap = cv2.VideoCapture(0)
            model = load_model()
            module = importlib.import_module(f"Exercise.{selected_exercise}")
            detect = module.detect

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                results = model(frame, verbose=False)
                annotated = frame.copy()

                for result in results:
                    if result.keypoints is not None:
                        keypoints = result.keypoints.xy[0].cpu().numpy()
                        label, reps, state = detect(keypoints, st.session_state.state, st.session_state.reps)

                        if reps > st.session_state.reps:
                            play_audio()

                        st.session_state.reps = reps
                        st.session_state.state = state
                        annotated = result.plot()

                cv2.putText(annotated, f"{selected_exercise} | Reps: {st.session_state.reps}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                FRAME_WINDOW.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
                time.sleep(0.03)

            cap.release()
        else:
            st.info("Camera is off.")

if __name__ == "__main__":
    main()
