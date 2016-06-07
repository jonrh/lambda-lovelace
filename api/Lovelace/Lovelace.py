from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


tweets = {
    'tweet1': {'content': 'this is test tweet'},
    'tweet2': {'content': 'this is test tweet'},
    'tweet3': {'content': 'this is test tweet'},
}

class Tweets(Resource):
    def get(self):
        return tweets

api.add_resource(Tweets, '/tweets')

if __name__ == '__main__':
    app.run()
