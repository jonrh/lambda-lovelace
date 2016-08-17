//
//  Tweet.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 14/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation
import SwiftyJSON

// this is custom object to represent subset data of origianl tweet JSON object, 
// because our app only require a small piece data

class Tweet : NSObject, NSCoding
{
    var id: String
    var tweet: String
    var userName: String
    var userDisplayName:String
    var userImageUrl: String
    var tweetImageUrl:String
    var tweetDateTime: String
    
    private static let dataFormatter = NSDateFormatter()
    
    init(id: String, tweet: String, userName: String, userDisplayName: String, userImageUrl:String, tweetDateTime:String, tweetImageUrl: String) {
        self.id = id
        self.tweet = tweet
        self.userName = userName
        self.userDisplayName = userDisplayName
        self.userImageUrl = userImageUrl
        self.tweetDateTime = Tweet.getReadableDate(tweetDateTime)
        self.tweetImageUrl = tweetImageUrl
    }
    
    required init?(coder aDecoder: NSCoder) {
        self.id = aDecoder.decodeObjectForKey("id") as! String
        self.tweet = aDecoder.decodeObjectForKey("tweet") as! String
        self.userName = aDecoder.decodeObjectForKey("userName") as! String
        self.userDisplayName = aDecoder.decodeObjectForKey("userDisplayName") as! String
        self.userImageUrl = aDecoder.decodeObjectForKey("userImageUrl") as! String
        self.tweetImageUrl = aDecoder.decodeObjectForKey("tweetImageUrl") as! String
        self.tweetDateTime = aDecoder.decodeObjectForKey("tweetDateTime") as! String
    }
    
    func encodeWithCoder(aCoder: NSCoder) {
        aCoder.encodeObject(id, forKey: "id")
        aCoder.encodeObject(tweet, forKey: "tweet")
        aCoder.encodeObject(userName, forKey: "userName")
        aCoder.encodeObject(userDisplayName, forKey: "userDisplayName")
        aCoder.encodeObject(tweetImageUrl, forKey: "tweetImageUrl")
        aCoder.encodeObject(userImageUrl, forKey: "userImageUrl")
        aCoder.encodeObject(tweetDateTime, forKey: "tweetDateTime")
    }
    
    convenience init (jsonTweet: JSON){
        let tweetId = jsonTweet["id_str"].stringValue
        
        let tweetText = jsonTweet["text"].stringValue
        let userName = jsonTweet["user"]["name"].stringValue
        let userScreenName = jsonTweet["user"]["screen_name"].stringValue
        let userImageUrl = jsonTweet["user"]["profile_image_url_https"].stringValue
        let tweetDateTime = jsonTweet["created_at"].stringValue
        var tweetImageUrl = ""
        if let items = jsonTweet["entities"]["media"].array {
            for item in items {
                tweetImageUrl = item["media_url_https"].stringValue
            }
        }
        self.init(id: tweetId, tweet: tweetText, userName: userName,
                             userDisplayName: userScreenName, userImageUrl: userImageUrl,
                             tweetDateTime: tweetDateTime, tweetImageUrl: tweetImageUrl)
    }
    
    // helper method to convert raw date to human readable format
    class private func getReadableDate(rawDate: String) -> String{
        dataFormatter.dateFormat = "EEE MMM dd HH:mm:ss Z yyyy"
        let tweetDate = dataFormatter.dateFromString(rawDate)
        dataFormatter.dateFormat = "HH:mm"
        
        var readableDate = ""
        if let date = tweetDate{
            readableDate = dataFormatter.stringFromDate(date)
        }
        return readableDate
    }
    
    
}
