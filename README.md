# 🍴 Restaurant Kitchen Service
> A modern Django-powered dashboard for managing dishes, cooks, and ingredients in your restaurant kitchen.

A beautiful and efficient web application built with **Django**, **Bootstrap**, and **Crispy Forms** to help manage every aspect of a restaurant kitchen — from dishes and ingredients to cooks and improvement suggestions.

---

## 🚀 Installing / Getting started

A quick setup guide to get your local environment running:

```bash
# Clone the repository
git clone https://github.com/toomuchtearz/restaurant-kitchen-service.git
cd restaurant-kitchen-service

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
# Windows + bash: source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## ✨ Features

Here’s what makes this project awesome:
* 🍽️ Manage and categorize dishes with ease  
* 🌿 Organize all ingredients and see where they’re used  
* 👨‍🍳 Add cooks and assign them to dishes  
* 🍴 Group dishes by type for quick access  
* 💡 Let cooks suggest improvements for dishes (staff can approve them)  
* 🔍 Built-in search and pagination for easy navigation  
* 💻 Modern responsive Bootstrap UI  
* 🔐 Role-based permissions for staff and cooks  
* ⚙️ Optimized queries with `prefetch_related` and `annotate`

---

## 🧪 Demo Credentials

You can explore the live demo without registration — just log in with one of the following test accounts:

| Role | Username | Password | Description |
|------|-----------|-----------|--------------|
| 👨‍🍳 Cook (regular user) | `mykh.ivanov` | `8GHwXa67M4VE` | Can browse dishes, ingredients, and create suggestions |
| 🧑‍💼 Admin / Staff | `admin` | `qLkc8TfjqhaR@` | Has full CRUD access to all models and can approve suggestions |

---

## 🧰 Tech Stack

- **Backend:** Django 5.2  
- **Frontend:** Bootstrap 5, Crispy Forms, JS
- **Database:** SQLite / PostgreSQL  
- **Deployment:** Render
- **Language:** Python 3.13

---

## 🌐 Check it out!

Visit the live project here 👉 [Restaurant Kitchen Service on Render](https://restaurant-kitchen-service-w6qh.onrender.com/)

---
