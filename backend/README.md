# λ Lovelace - Backend
This folder contains our backend code: Python Flask web service and recommender system that communicate with our iOS mobile client.

## Docker
Here is how to build our Docker backend image and name it *lovelace*. This assumes we are in a terminal located in the root *lambda-lovelace/* folder.

```
cd backend/
docker build -t lovelace .
```

To run our *lovelace* image (assuming we're in the *backend/* folder):

```
docker run -it -p 5000:5000 lovelace
```

## Setup instructions on OSX
Homebrew:
gcc -> includes a gfortran compiler. Required for pip to be able to install scipy.


## IOSAppRedirectHelper class explanation

Twitter API doesn’t accept custom url scheme (ex: **lovelace://**) into callback URL, only **http://** is allowed. But iOS app need a special url scheme to let iOS system know our app can handle the callback url, because only our app know what **lovelace://** mean.
To walk around this problem, we use [first solution suggested in OAuthSwift Wiki][1]. The following steps briefly explain how it works.
1. we set a flask endpoint, **https://lovelance.herokuapp.com/oauth-callback** as callback url on [Twitter application management page][2].

2. When our flask server receives callback request, flask server redirect to our custom scheme url, i.e. **lovelace://oauth-callback?oauth\_token=…**.
3. When iOS system received this custom scheme url, it reopen our iOS app to let us handle this custom url. Finally we extract the **access token** from parameters of custom url.


[1]:	https://github.com/OAuthSwift/OAuthSwift/wiki/API-with-only-HTTP-scheme-into-callback-URL
[2]:	https://apps.twitter.com/