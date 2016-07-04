//
//  PageViewController.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 6/29/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

struct PageVCStoryboard{
    static let contentViewControllerWithImageId = "ContentViewControllerWithImage"
    static let contentViewControllerWithoutImageId = "ContentViewControllerWithoutImage"
}
class PageViewController: UIPageViewController {
    
    var contentVCs = [ContentViewController]()
    var tweets = [Tweet]()
    var results = [ButtonsIdentifiers?](count: 20, repeatedValue: nil)
    var pageCount:Int {
        return min(tweets.count, 20)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        
        delegate = self
        dataSource = self
        loadTweets()
    }

    private func hideOtherViewsInParentView(hidden: Bool){
        let parentVC = parentViewController as! ParentViewController
        parentVC.setOtherViewsHidden(hidden)
    }
    
    
    private func configurePageVC(){
        for i in 0..<pageCount{
            let hasImage = tweets[i].tweetImageUrl != ""
            let contentVC = viewControllerOfIndex(i, hasImage: hasImage)
            contentVC.tweet = tweets[i]
            contentVCs.append(contentVC)
        }
        
        setViewControllers([contentVCs[0]], direction: .Forward, animated: false, completion: nil)
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
            self.hideOtherViewsInParentView(false)
            self.configurePageVC()
            
        }
    }

    func viewControllerOfIndex(index: Int, hasImage: Bool) -> ContentViewController{
        let VCIdentifier = hasImage == true ? PageVCStoryboard.contentViewControllerWithImageId :
                                             PageVCStoryboard.contentViewControllerWithoutImageId
        
       let contentVC = storyboard?.instantiateViewControllerWithIdentifier(VCIdentifier) as! ContentViewController
        contentVC.pageNumber = index
        return contentVC
    }
}

extension PageViewController: UIPageViewControllerDelegate{
}

extension PageViewController: UIPageViewControllerDataSource{
    private func indexOfContentVC(viewController: UIViewController) -> Int{
        let contentViewController = viewController as! ContentViewController
        return contentViewController.pageNumber
    }
    
    func pageViewController(pageViewController: UIPageViewController, viewControllerBeforeViewController viewController: UIViewController) -> UIViewController? {
        let currentPageNumber = indexOfContentVC(viewController)
        let beforePageNumber = currentPageNumber - 1
        if beforePageNumber >= 0 && beforePageNumber < pageCount {
            return contentVCs[beforePageNumber]
        }
        return nil
    }
    func pageViewController(pageViewController: UIPageViewController, viewControllerAfterViewController viewController: UIViewController) -> UIViewController? {
        let currentPageNumber = indexOfContentVC(viewController)
        let afterPageNumber = currentPageNumber + 1
        if afterPageNumber >= 0 && afterPageNumber < pageCount {
            return contentVCs[afterPageNumber]
        }
        return nil
    }
    
    func presentationIndexForPageViewController(pageViewController: UIPageViewController) -> Int {
        return 0
    }
    
    func presentationCountForPageViewController(pageViewController: UIPageViewController) -> Int {
        return pageCount
    }
    
}

extension PageViewController: ParentViewDelegate {
    func decisionButtonPressed(buttonId: ButtonsIdentifiers ){
        let currentVC = viewControllers![0] as! ContentViewController
        let currentPageNumber = currentVC.pageNumber
        results[currentPageNumber] = buttonId
    }
}