//
//  ViewController.swift
//  Lovelace
//
//  Created by Junyang ma on 6/7/16.
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
                let tweetObj = Tweet(tweet: tweetText, userName: userName)
                self.tweetList.append(tweetObj)
                print( tweet["text"] )
            }
            self.tweetsListTableView.reloadData()
        }
        //dispatch_async(dispatch_get_main_queue()){
        
            
       // }
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) ->
        Int
    {
        return self.tweetList.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell
    {
        let tweetCell = tableView.dequeueReusableCellWithIdentifier("tweetPrototypeCell", forIndexPath: indexPath)
        
        // Even if the prototype cell has not visible label in designer, it has the textLabel label by default
        tweetCell.textLabel?.text = tweetList[indexPath.row].userName
        tweetCell.detailTextLabel?.text = tweetList[indexPath.row].tweet
        
        return tweetCell
    }
    
    
}

