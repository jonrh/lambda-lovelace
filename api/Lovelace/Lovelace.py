from flask import Flask, redirect
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

class IOSAppRedirectHelper:
    def get(self):
        return redirect('lovelace://oauth-callback/')


# ios twitter authentication callback url redirect helper
api.add_resource(IOSAppRedirectHelper, '/oauth-callback')

api.add_resource(Tweets, '/tweets')

if __name__ == '__main__':
    app.run()
