from flask import Blueprint, request, jsonify
from models import Record
from database import db

records_bp = Blueprint('records', __name__)

@records_bp.route('/', methods=['GET'])
def get_records():
    records = Record.query.all()
    return jsonify([{
        "id": r.id,
        "amount": r.amount,
        "category": r.category,
        "type": r.type
    } for r in records])


@records_bp.route('/', methods=['POST'])
def add_record():
    data = request.json

    new_record = Record(
        amount=float(data['amount']),
        category=data['category'],
        type=data['type']
    )

    db.session.add(new_record)
    db.session.commit()

    return jsonify({"message": "Record added"})


@records_bp.route('/<int:id>', methods=['DELETE'])
def delete_record(id):
    record = Record.query.get(id)
    db.session.delete(record)
    db.session.commit()
    return {"message": "Deleted"}