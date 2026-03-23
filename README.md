# Context-Aware Identity Management System

This project is a **context-aware identity and profile management system** that allows users to have different identities across multiple contexts while enforcing **role-based access control (RBAC)**, **consent verification**, and **audit logging**.

---

##  Features

- Context-aware identity resolution  
- Role-based access control (RBAC)  
- Consent management system  
- Audit logging for traceability  
- JWT authentication (login & secure API access)  
- User dashboard with role-based UI  
- Context-specific display name updates  

---

##  System Architecture

### Backend (Django + DRF)
- Django REST Framework API  
- JWT authentication  
- Identity resolution service layer  
- Modular apps:
  - users
  - identities
  - contexts
  - consent
  - audit  

### Frontend (React)
- React UI for interacting with the API  
- Axios for API requests  
- Role-based dashboard  
- Identity resolution interface  

---

##  Authentication

JWT-based authentication using access and refresh tokens.

Endpoint:
```
/api/token/
```

---

##  Key API Endpoints

### Identity
```
POST /api/identities/resolve/
PATCH /api/identities/update-display-name/
```

### Users
```
GET /api/users/
GET /api/users/me/
```

### Contexts
```
GET /api/contexts/
```

### Audit Logs
```
GET /api/audit/logs/
```

---

##  How to Run the Project

### 1. Clone the repository
```
git clone https://github.com/tolaogundipe/Context-Aware-Identity-API
cd Context-Aware-Identity-API
```

### 2. Backend Setup
```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Frontend Setup
```
cd identity-ui
npm install
npm run dev
```

---

##  Testing

Run tests with:
```
python manage.py test
```

---

##  API Documentation

Swagger UI:
```
http://127.0.0.1:8000/api/docs/
```

---

##  Key Design Concepts

- Separation of concerns (views vs services)  
- Context-aware identity representation  
- Consent-based data access  
- Role-based permission control  
- Audit logging for accountability  

---

##  Notes

This project was developed as part of an academic project.
