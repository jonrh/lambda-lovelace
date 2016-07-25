//
//  Tweet.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 14/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation
import SwiftyJSON

public class Tweet
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
        self.userDisplayName = "@" + userDisplayName
        self.userImageUrl = userImageUrl
        self.tweetDateTime = Tweet.getReadableDate(tweetDateTime)
        self.tweetImageUrl = tweetImageUrl
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
