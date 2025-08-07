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


 2. Create and activate virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
3. Install dependencies:
   pip install -r requirements.txt

4.Apply migrations:
python manage.py migrate

5. Create superuser (optional):
   python manage.py createsuperuser
   
7. Run the server:
   python manage.py runserver




