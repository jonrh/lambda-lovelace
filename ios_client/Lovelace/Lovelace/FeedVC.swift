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
import SWTableViewCell
import Rollbar

struct FeedTableViewConstants {
    static let numberOfItemsLeftTriggerLoadNewPage = 5
}

struct FeedVCStoryboard{
    static let loginViewSegue = "login"
}

class FeedViewController: UIViewController {
    
    var isURLorHashtagSelected = false
    @IBOutlet weak var feedTableView: UITableView! {
        didSet{
            feedTableView.rowHeight = UITableViewAutomaticDimension
            feedTableView.estimatedRowHeight = 100
        }
    }
    
    var tweetList = [Tweet]()
    var countList = [Int]()
    
    let feedTableViewRefreshControl = UIRefreshControl()
    
    private var feedPage = 1
    private var isLoadingNewPage = true
    
    override func viewDidLoad() {
        super.viewDidLoad()
    
        APIManager.apiDataRefreshDelegate = self
        initRefreshControl()
        if !APIManager.isRequestingOAuthToken{
            if APIManager.LoadLocalOAuthToken() {
                refreshFeedTableView()
            }else{
                performSegueWithIdentifier(FeedVCStoryboard.loginViewSegue, sender: self)
            }
        }
    }
    
    private func initRefreshControl(){
        feedTableViewRefreshControl.addTarget(self, action:#selector(refreshFeedTableView) ,
                                              forControlEvents: .ValueChanged)
        feedTableView.addSubview(feedTableViewRefreshControl)
        self.feedTableViewRefreshControl.beginRefreshing()
    }
    
    
    private func loadTweetWithPage(page: Int = 1){
        APIManager.getRecommendTweetsWithPage(page)
        {   result in
            let recommendedTweeets = result["recommended_tweets"]
            for (_, tweetJson) in recommendedTweeets {
                let tweetObj = Tweet(jsonTweet: tweetJson)
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
        Rollbar.infoWithMessage("user pull to refresh tweets")
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


extension FeedViewController: UITableViewDataSource, UITableViewDelegate , SWTableViewCellDelegate{
    
    
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
        
        // Attach a block to be called when the user taps a user handle
        tweetCell.tweetText.userHandleLinkTapHandler = { label, handle, range in
            print("User handle \(handle) tapped")
            self.isURLorHashtagSelected = true
        }
        
        // Attach a block to be called when the user taps a hashtag
        tweetCell.tweetText.hashtagLinkTapHandler = { label, hashtag, range in
            print("Hashtah \(hashtag) tapped")
            self.isURLorHashtagSelected = true
        }
        
        // Attach a block to be called when the user taps a URL
        tweetCell.tweetText.urlLinkTapHandler = { label, url, range in
            print("URL \(url) tapped")
            self.isURLorHashtagSelected = true
            self.prepareToURLWebViewSegue(url)
        }
        
        if !isLoadingNewPage {
            let numberOfItemLeft = tweetList.count - indexPath.row
            if numberOfItemLeft < FeedTableViewConstants.numberOfItemsLeftTriggerLoadNewPage {
                feedPage += 1
                isLoadingNewPage = true
                loadTweetWithPage(feedPage)
            }
        }
        tweetCell.rightUtilityButtons = getRightSwipeButtonsToCell() as [AnyObject]
        tweetCell.leftUtilityButtons = getLeftSwipeButtonsToCell() as [AnyObject]
        tweetCell.delegate = self
        return tweetCell
    }
    
    func prepareToURLWebViewSegue(url:String)
    {
        performSegueWithIdentifier("webViewSegue", sender: url)
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if let tweet = sender as? FeedTableViewCell
        {
            let tweetDetailTVC = segue.destinationViewController as? TweetDetailVC
            tweetDetailTVC?.tweetObj = tweet.tweet
        }
        else if let url = sender as? String
        {
            let webViewVC = segue.destinationViewController as? URLWebViewController
            webViewVC?.urlString = url
        }
    }

    
    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        if (!isURLorHashtagSelected)
        {
            let tweetCell = tableView.cellForRowAtIndexPath(indexPath)
            performSegueWithIdentifier("tweetDetailSegue", sender: tweetCell)
        }
        isURLorHashtagSelected = false
    }
    
    func getRightSwipeButtonsToCell()-> NSMutableArray{
        let utilityButtons: NSMutableArray = NSMutableArray()
        utilityButtons.sw_addUtilityButtonWithColor(UIColor.redColor(), title: NSLocalizedString("Like", comment: ""))
        return utilityButtons
    }
    
    func getLeftSwipeButtonsToCell()-> NSMutableArray{
        let utilityButtons: NSMutableArray = NSMutableArray()
        utilityButtons.sw_addUtilityButtonWithColor(UIColor.blueColor(), title: NSLocalizedString("Dislike", comment: ""))
        return utilityButtons
    }
    
    func swipeableTableViewCell(cell: SWTableViewCell!, didTriggerRightUtilityButtonWithIndex index: Int) {
        
        let index = self.feedTableView.indexPathForCell(cell)
        let tweetCell = self.feedTableView.cellForRowAtIndexPath(index!) as! FeedTableViewCell
        let actionForLikeTweetController: UIAlertController = UIAlertController()
        //Create and add the Cancel action
        let cancelAction: UIAlertAction = UIAlertAction(title: "Cancel", style: .Cancel) { action -> Void in
            //Just dismiss the action sheet
        }
        actionForLikeTweetController.addAction(cancelAction)
        //Like from tweet author option
        let likeForAuthorAction: UIAlertAction = UIAlertAction(title: "Like more from " + (tweetCell.tweet?.userName)!, style: .Default)
        { action -> Void in
            
            //To-do
        }
        actionForLikeTweetController.addAction(likeForAuthorAction)
        // Like from this subject
        let likeForSubjectAction: UIAlertAction = UIAlertAction(title: "More of this Subject", style: .Default)
        { action -> Void in
            
            //To -do
            
        }
    
        actionForLikeTweetController.addAction(likeForSubjectAction)
        actionForLikeTweetController.popoverPresentationController?.sourceView = cell as UIView
        
        //Present the AlertController
        self.presentViewController(actionForLikeTweetController, animated: true, completion: nil)
        
    }
    
    func swipeableTableViewCell(cell: SWTableViewCell!, didTriggerLeftUtilityButtonWithIndex index: Int) {
        let index = self.feedTableView.indexPathForCell(cell)
        let tweetCell = self.feedTableView.cellForRowAtIndexPath(index!) as! FeedTableViewCell
        let actionForDisLikeTweetController: UIAlertController = UIAlertController()
        //Create and add the Cancel action
        let cancelAction: UIAlertAction = UIAlertAction(title: "Cancel", style: .Cancel) { action -> Void in
            //Just dismiss the action sheet
        }
        actionForDisLikeTweetController.addAction(cancelAction)
        //Like from tweet author option
        let dislikeForAuthorAction: UIAlertAction = UIAlertAction(title: "Like less from " + (tweetCell.tweet?.userName)!, style: .Default)
        { action -> Void in
            
            //To-do
        }
        actionForDisLikeTweetController.addAction(dislikeForAuthorAction)
        // Like from this subject
        let dislikeForSubjectAction: UIAlertAction = UIAlertAction(title: "Very old tweet", style: .Default)
        { action -> Void in
            
            //To -do
            
        }
        
        actionForDisLikeTweetController.addAction(dislikeForSubjectAction)
        actionForDisLikeTweetController.popoverPresentationController?.sourceView = cell as UIView
        
        //Present the AlertController
        self.presentViewController(actionForDisLikeTweetController, animated: true, completion: nil)
    }
    
}

extension FeedViewController: APIDataRefreshDelegate {
    func apiDataRefresh() {
        refreshFeedTableView()
    }
}



