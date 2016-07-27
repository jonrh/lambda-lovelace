import rollbar
import urllib2

rollbar.init("9a41d7e8fdbb49cead0cae434765a927", "testing")  # access_token, environment

def test_one_plus_one():
    assert 1 + 1 == 2

def test_recommender_backend():
	response = urllib2.urlopen("http://0.0.0.0/recommend?oauth_token=735845050458984448-oLfMuBPTyCnOw2yPEU0MdJ65YxX1BwU&oauth_token_secret=veyfudJQz0TMY5S8K6VwzPfteQFVPOSdU1yWwq5fWtZHC&page=1")