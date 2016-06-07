//
//  APIRouter.swift
//  Lovelace
//
//  Created by Junyang ma on 6/7/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation
import Alamofire

enum Router: URLRequestConvertible {
    
    static let baseURLString = "https://lovelance.herokuapp.com"
    
    case Tweets
    
    var method: Alamofire.Method {
        switch self {
        case .Tweets:
            return .GET
        }
    }
    
    var path: String {
        switch  self {
        case .Tweets:
            return ("/tweets")
        }
    }
    
    var URLRequest: NSMutableURLRequest{
        let URL = NSURL(string: Router.baseURLString)!
        let mutableURLRequest = NSMutableURLRequest(URL: URL.URLByAppendingPathComponent(path))
        mutableURLRequest.HTTPMethod = method.rawValue
        
        return mutableURLRequest
    }
}
