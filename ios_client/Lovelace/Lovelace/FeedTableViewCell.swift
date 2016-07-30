//
//  TweetViewCell.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 15/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit
import SWTableViewCell
import KILabel

class FeedTableViewCell: SWTableViewCell {
    
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
    
    
    @IBOutlet weak var tweetText: KILabel!
    
    @IBOutlet weak var weightBar: UIView!{
        didSet{
            weightBar.layer.cornerRadius = 6
            weightBar.clipsToBounds = true
        }
    }
    @IBOutlet weak var shadowView: UIView! {
        didSet{
            shadowView.layer.shadowColor = UIColor.blackColor().colorWithAlphaComponent(0.2).CGColor
            shadowView.layer.borderColor = UIColor.blackColor().colorWithAlphaComponent(0.1).CGColor
            shadowView.layer.borderWidth = 1
            shadowView.layer.shadowOffset = CGSizeMake(0, 1)
            shadowView.layer.shadowRadius = 3
            shadowView.layer.shadowOpacity = 1
            shadowView.layer.cornerRadius = 8
        }
    }

    
    
    func updateCell()
    {
        tweetUserName.text = tweet?.userName
        tweetUserDisplayName.text = "@" + tweet!.userDisplayName
        tweetText.text = tweet?.tweet
        tweetDateTime.text = tweet?.tweetDateTime
        if let url = NSURL(string: (tweet?.userImageUrl)!){
            let qos = Int(QOS_CLASS_USER_INITIATED.rawValue)
            dispatch_async(dispatch_get_global_queue(qos,0)) { () -> Void in
                if let avatar = NSData(contentsOfURL: url) {
                    dispatch_async(dispatch_get_main_queue()) { () -> Void in
                        self.tweetUserImage?.image = UIImage(data: avatar)
                    }
                }
            }
        }
    }
    
    
    var weight: Int = 0 {
        didSet{
            let weightBarColor = UIColor(hue: 0.725 + CGFloat(weight)/10, saturation: 1, brightness: 0.98, alpha: 1.0) /* #5700f9 */
            weightBar.backgroundColor = weightBarColor
        }
    }

}
