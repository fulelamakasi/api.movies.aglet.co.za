from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import uuid
from functools import wraps
import hashlib
import os
from dotenv import load_dotenv
import json
from pathlib import Path
import datetime
from datetime import datetime
import logging
import re
import socket

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:3000", "http://localhost:3000"],
        "supports_credentials": True,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }
})

load_dotenv()

db_config = {
    'host': os.getenv('DBHOST', "127.0.0.1"),
    'user': os.getenv('DBUSER', "root"),
    'password': os.getenv('DBPASS', "123456"),
    'database': os.getenv('DB', "aglet_movies")
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")

def has_permission(permission_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = request.headers.get('user-Id')  # Assume user ID is passed in headers
            if not user_id:
                return jsonify({'error': 'User ID is required'}), 400

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            try:
                # Check if the user has the required permission
                query = """
                SELECT p.name
                FROM users u
                JOIN user_roles ur ON u.id = ur.user_id
                JOIN role_permissions rp ON ur.role_id = rp.role_id
                JOIN permissions p ON rp.permission_id = p.id
                WHERE u.token = %s AND p.name = %s
                """
                cursor.execute(query, (user_id, permission_name))
                result = cursor.fetchone()

                if not result:
                    return jsonify({'error': 'Permission denied'}), 403

                return f(*args, **kwargs)
            except mysql.connector.Error as err:
                return jsonify({'error': str(err)}), 500
            finally:
                cursor.close()
                conn.close()
        return wrapped
    return decorator

##### AUTHENTICATION #####
@app.route('/api/auth/me/v1/<int:id>', methods=['GET'])
#@has_permission('auth_me_by_id')
def auth_me_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if not id:
        return jsonify({'error': 'auth token is required'}), 204
    
    try:
        cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
        user = cursor.fetchone()
        if user:
            return jsonify({"token": user['token'], "data": dict(zip((col[0] for col in cursor.description), user))}), 200
        else:
            return jsonify({'error': 'User not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/login/v1', methods=['POST'])
@has_permission('login')
def login():
    data = request.json
    email = data.get('email')
    password = hashlib.md5(data.get('password').encode("utf-8")).hexdigest()
    is_active = 1

    if not email or not password:
        return jsonify({'error': 'User Name & Password are required'}), 204

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s AND is_active = %s', (email, password, is_active))
        user = cursor.fetchone()
        if user:
            return jsonify({"data": dict(zip((col[0] for col in cursor.description), user))}), 200
        else:
            return jsonify({"data": "", 'error': 'Username or Password do not match'}), 403
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/update_password/v1/<int:id>', methods=['POST'])
@has_permission('update_password')
def update_password(id):
    data = request.json
    passW = data.get('password')
    confirm_password = data.get('confirm_password')

    if not confirm_password or not passW or not id:
        return jsonify({'error': 'User Token, Password & Confirm Password are required'}), 204

    if passW != confirm_password:
        return jsonify({'message': 'Passwords do not match'}), 304 

    password = hashlib.md5(data.get('password').encode("utf-8")).hexdigest()
    reset_password = 0

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE user SET password = %s, reset_password = %s WHERE id = %s', (password, reset_password, id))
        conn.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/renew-token/v1', methods=['PUT'])
@has_permission('renew_token')
def renew_token():
    data = request.json
    user_id = request.headers.get('user-Id')
    is_active = 1

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400


    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE token = %s AND is_active = %s', (user_id, is_active))        
        user = cursor.fetchone()

        if user:
            token = str(uuid.uuid4())
            cursor.execute('UPDATE users SET token = %s WHERE id = %s', (token, user_id))
            conn.commit()

            cursor.execute('SELECT * FROM users WHERE id = %s', (user['id'],))        
            user = cursor.fetchone()
            return jsonify(user), 200
        else:
            return jsonify({'error': 'Could Not Find Active User with token. Please contact support.'}), 403
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

##### MOVIES #####
@app.route('/api/movies/v1', methods=['POST'])
@has_permission('create_movie')
def create_movies():
    data = request.json

    tmdb_id = data.get('tmdb_id')
    title = data.get('title')
    overview = data.get('overview')
    release_date = data.get('release_date')
    poster_path = data.get('poster_path')
    backdrop_path = data.get('backdrop_path')
    popularity = data.get('popularity')
    vote_average = data.get('vote_average')
    vote_count = data.get('vote_count')
    language = data.get('language')

    if not tmdb_id or not title or not overview or not release_date or not poster_path or not backdrop_path or not popularity or not vote_average or not vote_count or not language:
        return jsonify({'error': 'Required fields are missing'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO movies(tmdb_id,title,overview,release_date,poster_path,backdrop_path,popularity,vote_average,vote_count,language) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (tmdb_id,title,overview,release_date,poster_path,backdrop_path,popularity,vote_average,vote_count,language))
        conn.commit()
        return jsonify({'message': 'Movie created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/movies/v1/<int:movie_id>', methods=['PUT'])
@has_permission('update_movie')
def update_movie(movie_id):
    data = request.json

    tmdb_id = data.get('tmdb_id')
    title = data.get('title')
    overview = data.get('overview')
    release_date = data.get('release_date')
    poster_path = data.get('poster_path')
    backdrop_path = data.get('backdrop_path')
    popularity = data.get('popularity')
    vote_average = data.get('vote_average')
    vote_count = data.get('vote_count')
    language = data.get('language')

    if not tmdb_id or not title or not overview or not release_date or not poster_path or not backdrop_path or not popularity or not vote_average or not vote_count or not language:
        return jsonify({'error': 'Required fields are missing'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE movies SET tmdb_id = %s, title = %s, overview = %s, release_date = %s, poster_path = %s, backdrop_path = %s, popularity = %s, vote_average = %s, vote_count = %s, language = %s WHERE id = %s', (tmdb_id, title, overview, release_date, poster_path, backdrop_path, popularity, vote_average, vote_count, language, movie_id))
        conn.commit()
        return jsonify({'message': 'Movie updated successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/movies/v1/<int:movie_id>', methods=['DELETE'])
@has_permission('delete_movie')
def delete_movie(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_deleted = 1

    try:
        #cursor.execute('DELETE FROM movies WHERE id = %s', (movie_id,))
        cursor.execute('UPDATE movies SET is_deleted = %s WHERE id = %s', (is_deleted, movie_id))
        conn.commit()
        return jsonify({'message': 'Movie deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/movies/v1', methods=['GET'])
@has_permission('get_all_movies')
def get_all_movies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM movies')
        movies = cursor.fetchall()

        return json.dumps(movies, default=str), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/movies/v1/<int:movie_id>', methods=['GET'])
@has_permission('get_movie_by_id')
def get_movie_by_id(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM movies WHERE id = %s', (movie_id,))
        movie = cursor.fetchone()
        if movie:
            return json.dumps(movie, default=str), 200
        else:
            return jsonify({'error': 'Movie not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/movies/get-active/v1/<int:is_active>', methods=['GET'])
@has_permission('get_active_movies')
def get_active_movies(is_active):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM movies WHERE is_active = %s', (is_active,))
        movies = cursor.fetchall()
        if movies:
            return json.dumps(movies, default=str), 200
        else:
            return jsonify({'error': 'Movies not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


##### PERMISSIONS #####
@app.route('/api/permissions/v1', methods=['POST'])
@has_permission('create_permission')
def create_permission():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    is_active = 1

    if not name:
        return jsonify({'error': 'Required fields are missing'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO permissions (name, description, is_active) VALUES (%s, %s, %s)', (name, description, is_active))
        conn.commit()
        return jsonify({'message': 'Permission created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/permissions/v1/<int:permission_id>', methods=['PUT'])
@has_permission('update_permission')
def update_permission(permission_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    is_active = data.get('is_active')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE permissions SET name = %s, description = %s, is_active = %s WHERE id = %s', (name, description, is_active, permission_id))
        conn.commit()
        return jsonify({'message': 'Permission updated successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/permissions/v1/<int:permission_id>', methods=['DELETE'])
@has_permission('delete_permission')
def delete_permission(permission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_deleted = 1

    try:
        #cursor.execute('DELETE FROM permissions WHERE id = %s', (permission_id,))
        cursor.execute('UPDATE permissions SET is_deleted = %s WHERE id = %s', (is_deleted, permission_id))
        conn.commit()
        return jsonify({'message': 'Permission deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/permissions/v1', methods=['GET'])
@has_permission('get_all_permissions')
def get_all_permissions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM permissions')
        permissions = cursor.fetchall()
        return jsonify(permissions), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/permissions/v1/<int:permission_id>', methods=['GET'])
@has_permission('get_permission_by_id')
def get_permission_by_id(permission_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM permissions WHERE id = %s', (permission_id,))
        permission = cursor.fetchone()
        if permission:
            return jsonify(permission), 200
        else:
            return jsonify({'error': 'Permission not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/permissions/get-active/v1/<int:is_active>', methods=['GET'])
@has_permission('get_active_permissions')
def get_active_permissions(is_active):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM permissions WHERE is_active = %s', (is_active,))
        permissions = cursor.fetchall()
        if permissions:
            return jsonify(permissions), 200
        else:
            return jsonify({'error': 'Permissions not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

##### ROLE_PERMISSIONS #####
@app.route('/api/role_permissions/v1', methods=['POST'])
@has_permission('create_role_permission')
def create_role_permission():
    data = request.json
    role_id = data.get('role_id')
    permission_id = data.get('permission_id')
    is_active = 1

    if not permission_id or not role_id:
        return jsonify({'error': 'Required fields are missing'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO role_permissions (permission_id, role_id, is_active) VALUES (%s, %s, %s)', (permission_id, role_id, is_active))
        conn.commit()
        return jsonify({'message': 'Role Permmission created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/role_permissions/v1/<int:role_permission_id>', methods=['PUT'])
@has_permission('update_role_permission')
def update_role_permission(role_permission_id):
    data = request.json
    role_id = data.get('role_id')
    permission_id = data.get('permission_id')
    is_active = data.get('is_active')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE permissions SET role_id = %s, permission_id = %s, is_active = %s WHERE id = %s', (role_id, permission_id, is_active, role_permission_id))
        conn.commit()
        return jsonify({'message': 'Role Permission updated successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/role_permissions/v1/<int:role_permission_id>', methods=['DELETE'])
@has_permission('delete_role_permission')
def delete_role_permission(role_permission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_deleted = 1

    try:
        #cursor.execute('DELETE FROM role_permissions WHERE id = %s', (role_permission_id,))
        cursor.execute('UPDATE role_permissions SET is_deleted = %s WHERE id = %s', (is_deleted, role_permission_id))
        conn.commit()
        return jsonify({'message': 'Role Permission deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/role_permissions/v1', methods=['GET'])
@has_permission('get_all_role_permissions')
def get_all_role_permissions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM role_permissions')
        role_permissions = cursor.fetchall()
        return jsonify(role_permissions), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close(),
        conn.close()

@app.route('/api/role_permissions/v1/<int:role_permission_id>', methods=['GET'])
@has_permission('get_role_permission_by_id')
def get_role_permission_by_id(role_permission_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM role_permissions WHERE id = %s', (role_permission_id,))
        role_permission = cursor.fetchone()
        if role_permission:
            return jsonify(role_permission), 200
        else:
            return jsonify({'error': 'Role Permission not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/role_permissions/get-by-permission/v1/<int:permission_id>', methods=['GET'])
@has_permission('get_active_role_permissions_by_permission')
def get_active_role_permissions_by_permission(permission_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM role_permissions WHERE permission_id = %s', (permission_id,))
        role_permissions = cursor.fetchall()
        if role_permissions:
            return jsonify(role_permissions), 200
        else:
            return jsonify({'error': 'Role Permissions not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/role_permissions/get-by-role/v1/<int:role_id>', methods=['GET'])
@has_permission('get_active_role_permissions_by_role')
def get_active_role_permissions_by_role(role_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM role_permissions WHERE role_id = %s', (role_id,))
        role_permissions = cursor.fetchall()
        if role_permissions:
            return jsonify(role_permissions), 200
        else:
            return jsonify({'error': 'Role Permissions not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/role_permissions/get-active/v1/<int:is_active>', methods=['GET'])
@has_permission('get_active_role_permissions')
def get_active_role_permissions(is_active):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM role_permissions WHERE is_active = %s', (is_active,))
        role_permissions = cursor.fetchall()
        if role_permissions:
            return jsonify(role_permissions), 200
        else:
            return jsonify({'error': 'Role Permissions not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

##### ROLES #####
@app.route('/api/roles/v1', methods=['POST'])
@has_permission('create_role')
def create_role():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    is_active = 1

    if not name:
        return jsonify({'error': 'Required fields are missing'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO roles (name, description, is_active) VALUES (%s, %s, %s)', (name, description, is_active))
        conn.commit()
        return jsonify({'message': 'Role created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/roles/v1/<int:role_id>', methods=['PUT'])
@has_permission('update_role')
def update_role(role_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    is_active = data.get('is_active')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE roles SET name = %s, description = %s, is_active = %s WHERE id = %s', (name, description, is_active, role_id))
        conn.commit()
        return jsonify({'message': 'Role updated successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/roles/v1/<int:role_id>', methods=['DELETE'])
@has_permission('delete_role')
def delete_role(role_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_deleted = 1

    try:
        #cursor.execute('DELETE FROM roles WHERE id = %s', (role_id,))
        cursor.execute('UPDATE roles SET is_deleted = %s WHERE id = %s', (is_deleted, role_id))
        conn.commit()
        return jsonify({'message': 'Role deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/roles/v1', methods=['GET'])
@has_permission('get_all_roles')
def get_all_roles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM roles')
        roles = cursor.fetchall()
        return jsonify(roles), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/roles/v1/<int:role_id>', methods=['GET'])
@has_permission('get_role_by_id')
def get_role_by_id(role_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM roles WHERE id = %s', (role_id,))
        role = cursor.fetchone()
        if role:
            return jsonify(role), 200
        else:
            return jsonify({'error': 'Role not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/roles/get-active/v1/<int:is_active>', methods=['GET'])
@has_permission('get_active_roles')
def get_active_roles(is_active):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM roles WHERE is_active = %s', (is_active,))
        roles = cursor.fetchall()
        if roles:
            return jsonify(roles), 200
        else:
            return jsonify({'error': 'Roles not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

##### USER_ROLES #####
@app.route('/api/user_roles/v1', methods=['POST'])
@has_permission('create_user_role')
def create_user_role():
    data = request.json
    role_id = data.get('role_id')
    user_id = data.get('user_id')
    is_active = 1

    if not user_id or not role_id:
        return jsonify({'error': 'Required fields are missing'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO user_roles (user_id, role_id, is_active) VALUES (%s, %s, %s)', (user_id, role_id, is_active))
        conn.commit()
        return jsonify({'message': 'User Role created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user_roles/v1/<int:user_role_id>', methods=['PUT'])
@has_permission('update_user_role')
def update_user_role(user_role_id):
    data = request.json
    role_id = data.get('role_id')
    user_id = data.get('user_id')
    is_active = data.get('is_active')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE user_roles SET role_id = %s, user_id = %s, is_active = %s WHERE id = %s', (role_id, user_id, is_active, user_role_id))
        conn.commit()
        return jsonify({'message': 'User Role updated successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user_roles/v1/<int:user_role_id>', methods=['DELETE'])
@has_permission('delete_user_role')
def delete_user_role(user_role_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_deleted = 1

    try:
        #cursor.execute('DELETE FROM user_roles WHERE id = %s', (user_role_id,))
        cursor.execute('UPDATE user_roles SET is_deleted = %s WHERE id = %s', (is_deleted, user_role_id))
        conn.commit()
        return jsonify({'message': 'User Role deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user_roles/v1', methods=['GET'])
@has_permission('get_all_user_roles')
def get_all_user_roles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_roles')
        user_roles = cursor.fetchall()
        return jsonify(user_roles), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user_roles/v1/<int:user_role_id>', methods=['GET'])
@has_permission('get_user_role_by_id')
def get_user_role_by_id(user_role_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_roles WHERE id = %s', (user_role_id,))
        user_role = cursor.fetchone()
        if user_role:
            return jsonify(user_role), 200
        else:
            return jsonify({'error': 'User Role not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user_roles/get-by-role/v1/<int:role_id>', methods=['GET'])
@has_permission('get_user_roles_by_role')
def get_user_roles_by_role(role_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_roles WHERE role_id = %s', (role_id,))
        user_roles = cursor.fetchall()
        if user_roles:
            return jsonify(user_roles), 200
        else:
            return jsonify({'error': 'User Roles not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user_roles/get-by-user/v1/<int:user_id>', methods=['GET'])
@has_permission('get_user_roles_by_user')
def get_user_roles_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_roles WHERE user_id = %s', (user_id,))
        user_roles = cursor.fetchall()
        if user_roles:
            return jsonify(user_roles), 200
        else:
            return jsonify({'error': 'User Roles not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user_roles/get-active/v1/<int:is_active>', methods=['GET'])
@has_permission('get_active_user_roles')
def get_active_user_roles(is_active):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_roles WHERE is_active = %s', (is_active,))
        user_roles = cursor.fetchall()
        if user_roles:
            return jsonify(user_roles), 200
        else:
            return jsonify({'error': 'User Roles not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

##### USERS #####
@app.route('/api/users/v1', methods=['POST'])
@has_permission('create_user')
def create_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phonenumber = data.get('phonenumber')
    company_id = data.get('company_id')
    password = hashlib.md5(phonenumber[-4:].encode("utf-8")).hexdigest()
    token = str(uuid.uuid4())
    is_active = 1
    reset_password = 1

    if not first_name or not last_name or not email or not phonenumber or not company_id:
        return jsonify({'error': 'Required fields are missing'}), 400
    
    name = first_name + " " + last_name

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, first_name, last_name, email, phonenumber, password, is_active, reset_password, token, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, first_name, last_name, email, phonenumber, password, is_active, reset_password, token, company_id))
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/v1/<int:user_id>', methods=['PUT'])
@has_permission('update_user')
def update_user(user_id):
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    name = data.get('name')
    phonenumber = data.get('phonenumber')
    password = hashlib.md5(data.get('password').encode("utf-8")).hexdigest()
    is_active = data.get('is_active')
    reset_password = data.get('reset_password')
    token = data.get('token')
    company_id = data.get('company_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET name = %s, first_name = %s, last_name = %s, phonenumber = %s, password = %s, is_active = %s, reset_password = %s, token = %s, company_id = %s WHERE id = %s', (name, first_name, last_name, phonenumber, password, is_active, reset_password, token, company_id, user_id))
        conn.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/v1/<int:user_id>', methods=['DELETE'])
@has_permission('delete_user')
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    is_deleted = 1

    try:
        #cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        cursor.execute('UPDATE users SET is_deleted = %s WHERE id = %s', (is_deleted, user_id))
        conn.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/v1', methods=['GET'])
@has_permission('get_all_users')
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return jsonify(users), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/v1/<int:user_id>', methods=['GET'])
@has_permission('get_user_by_id')
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify({"data": user}), 200
        else:
            return jsonify({'error': 'User not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/get-active/v1/<int:is_active>', methods=['GET'])
@has_permission('get_active_users')
def get_active_users(is_active):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM users WHERE is_active = %s', (is_active,))
        users = cursor.fetchall()
        if users:
            return jsonify(users), 200
        else:
            return jsonify({'error': 'Users not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/users/get-by-company/v1/<int:company_id>', methods=['GET'])
@has_permission('get_users_by_company')
def get_users_by_company(company_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM users WHERE company_id = %s', (company_id,))
        users = cursor.fetchall()
        if users:
            return jsonify(users), 200
        else:
            return jsonify({'error': 'Users not found'}), 204
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error):
    description = str(error.description)
    message = "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again..." + description

    return jsonify({"error": "Not Found", "message": message}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    description = str(error.description)
    message = "The method is not allowed for the requested URL." + description

    return jsonify({"error": "Method Not Allowed", "message": message}), 405

@app.errorhandler(403)
def forbidden(error):
    message = str(error.description)

    return jsonify({"error": "Forbidden", "message": message}), 403

if __name__ == '__main__':
    # app.run(debug=True) 
    app.run(host='0.0.0.0') 

