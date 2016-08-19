# λ Lovelace - iOS App

This folder contains code for the iOS mobile app. It will be written for iOS 9 and Swift 2.2. The project uses [CocoaPods][7] for third party dependencies. When this was written we [check Pods directly into our repository][6]. This means if you only have to bother with installing CocoaPods if you need to add, update, or delete dependencies.

**To start developing**: Open the file `ios_client/Locelace/Lovelace.xcworkspace`. We have to open the workspace file because we are using CocoaPods. Using the project file will not work.

## Libraries installed by CocoaPods

- [Alamofire][1]
- [SwiftyJSON][2]
- [OAuthSwift][3]
- [KILable][4]
- [SWTableViewCell][5]
- [Rollbar][6]

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

## User Interface
- [Login Screen - User logs in using Twitter account][1]
- [Home Screen - User's filtered home timeline of tweets][2]
- [User Profile Screen - Details of the user like screen name, avatar, number of followers and number of followees and log out option][3]
- [Tweet Details Screen - Detailed view of each tweet][4]

## Personalised Tweets
As the user logs in using his/her Twitter account, the Recommender system crunches the users home timeline tweets to output filtered home timeline based on the users likes. The communication between the Twitter client App and Recommender system is delivered by the Flask server.
The Recommender System filters the tweets using Algorithm based on:
- [Word frequency count contained in the user's timeline][1]
- [User's feedback from the Twitter client App][2]

## User Feedback to Recommender System
User can swipe the tweet right and left to give a 'Like' and 'Dislike' to the tweet respectively.
A more detailed description about 'Like' and 'Dislike' is given based on 
- [Author of the tweet - like/dislike more/less from Author][1]
- [Subject of the tweet - like/dislike more/less from the Subject][2]

## Filtered/Personalised Tweets order
The filtered tweets from the Recommender System has a weight associated with each tweet, more the weight, the more relevant the tweet is. Based on the weight the tweets are ordered in the timeline.
The weight are portrayed in the form of color spectrum ranging from  
- [Red - which is more relevent][1]
- [Blue - which is least relevent][2]
- [Shades between red and blue - each having a decreasing weight]

