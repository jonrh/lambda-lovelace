//
//  ContentViewController.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 6/29/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit


class ContentViewController: UIViewController {
    @IBOutlet weak var tweetBackgroundView: UIVisualEffectView!{
        didSet{
            tweetBackgroundView.layer.cornerRadius = 6
            tweetBackgroundView.clipsToBounds = true
        }
    }

    @IBOutlet weak var avatarImageView: UIImageView! {
        didSet{
            avatarImageView.layer.cornerRadius = 12
            avatarImageView.clipsToBounds = true
        }
    }
    @IBOutlet weak var userNameLabel: UILabel!
    @IBOutlet weak var screenNameLabel: UILabel!
    @IBOutlet weak var tweetContentLabel: UILabel!
    @IBOutlet weak var tweetImageView: UIImageView!
    
    var pageNumber = 0
    var tweet: Tweet!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        userNameLabel.text = tweet.userName
        screenNameLabel.text = tweet.userDisplayName
        tweetContentLabel.text = tweet.tweet
        
        let userImageURL = NSURL(string: tweet.userImageUrl)
        
        if let userImageData = NSData(contentsOfURL: userImageURL!){
            let userImage = UIImage(data: userImageData)
            avatarImageView.image = userImage
        }
        
        
        let tweetImageURL = NSURL(string: tweet.tweetImageUrl)
        
        if let tweetImageData = NSData(contentsOfURL: tweetImageURL!){
            let tweetImage = UIImage(data: tweetImageData)
            tweetImageView.image = tweetImage
        }
        

    }

}
