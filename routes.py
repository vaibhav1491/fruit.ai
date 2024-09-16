from flask import Blueprint, jsonify, request, abort
from models import db, FAQ

app = Blueprint('routes', __name__)

# GET /faqs - Fetch all FAQs
@app.route('/faqs', methods=['GET'])
def get_faqs():
    faqs = FAQ.query.all()
    return jsonify([faq.to_dict() for faq in faqs]), 200

# GET /faqs/:id - Fetch a single FAQ by ID
@app.route('/faqs/<int:id>', methods=['GET'])
def get_faq(id):
    faq = FAQ.query.get(id)
    if not faq:
        abort(404, description="FAQ not found")
    return jsonify(faq.to_dict()), 200

# POST /faqs - Create a new FAQ
@app.route('/faqs', methods=['POST'])
def create_faq():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question or not answer:
        abort(400, description="Missing question or answer")

    new_faq = FAQ(question=question, answer=answer)
    db.session.add(new_faq)
    db.session.commit()

    return jsonify(new_faq.to_dict()), 201

# PUT /faqs/:id - Update an FAQ by ID
@app.route('/faqs/<int:id>', methods=['PUT'])
def update_faq(id):
    faq = FAQ.query.get(id)
    if not faq:
        abort(404, description="FAQ not found")

    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question or not answer:
        abort(400, description="Missing question or answer")

    faq.question = question
    faq.answer = answer
    db.session.commit()

    return jsonify(faq.to_dict()), 200

# DELETE /faqs/:id - Delete a FAQ by ID
@app.route('/faqs/<int:id>', methods=['DELETE'])
def delete_faq(id):
    faq = FAQ.query.get(id)
    if not faq:
        abort(404, description="FAQ not found")

    db.session.delete(faq)
    db.session.commit()

    return jsonify({"message": "FAQ deleted"}), 200
