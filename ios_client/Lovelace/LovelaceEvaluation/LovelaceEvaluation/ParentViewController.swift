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

enum ButtonsIdentifiers:Int{
    case like = 0
    case neither = 1
    case dislike = 2
}

protocol ParentViewDelegate:class{
    func decisionButtonPressed(buttonId: ButtonsIdentifiers )
}

class ParentViewController: UIViewController {

    @IBOutlet weak var questionLabel: UILabel!
    @IBOutlet weak var buttonsStackView: UIStackView!
    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!
    private weak var delegate: ParentViewDelegate!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        setOtherViewsHidden(true)
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    func setOtherViewsHidden(hidden: Bool){
        buttonsStackView.hidden = hidden
        questionLabel.hidden = hidden
        switch hidden {
        case true:
            activityIndicator.startAnimating()
        case false:
            activityIndicator.stopAnimating()
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func decisionButtonPressed(sender: UIButton) {
        let buttonTag = sender.tag
        delegate.decisionButtonPressed(ButtonsIdentifiers.init(rawValue: buttonTag)!)
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if (segue.identifier == ParentVCStoryboard.pageViewSegue){
            delegate = segue.destinationViewController as! ParentViewDelegate
        }
    }

}
