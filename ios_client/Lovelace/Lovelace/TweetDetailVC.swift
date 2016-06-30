//
//  TweetDetailVC.swift
//  Lovelace
//
//  Created by Eazhilarasi Manivannan on 19/06/2016.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

class TweetDetailVC: UIViewController, UITextViewDelegate {
    var tweetObj:Tweet?
    
    @IBOutlet weak var userProfileImage: UIImageView!{
        didSet{
            userProfileImage.layer.cornerRadius = 8
            userProfileImage.clipsToBounds = true
        }
    }

    @IBOutlet weak var userNameLabel: UILabel!
    
    
    @IBOutlet weak var userScreenNameLabel: UILabel!
    
    
    
    @IBOutlet weak var tweetText: UITextView!
    
    
    @IBOutlet weak var tweetMediaImage: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tweetText.dataDetectorTypes = UIDataDetectorTypes.Link
        tweetText.delegate = self
        userNameLabel.text = tweetObj?.userName
        userScreenNameLabel.text = tweetObj?.userDisplayName
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
