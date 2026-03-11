# 🎫 Online Support Ticket System
## Technical Documentation & Setup Guide
**BCA Final Year Mini Project | Python Flask + MongoDB + Bootstrap 5**

---

## 📁 Project Structure

```
support-ticket-system/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration (DB URI, mail, secret key)
├── requirements.txt                # Python dependencies
├── seed.py                         # Database seeder (demo data + admin user)
│
├── models/
│   ├── user_model.py               # User MongoDB model + bcrypt auth
│   └── ticket_model.py             # Ticket MongoDB model + CRUD
│
├── routes/
│   ├── main_routes.py              # Index/redirect routes
│   ├── auth_routes.py              # /auth/login, /auth/register, /auth/logout
│   ├── ticket_routes.py            # /tickets/* + REST API
│   └── admin_routes.py             # /admin/* (admin-only)
│
├── templates/
│   ├── base.html                   # Base layout (navbar, flash messages)
│   ├── index.html                  # Landing page
│   ├── login.html                  # Login form
│   ├── register.html               # Registration form
│   ├── dashboard.html              # User ticket list
│   ├── create_ticket.html          # New ticket form
│   ├── view_ticket.html            # Ticket detail + comments
│   └── admin/
│       ├── dashboard.html          # Admin overview + all tickets
│       ├── manage_ticket.html      # Update ticket status
│       └── users.html              # User list
│
├── static/
│   ├── css/style.css               # Custom styles
│   └── js/main.js                  # Frontend JavaScript
│
├── database/
│   └── mongodb_connection.py       # PyMongo initialization
│
└── terraform/
    ├── main.tf                     # AWS resources (VPC, EC2, SG, EIP)
    ├── variables.tf                # Configurable variables
    ├── outputs.tf                  # Output values (IP, URL, SSH)
    └── userdata.sh                 # EC2 bootstrap script
```

---

## 🚀 Local Installation & Running

### Prerequisites
- Python 3.11+
- MongoDB 7.0 (running locally on port 27017)
- pip

### Step 1: Clone / Extract Project
```bash
# If using git:
git clone <your-repo-url>
cd support-ticket-system

# Or extract the zip and navigate to the folder
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv

# Activate (Linux/Mac):
source venv/bin/activate

# Activate (Windows):
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start MongoDB
```bash
# Linux (systemd):
sudo systemctl start mongod

# macOS (Homebrew):
brew services start mongodb-community

# Windows: Start MongoDB service from Services panel
# Or: mongod --dbpath C:\data\db
```

### Step 5: Seed Demo Data (Optional but Recommended)
```bash
python seed.py
```
This creates:
- **Admin account:** `admin@demo.com` / `admin123`
- **3 sample users** (password: `user123`)
- **5 sample tickets**

### Step 6: Run the Application
```bash
python app.py
```
Open browser: **http://localhost:5000**

---

## 🧪 How to Test the Application

### Test Admin Flow
1. Go to http://localhost:5000
2. Click **Login** → Enter `admin@demo.com` / `admin123`
3. Admin dashboard opens with ticket statistics
4. View/edit any ticket → Update status → Add admin comment
5. Click **Users** in navbar to see registered users

### Test User Flow
1. Click **Register** → Create a new account
2. After login → Click **New Ticket**
3. Fill in title, category, priority, description → Submit
4. See your ticket listed with status **Open**
5. Click the ticket → View details and add a comment
6. Use Search box and Status filter to test search/filter

### Test Pagination
1. Create 12+ tickets (or run seed.py which creates 5)
2. View dashboard → Pagination appears after 10 tickets

### Test REST API
```bash
# Using curl (must be logged in via browser session, or use Postman)
# List tickets:
curl -b cookies.txt http://localhost:5000/tickets/api/tickets

