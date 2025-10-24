

---

# 🚗 Automobile Emission Tracker

## 🌿 Overview
The **Automobile Emission Tracker** is a Machine Learning–based web application that predicts the **CO₂ emissions** of vehicles based on key engine and fuel parameters. It helps users understand their vehicle’s environmental impact and promotes eco-friendly driving habits.

---

## 🧩 Problem Statement
Transportation contributes significantly to global CO₂ emissions. However, most vehicle owners lack tools to monitor or estimate their emissions accurately.  
This project addresses that gap by providing a simple, data-driven platform that predicts emissions and raises awareness about sustainable mobility.

---

## 🎯 Objectives
- Predict automobile CO₂ emissions using ML models.
- Enable users to input engine parameters and fuel details.
- Visualize emission levels in an interactive interface.
- Suggest eco-friendly alternatives or improvements.

---

## ⚙️ Features
- 🧠 **Machine Learning Prediction:** Predict CO₂ (g/km) using trained regression models.
- 📊 **Data Visualization:** Real-time charts displaying emission trends.
- 💾 **Firebase Integration:** Secure user authentication and data storage.
- 🌐 **Responsive Frontend:** Built using **React** and **Tailwind CSS**.
- 🧰 **Flask API Backend:** Serves predictions from trained ML models (`joblib`).
- 🔥 **Deployed for Free:** Uses Firebase + Flask (free hosting stack).

---

## 🏗️ Tech Stack
| Layer | Technology Used |
|-------|------------------|
| **Frontend** | React.js, Tailwind CSS, Firebase Hosting |
| **Backend** | Flask (Python), REST API |
| **ML Model** | Scikit-learn, CatBoost Regressor |
| **Database** | Firebase Firestore |
| **Version Control** | Git & GitHub |

---

## 🧮 Machine Learning Model
The ML pipeline uses automobile datasets with features like:
- Engine Size (L)
- Number of Cylinders
- Fuel Consumption (City & Highway)
- Fuel Type (Petrol/Diesel/Gas/EV)

**Model Workflow:**
1. Data Preprocessing using `StandardScaler`
2. Model Training using `CatBoostRegressor`
3. Model and Scaler saved using `joblib`
4. Flask API returns predictions via JSON

---

## 🖥️ System Architecture
```plaintext
[User Input] → [Frontend: React] → [Flask API] → [ML Model]
                              ↓
                     [Prediction Output + Charts]


---

🚀 Installation & Setup

🔧 Prerequisites

Python 3.9+

Node.js 16+

Firebase Account

pip / npm installed


🪜 Steps

1. Clone the Repository

git clone https://github.com/yourusername/automobile-emission-tracker.git
cd automobile-emission-tracker

2. Backend Setup

cd backend
pip install -r requirements.txt
python app.py

3. Frontend Setup

cd frontend
npm install
npm start

4. Connect Firebase

Add your Firebase project credentials in firebaseConfig.js.

5. Deploy

firebase deploy


---

🧰 File Structure

Automobile-Emission-Tracker/
│
├── backend/
│   ├── app.py
│   ├── best_model.joblib
│   ├── scaler.joblib
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── firebaseConfig.js
│
├── dataset/
│   └── vehicle_emission_data.csv
│
├── README.md
└── LICENSE


---

📈 Results

Model	R² Score	MAE	MSE

CatBoost	0.93	5.42	18.7


The model achieved high accuracy and performs well across diverse fuel types.


---

💡 Future Enhancements

Add real-time GPS-based emission tracking.

Suggest electric/hybrid alternatives based on user input.

Include government emission norms & alert system.

Deploy as a full PWA mobile app.



---

👥 Team Members

Name	Role

Dhanush R	Developer & ML Engineer
Chandru J	Frontend Developer
Dhileepraj P	Data Analyst
Rakesh P	Data Analyst



---

🧾 License

This project is licensed under the MIT License.


---

🌍 Impact

By helping users measure and reduce emissions, this project supports UN Sustainable Development Goal 13 – Climate Action, encouraging responsible and green transportation choices.

---

Would you like me to add **GitHub badges** (Python version, License, Build passing, etc.) and a **preview image section** (for your app screenshot or banner)? That would make it look even more professional for submission or portfolio display.
