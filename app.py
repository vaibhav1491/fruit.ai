from flask import Flask, Blueprint, jsonify, request, abort
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__)

# Enable CORS for the application
CORS(app, resources={r"/faqs/*": {"origins": "http://localhost:3000"}}) 

routes = Blueprint('routes', __name__)


faqs = [
    {"id": 1, "question": "What is FruitAI?", "answer": "FruitAI helps you learn about fruits."},
    {"id": 2, "question": "How does FruitAI work?", "answer": "It uses AI to provide fruit-related information."}
]


def get_faq_by_id(faq_id):
    return next((faq for faq in faqs if faq["id"] == faq_id), None)


@routes.route('/faqs', methods=['GET'])
def get_faqs():
    return jsonify(faqs), 200
    
@routes.route('/faqs/<int:id>', methods=['GET'])
def get_faq(id):
    faq = get_faq_by_id(id)
    if not faq:
        abort(404, description="FAQ not found")
    return jsonify(faq), 200


@routes.route('/faqs', methods=['POST'])
def create_faq():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question or not answer:
        abort(400, description="Missing question or answer")

    new_id = max(faq["id"] for faq in faqs) + 1 if faqs else 1
    new_faq = {"id": new_id, "question": question, "answer": answer}
    faqs.append(new_faq)
    return jsonify(new_faq), 201

@routes.route('/faqs/<int:id>', methods=['PUT'])
def update_faq(id):
    faq = get_faq_by_id(id)
    if not faq:
        abort(404, description="FAQ not found")

    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question or not answer:
        abort(400, description="Missing question or answer")

    faq['question'] = question
    faq['answer'] = answer
    return jsonify(faq), 200

@routes.route('/faqs/<int:id>', methods=['DELETE'])
def delete_faq(id):
    global faqs
    faq = get_faq_by_id(id)
    if not faq:
        abort(404, description="FAQ not found")

    faqs = [f for f in faqs if f["id"] != id]
    return jsonify({"message": "FAQ deleted"}), 200

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
