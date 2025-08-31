# MindStream

Welcome to MindStream – a platform for online diaries and personal stories, built with Django and Django REST Framework.

## 📘 What is MindStream?

MindStream lets users create, manage, and share diary posts on a variety of topics: personal life, education, travel, career, art, psychology, and more. Each post can be liked, disliked, commented on, and categorized for easy discovery.

## ✨ Main Features

- **User Authentication**: Register, log in, and manage your profile securely.
- **Create & Manage Diary Posts**: Add, edit, delete, and filter diary entries.
- **Categories**: Organize posts by topics like travel, education, books, technology, etc.
- **Comments**: Engage with other users by commenting on posts.
- **Likes & Dislikes**: React to posts with likes or dislikes.
- **Subscriptions**: Follow other authors and receive updates when they post.
- **Admin Panel**: Manage users and content with Django’s admin interface.
- **API Documentation**: Interactive Swagger UI at `/api/docs`.

## 🛠 Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker
- **API Docs**: drf-spectacular (OpenAPI/Swagger)
- **Authentication**: JWT (via DRF)

## 🚀 Get Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/Maksim124512M/MindStream.git
   cd mind_stream
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Configure environment variables**
   ```bash
   copy .env.example .env
   ```

4. **Run with Docker**
   ```bash
   docker compose up --build
   ```

5. **Admin panel login**
   - Username: `admin`
   - Password: `admin123`

## 📚 Documentation

- Visit `/api/docs` for interactive API docs (Swagger UI).

## 📝 License

This project is open source and available under the MIT License.

---

Feel free to contribute, open issues, or start a discussion!
