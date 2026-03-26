# AI Resume Analyser 🤖

An intelligent resume analysis tool powered by Groq AI. Upload your PDF resume and get instant feedback — scores, skills analysis, ATS compatibility check, and job description matching.

## 🌐 Live Demo
- Frontend: [Coming Soon]
- Backend API: [Coming Soon]

## ✨ Features

- **PDF Upload** — Upload your resume in PDF format
- **AI Analysis** — Get overall score and ATS score out of 100
- **Skills Detection** — See what skills you have and what's missing
- **AI Suggestions** — Get top 5 improvement suggestions
- **Job Match** — Paste any job description and see match percentage
- **History** — View your last 10 resume analyses
- **Auth** — Secure JWT-based login and registration

## 🛠️ Tech Stack

**Backend**
- Python 3.14 + Django 6
- Django REST Framework
- JWT Authentication (SimpleJWT)
- Groq AI (LLaMA 3.3 70B)
- PyPDF2 — PDF text extraction
- Cloudinary — PDF file storage
- SQLite (dev) / PostgreSQL (prod)

**Frontend**
- React 19 + Vite
- Tailwind CSS
- Axios
- React Router DOM

**Deployment**
- Backend — Railway.app
- Frontend — Vercel

## 📁 Project Structure
```
ai-resume-analyser/
├── backend/
│   ├── resumes/
│   │   ├── models.py      # Resume, Analysis models
│   │   ├── views.py       # API endpoints
│   │   ├── urls.py        # URL routing
│   │   └── utils.py       # PDF parsing, AI calls
│   ├── settings.py
│   └── manage.py
└── frontend/
    └── src/
        ├── components/    # Navbar
        ├── pages/         # Login, Register, Upload, Dashboard
        └── api/           # Axios config
```

## 🚀 Local Setup

**Backend**
```bash
# Clone the repo
git clone https://github.com/AminnaKhalid/ai-resume-analyser.git
cd ai-resume-analyser/backend

# Create virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows
source .venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your keys in .env

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## 🔑 Environment Variables

Create `.env` file in `backend/` folder:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
GROQ_API_KEY=your-groq-api-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register new user |
| POST | `/api/login/` | Login + get JWT token |
| POST | `/api/upload/` | Upload PDF resume |
| POST | `/api/analyze/{id}/` | AI analysis |
| GET | `/api/history/` | Get analysis history |
| POST | `/api/match/{id}/` | Job description match |

## 👩‍💻 Author

**Amna Khalid**
- GitHub: [@AminnaKhalid](https://github.com/AminnaKhalid)
