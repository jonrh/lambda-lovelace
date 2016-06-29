//
//  PageViewController.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 6/29/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

struct PageVCStoryboardIdentifiers{
    static let contentViewControllerId = "ContentViewController"
}
class PageViewController: UIPageViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        view.backgroundColor = UIColor.clearColor()
        dataSource = self
        delegate = self
        let contentVC = viewControllerOfIndex(1)
        let contentVCs = [contentVC!]
        setViewControllers(contentVCs, direction: .Forward, animated: true, completion: nil)
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}

extension PageViewController: UIPageViewControllerDelegate{
    
}

extension PageViewController: UIPageViewControllerDataSource{
    func viewControllerOfIndex(index: Int) -> UIViewController?{
       let contentVC = storyboard?.instantiateViewControllerWithIdentifier(PageVCStoryboardIdentifiers.contentViewControllerId) as! ContentViewController
        contentVC.userName = "test"
        return contentVC
    }
    
    func pageViewController(pageViewController: UIPageViewController, viewControllerBeforeViewController viewController: UIViewController) -> UIViewController? {
        return viewControllerOfIndex(1)
    }
    
    func pageViewController(pageViewController: UIPageViewController, viewControllerAfterViewController viewController: UIViewController) -> UIViewController? {
        return viewControllerOfIndex(1)
    }
    
    func presentationCountForPageViewController(pageViewController: UIPageViewController) -> Int {
        return 20
    }
    
    func presentationIndexForPageViewController(pageViewController: UIPageViewController) -> Int {
        return 0
    }
}



