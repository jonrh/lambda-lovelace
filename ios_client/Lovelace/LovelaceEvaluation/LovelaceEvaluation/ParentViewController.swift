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
    @IBOutlet weak var containerView: UIView!
    
    
    var topAndBottomComponentsHidden = false
    
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
    }
    
    
    func displayTopAndBottomComponents(show show: Bool, animated: Bool){
        if show != !topAndBottomComponentsHidden{
            displayBottomComponents(show: show)
            topAndBottomComponentsHidden = !show
        }
    }
    
    private func displayBottomComponents(show show: Bool){
        let bottomHeight = bottomComponentView.bounds.height
        
        UIView.animateWithDuration(1, delay: 0, usingSpringWithDamping: 0.5, initialSpringVelocity: 0.5, options: .BeginFromCurrentState, animations: {
            self.bottomComponentView.center.y += show ? -bottomHeight : bottomHeight
            }, completion: nil)
        UIView.animateWithDuration(0.6, delay: 0, options: .CurveEaseInOut, animations: {
            self.containerView.frame.size.height += ( show ? -1 : 1 ) * ( bottomHeight - 30 )
            }, completion: nil)
    }
    
    private func displayTopComponents(show show: Bool){
        let deltaY:CGFloat = show ? 150 : -150
        UIView.animateWithDuration(1){
            self.topComponentView.center.y += deltaY
            self.bottomComponentView.center.y += -deltaY
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
    
    @IBAction func decisionButtonPressed(sender: UIButton) {
        let pressedButtonTag = sender.tag
        let pressedButtonId = ButtonsIdentifier(rawValue: pressedButtonTag)
        EvaluationResult.results[currentPageNumber] = pressedButtonId
        updataeButtonsStatesAndProgressBar()
    }
    
    
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if (segue.identifier == ParentVCStoryboard.pageViewSegue){
            pageVCDataSource = segue.destinationViewController as! PageViewControllerDataSource
        }
    }
    
    func restoreAllButtonsToDefaultState(){
        for button in buttons{
            button.deselect = true
        }
    }
    
    func updataeButtonsStatesAndProgressBar(){
        restoreAllButtonsToDefaultState()
        if currentPageNumber < AppConstant.tweetContentViewCount {
            if let buttonId = EvaluationResult.results[currentPageNumber]{
                let pressedButton = buttons[buttonId.rawValue]
                    pressedButton.deselect = false
            }
        }
        
        progressView.currentPageNumber = currentPageNumber
        progressView.setNeedsDisplay()
        pageNumberLabel.text = String(currentPageNumber + 1)
        
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

