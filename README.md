# 📊 ChemInSight

> A modern, full-stack analytics platform for processing and visualizing equipment CSV data across web and desktop interfaces.

---

## 🌟 What Makes This Different

Transform raw equipment CSV data into actionable insights with:

- **🎨 Stunning Dark UI** - Glassmorphism design that's easy on the eyes
- **📊 Interactive Visualizations** - Pie charts, bar graphs, and trend lines
- **🔄 Cross-Platform** - Same powerful features on web and desktop
- **⚡ Real-Time Processing** - Instant statistics and chart generation
- **🔐 Enterprise Security** - JWT authentication with token refresh
- **📱 Responsive Design** - Perfect on any screen size

---

## 🚀 Quick Start

### Prerequisites

Ensure you have these installed on your Mac M2:

```bash
# Check Python version (should be 3.8+)
python3 --version

# Check Node.js version (should be 16+)
node --version

# Check npm version
npm --version
```

**Don't have them?** Install via Homebrew:

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install Node.js
brew install node
```

---

### 🔧 Installation Steps

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd csv-dashboard
```

#### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Mac)
source venv/bin/activate

# Install dependencies
pip install -r Requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter: username, email (optional), password

# Start server
python manage.py runserver
```

✅ **Backend running at:** `http://127.0.0.1:8000`

---

#### 3. Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ **Frontend running at:** `http://localhost:5173`

---

#### 4. Desktop App Setup

```bash
# Open new terminal
cd desktop

# Install PyQt5 dependencies (Mac M2)
pip install PyQt5 requests matplotlib pandas

# Run desktop application
python main.py
```

---

## 📁 Project Architecture

```
csv-dashboard/
│
├── 🔧 backend/                      # Django REST API
│   ├── api/                         # Core application
│   │   ├── migrations/              # Database schemas
│   │   ├── models.py                # Data models
│   │   ├── views.py                 # API endpoints
│   │   ├── serializers.py           # JSON serializers
│   │   ├── urls.py                  # Route definitions
│   │   └── tests.py                 # Unit tests
│   │
│   ├── backend/                     # Django config
│   │   ├── settings.py              # App settings
│   │   ├── urls.py                  # Root routing
│   │   ├── wsgi.py                  # WSGI server
│   │   └── asgi.py                  # ASGI server
│   │
│   ├── db.sqlite3                   # Database
│   ├── manage.py                    # Django CLI
│   └── Requirements.txt             # Python packages
│
├── 🖥️ desktop/                      # PyQt5 Application
│   ├── main.py                      # App entry point
│   ├── api_client.py                # REST client
│   ├── charts.py                    # Chart renderer
│   └── tempCodeRunnerFile.py        # Temp file
│
├── 🌐 frontend/                     # React Application
│   ├── src/
│   │   ├── App.jsx                  # Main component
│   │   ├── api.js                   # API service
│   │   ├── App.css                  # Styles
│   │   ├── index.css                # Global CSS
│   │   ├── main.jsx                 # Entry point
│   │   └── assets/                  # Images, fonts
│   │
│   ├── public/                      # Static files
│   ├── package.json                 # Dependencies
│   ├── vite.config.js               # Build config
│   ├── eslint.config.js             # Linting rules
│   └── index.html                   # HTML template
│
└── 📖 README.md                     # Documentation
```

---

## 🎯 Core Features

### Data Management
- 📤 **CSV Upload** - Supports equipment data files
- 🔍 **Auto-Analysis** - Calculates totals, averages, distributions
- 📊 **Statistics** - Flow rate, pressure, temperature metrics
- 🕐 **History Tracking** - View all past uploads

### Visualizations
- 🥧 **Pie Charts** - Equipment type distribution
- 📊 **Bar Graphs** - Categorical comparisons
- 📈 **Line Charts** - Trend analysis over time
- 💎 **KPI Cards** - Key metrics at a glance

### User Experience
- 🌙 **Dark Theme** - Modern glassmorphism UI
- 📱 **Responsive** - Works on all devices
- ⚡ **Fast Loading** - Optimized performance
- 🎨 **Smooth Animations** - Polished interactions

