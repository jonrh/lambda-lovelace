//
//  Result.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/5/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation

// this class is userd to store evaluation results
class EvaluationResult {
    static var results = [ButtonsIdentifier?](count: AppConstant.tweetContentViewCount, repeatedValue: nil)
    class func removeAll(){
        results = [ButtonsIdentifier?](count: AppConstant.tweetContentViewCount, repeatedValue: nil)
    }
}

