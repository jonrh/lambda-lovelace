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

class ViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    
    @IBOutlet weak var tweetsListTableView: UITableView!
    var tweetList = [Tweet]()
    override func viewDidLoad() {
        
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        
        APIManager.authorize(viewControllerForOpeningWebView: self)
        
        
    }
    
    @IBAction func getHomeTimeline(sender: AnyObject) {
        APIManager.getHomeLine { homeLineTweets in
            for (_, tweet) in homeLineTweets {
                let tweetText = tweet["text"].stringValue
                let userName = tweet["user"]["name"].stringValue
                let userScreenName = tweet["user"]["screen_name"].stringValue
                let userImageUrl = tweet["user"]["profile_image_url_https"].stringValue
                let tweetObj = Tweet(tweet: tweetText, userName: userName, userDisplayName: userScreenName, userImageUrl: userImageUrl)
                self.tweetList.append(tweetObj)
                print( tweet["text"] )
            }
            self.tweetsListTableView.reloadData()
            
        }
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) ->
        Int
    {
        return self.tweetList.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell
    {
        let tweetCell = tableView.dequeueReusableCellWithIdentifier("tweetPrototypeCell", forIndexPath: indexPath) as! TweetViewCell
        
        // Even if the prototype cell has not visible label in designer, it has the textLabel label by default
        
        tweetCell.tweetUserName.text = tweetList[indexPath.row].userName
        tweetCell.tweetText.text = tweetList[indexPath.row].tweet
        tweetCell.tweetUserDisplayName.text = tweetList[indexPath.row].userDisplayName
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

