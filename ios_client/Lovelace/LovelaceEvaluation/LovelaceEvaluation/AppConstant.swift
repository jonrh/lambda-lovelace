//
//  AppConstant.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/5/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation

struct AppConstant {
    static var totalPageViewCount:Int {
        return tweetContentViewCount + 1
    }
    static let tweetContentViewCount = 10
    static let loginSubmitButtonScaleRatio = 1.4
}
