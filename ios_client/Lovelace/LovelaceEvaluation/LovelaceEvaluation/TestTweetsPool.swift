//
//  TestTweetsPool.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/25/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation

struct TestTweetsDataKeys{
    static let recommendTweetsList = "recommendTweetsList"
    static let originalTweetsList = "originalTweetsList"
    static let recommmendTweetsIndex = "recommmendTweetsIndex"
    static let originalTweetsIndex = "originalTweetsIndex"
    static let localDataAvailable = "localDataAvailable"
}

class TestTweetsPool {
    static var recommendTweets = [Tweet]()
    static var originalTweets = [Tweet]()
    static var mixedTweets = [Tweet]()
    static var mixedTweetsSource = [String]()
    static var recommendTweetsIndex = 0
    static var originalTweetsIndex = 0
    
    
    class func generateNewMixedTweetsList(){
        var usedRandom = [Int]()
        
        for _ in 0 ..< AppConstant.tweetContentViewCount {
            var random:Int
            
            repeat{
                random = Int(arc4random_uniform(UInt32(AppConstant.tweetContentViewCount)))
            } while(usedRandom.contains(random))
            usedRandom.append(random)
            
            if random < AppConstant.tweetContentViewCount / 2 {
                mixedTweets.append(recommendTweets[recommendTweetsIndex])
                recommendTweetsIndex += 1
                mixedTweetsSource.append("recommend")
            }
            else{
                mixedTweets.append(originalTweets[originalTweetsIndex])
                originalTweetsIndex += 1
                mixedTweetsSource.append("original")
            }
        }
        print("recommend count: \(recommendTweets.count)")
        print("original count: \(originalTweets.count)")
        print("recommend index: \(recommendTweetsIndex)")
        print("original  index: \(originalTweetsIndex)")
        saveTweetsIndexLocally()
    }
    
    class func initTestTweetsPool(callback : () -> Void){
        
        if recommendTweets.count == 0 {
            if loadLocalData() {
                generateNewMixedTweetsList()
                callback()
            }
            else {
                APIManager.getEvaluationDataWithPage(1)
                {   result in
                    let recommendTweetsJson = result["recommend_tweets"]
                    for (_, tweet) in recommendTweetsJson {
                        let tweetObj = Tweet(jsonTweet: tweet)
                        recommendTweets.append(tweetObj)
                    }
                    let originalTweetsJson = result["original_tweets"]
                    for (_, tweet) in originalTweetsJson {
                        let tweetObj = Tweet(jsonTweet: tweet)
                        originalTweets.append(tweetObj)
                    }
                    
                    saveTweetsListLocally()
                    generateNewMixedTweetsList()
                    callback()
                }
            }
        }
        else {
            generateNewMixedTweetsList()
            callback()
        }
    }
    
    class func loadLocalData() -> Bool{
        let defaults = NSUserDefaults.standardUserDefaults()
        if defaults.boolForKey(TestTweetsDataKeys.localDataAvailable) {
            let recommendTweetsData = defaults.objectForKey(TestTweetsDataKeys.recommendTweetsList) as! NSData
            recommendTweets = NSKeyedUnarchiver.unarchiveObjectWithData(recommendTweetsData) as! [Tweet]
            let originalTweetsData = defaults.objectForKey(TestTweetsDataKeys.originalTweetsList) as! NSData
            originalTweets = NSKeyedUnarchiver.unarchiveObjectWithData(originalTweetsData) as! [Tweet]
            recommendTweetsIndex = defaults.integerForKey(TestTweetsDataKeys.recommmendTweetsIndex)
            originalTweetsIndex = defaults.integerForKey(TestTweetsDataKeys.originalTweetsIndex)
            return true
        }
        else{
            return false
        }
    }
    
    class func cleanLocalData(){
        let defaults = NSUserDefaults.standardUserDefaults()
        defaults.removeObjectForKey(TestTweetsDataKeys.recommendTweetsList)
        defaults.removeObjectForKey(TestTweetsDataKeys.originalTweetsList)
        defaults.removeObjectForKey(TestTweetsDataKeys.recommmendTweetsIndex)
        defaults.removeObjectForKey(TestTweetsDataKeys.originalTweetsIndex)
        defaults.removeObjectForKey(TestTweetsDataKeys.localDataAvailable)
        
    }
    
    class func saveTweetsListLocally(){
        let defaults = NSUserDefaults.standardUserDefaults()
        defaults.setObject(NSKeyedArchiver.archivedDataWithRootObject(recommendTweets), forKey: TestTweetsDataKeys.recommendTweetsList)
        defaults.setObject(NSKeyedArchiver.archivedDataWithRootObject(originalTweets), forKey: TestTweetsDataKeys.originalTweetsList)
        defaults.setBool(true, forKey: TestTweetsDataKeys.localDataAvailable)
    }
    
    class func saveTweetsIndexLocally(){
        let defaults = NSUserDefaults.standardUserDefaults()
        defaults.setInteger(recommendTweetsIndex, forKey: TestTweetsDataKeys.recommmendTweetsIndex)
        defaults.setInteger(originalTweetsIndex, forKey: TestTweetsDataKeys.originalTweetsIndex)
    }
    
    
    class func removePreviousTestTweetsSet(){
        mixedTweets.removeAll()
        mixedTweetsSource.removeAll()
    }
    
}