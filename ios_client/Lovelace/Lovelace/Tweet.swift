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
    
    init(tweet: String, userName: String, userDisplayName: String, userImageUrl:String, tweetDateTime:String, tweetImageUrl: String) {
        self.tweet = tweet
        self.userName = userName
        self.userDisplayName = userDisplayName
        self.userImageUrl = userImageUrl
        self.tweetDateTime = tweetDateTime
        self.tweetImageUrl = tweetImageUrl
    }
    
}
