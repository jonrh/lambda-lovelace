//
//  ViewController.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 18/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.

/***  
  This is controller class for the home screen that displays the filtered tweets
 ***/

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
            feedTableView.estimatedRowHeight = 300
        }
    }
    
    var tweetList = [Tweet]()
    var countList = [Int]()
    
    let feedTableViewRefreshControl = UIRefreshControl()
    
    private var feedPage = 1
    private var isLoadingNewPage = true
    
    var needReloadTable = true
    
    // call to get filtered tweets from the server
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        
        if needReloadTable == true {
            needReloadTable = false
            APIManager.apiDataRefreshDelegate = self
            initRefreshControl()
            if !APIManager.isRequestingOAuthToken{
                if APIManager.LoadLocalOAuthToken() {
                    refreshFeedTableView(true)
                }else{
                    performSegueWithIdentifier(FeedVCStoryboard.loginViewSegue, sender: self)
                }
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
    
    @objc private func refreshFeedTableView(reloadData: Bool = false){
        cleanTableView(reloadData)
        feedPage = 1
        loadTweetWithPage(feedPage)
    }
    
    func cleanTableView(reloadData: Bool = false){
        tweetList.removeAll()
        countList.removeAll()
        if reloadData == true {
            feedTableView.reloadData()
        }
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
        let tweetObj = tweetList[indexPath.row]
        let tweetCell:FeedTableViewCell
        if tweetObj.tweetImageUrl.isEmpty
        {
            
             tweetCell = tableView.dequeueReusableCellWithIdentifier("tweetPrototypeCell",
                                                                        forIndexPath: indexPath) as! FeedTableViewCell
        }
        else
        {
             tweetCell = tableView.dequeueReusableCellWithIdentifier("tweetImagePrototypeCell",
                                                                        forIndexPath: indexPath) as! FeedTableViewCell
        }
        
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
        // Setting up the left and right buttons on swipe of the tableview cell
        tweetCell.rightUtilityButtons = getRightSwipeButtonsToCell() as [AnyObject]
        tweetCell.leftUtilityButtons = getLeftSwipeButtonsToCell() as [AnyObject]
        tweetCell.delegate = self
        return tweetCell
    }
    
    //Navigate to web view when URL in the tweet is selected by the user
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
    
    //Set up the button image and name for the right swipe button
    func getRightSwipeButtonsToCell()-> NSMutableArray{
        let utilityButtons: NSMutableArray = NSMutableArray()
        utilityButtons.sw_addUtilityButtonWithColor(UIColor.clearColor(), icon: UIImage(named: "like icon"))
        return utilityButtons
    }
    //Set up the button image and name for the left swipe button
    func getLeftSwipeButtonsToCell()-> NSMutableArray{
        let utilityButtons: NSMutableArray = NSMutableArray()
        utilityButtons.sw_addUtilityButtonWithColor(UIColor.clearColor(), icon: UIImage(named: "dislike icon"))
        return utilityButtons
    }
    
    //Event when table cell is swiped right to open up the menu to give feedback about what they liked/disliked abou the tweet.
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
        let followerName = tweetCell.tweet!.userDisplayName
        let tweetContent = tweetCell.tweet!.tweet
        let likeForAuthorAction: UIAlertAction = UIAlertAction(title: "Like more from " + followerName, style: .Default)
        { action -> Void in
            self.postSingleTweetFeedbackToServer(followerName: followerName, feedback: "like", tweetContent: tweetContent, reason: "Author")
        }
        actionForLikeTweetController.addAction(likeForAuthorAction)
        // Like from this subject
        let likeForSubjectAction: UIAlertAction = UIAlertAction(title: "More of this Subject", style: .Default)
        { action -> Void in
            self.postSingleTweetFeedbackToServer(followerName: followerName, feedback: "like", tweetContent: tweetContent, reason: "Subject")
        }
    
        actionForLikeTweetController.addAction(likeForSubjectAction)
        actionForLikeTweetController.popoverPresentationController?.sourceView = cell as UIView
        
        //Present the AlertController
        self.presentViewController(actionForLikeTweetController, animated: true, completion: nil)
        cell.hideUtilityButtonsAnimated(true)
        
    }
    
    //Event when table cell is swiped left to open up the menu to give feedback about what they liked/disliked abou the tweet.
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
        let followerName = tweetCell.tweet!.userDisplayName
        let tweetContent = tweetCell.tweet!.tweet
        let dislikeForAuthorAction: UIAlertAction = UIAlertAction(title: "Like less from " + followerName, style: .Default)
        { action -> Void in
            
            self.postSingleTweetFeedbackToServer(followerName: followerName, feedback: "dislike", tweetContent: tweetContent, reason: "Author")
        }
        actionForDisLikeTweetController.addAction(dislikeForAuthorAction)
        // Like from this subject
        let dislikeForSubjectAction: UIAlertAction = UIAlertAction(title: "Less of this Subject", style: .Default)
        { action -> Void in
            self.postSingleTweetFeedbackToServer(followerName: followerName, feedback: "dislike", tweetContent: tweetContent, reason: "Subject")
            
        }
        
        actionForDisLikeTweetController.addAction(dislikeForSubjectAction)
        actionForDisLikeTweetController.popoverPresentationController?.sourceView = cell as UIView
        
        //Present the AlertController
        self.presentViewController(actionForDisLikeTweetController, animated: true, completion: nil)
        cell.hideUtilityButtonsAnimated(true)
    }
    
    //Network call to send feedback to the flask server.
    private func postSingleTweetFeedbackToServer(followerName followerName: String, feedback: String, tweetContent: String, reason: String){
        var feedbackParams = ["followerScreenName":followerName,
                              "feedback":feedback,
                              "reason"  :reason,
                              "tweetContent" : tweetContent
                              ]
        CurrentUserAccountInfo.getCurrentUser { currentUser in
            feedbackParams["user_name"] = currentUser.screenName
            APIManager.postSingleTweetFeedback(feedbackParams)
        }
    }
    
}

extension FeedViewController: APIDataRefreshDelegate {
    func apiDataRefresh() {
        refreshFeedTableView()
    }
}



