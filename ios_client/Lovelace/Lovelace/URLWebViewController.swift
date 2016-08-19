//
//  URLWebViewController.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 14/07/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//
/***
 This is controller class used for displaying the web page of the URL selected in the tweet ***/

import UIKit

class URLWebViewController: UIViewController {
    var urlString = ""
    
    @IBOutlet weak var webView: UIWebView!
    override func viewDidLoad() {
        super.viewDidLoad()
        let url = NSURL(string: urlString)
        let request = NSURLRequest(URL: url!)
        webView.loadRequest(request)
        
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}
