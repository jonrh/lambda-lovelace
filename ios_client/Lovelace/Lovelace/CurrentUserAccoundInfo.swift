//
//  CurrentUserAccoundInfo.swift
//  Lovelace
//
//  Created by Junyang ma on 8/3/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation

class CurrentUserAccountInfo {
    private static var currentUser: CurrentUserAccountInfo!
    
    var userName: String!
    var screenName: String!
    var avatarImageData: NSData!
    var followingNumber: Int!
    var followerNumber: Int!
    
    init(userName: String, screenName: String, avatarImageData: NSData, followingNumber: Int, followerNumber: Int){
        self.userName = userName
        self.screenName = screenName
        self.avatarImageData = avatarImageData
        self.followingNumber = followingNumber
        self.followerNumber = followerNumber
    }
    
    class func removeCurrentUserLocalData(){
        let defaults = NSUserDefaults.standardUserDefaults()
        defaults.removeObjectForKey("userInfoAvailable")
        currentUser = nil
        
    }
    class func getCurrentUser(complete: (CurrentUserAccountInfo) -> Void) {
        if currentUser == nil {
            let defaults = NSUserDefaults.standardUserDefaults()
            if defaults.boolForKey("userInfoAvailable") {
                let userName = defaults.stringForKey("userName")!
                let screenName = defaults.stringForKey("screenName")!
                let avatarImageData = defaults.dataForKey("avatarImageData")!
                let followerNumber = defaults.integerForKey("followerNumber")
                let followingNumber = defaults.integerForKey("followingNumber")
                CurrentUserAccountInfo.currentUser = CurrentUserAccountInfo(userName: userName, screenName: screenName,avatarImageData: avatarImageData, followingNumber: followingNumber, followerNumber: followerNumber)
                complete(currentUser)
            }
            else {
                APIManager.getUserProfile { profileJson in
                    let userName = profileJson["name"].stringValue
                    let screenName = profileJson["screen_name"].stringValue
                    
                    let avatarUrlString = profileJson["profile_image_url_https"].stringValue
                    let avatarUrl = NSURL(string: avatarUrlString)!
                    let avatarImageData = NSData(contentsOfURL: avatarUrl)!
                    
                    let followingNumber = profileJson["friends_count"].intValue
                    let followerNumber = profileJson["followers_count"].intValue
                    
                    let defaults = NSUserDefaults.standardUserDefaults()
                    defaults.setBool(true, forKey: "userInfoAvailable")
                    defaults.setObject(userName, forKey: "userName")
                    defaults.setObject(screenName, forKey: "screenName")
                    defaults.setObject(avatarImageData, forKey: "avatarImageData")
                    defaults.setInteger(followerNumber, forKey: "followerNumber")
                    defaults.setInteger(followingNumber, forKey: "followingNumber")
                    
                    currentUser = CurrentUserAccountInfo(userName: userName, screenName: screenName,avatarImageData: avatarImageData, followingNumber: followingNumber, followerNumber: followerNumber)
                    complete(currentUser)
                }
            }
            
        }
        else {
            complete(currentUser)
        }
    }
    
    
}