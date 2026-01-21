import streamlit as st import pandas as pd from sklearn.tree import DecisionTreeClassifier from io import BytesIO from PyPDF2 import PdfWriter

-----------------------------

Page Config and Title

-----------------------------

st.set_page_config(page_title="AI Career Guidance", layout="centered") st.title("🎓 AI Career Guidance System")

-----------------------------

Training Data

-----------------------------

data = { 'Maths':[85,70,90,60,40,88,65,75,92,55], 'Physics':[85,60,88,65,45,80,60,70,95,55], 'Chemistry':[80,70,85,60,50,75,65,68,92,55], 'Computer':[90,50,95,40,30,85,60,65,98,50], 'Biology':[70,65,60,80,85,75,70,72,65,80], 'Accounts':[0,0,0,0,0,0,80,85,75,65], 'Economics':[0,0,0,0,0,0,70,80,75,60], 'Business':[0,0,0,0,0,0,75,85,80,60], 'English':[75,80,90,60,50,78,70,72,85,60], 'Coding':[1,0,1,0,0,1,0,0,1,0], 'Communication':[1,1,0,1,1,0,1,1,0,1], 'Creativity':[0,1,0,1,1,0,1,1,0,1], 'Art':[0,1,0,1,1,0,1,1,0,1], 'Sports':[0,0,0,0,1,0,1,1,0,1], 'Leadership':[0,1,0,1,0,0,1,1,0,1], 'Teamwork':[1,1,0,1,1,0,1,1,0,1], 'ProblemSolving':[1,0,1,0,0,1,1,0,1,0], 'Career':[ 'Software Engineer','Teacher','Data Scientist','Designer','Clerk','Software Engineer','Doctor','Accountant','Entrepreneur','Sports Coach'] }

Add new careers

new_careers = ['Lawyer', 'Civil Engineer', 'Chartered Accountant', 'Government Jobs'] for c in new_careers: for f in ['Maths','Physics','Chemistry','Computer','Biology','Accounts','Economics','Business','English','Coding','Communication','Creativity','Art','Sports','Leadership','Teamwork','ProblemSolving']: data[f].append(50)  # average marks / 0/1 skills data['Career'].append(c)

DataFrame

df = pd.DataFrame(data) features = ['Maths','Physics','Chemistry','Computer','Biology','Accounts','Economics','Business','English','Coding','Communication','Creativity','Art','Sports','Leadership','Teamwork','ProblemSolving'] X = df[features] y = df['Career'] model = DecisionTreeClassifier() model.fit(X, y)

-----------------------------

Step 1: Select Stream

-----------------------------

st.header("Step 1: Select Stream") stream = st.radio("Choose your stream:",["Computer Science", "Biology", "Commerce"])

-----------------------------

Step 2: Enter Marks

-----------------------------

st.header("Step 2: Enter Marks") student = {} if stream == "Computer Science": subjects = ["Maths","Physics","Chemistry","Computer","English"] elif stream == "Biology": subjects = ["Maths","Physics","Chemistry","Biology","English"] else: subjects = ["Maths","Accounts","Economics","Business","English"]

for s in subjects: student[s] = st.slider(s,0,100,60)

Fill other subjects with 0

for f in ['Maths','Physics','Chemistry','Computer','Biology','Accounts','Economics','Business','English']: if f not in student: student[f] = 0

-----------------------------

Step 3: Skills

-----------------------------

st.header("Step 3: Skills") student['Coding'] = int(st.checkbox("Interested in Coding")) student['Communication'] = int(st.checkbox("Good Communication")) student['Creativity'] = int(st.checkbox("Creative Thinking")) student['Art'] = int(st.checkbox("Art / Design")) student['Sports'] = int(st.checkbox("Sports"))

-----------------------------

Step 4: Personality

-----------------------------

st.header("Step 4: Personality") student['Leadership'] = int(st.checkbox("Leadership")) student['Teamwork'] = int(st.checkbox("Teamwork")) student['ProblemSolving'] = int(st.checkbox("Problem Solving"))

-----------------------------

Step 5: Predict Career

-----------------------------

if st.button("Predict Career"): # Marks validation (Maths <40 no Software Engineer / Civil Engineer) if student['Maths'] < 40: exclude_careers = ['Software Engineer', 'Civil Engineer'] else: exclude_careers = []

# Filter stream-specific careers
allowed_careers = []
for c in df['Career'].unique():
    if c in exclude_careers:
        continue
    if stream == 'Computer Science' and c in ['Software Engineer','Data Scientist','Designer'] + new_careers:
        allowed_careers.append(c)
    elif stream == 'Biology' and c in ['Doctor','Teacher','Sports Coach']:
        allowed_careers.append(c)
    elif stream == 'Commerce' and c in ['Accountant','Entrepreneur','Clerk','Lawyer','Chartered Accountant','Government Jobs']:
        allowed_careers.append(c)

# Predict career
input_data = [student[f] for f in features]
prediction = model.predict([input_data])[0]

# If predicted career not allowed, choose first allowed career
if prediction not in allowed_careers and allowed_careers:
    prediction = allowed_careers[0]

st.success(f"🎯 Suggested Career / பரிந்துரைக்கப்பட்ட தொழில்: {prediction}")

# -----------------------------
# Step 6: PDF Download
# -----------------------------
pdf_writer = PdfWriter()
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

buffer = BytesIO()
c = canvas.Canvas(buffer, pagesize=letter)
c.setFont("Helvetica", 14)
c.drawString(50, 750, "🎓 AI Career Guidance Report")
c.drawString(50, 720, f"Suggested Career / பரிந்துரைக்கப்பட்ட தொழில்: {prediction}")
y_position = 680
c.drawString(50, y_position, "\nStudent Marks and Skills:")
for key, val in student.items():
    y_position -= 20
    c.drawString(50, y_position, f"{key}: {val}")
c.showPage()
c.save()
buffer.seek(0)

st.download_button(
    label="📄 Download PDF Report",
    data=buffer,
    file_name="career_report.pdf",
    mime="application/pdf"
)