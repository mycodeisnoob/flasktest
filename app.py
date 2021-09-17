from flask import Flask, url_for, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0534123'
app.config['MYSQL_DATABASE_DB'] = 'flask_test'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)


@app.route('/')
class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('user_name', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            _userEmail = args['email']
            _userName = args['user_name']
            _userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_create_user', (_userEmail, _userName, _userPassword))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return {'StatusCode': '200', 'Message': 'User creation success'}
            else:
                return {'StatusCode': '1000', 'Message': str(data[0])}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/user')

@app.route('/user/<string:_userName>')
class CheckUser(Resource):
    def get(self, _userName):
        return {
            '_username': _userName
        }

    def put(self, _userName):
        return {
            '_username': _userName
        }

    def delete(self, _userName):
        return {
            "delete" : "success"
        }

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',port=5000)
