"""Generate a synthetic student performance dataset (255 rows, 12 columns).

The data is computer-generated and contains NO real student information.
Student names are fictional (random first + last name combinations).
It deliberately includes missing values, duplicate rows, inconsistent text
and one impossible value so that data cleaning can be practised.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 250

branches = rng.choice(["CSE", "IT", "ECE", "ME"], N, p=[0.35, 0.25, 0.25, 0.15])
gender = rng.choice(["Male", "Female"], N)
residence = rng.choice(["Hostel", "Day Scholar"], N, p=[0.45, 0.55])
tutoring = rng.choice(["Yes", "No"], N, p=[0.35, 0.65])

# Fictional student names that match the Gender column
# (separate generator so the other columns stay unchanged)
MALE = ["Aarav", "Vivaan", "Aditya", "Arjun", "Rohan", "Kabir", "Ishaan", "Dev", "Karan", "Nikhil",
        "Aryan", "Harsh", "Manav", "Yash", "Tanmay", "Rahul", "Siddharth", "Varun", "Pranav", "Mohit"]
FEMALE = ["Priya", "Ananya", "Diya", "Isha", "Kavya", "Meera", "Neha", "Riya", "Sneha", "Tanya",
          "Pooja", "Aditi", "Shreya", "Naina", "Simran", "Anjali", "Khushi", "Muskan", "Nisha", "Sakshi"]
LAST = ["Sharma", "Verma", "Gupta", "Singh", "Yadav", "Mishra", "Tiwari", "Pandey", "Jain", "Agarwal",
        "Chauhan", "Saxena", "Kapoor", "Malhotra", "Bansal", "Joshi", "Rastogi", "Srivastava"]
name_rng = np.random.default_rng(123)
names, used = [], set()
for g in gender:
    while True:
        first = name_rng.choice(MALE if g == "Male" else FEMALE)
        full = f"{first} {name_rng.choice(LAST)}"
        if full not in used:
            used.add(full)
            names.append(full)
            break

attendance = np.clip(rng.normal(75, 12, N), 35, 100).round(1)
study = np.clip(rng.normal(12, 4, N), 1, 30).round(1)
sleep = np.clip(rng.normal(6.8, 1.0, N), 4, 9).round(1)

# Marks depend on attendance, study hours and tutoring, plus noise
base = 20 + 0.30 * attendance + 1.1 * study + np.where(tutoring == "Yes", 4, 0)


def marks(shift=0):
    return np.clip(base + shift + rng.normal(0, 9, N), 5, 100).round(0)


df = pd.DataFrame({
    "Student_ID": [f"S{1001 + i}" for i in range(N)],
    "Student_Name": names,
    "Gender": gender,
    "Branch": branches,
    "Residence": residence,
    "Attendance_Pct": attendance,
    "Study_Hours_Per_Week": study,
    "Sleep_Hours": sleep,
    "Tutoring": tutoring,
    "Maths_Marks": marks(-3),
    "Physics_Marks": marks(-1),
    "Programming_Marks": marks(2),
})

# --- Deliberate data problems ---
for col in ["Attendance_Pct", "Study_Hours_Per_Week", "Sleep_Hours",
            "Maths_Marks", "Physics_Marks", "Programming_Marks"]:
    df.loc[rng.choice(N, 4, replace=False), col] = np.nan

df.loc[rng.choice(N, 8, replace=False), "Gender"] = "male"
df.loc[rng.choice(N, 6, replace=False), "Branch"] = " cse "
df.loc[rng.choice(N, 5, replace=False), "Residence"] = "hostel"
df.loc[rng.choice(N, 6, replace=False), "Tutoring"] = "yes"
df.loc[17, "Maths_Marks"] = 145  # impossible value

df = pd.concat([df, df.sample(5, random_state=1)], ignore_index=True)  # duplicates
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("data/raw/student_performance.csv", index=False)
df.to_excel("data/raw/student_performance.xlsx", index=False)
print(df.shape)
