//
//  ResultContentViewController.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/7/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

class ResultContentViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, PageNumberDataSource {

    @IBOutlet weak var resultTableView: UITableView!{
        didSet{
            resultTableView.rowHeight = UITableViewAutomaticDimension
            resultTableView.estimatedRowHeight = 100
        }
    }
    var pageNumber = 0
    var results: [ButtonsIdentifier?] {
        return EvaluationResult.results
    }
    
    var tweets: [Tweet]!
    
    @IBOutlet weak var tweetBackgroundView: UIVisualEffectView!{
        didSet{
            tweetBackgroundView.layer.cornerRadius = 6
            tweetBackgroundView.clipsToBounds = true
        }
    }
    
//    override func viewDidAppear(animated: Bool) {
//        super.viewDidAppear(animated)
//        tableView.reloadData()
//    }
    
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        resultTableView.reloadData()
    }
    
    
    // MARK: - Table view data source
    func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 1
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return AppConstant.tweetContentViewCount
    }
    
    // feed table view with test result
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("reuseIdentifier", forIndexPath: indexPath) as! ResultTableViewCell
        
        if let buttonId = results[indexPath.row] {
            cell.userChoice = buttonId
        }
        cell.tweet = tweets[indexPath.row]
        
        return cell
    }
    
    


}
