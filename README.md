# Remote Healthcare System

## ⚠️ CRITICAL SECURITY WARNING ⚠️

**THIS VERSION HAS INTENTIONALLY DISABLED SECURITY FEATURES AND SHOULD NEVER BE USED IN PRODUCTION!**

This branch has been modified to **remove CSRF protection** and contains **no encryption for medical data**:
- ❌ CSRF middleware has been disabled
- ❌ CSRF tokens removed from all forms  
- ❌ Medical records stored in plaintext (no encryption)
- ❌ Sensitive patient data unprotected

**DO NOT** use this version with real patient data or in any production environment. This configuration violates HIPAA, GDPR, and other healthcare data protection regulations.

📄 **See [SECURITY_NOTICE.md](SECURITY_NOTICE.md) for complete details on security removals and risks.**

---

A Django-based remote healthcare system designed for A-Level NEA Computer Science project. This system provides a complete solution for managing healthcare appointments, medical records, consultations, and patient-doctor interactions.

## 🎯 Project Overview

This healthcare system enables:
- **Patient Management**: Register, manage profiles, book appointments, view medical history
- **Doctor Management**: Manage schedules, view appointments, create medical records
- **Appointment System**: Book, reschedule, cancel appointments with status tracking
- **Medical Records**: Secure storage and retrieval of patient medical information
- **Consultation Features**: Video sessions and chat interface for remote consultations
- **Reports & Analytics**: Generate and export medical reports in PDF/CSV formats
- **User Settings**: Customizable preferences and privacy settings

## 🚀 Features

### 1. Authentication & User Management
- User registration with role selection (Doctor/Patient)
- Secure login/logout functionality
- Profile management for both doctors and patients
- Password change functionality

### 2. Appointment System
- **Book Appointments**: Patients can book appointments with available doctors
- **View Appointments**: List of all appointments with filtering
- **Reschedule**: Change appointment date and time
- **Cancel**: Cancel unwanted appointments
- **Status Management**: Doctors can update appointment status (scheduled, confirmed, completed, cancelled)

### 3. Dashboard
- **Doctor Dashboard**:
  - View today's appointments
  - Access patient details
  - Quick stats (total patients, appointments)
  - Recent consultation notes
  
- **Patient Dashboard**:
  - View upcoming appointments
  - Access medical history
  - Past consultations
  - Quick action buttons

### 4. Reports & Medical Records
- **Medical Records**:
  - Create and store patient medical records
  - Include symptoms, diagnosis, prescription, lab results
  - Secure access control
  
- **Reports**:
  - Generate consultation summaries
  - Export reports as PDF or CSV
  - Multiple report types (consultation, prescription, lab, medical history)

### 5. Consultation Features
- **Consultation Notes**: Doctors can record detailed consultation notes
- **Chat Interface**: Real-time messaging between doctor and patient
- **Video Sessions**: Video call interface (placeholder for WebRTC integration)

### 6. Settings
- **User Settings**:
  - Update personal information
  - Change password
  - Notification preferences
  - Privacy settings
  
- **System Settings**: Admin-only system-wide configuration

## 📋 Requirements

- Python 3.8+
- Django 4.2.7
- SQLite (included with Python)
- Pillow 10.1.0 (for image handling)
- ReportLab 4.0.7 (for PDF generation)

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/fahmadgh/remote-healthcare.git
cd remote-healthcare
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Create sample data** (optional):
```bash
python populate_db.py
```

5. **Run the development server**:
```bash
python manage.py runserver
```

6. **Access the application**:
Open your browser and navigate to `http://localhost:8000`

## 👤 Test Users

After running `populate_db.py`, you can login with:

### Admin
- Username: `admin`
- Password: `admin123`

### Doctors
- **Dr. John Smith** (General Physician)
  - Username: `drsmith`
  - Password: `doctor123`

- **Dr. Emily Johnson** (Cardiologist)
  - Username: `drjohnson`
  - Password: `doctor123`

