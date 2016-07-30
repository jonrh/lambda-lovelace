//
//  UserProfileViewController.swift
//  Lovelace
//
//  Created by Junyang ma on 7/30/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

class UserProfileViewController: UIViewController {

    @IBOutlet weak var avatarImageView: UIImageView! {
        didSet{
            avatarImageView.layer.cornerRadius = 12
            avatarImageView.clipsToBounds = true
            avatarImageView.layer.borderWidth = 4
            avatarImageView.layer.borderColor = UIColor.whiteColor().CGColor
        }
    }
    @IBOutlet weak var userNameLabel: UILabel!
    @IBOutlet weak var screenNameLabel: UILabel!
    @IBOutlet weak var followingNumberLabel: UILabel!
    @IBOutlet weak var followerNumberLabel: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()

        APIManager.getUserProfile { profileJson in
            let userName = profileJson["name"].stringValue
            self.userNameLabel.text = userName
            
            let screenName = profileJson["screen_name"].stringValue
            self.screenNameLabel.text = screenName
            
            let avatarUrlString = profileJson["profile_image_url_https"].stringValue
            let avatarUrl = NSURL(string: avatarUrlString)!
            let avatarData = NSData(contentsOfURL: avatarUrl)
            let avatarImage = UIImage(data: avatarData!)
            self.avatarImageView.image = avatarImage
            
            let followingNumber = profileJson["friends_count"].stringValue
            self.followingNumberLabel.text = followingNumber
            
            let followerNumber = profileJson["followers_count"].stringValue
            self.followerNumberLabel.text = followerNumber
            
        }
    }

    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

    @IBAction func logoutButtonPressed() {
    }
}
