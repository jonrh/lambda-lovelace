//
//  ViewController.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 6/29/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

struct ParentVCStoryboard{
    static let pageViewSegue = "PageViewSegue"
    static let loginViewSegue = "login"
}

enum ButtonsIdentifier:Int{
    case like = 0
    case neither = 1
    case dislike = 2
}


class ParentViewController: UIViewController {
    
    @IBOutlet weak var topComponentView: UIStackView!
    @IBOutlet weak var bottomComponentView: UIStackView!
    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!
    private weak var pageVCDataSource: PageViewControllerDataSource!
    @IBOutlet weak var likeButton: UIButton!
    @IBOutlet weak var neitherButton: UIButton!
    @IBOutlet weak var dislikeButton: UIButton!
    @IBOutlet weak var progressView: EvaluationProgressView!
    @IBOutlet weak var pageNumberLabel: UILabel!
    @IBOutlet weak var containerView: UIView! {
        didSet{
            containerView.layer.shadowColor = UIColor.blackColor().CGColor
            containerView.layer.shadowOffset = CGSize(width: 0, height: 1)
            containerView.layer.shadowOpacity = 0.7
            containerView.layer.shadowRadius = 6
        }
    }
    
    @IBOutlet weak var logoutSubmitButton: UIButton! {
        didSet{
            logoutSubmitButton.layer.shadowColor = UIColor.blackColor().CGColor
            logoutSubmitButton.layer.shadowOffset = CGSizeMake(0, 1)
            logoutSubmitButton.layer.shadowOpacity = 0.5
            logoutSubmitButton.layer.shadowRadius = 3
        }
    }
    
    @IBOutlet weak var pageNumberBackgroundImageView: UIImageView!{
        didSet{
            pageNumberBackgroundImageView.layer.shadowColor = UIColor.blackColor().CGColor
            pageNumberBackgroundImageView.layer.shadowOffset = CGSizeMake(0, 1)
            pageNumberBackgroundImageView.layer.shadowOpacity = 0.5
            pageNumberBackgroundImageView.layer.shadowRadius = 3
        }
    }
    var isSubmitted = false
    
    var currentPageNumber:Int {
        return pageVCDataSource.pageNumberOfCurrentPageView
    }
    
