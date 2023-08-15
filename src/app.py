import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "name": "John Jackson",
    "id": jackson_family._generateId(),
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})

jackson_family.add_member({
    "name": "Jane Jackson",
    "id": jackson_family._generateId(),
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})

jackson_family.add_member({
    "name": "Jimmy Jackson",
    "id": jackson_family._generateId(),
    "age": 5,
    "lucky_numbers": [1]
})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        raise APIException("Member not found", status_code=404)

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.get_json()
    jackson_family.add_member(member_data)
    return jsonify({}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if deleted:
        return jsonify({"done": True}), 200
    else:
        raise APIException("Member not found", status_code=404)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
