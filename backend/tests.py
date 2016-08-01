import rollbar
import urllib2

rollbar.init("9a41d7e8fdbb49cead0cae434765a927", "testing")  # access_token, environment


def test_one_plus_one():
    assert 1 + 1 == 2


def test_recommender_backend():
    url = """http://backend-testing/recommend
        ?oauth_token=735845050458984448-oLfMuBPTyCnOw2yPEU0MdJ65YxX1BwU
        &oauth_token_secret=veyfudJQz0TMY5S8K6VwzPfteQFVPOSdU1yWwq5fWtZHC
        &page=1"""

    urllib2.urlopen(url).read()


def test_hello_endpoint():
    html = urllib2.urlopen("http://backend-testing/").read()
    assert "Hello" in html
