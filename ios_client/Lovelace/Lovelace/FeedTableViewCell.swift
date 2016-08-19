//
//  TweetViewCell.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 15/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//
/***
 This is class represents each cell in the table view of home tweets
 ***/

import UIKit
import SWTableViewCell
import KILabel

class FeedTableViewCell: SWTableViewCell {
    
    //when a value is set to this var, update the cell
    var tweet: Tweet? {
        didSet {
            updateCell()
        }
    }
    
   
    //configure how the image view in the cell looks like
    @IBOutlet weak var tweetUserImage: UIImageView! {
        didSet{
            tweetUserImage.layer.cornerRadius = 8
            tweetUserImage.clipsToBounds = true
        }
    }
    
    //image view that displays the user image of the tweet
    @IBOutlet weak var tweetImage: UIImageView! {
        didSet{
            tweetImage.clipsToBounds = true
        }
    }
    
    //label that displays the user name
    @IBOutlet weak var tweetUserName: UILabel!
    
    //label that displays the date of the tweet
    @IBOutlet weak var tweetDateTime: UILabel!
    
    //label that displays the user's screen name
    @IBOutlet weak var tweetUserDisplayName: UILabel!
    
    //label that displays the text of the tweets
    @IBOutlet weak var tweetText: KILabel!
    
    //the view that indicates the weighting of the tweet, in different colors
    @IBOutlet weak var weightBar: UIView!{
        didSet{
            weightBar.layer.cornerRadius = 6
            weightBar.clipsToBounds = true
        }
    }
    
    @IBOutlet weak var shadowView: UIView! {
        didSet{
            shadowView.layer.shadowColor = UIColor.blackColor().CGColor
//            shadowView.layer.borderColor = UIColor.blackColor().CGColor
//            shadowView.layer.borderWidth = 1
            shadowView.layer.shadowOffset = CGSizeMake(0, 1)
            shadowView.layer.shadowRadius = 3
            shadowView.layer.shadowOpacity = 0.2
            shadowView.layer.cornerRadius = 8
//            let path = UIBezierPath(roundedRect: shadowView.layer.bounds, cornerRadius: 6).CGPath
//            shadowView.layer.shadowPath = path
        }
    }

    
    // Initialise value for each cell. So each cell will display different tweet
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
        if !(tweet?.tweetImageUrl.isEmpty)!
        {
            if let url = NSURL(string: (tweet?.tweetImageUrl)!){
                let qos = Int(QOS_CLASS_USER_INITIATED.rawValue)
                dispatch_async(dispatch_get_global_queue(qos,0)) { () -> Void in
                    if let avatar = NSData(contentsOfURL: url) {
                        dispatch_async(dispatch_get_main_queue()) { () -> Void in
                            self.tweetImage?.image = UIImage(data: avatar)
                        }
                    }
                }
            }
        }

    }
    
    //Calculation to get colour for the weight of tweet.
    var weight: Int = 0 {
        didSet{
            let weightBarColor = UIColor(hue: 0.725 + CGFloat(weight)/10, saturation: 1, brightness: 0.98, alpha: 1.0) /* #5700f9 */
            weightBar.backgroundColor = weightBarColor
        }
    }

}
