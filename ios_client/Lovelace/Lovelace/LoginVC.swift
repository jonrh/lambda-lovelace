//
//  Login.swift
//  Lovelace
//
//  Created by Junyang ma on 6/20/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit


class LoginVC: UIViewController {
    
    @IBAction func loginButtonPressed() {
        APIManager.authorize(vcForOpeningWebView: self)
    }
}
