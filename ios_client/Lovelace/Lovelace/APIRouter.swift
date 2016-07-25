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
    
    static let baseURLString = "http://csi6220-1-vm1.ucd.ie"
    
    case Tweets(Int)
    case Result([String:String])
    
    var method: Alamofire.Method {
        switch self {
        case .Tweets:
            return .GET
        case .Result:
            return .PUT
        }
    }
    
    var path: String {
        switch  self {
        case .Tweets:
//            return ("/tweets")
            return ("/recommend")
        case .Result:
            return ("/evaluationResult")
        }
    }
    
    var URLRequest: NSMutableURLRequest{
        let URL = NSURL(string: Router.baseURLString)!
        let mutableURLRequest = NSMutableURLRequest(URL: URL.URLByAppendingPathComponent(path))
        mutableURLRequest.HTTPMethod = method.rawValue
        
        if APIManager.hasOAuthToken {
            let oauthToken = APIManager.getOAuthTokenAndTokenSecret()
            var parameters = ["oauth_token" : oauthToken.oauth_token,
                              "oauth_token_secret" : oauthToken.oauth_token_secret]
            var encodeing = Alamofire.ParameterEncoding.URL
            switch self {
            case .Tweets(let page):
                parameters["page"] = String(page)
            case .Result(let resultParameters) :
                parameters = resultParameters
                encodeing = Alamofire.ParameterEncoding.JSON
            }
            
            return encodeing.encode(mutableURLRequest, parameters: parameters).0
        }
        return mutableURLRequest
    }
}
