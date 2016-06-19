//
//  TweetViewCell.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 15/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

class FeedTableViewCell: UITableViewCell {
    

    @IBOutlet weak var tweetUserImage: UIImageView! {
        didSet{
            tweetUserImage.layer.cornerRadius = 10
            tweetUserImage.clipsToBounds = true
        }
    }
    
    
    @IBOutlet weak var tweetUserName: UILabel!
    
  
    @IBOutlet weak var tweetDateTime: UILabel!
    
    
    @IBOutlet weak var tweetUserDisplayName: UILabel!
    
    
    @IBOutlet weak var tweetText: UILabel!
    
}
