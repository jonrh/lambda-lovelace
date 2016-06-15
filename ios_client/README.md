# λ Lovelace - iOS App

This folder contains code for the iOS mobile app. It will be written for iOS 9 and Swift 2.2. The project uses [CocoaPods][7] for third party dependencies. When this was written we [check Pods directly into our repository][6]. This means if you only have to bother with installing CocoaPods if you need to add, update, or delete dependencies.

**To start developing**: Open the file `ios_client/Locelace/Lovelace.xcworkspace`. We have to open the workspace file because we are using CocoaPods. Using the project file will not work.

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
[6]:	https://guides.cocoapods.org/using/using-cocoapods.html#should-i-check-the-pods-directory-into-source-control
[7]:	https://cocoapods.org/
