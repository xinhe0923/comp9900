from flask import Flask, Blueprint
from flask import jsonify
from flask_restful import reqparse

home_page = Blueprint('user_page',__name__)
database = []




class Property:
    def __init__(self, ID, name, location,number_bedroom):
        self.ID = name
        self.name = name
        self.location = location
        self.number_bedroom = number_bedroom


@home_page.route("/home", methods=['POST'])
def add_student():
    parser = reqparse.RequestParser()
    parser.add_argument('ID', type=str)
    parser.add_argument('name', type=int)
    parser.add_argument('location', type=str)
    parser.add_argument('number_bedroom', type=int)


    args = parser.parse_args()

    ID = args.get("ID")
    name = args.get("name")
    location  = args.get("location")
    number_bedroom = args.get("number_bedroom")

    database.append(Property(ID, name, location, number_bedroom))
    return jsonify(propertyName= name),200
    
@home_page.route("/property", methods=['GET'])
def search_property():
    response = jsonify([st.__dict__ for st in database])
    response.headers._list.append(('Access-Control-Allow-Origin', '*'))
    return response






if __name__ == "__main__":
    home_page.run()