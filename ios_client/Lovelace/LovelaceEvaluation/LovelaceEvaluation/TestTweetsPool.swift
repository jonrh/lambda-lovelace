//
//  TestTweetsPool.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/25/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation

class TestTweetsPool {
    static var recommendTweets = [Tweet]()
    static var originalTweets = [Tweet]()
    static var mixedTweets = [Tweet]()
    static var mixedTweetsSource = [String]()
    
    
    class func initMixedTweets(){
        var usedRandom = [Int]()
        
        for mixedIndex in 0 ..< AppConstant.tweetContentViewCount {
            var random:Int
            
            repeat{
                random = Int(arc4random_uniform(UInt32(AppConstant.tweetContentViewCount)))
            } while(usedRandom.contains(random))
            usedRandom.append(random)
            
            if random < AppConstant.tweetContentViewCount / 2 {
                let recommendIndex = random
                mixedTweets.append(recommendTweets[recommendIndex])
                mixedTweetsSource.append("recommend")
            }
            else{
                let originalIndex = random - AppConstant.tweetContentViewCount / 2
                mixedTweets.append(originalTweets[originalIndex])
                mixedTweetsSource.append("original")
            }
        }
        print(usedRandom)
    }
    
    class func removeAll(){
        recommendTweets.removeAll()
        originalTweets.removeAll()
        mixedTweets.removeAll()
        mixedTweetsSource.removeAll()
    }
}