//
//  Login.swift
//  Lovelace
//
//  Created by Junyang ma on 6/20/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

/*
 Controller of the login view
 which is the first view displayed to a new user
 */

class LoginVC: UIViewController {
    
    //this is called when the login button is clicked
    //it will call the authorize function in the class APIManager
    @IBAction func loginButtonPressed() {
        APIManager.authorize(vcForOpeningWebView: self)
    }
}
