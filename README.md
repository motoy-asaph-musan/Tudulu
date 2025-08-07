# 🛠️ Tudulu - Equipment Maintenance Scheduler

**Tudulu** is a Django-based web application that helps users manage medical equipment details and schedule timely maintenance. The system provides intelligent reminders via email or WhatsApp to ensure critical devices are serviced without delay—supporting better equipment uptime and safer healthcare delivery.

---
**Tudulu** is a smart equipment tracking and preventive maintenance scheduling app tailored for healthcare facilities. It allows users to register installed medical equipment, track their status, and automatically get reminders for servicing via SMS, Email, or WhatsApp.  

---

## 🌍 Project Vision  
Tudulu (meaning "first" or "starting point") is designed to be the baseline tool to digitize medical equipment records across hospitals, especially in low-resource settings. It aims to improve operational efficiency, patient safety, and informed decision-making.

---

## ✨ Key Features  
- 🔐 **User Registration & Login** (with password reset support)  
- 🏥 **Register Installed Equipment** with details like name, description, and installation date  
- 📆 **Service Scheduler**: Generates alerts for preventive maintenance  
- 📨 **Email/SMS/WhatsApp Notifications** (Planned Feature)  
- 🔎 **Search & Filter Equipment**  
- 🧾 **Admin Dashboard** for managing users and equipment  
- 📦 Modular Django structure for scalability  

---

## ⚙️ Tech Stack  
- **Backend**: Django + SQLite/PostgreSQL  
- **Frontend**: HTML5 + CSS3 (Custom Styles)  
- **Authentication**: Django built-in auth system  
- **Deployment**: Render / PythonAnywhere / Heroku  
- **Notifications**: Email (via Django), SMS/WhatsApp (planned integrations with Twilio or WhatsApp API)

---

## 🚀 Getting Started

### 🔧 Prerequisites  
- Python 3.8+  
- pip  
- Git  
- Virtualenv (recommended)

### 📥 Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/tudulu.git
   cd tudulu


Create and activate virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

---

## 🌐 Deployment Guide (Render)

1. **Create a Render account**: [https://render.com](https://render.com)

2. **Connect your GitHub repository** to Render.

3. **Add a new Web Service** and fill in the details.

4. **Set the following build & start commands**:

   - **Build command**:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```

   - **Start command**:
     ```bash
     gunicorn tudulu.wsgi
     ```

5. **Set environment variables**:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`, etc.

6. **Add Render’s domain** to Django’s `ALLOWED_HOSTS` in `settings.py`.

7. **Configure static files** using:
   - [WhiteNoise](http://whitenoise.evans.io/en/stable/) (for simplicity), or
   - [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) (for scalability)

8. **Link your custom domain** via Render’s dashboard.

---

## 🔐 Security Checklist

- ✅ Password reset support
- ✅ HTTPS enabled in production
- 🔜 Two-Factor Authentication (Planned)
- ✅ Admin activity logging

---

## 🗺 Roadmap

- 🔄 REST API support for mobile/IoT devices
- 📱 Progressive Web App (PWA) interface
- 🔧 Equipment usage log history
- 📊 Analytics dashboard for hospital admins
- 🔗 WhatsApp Bot for automatic reminders

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repo  
2. Create a new branch  
3. Make your changes  
4. Submit a pull request

Thank you for helping us improve Tudulu!

---

## 📜 License

This project is licensed.

---

## 👤 Author

**Motoy Asaph Musan**  
Biomedical Engineer | Health Informatician | Django Developer  
🇺🇬 Uganda

---

## 📧 Contact

For support or collaboration, reach out via email:  
**motoyasaphmusan@gmail.com]**







