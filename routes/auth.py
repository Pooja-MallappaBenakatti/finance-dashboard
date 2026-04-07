from flask import Blueprint, request, jsonify
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        return jsonify({"message": "Login success", "role": user.role})
    
    return jsonify({"message": "Invalid credentials"}), 401