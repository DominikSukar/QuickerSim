# QuickerSim

### Installation

1. Clone the repository

2. Start the Database
```bash
docker-compose up
```

2. Set up backend (FastAPI)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

3. Set up frontend (React.js)
```bash
cd frontend
npm install
```

4. Environment Variables
Create .env file in main project directory and put those:
```
DB_USER=
DB_PASSWORD=
DB_NAME=
```

## 🛠️ Development

### Running Backend
```bash
cd backend
.\venv\Scripts\activate
python -m uvicorn main:app --reload
```
Backend runs on: http://localhost:8000

### Running Frontend
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

## 📚 API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing
```bash
cd backend
python -m pytest

```
---