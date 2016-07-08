//
//  PageViewController.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 6/29/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

enum ContentViewControllerType:String {
    case textAndImage = "ContentViewControllerWithImage"
    case textOnly = "ContentViewControllerWithoutImage"
}

struct PageStoryboard {
    static let resultTableId = "ResultTableViewController"
}

protocol PageNumberDataSource {
    var pageNumber: Int {get set}
}


protocol PageViewControllerDataSource:class{
    var pageNumberOfCurrentPageView:Int {get}
}

extension PageViewController: PageViewControllerDataSource {
    var pageNumberOfCurrentPageView:Int {
        let currentVC = viewControllers![0] as! PageNumberDataSource
        return currentVC.pageNumber
    }
}

class PageViewController: UIPageViewController {
    
    var contentVCs = [ContentViewController]()
    var resultTableVC = ResultContentViewController()
    var tweets = [Tweet]()
    
    var parentVC:ParentViewController{
        return parentViewController as! ParentViewController
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        delegate = self
        dataSource = self
        if  APIManager.LoadLocalOAuthToken() {
            initTestData()
        }
    }
    
    
    private func configurePageVC(){
        for i in 0 ..< AppConstant.tweetContentViewCount{
            let hasImage = tweets[i].tweetImageUrl != ""
            let contentViewType:ContentViewControllerType = hasImage ? .textAndImage : .textOnly
            let contentVC = viewControllerOfIndex(i, contentViewType: contentViewType)
            contentVC.tweet = tweets[i]
            contentVCs.append(contentVC)
        }
        
        resultTableVC = storyboard?.instantiateViewControllerWithIdentifier(PageStoryboard.resultTableId) as! ResultContentViewController
        resultTableVC.pageNumber = AppConstant.totalPageViewCount - 1
        resultTableVC.tweets = tweets
        setViewControllers([contentVCs[0]], direction: .Forward, animated: false, completion: nil)
    }
    
    func initTestData(){
        tweets.removeAll()
        EvaluationResult.cleanAllResult()
        contentVCs.removeAll()
        
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
            print("load tweets successfully")
            self.configurePageVC()
            self.parentVC.hideViewsAtStartup(false)
            self.parentVC.updatePageNumberView()
        }
    }
    
    func viewControllerOfIndex(index: Int, contentViewType: ContentViewControllerType) -> ContentViewController{
        let contentVC = storyboard?.instantiateViewControllerWithIdentifier(contentViewType.rawValue) as! ContentViewController
        contentVC.pageNumber = index
        return contentVC
    }
}

extension PageViewController:APIDataRefreshDelegate{
    func apiDataRefresh(){
        initTestData()
    }
}

extension PageViewController: UIPageViewControllerDelegate{
    func pageViewController(pageViewController: UIPageViewController, didFinishAnimating finished: Bool, previousViewControllers: [UIViewController], transitionCompleted completed: Bool) {
        if completed {
            parentVC.updataeButtonsStates()
            parentVC.updatePageNumberView()
            switch pageNumberOfCurrentPageView {
            case AppConstant.totalPageViewCount - 1:
                parentVC.toggleLogoutSubmitButton()
                parentVC.toggleBottomComponents()
            case AppConstant.tweetContentViewCount - 1:
                let previousVC = previousViewControllers[0] as! PageNumberDataSource
                let previousPageNumber = previousVC.pageNumber
                if previousPageNumber == AppConstant.totalPageViewCount - 1{
                    parentVC.toggleLogoutSubmitButton()
                    parentVC.toggleBottomComponents()
                }
            default:
                break
            }
            
        }
    }
}

extension PageViewController: UIPageViewControllerDataSource{
    private func getPageNumberFromChildViewController(viewController: UIViewController) -> Int{
        let dataSource = viewController as! PageNumberDataSource
        return dataSource.pageNumber
    }
    
    func pageViewController(pageViewController: UIPageViewController, viewControllerBeforeViewController viewController: UIViewController) -> UIViewController? {
        let currentPageNumber = getPageNumberFromChildViewController(viewController)
        let beforePageNumber = currentPageNumber - 1
        if beforePageNumber >= 0 && beforePageNumber < AppConstant.tweetContentViewCount {
            return contentVCs[beforePageNumber]
        }
        return nil
    }
    func pageViewController(pageViewController: UIPageViewController, viewControllerAfterViewController viewController: UIViewController) -> UIViewController? {
        let currentPageNumber = getPageNumberFromChildViewController(viewController)
        let afterPageNumber = currentPageNumber + 1
        if afterPageNumber >= 0 && afterPageNumber < AppConstant.tweetContentViewCount {
            return contentVCs[afterPageNumber]
        }
        if afterPageNumber == AppConstant.totalPageViewCount - 1 {
            return resultTableVC
        }
        return nil
    }
    
}

