# λ Lovelace - API

This folder will contain code for the Python + Flask web service that will speak with our mobile client.
---- 
## Push Flask project to Heroku commands
Because git repository doesn’t allow nested. So we need use following commands to push Flask project to Heroku.
```
` 1. go to the root directory of this repository (lambda-lovelace)
2. git add -A 
3. git commit -am “… …”
 4. git subtree push --prefix api/Lovelace/ heroku master
```
`---- 
## IOSAppRedirectHelper class explanation
Twitter API doesn’t accept custom url scheme (ex: **lovelace://**) into callback URL, only **http://** is allowed. But iOS app need a special url scheme to let iOS system know our app can handle the callback url, because only our app know what **lovelace://** mean.
To walk around this problem, we use [first solution suggested in OAuthSwift Wiki][1]. The following steps briefly explain how it works.
1. we set a flask endpoint, **https://lovelance.herokuapp.com/oauth-callback** as callback url on [Twitter application management page][2].
2. When our flask server receives callback request, flask server redirect to our custom scheme url, i.e. **lovelace://oauth-callback?oauth_token=…**_ 3. When iOS system received this custom scheme url, it reopen our iOS app to let us handle this custom url. Finally we extract the **access token** from parameters of custom url.



[1]:	https://github.com/OAuthSwift/OAuthSwift/wiki/API-with-only-HTTP-scheme-into-callback-URL
[2]:	https://apps.twitter.com/