### Security & Export
- 🔐 **JWT Auth** - Secure token-based login
- 🔄 **Token Refresh** - Automatic session renewal
- 📄 **PDF Reports** - Professional exports
- 💾 **Data Persistence** - SQLite database

---

## 🔐 Authentication Flow

### Creating Your Account

```bash
# In backend directory with venv activated
python manage.py createsuperuser

# Enter credentials when prompted:
# Username: admin
# Email: admin@example.com
# Password: ••••••••
```

### Logging In

**Web App:**
1. Go to `http://localhost:5173`
2. Enter credentials
3. Click "Login"

**Desktop App:**
1. Run `python main.py`
2. Enter same credentials
3. Access all features

---

### Endpoints

#### 🔑 Authentication

**Login**
```http
POST /api/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1...",
  "refresh": "eyJ0eXAiOiJKV1..."
}
```

#### 📤 Upload CSV

```http
POST /api/upload/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: equipment_data.csv

Response: 201 Created
{
  "id": 1,
  "filename": "equipment_data.csv",
  "uploaded_at": "2026-02-10T21:30:00Z",
  "summary": {
    "total_equipment": 15,
    "avg_flowrate": 119.8,
    "avg_pressure": 6.11,
    "avg_temperature": 117.47,
    "type_distribution": {
      "Pump": 4,
      "Valve": 3,
      "Compressor": 3,
      "HeatExchanger": 2,
      "Reactor": 3
    }
  }
}
```

#### 📜 Get History

```http
GET /api/history/
Authorization: Bearer <access_token>

Response: 200 OK
[
  {
    "id": 1,
    "filename": "equipment_data.csv",
    "uploaded_at": "2026-02-10T21:30:00Z",
    "summary": { ... }
  }
]
```

#### 📄 Download Report

```http
GET /api/report/
Authorization: Bearer <access_token>

Response: 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="report.pdf"
```

---

## 📊 CSV File Format

Your CSV must include these columns:

| Column | Type | Example | Required |
|--------|------|---------|----------|
| Equipment_ID | String | EQ001 | ✅ |
| Equipment_Type | String | Pump | ✅ |
| Flowrate | Number | 120.5 | ✅ |
| Pressure | Number | 6.2 | ✅ |
| Temperature | Number | 115.3 | ✅ |

**Requirements:**
- ✅ First row must be headers
- ✅ Numeric columns for calculations
- ✅ UTF-8 encoding
- ✅ Comma-separated values
- ✅ No empty rows

---

## 🎨 UI/UX Showcase

### Web Application

**🌐 Dashboard Layout**
- **Top-Left:** Equipment Overview (4 KPIs)
- **Top-Right:** Interactive Pie Chart
- **Bottom-Left:** Upload History Table
- **Bottom-Right:** System Status Monitor

