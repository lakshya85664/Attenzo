# 🎓 Attenzo
### AI-Powered Classroom Attendance Management System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-attenzo.streamlit.app-1565C0?style=for-the-badge&logo=streamlit&logoColor=white)](https://attenzo.streamlit.app)

**Attenzo** replaces manual roll-calls with dual biometric authentication — face recognition and voice identification — built entirely in Python and deployed on the cloud.

[🚀 Try Live Demo](https://attenzo.streamlit.app) · [🌐 Landing Page](https://attenzo-landing-page.vercel.app) · [📖 Report Bug](https://github.com/lakshya85664/Attenzo/issues)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
  - [Face Recognition Attendance](#-face-recognition-attendance)
  - [Voice Biometric Roll-Call](#-voice-biometric-roll-call)
  - [QR Code Enrollment](#-qr-code-enrollment)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [Deployment](#-deployment)
- [Database Schema](#-database-schema)
- [Security](#-security)
- [Author](#-author)

---

## 🔍 Overview

Traditional classroom attendance is slow, error-prone, and vulnerable to proxy marking. **Attenzo** solves this with two AI-powered attendance modes:

| Mode | Technology | Best For |
|------|-----------|----------|
| 📸 **FaceID Attendance** | face_recognition + dlib (ResNet-34) | Full class scan from one photo |
| 🎙️ **Voice Roll-Call** | Resemblyzer + Librosa (GE2E LSTM) | Sequential voice-based marking |

Teachers get a dashboard to manage subjects, take attendance, and export CSV reports. Students get a personal portal to track their attendance percentage across all enrolled subjects.

---

## ✨ Key Features

### 👨‍🏫 For Teachers
- **FaceID Attendance** — Upload or capture a classroom photo; AI detects and matches all student faces in seconds
- **Voice Roll-Call** — Students say "Present" one by one; AI verifies their voice against stored biometric
- **Subject Management** — Create subjects, generate unique QR codes for enrollment
- **Attendance Dashboard** — View and manage records, see per-student attendance percentages
- **CSV Export** — Download attendance records for any subject

### 👨‍🎓 For Students
- **QR Code Enrollment** — Scan a QR code to instantly join a class
- **Attendance Tracker** — View attendance % across all enrolled subjects
- **Biometric Registration** — Register face and voice once; used for all future sessions

### 🔐 System
- Role-based access control (Teacher / Student)
- JWT authentication via Supabase Auth
- Row Level Security (RLS) — database-level data isolation per user
- Secure password hashing with bcrypt

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Home Screen  │  │Teacher Screen│  │  Student Screen  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│          app.py — session_state routing (match-case)         │
└─────────────────────────────────┬───────────────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
   ┌──────────▼──────┐  ┌────────▼────────┐  ┌──────▼──────────┐
   │  Face Pipeline  │  │  Voice Pipeline │  │  Auth & QR Code │
   │                 │  │                 │  │                  │
   │ face_recognition│  │  Resemblyzer    │  │  Supabase Auth  │
   │ dlib (ResNet-34)│  │  Librosa        │  │  PyJWT + bcrypt │
   │ 128-d encodings │  │  256-d d-vector │  │  segno (QR)     │
   └────────┬────────┘  └────────┬────────┘  └──────┬──────────┘
            │                    │                   │
            └────────────────────┼───────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Supabase (PostgreSQL)  │
                    │                          │
                    │  • users / profiles      │
                    │  • subjects              │
                    │  • enrollments           │
                    │  • attendance_records    │
                    │  • face_encodings (JSONB)│
                    │  • voice_embeddings(JSONB│
                    └──────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Frontend** | Streamlit 1.57 | UI, session routing, camera/audio input |
| **Face Recognition** | face_recognition, dlib-bin 20.0.1 | HOG detection + ResNet-34 128-d encodings |
| **Voice Biometrics** | Resemblyzer 0.1.1, Librosa 0.10.2 | GE2E-LSTM 256-d speaker embeddings |
| **Database** | Supabase (PostgreSQL) | Cloud DB, Auth, Row Level Security |
| **Authentication** | Supabase Auth, PyJWT 2.12.1, bcrypt 5.0.0 | JWT-based secure login |
| **QR Codes** | segno 1.6.6 | Course enrollment QR generation |
| **Audio** | soundfile 0.12.1 | Audio format conversion/processing |
| **Landing Page** | Flask + Vercel | Static marketing page |

---

## 📁 Project Structure

```
Attenzo/
├── app.py                          # Entry point — Streamlit routing
├── requirements.txt                # All Python dependencies
├── .gitignore
└── src/
    ├── screens/
    │   ├── home_screen.py          # Landing/login selection
    │   ├── teacher_screen.py       # Teacher dashboard & tools
    │   └── student_screen.py       # Student portal
    └── components/
        └── dialog_auto_enroll.py   # QR code auto-enrollment dialog
```

---

## ⚙️ How It Works

### 📸 Face Recognition Attendance

1. Teacher navigates to **FaceID Attendance** for a subject
2. Uploads or captures a classroom photo via `st.camera_input()`
3. `face_recognition.face_locations()` detects all faces in the image
4. `face_recognition.face_encodings()` generates a **128-dimensional vector** for each detected face
5. Each encoding is compared against stored student encodings (fetched from Supabase as JSONB → numpy arrays) using **Euclidean distance** with a threshold of `0.6`
6. Matched students are marked **Present**; unrecognised faces flagged for manual review
7. Attendance records written to Supabase

```python
# Core matching logic (simplified)
known_encodings = [np.array(row['encoding']) for row in stored_data]
matches = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=0.6)
distances = face_recognition.face_distance(known_encodings, unknown_encoding)
best_match_idx = np.argmin(distances)
```

### 🎙️ Voice Biometric Roll-Call

1. Teacher starts a voice roll-call session for a subject
2. Each student records themselves saying **"Present"** (~2 seconds)
3. Audio is preprocessed: resampled to **16kHz mono**, silence-trimmed, normalised
4. `Resemblyzer`'s GE2E-trained LSTM encoder generates a **256-dimensional d-vector**
5. Cosine similarity is computed against each student's stored voice embedding
6. Student with similarity above threshold is marked **Present**

```python
from resemblyzer import VoiceEncoder, preprocess_wav

encoder = VoiceEncoder()
wav = preprocess_wav(audio_path)           # resample → 16kHz, normalise
embedding = encoder.embed_utterance(wav)   # 256-d speaker vector

# Compare using cosine similarity
similarity = np.dot(embedding, stored_embedding)  # both are L2-normalised
is_match = similarity >= 0.75
```

### 🔗 QR Code Enrollment

1. Teacher creates a subject → Attenzo generates a unique `join_code`
2. `segno` renders it as a QR code encoding the URL:
   `https://attenzo.streamlit.app/?join-code=<CODE>`
3. Student scans QR → browser opens Attenzo with `join-code` in URL
4. `st.query_params.get('join-code')` reads the code
5. Student is prompted to log in if not already authenticated
6. `auto_enroll_dialog` fires and inserts the enrollment into Supabase

```python
# app.py — QR enrollment handling
join_code = st.query_params.get('join-code')
if join_code:
    if st.session_state.login_type != 'student':
        st.session_state.login_type = 'student'
        st.rerun()
    if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
        auto_enroll_dialog(join_code)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A [Supabase](https://supabase.com) project (free tier works)
- `cmake` and a C++ compiler are **not required** — `dlib-bin` ships pre-compiled wheels

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/lakshya85664/Attenzo.git
cd Attenzo

# 2. Create and activate a virtual environment (recommended)
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt
```

> **Note:** `face_recognition_models` is installed directly from GitHub (pinned to a specific commit) to ensure the correct pre-trained model files are used. This is handled automatically by `requirements.txt`.

### Environment Variables

Create a `.env` file in the project root (never commit this file):

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

You can find these values in your Supabase project under **Settings → API**.

### Running the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ☁️ Deployment

### Streamlit Cloud (Main App)

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch (`main`), and entry file (`app.py`)
4. Add secrets in **Settings → Secrets**:
   ```toml
   SUPABASE_URL = "https://your-project-id.supabase.co"
   SUPABASE_KEY = "your-supabase-anon-key"
   ```
5. Click **Deploy**

### Vercel (Landing Page)

The landing page lives in a separate repo ([attenzo-landing-page](https://github.com/lakshya85664/attenzo-landing-page)) and is deployed as a Flask serverless app on Vercel.

---

## 🗄️ Database Schema

| Table | Key Columns | Description |
|-------|------------|-------------|
| `profiles` | `user_id`, `full_name`, `role` | Teacher or Student profile |
| `subjects` | `id`, `teacher_id`, `name`, `join_code` | Course records |
| `enrollments` | `student_id`, `subject_id` | Student-subject many-to-many |
| `attendance_records` | `student_id`, `subject_id`, `date`, `is_present`, `mode`, `confidence_score` | Per-session records |
| `face_encodings` | `student_id`, `subject_id`, `encoding` (JSONB) | 128-d face vectors |
| `voice_embeddings` | `student_id`, `subject_id`, `embedding` (JSONB) | 256-d voice vectors |

All tables are protected by **Row Level Security (RLS)** policies — teachers can only access their own subjects; students can only see their own records.

---

## 🔐 Security

| Concern | Implementation |
|---------|---------------|
| **Password storage** | bcrypt adaptive hashing via Supabase Auth |
| **Authentication** | JWT tokens (PyJWT); validated on every request |
| **Data isolation** | PostgreSQL Row Level Security — `auth.uid()` scoping |
| **API keys** | Stored in `.env` locally; Streamlit Secrets in production |
| **Biometric data** | Only embeddings stored (not raw photos/audio); encrypted at rest by Supabase (AES-256) |
| **Transport** | All traffic over HTTPS/TLS |

---

## 👨‍💻 Author

**Lakshya Paliwal**

[![GitHub](https://img.shields.io/badge/GitHub-lakshya85664-181717?style=flat-square&logo=github)](https://github.com/lakshya85664)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-lakshya--paliwal-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/lakshya-paliwal)

---

Made with ❤️ using Python, Streamlit & Supabase

⭐ Star this repo if you found it useful!
