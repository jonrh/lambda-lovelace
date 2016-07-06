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
    @IBOutlet weak var buttonsStackView: UIStackView!
    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!
    private weak var pageVCDataSource: PageViewControllerDataSource!
    @IBOutlet weak var likeButton: UIButton!
    @IBOutlet weak var neitherButton: UIButton!
    @IBOutlet weak var dislikeButton: UIButton!
    @IBOutlet weak var progressView: EvaluationProgressView!
    @IBOutlet weak var pageNumberLabel: UILabel!
    
    var currentPageNumber:Int {
        return pageVCDataSource.pageNumberOfCurrentPageView
    }
    
    private var buttons: [UIButton]{
        return [likeButton,neitherButton,dislikeButton]
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        restoreAllButtonsToDefaultState()
        setOtherViewsHidden(true)
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    func setOtherViewsHidden(hidden: Bool){
        buttonsStackView.hidden = hidden
        topComponentView.hidden = hidden
        switch hidden {
        case true:
            activityIndicator.startAnimating()
        case false:
            activityIndicator.stopAnimating()
            updataeButtonsStatesAndProgressBar()
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

