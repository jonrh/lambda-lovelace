//
//  ViewController.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 18/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

struct FeedTableViewConstants {
    static let numberOfItemsLeftTriggerLoadNewPage = 5
}


class FeedViewController: UIViewController  {
    

    @IBOutlet weak var feedTableView: UITableView! 
    
    var tweetList = [Tweet]()
    var countList = [Int]()
    
    let feedTableViewRefreshControl = UIRefreshControl()
    
    private var feedPage = 1
    private var isLoadingNewPage = true
    
    override func viewDidLoad() {
        super.viewDidLoad()
    
        APIManager.apiDataRefreshDelegate = self
        initRefreshControl()
        if !APIManager.isRequestingOAuthToken {
            refreshFeedTableView()
        }
    }
    
    private func initRefreshControl(){
        feedTableViewRefreshControl.addTarget(self, action:#selector(refreshFeedTableView) ,
                                              forControlEvents: .ValueChanged)
        feedTableView.addSubview(feedTableViewRefreshControl)
        self.feedTableViewRefreshControl.beginRefreshing()
    }
    
    
    private func loadTweetWithPage(page: Int = 1){
        APIManager.getHomeLineWithPage(page)
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
                self.tweetList.append(tweetObj)
            }
            
            for (_,count) in result["counts"]{
                self.countList.append(count.intValue)
            }
            
            self.feedTableView.reloadData()
            self.feedTableViewRefreshControl.endRefreshing()
            self.isLoadingNewPage = false
        }
    }
    
    @objc private func refreshFeedTableView(){
        tweetList.removeAll()
        countList.removeAll()
        feedPage = 1
        loadTweetWithPage(feedPage)
    }
    
    @IBAction func removeLocalOAuthTokenButtonPressed(sender: UIBarButtonItem) {
        let defaults = NSUserDefaults.standardUserDefaults()
        defaults.removeObjectForKey( NSUserDefaultKeys.oauthTokenKey)
        defaults.removeObjectForKey( NSUserDefaultKeys.oauthTokenSecretKey)
        
        let alertVC = UIAlertController(title: "Remove Token", message: "You have removed Twitter access token.", preferredStyle: .Alert)
        let alertAction = UIAlertAction(title: "OK", style: .Default, handler: nil)
        alertVC.addAction(alertAction)
        presentViewController(alertVC, animated: true, completion: nil)
    }
}


extension FeedViewController: UITableViewDataSource, UITableViewDelegate {
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) ->
        Int
    {
        return self.tweetList.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell
    {
        let tweetCell = tableView.dequeueReusableCellWithIdentifier("tweetPrototypeCell",
                                                                    forIndexPath: indexPath) as! FeedTableViewCell
        
        
        tweetCell.weight = countList[indexPath.row]
        tweetCell.tweet = tweetList[indexPath.row]
        
        
        if !isLoadingNewPage {
            let numberOfItemLeft = tweetList.count - indexPath.row
            if numberOfItemLeft < FeedTableViewConstants.numberOfItemsLeftTriggerLoadNewPage {
                feedPage += 1
                isLoadingNewPage = true
                loadTweetWithPage(feedPage)
            }
        }
        
        return tweetCell
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if let tweet = sender as? FeedTableViewCell
        {
            let tweetDetailTVC = segue.destinationViewController as? TweetDetailVC
            tweetDetailTVC?.tweetObj = tweet.tweet
        }
    }
    
}

extension FeedViewController: APIDataRefreshDelegate {
    func apiDataRefresh() {
        refreshFeedTableView()
    }
}



