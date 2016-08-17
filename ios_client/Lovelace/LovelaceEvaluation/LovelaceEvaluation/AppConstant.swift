//
//  AppConstant.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/5/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation

// this file is userd configure evaluation parameters, such as test tweets numbers
struct AppConstant {
    
    // do not need chnage this value manually, it will update self based on constant: tweetContentViewCount
    static var totalPageViewCount:Int {
        return tweetContentViewCount + 1
    }
    
    // this constant decide test tweets number, in this case user will read 20 tweets for each test
    static let tweetContentViewCount = 20
    // this constant is used to tweak submit button animaiton effect
    static let loginSubmitButtonScaleRatio = 1.4
}
