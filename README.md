# Aglet Movies API

A Flask REST API that serves movie content sourced from [The Movie Database (TMDB) API](https://developers.themoviedb.org/3/getting-started/introduction). The application includes user authentication, role-based access control (RBAC), and a cron job to periodically sync popular movies from TMDB into a local MySQL database.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Environment Configuration](#environment-configuration)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Cron Job Setup](#cron-job-setup)
7. [Running Tests](#running-tests)
8. [API Endpoints](#api-endpoints)
9. [Swagger Documentation](#swagger-documentation)
10. [Project Structure](#project-structure)

---

## Prerequisites

Before you begin, make sure the following are installed on your system:

- **Python 3.8+**
- **pip** (Python package manager)
- **MySQL 5.7+** or **MariaDB 10.3+**
- **Git**
- A **TMDB API account** — sign up at [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api) to get your API key and access token.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/api.movies.aglet.co.za.git
cd api.movies.aglet.co.za
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

You will also need `flask`, `flask-cors`, and `mysql-connector-python`, which should be added to your environment if not already present:

```bash
pip install flask flask-cors mysql-connector-python
```

---

## Environment Configuration

### 1. Copy the Example Environment File

```bash
cp .env.example .env
```

### 2. Edit the `.env` File

Open `.env` in your editor and fill in the values:

```dotenv
# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=aglet_movies
DB_USER=root
DB_PASSWORD=your_mysql_password

# TMDB API Configuration
API_KEY="your_tmdb_api_key"
ACCESS_TOKEN="your_tmdb_access_token"
BASE_URL="https://api.themoviedb.org/3/movie/popular"

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173
```

**Where to get TMDB credentials:**

1. Create an account at [https://www.themoviedb.org/signup](https://www.themoviedb.org/signup).
2. Go to **Settings → API** in your TMDB account.
3. Copy the **API Key (v3 auth)** into `API_KEY`.
4. Copy the **API Read Access Token (v4 auth)** into `ACCESS_TOKEN`.

> **Important:** Never commit your `.env` file to version control. Ensure `.env` is listed in your `.gitignore`.

---

## Database Setup

### 1. Log In to MySQL

```bash
mysql -u root -p
```

### 2. Run the Schema Script

From within the MySQL shell:

```sql
source /full/path/to/api.movies.aglet.co.za/database.sql;
```

Or from the command line:

```bash
mysql -u root -p < database.sql
```

This will:

- Drop and recreate the `aglet_movies` database.
- Create all required tables: `languages`, `contactus`, `users`, `permissions`, `roles`, `role_permissions`, `user_roles`, and `movies`.
- Seed the dB with test data

---

## Running the Application

### Development Mode

```bash
python app.py
```

The API will start on `http://0.0.0.0:5000`.

To enable debug mode with auto-reload, edit the last line of `app.py`:

```python
app.run(debug=True)
```

### Production Mode (with Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Verify the API Is Running

```bash
curl http://127.0.0.1:5000/api/movies/v1 -H "user-Id: YOUR_USER_TOKEN_FOUND_IN_USERS_TABLE"
```

---

## Cron Job Setup

The `cronFetchMovies.py` script syncs popular movies from TMDB into your local database. It fetches 5 pages of popular movies (100 movies total) and upserts them into the `movies` table this can also be ran manually REFER to STEP 4.

### 1. Open the Crontab Editor

```bash
crontab -e
```

### 2. Add the Cron Entry

Add the following line to run the sync daily at 02:05 AM:

```cron
05 02 * * * /path/to/your/venv/bin/python /full/path/to/api.movies.aglet.co.za/cronFetchMovies.py --limit 250 >> /var/log/aglet_movies_cron.log 2>&1
```

**Important notes:**

- Replace `/path/to/your/venv/bin/python` with the absolute path to the Python binary inside your virtual environment (e.g., `/home/user/api.movies.aglet.co.za/venv/bin/python`).
- Replace `/full/path/to/api.movies.aglet.co.za/cronFetchMovies.py` with the absolute path to the cron script.
- The `>> /var/log/aglet_movies_cron.log 2>&1` part logs output and errors for debugging.
- Make sure the `.env` file is in the same directory as `cronFetchMovies.py`, since it uses `load_dotenv()` to read configuration.

### 3. Verify the Cron Is Registered

```bash
crontab -l
```

### 4. Run the Cron Script Manually (to test)

```bash
cd /path/to/api.movies.aglet.co.za
source venv/bin/activate
python cronFetchMovies.py
```

You should see output like: `100 movies synced successfully`.

---

## Running Tests

The project uses `pytest` for testing. Tests are located in the `tests/` directory and are split into positive and negative test cases for each module.

### 1. Set Up the conftest.py (Required)

The tests expect `client` and `headers` fixtures. Create a `tests/conftest.py` file if one doesn't exist:

```python
import pytest

@pytest.fixture
def client():
    return "http://127.0.0.1:5000/api"

@pytest.fixture
def headers():
    return {
        "Content-Type": "application/json",
        "user-Id": "YOUR_USER_TOKEN"
    }
```

Replace `YOUR_USER_TOKEN` with a valid user token from the `users` table in your database.

> **Note:** The integration tests run against a **live server**, so make sure the Flask app is running before executing tests.

### 2. Run All Tests

```bash
pytest tests/ -v
```

### 3. Run a Specific Test File

```bash
pytest tests/test_movies_positive.py -v
pytest tests/test_auth_negative.py -v
```

### 4. Run Tests with Coverage Report

```bash
pytest tests/ --cov=. --cov-report=term-missing -v
```

### 5. Run Only the Cron Unit Tests

The cron tests are standalone unit tests (mocked, no live server needed):

```bash
pytest tests/testCronFetchMovies.py -v
```

### Test File Overview

| File | Description |
|------|-------------|
| `auth/test_auth_positive.py` | Successful login and auth flows |
| `auth/test_auth_negative.py` | Invalid credentials, missing fields |
| `movies/test_movies_positive.py` | CRUD operations on movies (happy path) |
| `movies/test_movies_negative.py` | Invalid IDs, missing data, no auth |
| `languages/test_languages_poisitive.py` | Language creation (happy path) |
| `languages/test_languages_negative.py` | Missing/invalid language data |
| `contact_us/test_contact_us_positive.py` | Contact form submission |
| `contact_us/test_contact_us_negative.py` | Missing fields, invalid email |
| `roles/test_roles_positive.py` | Role creation |
| `roles/test_roles_negative.py` | Empty role payload |
| `role_permissions/test_role_permissions_positive.py` | Fetching active role permissions |
| `role_permissions/test_role_permissions_negative.py` | Invalid permission flag type |
| `user_roles/test_user_roles_positive.py` | Fetching active user roles |
| `user_roles/test_user_roles_negative.py` | Fetching active user roles |
| `testCronFetchMovies.py` | Unit tests for the TMDB sync cron job |

---

## API Endpoints

All endpoints are prefixed with `/api` and require a `user-Id` header containing a valid user token (except where noted).

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/me/v1/<id>` | Get user by ID |
| POST | `/api/auth/login/v1` | Login with email and password |
| POST | `/api/auth/update_password/v1/<id>` | Update user password |
| PUT | `/api/auth/renew-token/v1` | Renew authentication token |

### Movies

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/movies/v1` | Create a movie |
| PUT | `/api/movies/v1/<id>` | Update a movie |
| DELETE | `/api/movies/v1/<id>` | Soft-delete a movie |
| GET | `/api/movies/v1` | Get all movies |
| GET | `/api/movies/v1/<id>` | Get movie by ID |
| GET | `/api/movies/get-active/v1/<is_active>` | Get movies by active status |

### Languages

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/languages/v1` | Create a language |
| PUT | `/api/languages/v1/<id>` | Update a language |
| DELETE | `/api/languages/v1/<id>` | Soft-delete a language |
| GET | `/api/languages/v1` | Get all languages |
| GET | `/api/languages/v1/<id>` | Get language by ID |
| GET | `/api/languages/get-active/v1/<is_active>` | Get languages by active status |

### Contact Us

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/contact_us/v1` | Submit a contact message |
| PUT | `/api/contact_us/v1/<id>` | Update a contact message |
| DELETE | `/api/contact_us/v1/<id>` | Soft-delete a contact message |
| GET | `/api/contact_us/v1` | Get all contact messages |
| GET | `/api/contact_us/v1/<id>` | Get contact message by ID |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/v1` | Create a user |
| PUT | `/api/users/v1/<id>` | Update a user |
| DELETE | `/api/users/v1/<id>` | Soft-delete a user |
| GET | `/api/users/v1` | Get all users |
| GET | `/api/users/v1/<id>` | Get user by ID |
| GET | `/api/users/get-active/v1/<is_active>` | Get users by active status |
| GET | `/api/users/get-by-company/v1/<company_id>` | Get users by company |

### Roles

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/roles/v1` | Create a role |
| PUT | `/api/roles/v1/<id>` | Update a role |
| DELETE | `/api/roles/v1/<id>` | Soft-delete a role |
| GET | `/api/roles/v1` | Get all roles |
| GET | `/api/roles/v1/<id>` | Get role by ID |
| GET | `/api/roles/get-active/v1/<is_active>` | Get roles by active status |

### Role Permissions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/role_permissions/v1` | Create a role permission |
| PUT | `/api/role_permissions/v1/<id>` | Update a role permission |
| DELETE | `/api/role_permissions/v1/<id>` | Soft-delete a role permission |
| GET | `/api/role_permissions/v1` | Get all role permissions |
| GET | `/api/role_permissions/v1/<id>` | Get role permission by ID |
| GET | `/api/role_permissions/get-active/v1/<is_active>` | Get active role permissions |
| GET | `/api/role_permissions/get-by-role/v1/<role_id>` | Get permissions by role |

### User Roles

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/user_roles/v1` | Assign a role to a user |
| PUT | `/api/user_roles/v1/<id>` | Update a user role |
| DELETE | `/api/user_roles/v1/<id>` | Soft-delete a user role |
| GET | `/api/user_roles/v1` | Get all user roles |
| GET | `/api/user_roles/v1/<id>` | Get user role by ID |
| GET | `/api/user_roles/get-active/v1/<is_active>` | Get active user roles |
| GET | `/api/user_roles/get-by-role/v1/<role_id>` | Get user roles by role |
| GET | `/api/user_roles/get-by-user/v1/<user_id>` | Get user roles by user |

---

## Swagger Documentation

Full API documentation is available via the included Swagger/OpenAPI spec:

1. Open the [Swagger Editor](https://editor.swagger.io/).
2. Copy the contents of `agletMovieDB.yaml`.
3. Paste it into the Swagger Editor to browse all endpoints interactively.
