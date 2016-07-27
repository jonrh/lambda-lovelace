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
    
//    static let baseURLString = "http://csi6220-1-vm1.ucd.ie"
    static let baseURLString = "http://127.0.0.1:5000"
    
    case RecommendTweets(Int)
    case EvaluationData(Int)
    case EvaluationResult([String:AnyObject])
    
    var method: Alamofire.Method {
        switch self {
        case .RecommendTweets:
            return .GET
        case .EvaluationData:
            return .GET
        case .EvaluationResult:
            return .PUT
        }
    }
    
    var path: String {
        switch  self {
        case .RecommendTweets:
            return ("/recommend")
        case .EvaluationData:
            return ("/evaluationData")
        case .EvaluationResult:
            return ("/evaluationResult")
        }
    }
    
    var URLRequest: NSMutableURLRequest{
        let URL = NSURL(string: Router.baseURLString)!
        let mutableURLRequest = NSMutableURLRequest(URL: URL.URLByAppendingPathComponent(path))
        mutableURLRequest.HTTPMethod = method.rawValue
        
        if APIManager.hasOAuthToken {
            let oauthToken = APIManager.getOAuthTokenAndTokenSecret()
            var parameters:[String: AnyObject] = ["oauth_token" : oauthToken.oauth_token,
                              "oauth_token_secret" : oauthToken.oauth_token_secret]
            var encodeing = Alamofire.ParameterEncoding.URL
            switch self {
            case .RecommendTweets(let page):
                parameters["page"] = String(page)
            case .EvaluationData(let page):
                parameters["page"] = String(page)
            case .EvaluationResult(let resultParameters) :
                parameters = resultParameters
                encodeing = Alamofire.ParameterEncoding.JSON
            }
            
            return encodeing.encode(mutableURLRequest, parameters: parameters).0
        }
        return mutableURLRequest
    }
}
