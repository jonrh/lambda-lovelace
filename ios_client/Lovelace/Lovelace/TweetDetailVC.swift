//
//  TweetDetailVC.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 19/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//
/***
 This is controller class for details view of tweet selected from the home timeline
 When the user click the cell in the table view, the detail view will pop up.
 ***/

import UIKit

class TweetDetailVC: UIViewController, UITextViewDelegate {
    
    //the tweet object of the cell the user clicked
    var tweetObj:Tweet?
    
    //image view that displays the user image of the tweet
    @IBOutlet weak var userProfileImage: UIImageView!{
        didSet{
            userProfileImage.layer.cornerRadius = 8
            userProfileImage.clipsToBounds = true
        }
    }

    //label that displays the user name
    @IBOutlet weak var userNameLabel: UILabel!
    
    //label that displays the screen name of the user
    @IBOutlet weak var userScreenNameLabel: UILabel!
    
    //label that displays the text of the tweets
    @IBOutlet weak var tweetText: UITextView!
    
    ////label that displays the image in the tweet content
    @IBOutlet weak var tweetMediaImage: UIImageView!
    
    //will be called then the detail view appears
    override func viewDidLoad() {
        super.viewDidLoad()
        
        //set values to all the UI components in the detail view
        //basically the detail view will get a tweet object from the Feed View, 
        //then displays detail of this tweet object
        tweetText.dataDetectorTypes = UIDataDetectorTypes.Link
        tweetText.delegate = self
        userNameLabel.text = tweetObj?.userName
        userScreenNameLabel.text = "@" + tweetObj!.userDisplayName
        tweetText.text = tweetObj?.tweet
        let userImageUrl = NSURL(string: (tweetObj?.userImageUrl)!)
        let avatar = NSData(contentsOfURL: userImageUrl!)
        userProfileImage.image = UIImage(data: avatar!)
        let tweetImageUrl = NSURL(string: (tweetObj?.tweetImageUrl)!)
        if let tweetImage = NSData(contentsOfURL: tweetImageUrl!)
        {
            tweetMediaImage.image = UIImage(data: tweetImage)
        }
        
    }
    
    func textView(textView: UITextView, shouldInteractWithURL URL: NSURL, inRange characterRange: NSRange) -> Bool {
        return true
    }
    
}