    private var buttons: [UIButton]{
        return [likeButton,neitherButton,dislikeButton]
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        restoreAllButtonsToDefaultState()
        hideViewsAtStartup(true)
        
    }
    
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        if !(APIManager.isRequestingOAuthToken || APIManager.LoadLocalOAuthToken()) {
            performSegueWithIdentifier(ParentVCStoryboard.loginViewSegue, sender: self)
        }
    }
    
    
    func hideViewsAtStartup(hide: Bool){
        UIView.animateWithDuration(0.8, delay: 0, options: .CurveEaseInOut, animations: {
            self.containerView.alpha = hide ? 0 : 1
            self.topComponentView.alpha = hide ? 0 : 1
            self.bottomComponentView.alpha = hide ? 0 : 1
            }, completion: nil)
        if hide {
            activityIndicator.startAnimating()
        }
        else {
            activityIndicator.stopAnimating()
        }
    }
    
    func toggleBottomComponents(){
        let isResultPage = currentPageNumber == AppConstant.totalPageViewCount - 1
        let bottomHeight = bottomComponentView.bounds.height
        let bottomMargin = view.bounds.width / 7 / 2
        
        UIView.animateWithDuration(1, delay: 0, usingSpringWithDamping: 0.5, initialSpringVelocity: 0.5, options: .BeginFromCurrentState, animations: {
            self.bottomComponentView.center.y += isResultPage ? bottomHeight : -bottomHeight
            }, completion: nil)
        UIView.animateWithDuration(0.6, delay: 0, options: .CurveEaseInOut, animations: {
            self.containerView.frame.size.height += ( isResultPage ? 1 : -1 ) * ( bottomHeight - bottomMargin )
            }, completion: nil)
    }
    
    func toggleLogoutSubmitButton(){
        let isResultPage = currentPageNumber == AppConstant.totalPageViewCount - 1
        let scaleRatio:CGFloat = CGFloat(AppConstant.loginSubmitButtonScaleRatio)
        
        UIView.animateWithDuration(0.2,delay: 0,options: .CurveEaseInOut,animations: { _ in
            self.logoutSubmitButton.transform = CGAffineTransformMakeScale(scaleRatio, scaleRatio)
            }, completion: { _ in
                self.logoutSubmitButton.selected = isResultPage
        })
        UIView.animateWithDuration(0.4, delay: 0.2, usingSpringWithDamping: 0.4, initialSpringVelocity: 0.6, options: .BeginFromCurrentState, animations: {
            self.logoutSubmitButton.transform = CGAffineTransformMakeScale(1, 1)
            }, completion: nil)
        
    }
    
    @IBAction func decisionButtonPressed(sender: UIButton) {
        let pressedButtonTag = sender.tag
        let pressedButtonId = ButtonsIdentifier(rawValue: pressedButtonTag)
        EvaluationResult.results[currentPageNumber] = pressedButtonId
        updataeButtonsStates()
        refreshProgressView()
    }
    
    
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        switch segue.identifier! {
        case ParentVCStoryboard.pageViewSegue:
            pageVCDataSource = segue.destinationViewController as! PageViewControllerDataSource
            APIManager.apiDataRefreshDelegate = (segue.destinationViewController as! APIDataRefreshDelegate)
        default:
            break
        }
    }
    
    func restoreAllButtonsToDefaultState(){
        for button in buttons{
            button.deselect = true
        }
    }
    
    func updataeButtonsStates(){
        restoreAllButtonsToDefaultState()
        if currentPageNumber < AppConstant.tweetContentViewCount {
            if let buttonId = EvaluationResult.results[currentPageNumber]{
                let pressedButton = buttons[buttonId.rawValue]
                    pressedButton.deselect = false
            }
        }
    }
    
    func updatePageNumberView(){
        pageNumberLabel.text = String(currentPageNumber + 1)
    }
    
    func refreshProgressView(){
        progressView.setNeedsDisplay()
    }
    
    private func logoutHandler(){
        let alertController = UIAlertController(title: "Leave", message: "Do you want logout or restart test?", preferredStyle: .Alert)
        let logoutAction = UIAlertAction(title: "Logout", style: .Destructive) { _ in
            let defaults = NSUserDefaults.standardUserDefaults()
            defaults.removeObjectForKey( NSUserDefaultKeys.oauthTokenKey)
            defaults.removeObjectForKey( NSUserDefaultKeys.oauthTokenSecretKey)
        }
        alertController.addAction(logoutAction)
        
        
        
        let restartAction = UIAlertAction(title: "Restart", style: .Default) { _ in
            // todo restart
        }
        
        let cancelAction = UIAlertAction(title: "Cancel", style: .Cancel, handler: nil)
        alertController.addAction(cancelAction)
        alertController.addAction(restartAction)
        presentViewController(alertController, animated: true, completion: nil)
    }
    
    private func submitHandler(){
        if isSubmitted == false {
            let alertController = UIAlertController(title: "Submit", message: "Do you want submit?", preferredStyle: .Alert)
            let submitAction = UIAlertAction(title: "Submit", style: .Default) { _ in
                self.isSubmitted = true
                let submittedImage = UIImage(named: "submitted")
                self.logoutSubmitButton.setImage(submittedImage, forState: .Selected)
                
                self.postResultDataToServer()
            }
            alertController.addAction(submitAction)
            let cancelAction = UIAlertAction(title: "Cancel", style: .Cancel, handler: nil)
            alertController.addAction(cancelAction)
            presentViewController(alertController, animated: true, completion: nil)
            
        }
        else {
            let alertController = UIAlertController(title: "Can't submit again"
                                                    , message: "You have submitted current test result. Do you want logout or restart test?"
                                                    , preferredStyle: .Alert)
            
            let logoutAction = UIAlertAction(title: "Logout", style: .Destructive) { _ in
                let defaults = NSUserDefaults.standardUserDefaults()
                defaults.removeObjectForKey( NSUserDefaultKeys.oauthTokenKey)
                defaults.removeObjectForKey( NSUserDefaultKeys.oauthTokenSecretKey)
            }
            alertController.addAction(logoutAction)
            
            
            
            let restartAction = UIAlertAction(title: "Restart", style: .Default) { _ in
               // todo restart
            }
            
            let cancelAction = UIAlertAction(title: "Cancel", style: .Cancel, handler: nil)
            alertController.addAction(cancelAction)
            alertController.addAction(restartAction)
            presentViewController(alertController, animated: true, completion: nil)
        }
    
    }
    
    private func postResultDataToServer(){
        var resultParams = [String:String]()
        
        for (index, result) in EvaluationResult.results.enumerate(){
            switch result! {
            case .like:
                resultParams[String(index)] = "like"
            case .neither:
                resultParams[String(index)] = "neither"
            case .dislike:
                resultParams[String(index)] = "dislike"
            }
        }
        
        APIManager.postEvaluationResult(resultParams)
    }
    
    @IBAction func logoutSubmitButtonPressed() {
        switch currentPageNumber {
        case AppConstant.totalPageViewCount - 1:
            submitHandler()
        default:
            logoutHandler()
        }
    }
}

extension UIButton {
    var deselect:Bool {
        set{
            selected = newValue
        }
        get {
            return selected
        }
    }
}