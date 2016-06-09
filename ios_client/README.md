# λ Lovelace - iOS App

This folder will contain code for the iOS mobile app. It will be written for iOS 9 and Swift 2.2.

## Libraries installed by CocoaPods

- [Alamofire][1]
- [SwiftyJSON][2]
- [OAuthSwift][3]


## Twitter custom callback url scheme problem and our solution
Twitter API doesn’t accept custom url scheme (ex: **lovelace://**) into callback URL, only **http://** is allowed. But iOS app need a special url scheme to let iOS system know our app can handle the callback url, because only our app know what **lovelace://** mean.
To walk around this problem, we use [first solution suggested in OAuthSwift Wiki][4]. The following steps briefly explain how it works.
1. we set a flask endpoint, **https://lovelance.herokuapp.com/oauth-callback** as callback url on [Twitter application management page][5].
2. When our flask server receives callback request, flask server redirect to our custom scheme url, i.e. **lovelace://oauth-callback?oauth_token=…**_ 3. When iOS system received this custom scheme url, it reopen our iOS app to let us handle this custom url. Finally we extract the **access token** from parameters of custom url.

[1]:	https://github.com/Alamofire/Alamofire
[2]:	https://github.com/SwiftyJSON/SwiftyJSON
[3]:	https://github.com/OAuthSwift/OAuthSwift
[4]:	https://github.com/OAuthSwift/OAuthSwift/wiki/API-with-only-HTTP-scheme-into-callback-URL
[5]:	https://apps.twitter.com/