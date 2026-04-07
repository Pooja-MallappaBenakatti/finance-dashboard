from flask import Blueprint, request, jsonify
from models import User
from database import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "role": u.role
    } for u in users])


@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.json

    user = User(
        username=data['username'],
        password=data['password'],
        role=data['role']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"})