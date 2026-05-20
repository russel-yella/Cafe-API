
# ☕ Cafe API

A simple REST API built with Flask and SQLAlchemy for managing cafes, including features like searching, adding, updating prices, random selection, and deleting records with API key protection.

---

## 🚀 Features

* Get all cafes
* Get a random cafe
* Search cafes by location
* Add a new cafe
* Update coffee price
* Delete a cafe (protected by API key)

---

## 🛠️ Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* SQLite

---

## 📁 Project Structure

```
project/
│
├── app.py
├── cafes.db
├── templates/
│   └── index.html
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cafe-api.git
cd cafe-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install flask flask_sqlalchemy
```

### 4. Run the app

```bash
python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

## 📡 API Endpoints

### Get all cafes

```http
GET /all
```

---

### Get a random cafe

```http
GET /random
```

---

### Search by location

```http
GET /search?loc=Paris
```

---

### Add a new cafe

```http
POST /add
```

Form Data:

* name
* map_url
* img_url
* location
* seats
* has_wifi
* has_sockets
* has_toilet
* can_take_calls
* coffee_price

---

### Update coffee price

```http
PATCH /update-price/<cafe_id>?new_price=$4.50
```

---

### Delete a cafe (requires API key)

```http
DELETE /report-closed/<cafe_id>?api-key=TopSecretAPIKey
```

---

## 🔐 API Key

Required for deleting cafes:

```
TopSecretAPIKey
```

---

## 📌 Notes

* Ensure `to_dict()` exists in your `Cafe` model for JSON responses.
* Boolean values from forms are received as strings.
* Database is SQLite (`cafes.db`).

---

