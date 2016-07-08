//
//  ResultTableViewCell.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/8/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

class ResultTableViewCell: UITableViewCell {

    @IBOutlet weak var avatarImageView: UIImageView!{
        didSet{
            avatarImageView.layer.cornerRadius = 8
            avatarImageView.clipsToBounds = true
        }
    }
    @IBOutlet weak var tweetLabel: UILabel!
    @IBOutlet weak var userChoiceImageView: UIImageView!
    
    var userChoice: ButtonsIdentifier? {
        didSet{
            var choiceImageName = ""
            switch userChoice! {
            case .like:
                choiceImageName = "likeImage"
            case .neither:
                choiceImageName = "neitherImage"
            case .dislike:
                choiceImageName = "dislikeImage"
            }
            userChoiceImageView.image = UIImage(named: choiceImageName)
        }
    }
    
    var tweet: Tweet? {
        didSet{
            tweetLabel.text = tweet?.tweet
            if let avatarUrl = NSURL(string: (tweet?.userImageUrl)!){
                dispatch_async(dispatch_get_global_queue(QOS_CLASS_USER_INITIATED, 0), {
                    if let avatarData = NSData(contentsOfURL: avatarUrl){
                        dispatch_async(dispatch_get_main_queue(), {
                            self.avatarImageView.image = UIImage(data: avatarData)
                        })
                    }
                })
            }
        }
    }
    
    

    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
