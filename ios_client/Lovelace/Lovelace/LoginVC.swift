//
//  Login.swift
//  Lovelace
//
//  Created by Junyang ma on 6/20/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

struct LoignVCStoryboardIdentifiers{
    static let loginToFeedTableViewSegue = "login"
}

class LoginVC: UIViewController {
    
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        if APIManager.isRequestingOAuthToken || APIManager.LoadLocalOAuthToken() {
            performSegueWithIdentifier(LoignVCStoryboardIdentifiers.loginToFeedTableViewSegue, sender: self)
        }
    }

    @IBAction func loginButtonPressed() {
        APIManager.authorize(vcForOpeningWebView: self)
    }
}