**🎨 Design Features**
- Dark theme (#0f172a background)
- Glassmorphism cards
- Gradient accents (#6366f1 → #ec4899)
- Smooth hover animations
- Responsive 2x2 grid

### Desktop Application

**🖥️ Sidebar Navigation**
- 📊 Overview Tab
- 📁 Upload History Tab
- 📈 Analytics Tab
- ⚡ System Status Tab
- 🚪 Logout Button (bottom)

**📊 Visualizations**
- Matplotlib pie charts
- Bar chart distributions
- Multi-line trend graphs
- Real-time KPI updates

---

## 🛠️ Technology Stack

### Backend Stack

| Tech | Version | Purpose |
|------|---------|---------|
| Python | 3.8+ | Language |
| Django | 4.0+ | Framework |
| DRF | 3.14+ | REST API |
| JWT | 5.2+ | Authentication |
| Pandas | 1.5+ | Data processing |
| ReportLab | 3.6+ | PDF generation |
| SQLite | 3.x | Database |

### Frontend Stack

| Tech | Version | Purpose |
|------|---------|---------|
| React | 18.0+ | UI library |
| Vite | 4.0+ | Build tool |
| Axios | 1.4+ | HTTP client |
| Chart.js | 4.0+ | Charts |

### Desktop Stack

| Tech | Version | Purpose |
|------|---------|---------|
| PyQt5 | 5.15+ | GUI framework |
| Matplotlib | 3.7+ | Visualization |
| Requests | 2.31+ | API client |

---

## 🔧 Mac M2 Specific Notes

### Python on Apple Silicon

If you encounter issues with Python packages:

```bash
# Use Rosetta for compatibility
arch -x86_64 pip install <package>

# Or install ARM64 compatible versions
pip install --only-binary :all: PyQt5
```

### Common M2 Issues

**PyQt5 Installation Error:**
```bash
# Solution 1: Use Homebrew version
brew install pyqt5
pip install pyqt5-sip

# Solution 2: Use conda
conda install -c conda-forge pyqt
```

**Matplotlib Font Warnings:**
```bash
# Clear font cache
rm -rf ~/.matplotlib
```

---

## 🐛 Troubleshooting

### Backend Issues

**Port Already in Use**
```bash
# Find process on port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

**Database Errors**
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Frontend Issues

**Dependencies Won't Install**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm cache clean --force

# Reinstall
npm install
```

**CORS Errors**
- Check `backend/backend/settings.py`
- Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
- Restart Django server

### Desktop Issues

**App Won't Launch**
```bash
# Check PyQt5 installation
python -c "import PyQt5; print(PyQt5.__version__)"

# Reinstall if needed
pip uninstall PyQt5
pip install PyQt5
```

**Charts Not Displaying**
```bash
# Verify Matplotlib
python -c "import matplotlib; print(matplotlib.__version__)"
```

---

## 📖 Usage Examples

### Complete Workflow

**1. Start All Services**
```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate
python manage.py runserver

# Terminal 2: Frontend  
cd frontend
npm run dev

# Terminal 3: Desktop (optional)
cd desktop
python main.py
```

**2. Upload Data**
- Click "Choose File"
- Select your CSV
- Click "Upload CSV"
- Wait for processing

**3. View Analytics**
- Overview shows KPIs
- Pie chart displays distribution
- History tracks all uploads
- Status monitors system

**4. Generate Report**
- Click "Download Report"
- PDF downloads with charts
- Share with team

---

## 🎓 Learning Resources

This project demonstrates:

- ✅ Django REST Framework APIs
- ✅ JWT authentication
- ✅ React hooks and state
- ✅ PyQt5 desktop apps
- ✅ Matplotlib data viz
- ✅ CORS configuration
- ✅ File upload handling
- ✅ PDF generation
- ✅ Responsive CSS Grid
- ✅ Dark theme design

---

## 🚀 Deployment Guide

### Production Checklist

- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up static file serving
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up monitoring

### Recommended Platforms

- **Backend:** Heroku, Railway, DigitalOcean
- **Frontend:** Vercel, Netlify, GitHub Pages
- **Database:** PostgreSQL on Heroku/Railway

---

## 🗺️ Roadmap

### Phase 1 (Current)
- [x] Basic CRUD operations
- [x] JWT authentication
- [x] CSV upload & processing
- [x] Chart visualizations
- [x] PDF report generation
- [x] Desktop application

### Phase 2 (Planned)
- [ ] Excel file support (.xlsx)
- [ ] Advanced filtering options
- [ ] Data export in multiple formats
- [ ] Email notifications
- [ ] Scheduled reports
- [ ] User roles (Admin/Viewer)
      
---

## 📄 License

This project is open source and available under the MIT License.

**You can:**
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

---

## 🙏 Acknowledgments

Built with amazing open-source tools:

- **Django** - Robust web framework
- **React** - Component-based UI
- **PyQt5** - Cross-platform GUI
- **Chart.js** - Beautiful charts
- **Vite** - Lightning-fast bundler
- **Matplotlib** - Scientific plotting

---

<div align="center">

### 💙 Built with passion for data analytics

**Mac M2 Optimized** | **Full-Stack** | **Cross-Platform**

![Made with Love](https://img.shields.io/badge/Made%20with-💙-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)

---

⭐ **Star this repo if you find it useful!**

</div>
