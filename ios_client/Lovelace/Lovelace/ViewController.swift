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
        
        Alamofire.request(Router.Tweets)
            .responseJSON { response in
                guard response.result.error == nil else {
                    print(response.result.error)
                    return
                }
                if let value = response.result.value {
                    let tweets = JSON(value)
                    for tweet in tweets {
                        print( tweet)
                    }
                }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

