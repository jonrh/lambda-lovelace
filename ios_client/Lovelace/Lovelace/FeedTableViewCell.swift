//
//  TweetViewCell.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 15/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

class FeedTableViewCell: UITableViewCell {
    
    var tweet: Tweet? {
        didSet {
            updateCell()
        }
    }
    
   

    @IBOutlet weak var tweetUserImage: UIImageView! {
        didSet{
            tweetUserImage.layer.cornerRadius = 8
            tweetUserImage.clipsToBounds = true
        }
    }
    
    
    @IBOutlet weak var tweetUserName: UILabel!
    
  
    @IBOutlet weak var tweetDateTime: UILabel!
    
    
    @IBOutlet weak var tweetUserDisplayName: UILabel!
    
    
    @IBOutlet weak var tweetText: UILabel!
    
    func updateCell()
    {
        tweetUserName.text = tweet?.userName
        tweetUserDisplayName.text = tweet?.userDisplayName
        tweetText.text = tweet?.tweet
        let url = NSURL(string: (tweet?.userImageUrl)!)
        let avatar = NSData(contentsOfURL: url!)
        tweetUserImage.image = UIImage(data: avatar!)
        tweetDateTime.text = tweet?.tweetDateTime
    }
    
}
