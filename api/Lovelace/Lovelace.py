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

# class IOSAppRedirectHelper(Resource):
#     def get(self):
#         return redirect('lovelace://oauth-callback/')

@app.route('/oauth-callback/<params>')
def show_user_profile(params):
    # show the user profile for that user
    redirectUrl = 'lovelace://oauth-callback/' + params
    return redirect(redirectUrl)


# ios twitter authentication callback url redirect helper
# api.add_resource(IOSAppRedirectHelper, '/oauth-callback')

api.add_resource(Tweets, '/tweets')

if __name__ == '__main__':
    app.run()
