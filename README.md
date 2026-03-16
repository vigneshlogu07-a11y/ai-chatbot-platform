# ⚡ LexRam.AI — Intelligent Chat Platform

Modern full-stack chatbot web app integrated with Google Gemini, offering secure authentication, real-time streaming responses, document uploads, persistent chat history, and an interactive feedback system.

Built with **React + Vite** (frontend) and **Python FastAPI** (backend) on **MySQL**.

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────┐
│                  React + Vite (5173)                  │
│  Login │ Signup │ Chat UI │ Sidebar │ Upload │ Feedback│
└──────────────┬──────────────┬────────────────────────┘
               │ REST (JSON)  │ SSE (streaming)
┌──────────────▼──────────────▼────────────────────────┐
│                  FastAPI (8000)                        │
│  Auth │ Chat │ Messages │ Documents │ Feedback         │
└──────────────────────┬───────────────────────────────┘
                       │ SQLAlchemy ORM
┌──────────────────────▼───────────────────────────────┐
│                     MySQL                             │
│  users │ chats │ messages │ documents │ feedback       │
└──────────────────────────────────────────────────────┘
```

---

## 📷 Screenshots

### Login Page
![Login Page](screenshots/screenshot_login.png)

### Chat Interface
![Chat Interface](screenshots/screenshot_chat.png)

### Gemini AI Chat Experience
![Gemini Chat](screenshots/screenshot_chat_gemini_1773274277865.png)

---

## 📂 Project Structure

```
Chat Bot Application/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Environment settings
│   │   ├── database.py        # SQLAlchemy setup
│   │   ├── models.py          # ORM models
│   │   ├── schemas.py         # Pydantic validation
│   │   ├── auth.py            # JWT + bcrypt
│   │   └── routers/
│   │       ├── auth_router.py
│   │       ├── chat_router.py
│   │       ├── message_router.py
│   │       ├── upload_router.py
│   │       └── feedback_router.py
│   ├── uploads/               # Uploaded files
│   ├── schema.sql             # Database init
│   ├── requirements.txt
│   ├── .env                   # Config (edit this!)
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/client.js
│   │   ├── context/AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── SignupPage.jsx
│   │   │   └── ChatPage.jsx
│   │   └── components/
│   │       ├── Sidebar.jsx
│   │       ├── ChatWindow.jsx
│   │       ├── MessageBubble.jsx
│   │       ├── UploadPanel.jsx
│   │       ├── FeedbackButtons.jsx
│   │       └── ProtectedRoute.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

---

## ⚙️ Prerequisites

- **Node.js** 18+
- **Python** 3.10+
- **MySQL** 8.x

---

## 🚀 Setup & Installation

### 1. Database Setup

```bash
# Login to MySQL
mysql -u root -p

# Run the schema script
source backend/schema.sql;
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Edit .env with your MySQL credentials
# DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/lexram_db

# Start the server
uvicorn app.main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**  
Swagger docs at **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies (already done if you ran create-vite)
npm install

# Start dev server
npm run dev
```

The app will be available at **http://localhost:5173**

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | Login, returns JWT |
| GET | `/api/auth/me` | Get current user |

### Chats
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chats/` | Create new chat |
| GET | `/api/chats/` | List all user chats |
| GET | `/api/chats/{id}` | Get chat details |
| DELETE | `/api/chats/{id}` | Delete chat |

### Messages
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chats/{id}/messages` | Send message (sync) |
| GET | `/api/chats/{id}/messages` | Get chat messages |
| GET | `/api/chats/{id}/stream?message=...&token=...` | SSE streaming response |

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/documents/upload` | Upload file (multipart) |
| GET | `/api/documents/` | List user documents |

### Feedback
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/feedback/` | Submit feedback |
| GET | `/api/feedback/{message_id}` | Get feedback |

---

## 🗄️ Database Schema

| Table | Key Fields |
|-------|------------|
| **users** | id, username, email, password_hash |
| **chats** | id, user_id (FK), title, timestamps |
| **messages** | id, chat_id (FK), role, content |
| **documents** | id, user_id (FK), chat_id (FK), filename, file_type, file_size |
| **feedback** | id, message_id (FK), user_id (FK), rating, comment |

---

## 🎨 Features

- ✅ **Google Gemini AI** — Integrated with `gemini-2.5-flash` for high-speed, intelligent responses
- ✅ **JWT Authentication** — Secure signup/login with bcrypt password hashing
- ✅ **Chat Interface** — Real-time message bubbles with typing animation
- ✅ **SSE Streaming** — Token-by-token response streaming
- ✅ **Chat History** — Persistent sidebar with create/delete/switch
- ✅ **Document Upload** — Drag-and-drop for PDF, TXT, DOCX
- ✅ **Feedback System** — Like/dislike with optional comments
- ✅ **Responsive Design** — Works on desktop and mobile
- ✅ **Dark Theme** — Premium glassmorphism UI

---

## 🧪 Testing

### API Testing (Swagger)
Navigate to `http://localhost:8000/docs` — interactive OpenAPI docs.

### Manual Flow
1. Open `http://localhost:5173/home` or `http://localhost:5173` → redirected to Login
2. Click "Create one" → Signup
3. Login with credentials
4. Click "+ New Chat"
5. Send a message → see streaming response
6. Use 👍/👎 to give feedback
7. Click 📎 to upload documents
8. Chat history appears in sidebar

---

## 🔧 Configuration

Edit `backend/.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `mysql+pymysql://root:password@localhost:3306/lexram_db` | MySQL connection |
| `SECRET_KEY` | `change-me` | JWT signing key |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token lifetime (24h) |
| `UPLOAD_DIR` | `uploads` | File storage path |
| `MAX_FILE_SIZE_MB` | `10` | Max upload size |

---

## 🚢 Deployment

### Local Production Build
```bash
# Frontend
cd frontend && npm run build
# Serve the dist/ folder with any static server

# Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Cloud (Docker-ready architecture)
The project structure supports containerization:
- Backend: Python container with uvicorn
- Frontend: Nginx serving static build
- MySQL: Managed database service

---

## 📝 Notes

- **AI Responses**: Currently integrated with Google Gemini API for powerful text generation via the `google-generativeai` SDK.
- **File Processing**: Upload stores files and metadata. Add document parsing logic as needed.
- **Security**: Change `SECRET_KEY` in production. Use HTTPS. Add rate limiting.

---

## 📄 License

MIT — Built for educational and technical evaluation purposes.
