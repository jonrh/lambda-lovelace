//
//  PageViewController.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 6/29/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

struct PageVCStoryboardIdentifiers{
    static let contentViewControllerId = "ContentViewController"
}
class PageViewController: UIPageViewController {
    
    var contentVCs = [ContentViewController]()
    var tweets = [Tweet]()
    var pageCount:Int {
        return min(tweets.count, 20)
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        view.backgroundColor = UIColor.clearColor()
        delegate = self
        loadTweets()
    }

    private func initContentVCs(){
    }
    
    private func configurePageVC(){
        for i in 0..<pageCount{
            let contentVC = viewControllerOfIndex(i)
            contentVC.tweet = tweets[i]
            contentVCs.append(contentVC)
        }
        
        setViewControllers([contentVCs[0]], direction: .Forward, animated: true, completion: nil)
    }
    
    private func loadTweets(){
        APIManager.getHomeLineWithPage(1)
        {   result in
            let recommendedTweeets = result["recommended_tweets"]
            for (_, tweet) in recommendedTweeets {
                let tweetText = tweet["text"].stringValue
                let userName = tweet["user"]["name"].stringValue
                let userScreenName = tweet["user"]["screen_name"].stringValue
                let userImageUrl = tweet["user"]["profile_image_url_https"].stringValue
                let tweetDateTime = tweet["created_at"].stringValue
                var tweetImageUrl = ""
                if let items = tweet["entities"]["media"].array {
                    for item in items {
                        tweetImageUrl = item["media_url_https"].stringValue
                    }
                }
                let tweetObj = Tweet(tweet: tweetText, userName: userName,
                                     userDisplayName: userScreenName, userImageUrl: userImageUrl,
                                     tweetDateTime: tweetDateTime, tweetImageUrl: tweetImageUrl)
                self.tweets.append(tweetObj)
            }
            self.configurePageVC()
        }
    }

    func viewControllerOfIndex(index: Int) -> ContentViewController{
       let contentVC = storyboard?.instantiateViewControllerWithIdentifier(PageVCStoryboardIdentifiers.contentViewControllerId) as! ContentViewController
        return contentVC
    }
}

extension PageViewController: UIPageViewControllerDelegate{
    
}



