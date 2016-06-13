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

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        
        APIManager.authorize(viewControllerForOpeningWebView: self)
        
        
    }
    
    @IBAction func buttonClicked(sender: UIButton) {
        APIManager.getHomeLine()
    }



}

