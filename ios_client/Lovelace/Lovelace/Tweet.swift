//
//  Tweet.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 14/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation

public class Tweet
{
    var tweet: String
    var userName: String
    var userDisplayName:String
    var userImageUrl: String
    var tweetImageUrl:String
    var tweetDateTime: String
    
    private static let dataFormatter = NSDateFormatter()
    
    init(tweet: String, userName: String, userDisplayName: String, userImageUrl:String, tweetDateTime:String, tweetImageUrl: String) {
        self.tweet = tweet
        self.userName = userName
        self.userDisplayName = userDisplayName
        self.userImageUrl = userImageUrl
        self.tweetDateTime = Tweet.getReadableDate(tweetDateTime)
        self.tweetImageUrl = tweetImageUrl
    }
    
    class private func getReadableDate(rawDate: String) -> String{
        dataFormatter.dateFormat = "EEE MMM dd HH:mm:ss Z yyyy"
        let tweetDate = dataFormatter.dateFromString(rawDate)
        dataFormatter.dateFormat = "HH:SS"
        
        var readableDate = ""
        if let date = tweetDate{
            readableDate = dataFormatter.stringFromDate(date)
        }
        return readableDate
    }
    
}