### Patients
- **Alice Brown**
  - Username: `patient1`
  - Password: `patient123`

- **Charlie Davis**
  - Username: `patient2`
  - Password: `patient123`

## 📂 Project Structure

```
remote-healthcare/
├── accounts/               # User authentication and profiles
├── appointments/           # Appointment management
├── consultation/          # Consultation notes, chat, video
├── dashboard/             # User dashboards
├── reports/               # Medical records and reports
├── settings_app/          # User and system settings
├── healthcare_system/     # Main project settings
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── media/                 # Uploaded files
├── manage.py             # Django management script
├── populate_db.py        # Sample data script
└── requirements.txt      # Python dependencies
```

## 🎨 Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite
- **Frontend**: HTML, CSS (embedded in templates)
- **PDF Generation**: ReportLab
- **Image Processing**: Pillow

## 🔒 Security Features

⚠️ **SECURITY DISABLED IN THIS VERSION** ⚠️

**Removed/Disabled:**
- ❌ CSRF protection (middleware disabled, tokens removed)
- ❌ Medical data encryption (all data stored in plaintext)

**Still Active:**
- ✅ Password hashing and validation
- ✅ User authentication required for protected views
- ✅ Role-based access control (Doctor/Patient)

**This configuration is INSECURE and for demonstration purposes only!**
See [SECURITY_NOTICE.md](SECURITY_NOTICE.md) for complete details.

## 📱 User Guide

### For Patients:

1. **Register**: Create an account with patient role
2. **Login**: Access your dashboard
3. **Book Appointment**: 
   - Navigate to Appointments → Book
   - Select a doctor
   - Choose date and time
   - Provide reason for visit
4. **View Appointments**: Check upcoming and past appointments
5. **Reschedule/Cancel**: Manage your appointments
6. **Chat**: Communicate with your doctor
7. **View Medical Records**: Access your medical history
8. **Update Settings**: Customize your preferences

### For Doctors:

1. **Login**: Access doctor dashboard
2. **View Appointments**: See today's and upcoming appointments
3. **Update Status**: Change appointment status
4. **Create Medical Records**: Document patient visits
5. **Add Consultation Notes**: Record detailed consultation information
6. **Generate Reports**: Create and export patient reports
7. **Chat with Patients**: Respond to patient messages
8. **Video Consultations**: Conduct remote consultations

## 🎓 A-Level NEA Context

This project demonstrates:
- **Problem Identification**: Healthcare management system need
- **Database Design**: Well-structured relational database with SQLite
- **Algorithm Implementation**: Booking system, scheduling logic
- **User Interface**: Clean, intuitive design suitable for users
- **Testing**: Sample data and test scenarios
- **Documentation**: Comprehensive README and code comments

### Key Features for NEA:
- Modular code structure (easy to explain)
- Clear separation of concerns (MVC pattern)
- Real-world application (healthcare domain)
- Multiple user roles and permissions
- CRUD operations on all models
- Data validation and error handling

## 🧪 Testing

To test the system:

1. Run the populate script to create test data
2. Login as different users (patient, doctor, admin)
3. Test each feature:
   - Registration and login
   - Booking appointments
   - Creating medical records
   - Generating reports
   - Chat functionality
   - Settings management

## 🔄 Future Enhancements

- Real-time chat with WebSockets
- Actual video call integration (WebRTC, Twilio)
- Email notifications
- SMS reminders
- Payment integration for consultation fees
- Advanced search and filtering
- Mobile responsive design
- API for mobile app integration
- Analytics and reporting dashboard
- Multi-language support

## 📝 License

This project is created for educational purposes (A-Level NEA).

## 👨‍💻 Author

Created as an A-Level Computer Science NEA project.

## 🤝 Contributing

This is an educational project. Feel free to fork and modify for your own learning purposes.

## 📞 Support

For any questions or issues, please create an issue in the GitHub repository.

---

**Note**: This system is designed for educational purposes and should not be used in production without proper security audits and enhancements.
