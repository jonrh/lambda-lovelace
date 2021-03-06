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
    
    var parentVC:ParentViewController{
        return parentViewController as! ParentViewController
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
    }
    
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        delegate = self
        dataSource = self
        if  APIManager.LoadLocalOAuthToken() {
            initTestData()
        }
    }
    
    
    // configure page contemts
    private func configurePageVC(){
        for i in 0 ..< AppConstant.tweetContentViewCount{
            let hasImage = TestTweetsPool.mixedTweets[i].tweetImageUrl != ""
            let contentViewType:ContentViewControllerType = hasImage ? .textAndImage : .textOnly
            let contentVC = viewControllerOfIndex(i, contentViewType: contentViewType)
            contentVC.tweet = TestTweetsPool.mixedTweets[i]
            contentVCs.append(contentVC)
        }
        
        resultTableVC = storyboard?.instantiateViewControllerWithIdentifier(PageStoryboard.resultTableId) as! ResultContentViewController
        resultTableVC.pageNumber = AppConstant.totalPageViewCount - 1
        resultTableVC.tweets = TestTweetsPool.mixedTweets
        setViewControllers([contentVCs[0]], direction: .Reverse , animated: true, completion: nil)
    }
    
    // generate test data
    func initTestData(){
        TestTweetsPool.removePreviousTestTweetsSet()
        EvaluationResult.removeAll()
        contentVCs.removeAll()
        
        TestTweetsPool.initTestTweetsPool {
            self.configurePageVC()
            self.parentVC.hideViewsAtStartup(false)
            self.parentVC.updatePageNumberView()
            self.parentVC.refreshProgressView()
            self.parentVC.toggleLogoutSubmitButton()
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
    // invoked when user change page where ui eleements are updated based on current page number
    func pageViewController(pageViewController: UIPageViewController, didFinishAnimating finished: Bool, previousViewControllers: [UIViewController], transitionCompleted completed: Bool) {
        if completed {
            parentVC.updataeButtonsStates()
            parentVC.updatePageNumberView()
            switch pageNumberOfCurrentPageView {
            case AppConstant.totalPageViewCount - 1:
                parentVC.toggleLogoutSubmitButton()
                parentVC.toggleBottomComponents(moveDown: true)
            case AppConstant.tweetContentViewCount - 1:
                let previousVC = previousViewControllers[0] as! PageNumberDataSource
                let previousPageNumber = previousVC.pageNumber
                if previousPageNumber == AppConstant.totalPageViewCount - 1{
                    parentVC.toggleLogoutSubmitButton()
                    parentVC.toggleBottomComponents(moveDown: false)
                }
            default:
                break
            }
            
        }
    }
}

// feed page content
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

