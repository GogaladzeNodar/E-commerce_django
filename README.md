# 🐍 Django + PostgreSQL DevContainer Setup

This project uses **Django**, **PostgreSQL**, **Docker Compose**, and **DevContainers** to provide a fully isolated development environment inside Visual Studio Code.

---

## 📦 Prerequisites

Before getting started, make sure you have the following installed:

- ✅ [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- ✅ [Visual Studio Code](https://code.visualstudio.com/)
- ✅ [Dev Containers Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

---

## ⚙️ Project Structure


.
├── .devcontainer/
│ └── devcontainer.json # DevContainer configuration
├── Dockerfile.dev # Dockerfile for Django container
├── docker-compose.yml # Docker Compose config (Django + PostgreSQL)
├── .env # Environment variables (you must create)
├── manage.py
├── requirements.txt
├── your_django_app/
└── README.md

## 🔐 Step 1 – Create `.env` file

------------------------
.env example 

DJANGO_SECRET_KEY= "your secret key"
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432
-------------------------


Step 2 – Open Project in DevContainer

Open this project in VS Code.
Open the command palette with:
Windows/Linux: Ctrl+Shift+P
macOS: Cmd+Shift+P
Search for:
Dev Containers: Reopen in Container
Wait for the containers to build and start up. VS Code will attach you inside the Django container.



Step 3 – Initial Setup

Once inside the container terminal:

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver 0.0.0.0:8000  # or it will be run automatically






Database Info

The PostgreSQL service runs in a separate Docker container.
Connection is handled via environment variables.
Your Django DATABASES setting should look like:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}




🔁 Restarting / Stopping

🔄 Restart DevContainer
Open command palette → Dev Containers: Reopen in Container
❌ Stop DevContainer
Dev Containers: Close Remote Connection
Or stop containers with Docker Desktop
Or use terminal:
docker compose down


Notes

All Django code runs inside the DevContainer (/app).
Project files are mounted as volumes so live code changes reflect instantly.
PostgreSQL is isolated from your host and talks to Django via internal Docker network.