import streamlit as st

st.set_page_config(page_title="AI Career Guidance", layout="centered")

st.title("🎓 AI Career Guidance System")
st.write("Enter your marks and get career suggestions")

name = st.text_input("Student Name")

maths = st.slider("Maths", 0, 100, 50)
physics = st.slider("Physics", 0, 100, 50)
chemistry = st.slider("Chemistry", 0, 100, 50)
computer = st.slider("Computer", 0, 100, 50)
biology = st.slider("Biology", 0, 100, 50)

if st.button("Submit"):
    st.success(f"Thanks {name}! Marks submitted successfully ✅")