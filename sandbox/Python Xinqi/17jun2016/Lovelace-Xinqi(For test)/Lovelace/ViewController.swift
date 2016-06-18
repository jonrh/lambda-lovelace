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
    
    @IBAction func userClicked(sender: UIButton) {
        APIManager.getUserTimeline { userLineTweets in
            
            print("\n\nUser Timeline:\n\n")
            for (_, tweet) in userLineTweets["user_tweets"] {
                print( tweet["text"] )
            }
            print("\n\nWord Counts:\n\n")
            print( userLineTweets["word_count"])
            print("\n\nUnfollowed Tweets:\n\n")
            print( userLineTweets["unfollowed_tweets"])
            
        }
    }
    
    @IBAction func homeClicked(sender: UIButton) {
        APIManager.getHomeTimeline { homeLineTweets in
            
            print("\n\nHome Timeline:\n\n")
            for (_, tweet) in homeLineTweets {
                
                print( tweet["text"] )
            }
//            print(homeLineTweets)
        }
    }
}

