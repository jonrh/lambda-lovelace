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

        CurrentUserAccountInfo.getCurrentUser{ currentUser in
            self.userNameLabel.text = currentUser.userName
            self.screenNameLabel.text = currentUser.screenName
            self.followerNumberLabel.text = String(currentUser.followerNumber)
            self.followingNumberLabel.text = String(currentUser.followingNumber)
            
            let avatarImage = UIImage(data: currentUser.avatarImageData)
            self.avatarImageView.image = avatarImage
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
