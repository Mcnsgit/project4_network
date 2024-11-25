# Social Network Web Application

A feature-rich social networking platform built with Django, featuring real-time notifications, image sharing, and interactive posts.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-3.2%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- 👤 User Authentication & Authorization
- 📝 Create, Edit & Delete Posts
- 🖼️ Image Upload Support
- 💬 Comments & Replies
- ❤️ Like & Save Posts
- 🔔 Real-time Notifications
- 🔍 User Search
- 📱 Responsive Design

## 🚀 Deployment

This project is configured for deployment on Render.com. To deploy:

1. Create an account on [Render](https://render.com)
2. Fork this repository to your GitHub account
3. In Render:
   - Create a new Web Service
   - Connect your GitHub repository
   - Use the following settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn project4.wsgi:application`

4. Add the following environment variables in Render:
   - `DJANGO_SECRET_KEY`: Your Django secret key
   - `DEBUG`: false
   - `ALLOWED_HOSTS`: your-app.onrender.com

The deployment will be handled automatically through GitHub Actions whenever you push to the main branch.

## 🚀 Demo

[View Live Demo](#) _(Coming Soon)_

## 📸 Screenshots

_(Coming Soon)_

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-network.git
cd social-network
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Generate sample data (optional):
```bash
python manage.py generate_fake_data
```

7. Run the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 🔧 Environment Variables

The following environment variables are required:

- `DJANGO_SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'False' in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Your database URL (provided by Render)

## 🧪 Running Tests

```bash
python manage.py test
```

## 🔧 Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (development) / PostgreSQL (production)
- **Image Storage**: Django File Storage
- **Authentication**: Django Authentication System

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- All contributors
# project4_network
