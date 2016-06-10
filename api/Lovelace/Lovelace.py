from flask import Flask, redirect,request
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

class IOSAppRedirectHelper(Resource):
    def get(self):
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')

        location = 'lovelace://oauth-callback?oauth_token='
        location += oauth_token
        location += '&oauth_verifier='
        location += oauth_verifier
        return redirect(location)



# ios twitter authentication callback url redirect helper
api.add_resource(IOSAppRedirectHelper, '/oauth-callback')

api.add_resource(Tweets, '/tweets')

if __name__ == '__main__':
    app.run()
