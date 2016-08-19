//
//  UserProfileViewController.swift
//  Lovelace
//
//  Created by Junyang ma on 7/30/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit
import Rollbar

/***
 This class is the View Controller of the user profile view. 
 User profile view displays the user's profile.
 For example, the avatar image of the user,screen name, 
 number of followers and users following.
 ***/
class UserProfileViewController: UIViewController {

    //The image view that displays the user's avatar image
    @IBOutlet weak var avatarImageView: UIImageView! {
        didSet{
            //set how the image view looks like
            avatarImageView.layer.cornerRadius = 12
            avatarImageView.clipsToBounds = true
            avatarImageView.layer.borderWidth = 4
            avatarImageView.layer.borderColor = UIColor.whiteColor().CGColor
        }
    }
    
    // the UILabel that dispalys user name
    @IBOutlet weak var userNameLabel: UILabel!
    
    // the UILabel that dispalys user's screen name
    @IBOutlet weak var screenNameLabel: UILabel!
    
    // the UILabel that dispalys number of users following
    @IBOutlet weak var followingNumberLabel: UILabel!
    
    // the UILabel that dispalys number of followers
    @IBOutlet weak var followerNumberLabel: UILabel!
    
    //called when the view appears
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        
        //get user profile and set values for each lable
        CurrentUserAccountInfo.getCurrentUser{ currentUser in
            self.userNameLabel.text = currentUser.userName
            self.screenNameLabel.text = currentUser.screenName
            self.followerNumberLabel.text = String(currentUser.followerNumber)
            self.followingNumberLabel.text = String(currentUser.followingNumber)
            
            let avatarImage = UIImage(data: currentUser.avatarImageData)
            self.avatarImageView.image = avatarImage
        }
        
    }
    
    
    // MARK: - Navigation

    //this will be called when logout button is clicked
    @IBAction func logoutButtonPressed() {
        
        //an alert view will pop up to make sure the user wants to sign out
        let alertVC = UIAlertController(title: "Sign out", message: "Are you sure you want to sign out?", preferredStyle: .Alert)
        
        //if the user click yes, remove all the info of the current user, then jump to the initial login view
        let yesAction = UIAlertAction(title: "Yes", style: .Destructive ){ _ in
            APIManager.deleteUser()
            var userName = ""
            CurrentUserAccountInfo.getCurrentUser{ user in
                userName = user.screenName
            }
            Rollbar.infoWithMessage(userName + "has log out")
            let defaults = NSUserDefaults.standardUserDefaults()
            defaults.removeObjectForKey( NSUserDefaultKeys.oauthTokenKey)
            defaults.removeObjectForKey( NSUserDefaultKeys.oauthTokenSecretKey)
            CurrentUserAccountInfo.removeCurrentUserLocalData()
            let nevigationVC = self.tabBarController?.viewControllers![0] as! UINavigationController
            nevigationVC.popToRootViewControllerAnimated(true)
            let feedVC = nevigationVC.viewControllers[0] as! FeedViewController
            feedVC.cleanTableView(true)
            feedVC.needReloadTable = true
            self.tabBarController?.selectedIndex = 0
            
        }
        alertVC.addAction(yesAction)
        let cancelAction = UIAlertAction(title: "Cancel", style: .Cancel, handler: nil)
        alertVC.addAction(cancelAction)
        presentViewController(alertVC, animated: true, completion: nil)
    }
}
