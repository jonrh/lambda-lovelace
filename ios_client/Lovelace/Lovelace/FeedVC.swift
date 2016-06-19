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


class FeedViewController: UIViewController  {
    
    @IBOutlet weak var feedTableView: UITableView! {
        didSet{
            feedTableView.allowsSelection = false
        }
    }
    
    var tweetList = [Tweet]()
    
    let feedTableViewRefreshControl = UIRefreshControl()
    
    override func viewDidLoad() {
        super.viewDidLoad()
    
        initRefreshControl()
    }
    
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        
        
        if APIManager.hasOAuthToken {
            refreshFeedTableView()
        }
        else {
            if !APIManager.reqestingAccessToken {
                APIManager.initOAuthTokenAndSecret(viewControllerForOpeningWebView: self, dataRefreshDelegate: self)
            }
        }
    }
    
    private func initRefreshControl(){
        feedTableViewRefreshControl.addTarget(self, action:#selector(refreshFeedTableView) , forControlEvents: .ValueChanged)
        feedTableView.addSubview(feedTableViewRefreshControl)
    }
    
    
    @objc private func refreshFeedTableView(){
        APIManager.getHomeLine { homeLineTweets in
            for (_, tweet) in homeLineTweets {
                let tweetText = tweet["text"].stringValue
                let userName = tweet["user"]["name"].stringValue
                let userScreenName = tweet["user"]["screen_name"].stringValue
                let userImageUrl = tweet["user"]["profile_image_url_https"].stringValue
                let tweetDateTime = tweet["created_at"].stringValue
                let tweetImageUrl = tweet["media"]["media_url_https"].stringValue
                let tweetObj = Tweet(tweet: tweetText, userName: userName, userDisplayName: userScreenName, userImageUrl: userImageUrl, tweetDateTime: tweetDateTime, tweetImageUrl: tweetImageUrl)
                self.tweetList.append(tweetObj)
                print( tweet["text"] )
            }
            self.feedTableView.reloadData()
            self.feedTableViewRefreshControl.endRefreshing()
            
        }
    }
    
}

extension FeedViewController: APIDataRefreshDelegate {
    func apiDataRefresh(){
        refreshFeedTableView()
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
        let tweetCell = tableView.dequeueReusableCellWithIdentifier("tweetPrototypeCell", forIndexPath: indexPath) as! FeedTableViewCell
        
        // Even if the prototype cell has not visible label in designer, it has the textLabel label by default
        
        tweetCell.tweetUserName.text = tweetList[indexPath.row].userName
        tweetCell.tweetText.text = tweetList[indexPath.row].tweet
        tweetCell.tweetUserDisplayName.text = tweetList[indexPath.row].userDisplayName
        tweetCell.tweetDateTime.text = tweetList[indexPath.row].tweetDateTime
        if let url = NSURL(string: tweetList[indexPath.row].userImageUrl) {
            let qos = Int(QOS_CLASS_USER_INITIATED.rawValue)
            dispatch_async(dispatch_get_global_queue(qos,0)) { () -> Void in
                if let avatar = NSData(contentsOfURL: url) {
                    dispatch_async(dispatch_get_main_queue()) { () -> Void in
                        tweetCell.tweetUserImage?.image = UIImage(data: avatar)
                    }
                }
            }
        }
        return tweetCell
    }
    
}





