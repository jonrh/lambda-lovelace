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
    case UserTimeline
    case HomeTimeline
    
    var method: Alamofire.Method {
        switch self {
        case .Tweets:
            return .GET
        case .UserTimeline:
            return .GET
        case .HomeTimeline:
            return .GET
        }
    }
    
    var path: String {
        switch  self {
        case .Tweets:
            return ("/tweets")
        case .UserTimeline:
            return ("/user_timeline")
        case .HomeTimeline:
            return ("/home_timeline")
        }
    }
    
    var URLRequest: NSMutableURLRequest{
        let URL = NSURL(string: Router.baseURLString)!
        let mutableURLRequest = NSMutableURLRequest(URL: URL.URLByAppendingPathComponent(path))
        mutableURLRequest.HTTPMethod = method.rawValue
        
        if APIManager.hasOAuthToken {
            let oauthToken = APIManager.getOAuthTokenAndTokenSecret()
            print(oauthToken)
            let parameters = ["oauth_token" : oauthToken.oauth_token,
                              "oauth_token_secret" : oauthToken.oauth_token_secret]
            let encodeing = Alamofire.ParameterEncoding.URL
            return encodeing.encode(mutableURLRequest, parameters: parameters).0
        }
        return mutableURLRequest
    }
}
