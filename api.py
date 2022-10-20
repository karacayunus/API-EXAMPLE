from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd


app = Flask(_name_)
api = Api(app)

class email(Resource):
    def get(self):
        data = pd.read_csv('email.csv')
        data = data.to_dict('records')
        
        return {'data' : data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Login email')
        parser.add_argument('First name')
        parser.add_argument('Last name')
        args = parser.parse_args()

        data = pd.read_csv('email.csv')

        new_data = pd.DataFrame({
            'Login email'      : [args['Login email']],
            'First name'      : [args['First name']],
            'Last name'      : [args['Last name']]
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('email.csv', index=False)
        return {'data' : new_data.to_dict('records')}, 201
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Login email', required=True)
        parser.add_argument('First name', required=True)
        args = parser.parse_args()

        data = pd.read_csv('email.csv')

        data = data[data['Login email'] != args['Login email']]

        data.to_csv('email.csv', index=False)
        return {'message' : 'Record deleted successfully.'}, 200

api.add_resource(email, "/email")


if _name_ == '_main_':
    app.run(host="127.0.0.1", port=5000)