# Get stats (admin):
curl -b cookies.txt http://localhost:5000/admin/api/stats
```

---

## 🔑 API Endpoints Reference

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/tickets/api/tickets` | User | List authenticated user's tickets |
| POST | `/tickets/api/tickets` | User | Create new ticket (JSON body) |
| GET | `/tickets/api/tickets/:id` | User | Get specific ticket by ID |
| GET | `/admin/api/stats` | Admin | Get ticket count statistics |
| PUT | `/admin/api/tickets/:id/status` | Admin | Update ticket status |

### Example POST body (create ticket):
```json
{
  "title": "Cannot access my account",
  "description": "Getting error code 403 when logging in",
  "category": "Account Issue",
  "priority": "High"
}
```

---

## ☁️ AWS Deployment with Terraform

### Prerequisites
- AWS Account with IAM credentials configured
- Terraform 1.0+ installed: https://developer.hashicorp.com/terraform/downloads
- SSH key pair: `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`

### Step 1: Configure AWS Credentials
```bash
aws configure
# Enter: AWS Access Key ID, Secret Access Key, Region (us-east-1)
```

### Step 2: Initialize Terraform
```bash
cd terraform/
terraform init
```

### Step 3: Preview Changes
```bash
terraform plan
```

### Step 4: Deploy Infrastructure
```bash
terraform apply
# Type 'yes' when prompted
```
Terraform will output:
```
app_public_ip = "54.x.x.x"
app_url = "http://54.x.x.x:5000"
ssh_command = "ssh -i ~/.ssh/id_rsa ubuntu@54.x.x.x"
```

### Step 5: Upload Application Files
```bash
# SSH into the server
ssh -i ~/.ssh/id_rsa ubuntu@<ELASTIC_IP>

# Copy app files (run from your local machine):
scp -i ~/.ssh/id_rsa -r support-ticket-system/ ubuntu@<ELASTIC_IP>:/opt/supportdesk/
```

### Step 6: Start the Application
```bash
# On the EC2 server:
cd /opt/supportdesk
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed.py

# Start service:
sudo systemctl start supportdesk
sudo systemctl status supportdesk
```

### Step 7: Access the Application
Open: `http://<ELASTIC_IP>:5000` or `http://<ELASTIC_IP>` (via Nginx on port 80)

### Tear Down Infrastructure
```bash
terraform destroy
# Type 'yes' to confirm - this deletes all AWS resources
```

---

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
# Secret key (change in production!)
SECRET_KEY = 'your-strong-random-secret-key'

# MongoDB URI
MONGO_URI = 'mongodb://localhost:27017/support_ticket_db'

# Email (configure for real notifications)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'  # Gmail App Password

# Pagination
TICKETS_PER_PAGE = 10
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| `ConnectionRefusedError` (MongoDB) | Start MongoDB: `sudo systemctl start mongod` |
| `Error: Address already in use` | Change port: `python app.py --port 5001` |
| Admin login fails | Run `python seed.py` to create admin user |
| Terraform `InvalidAMI` | Check AMI ID for your region in variables.tf |
| EC2 connection refused | Wait 2-3 min for instance to boot fully |

---

## 📊 Ticket Status Flow

```
User Creates Ticket
       │
       ▼
    [OPEN] ──────────────────────────────────────┐
       │                                          │
       ▼ (Admin picks up)                        │
 [IN PROGRESS] ───────────────────────────────── │
       │                                          │
       ▼ (Issue resolved)                        │
   [CLOSED] ◄────────────────────────────────────┘
```

---

## 🔐 Security Features

- **Password Hashing:** bcrypt with 12 salt rounds
- **Session Management:** Flask-Login secure sessions  
- **Authorization:** Role-based decorators (`@admin_required`)
- **Input Validation:** Server-side validation on all forms
- **Network Security:** AWS Security Groups restrict access

---

## 📝 Credentials (Demo)

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@demo.com | admin123 |
| User | arjun@test.com | user123 |
| User | priya@test.com | user123 |

> ⚠️ Change all passwords before deploying to production!
