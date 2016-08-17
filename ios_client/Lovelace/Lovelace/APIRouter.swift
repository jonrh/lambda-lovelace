//
//  APIRouter.swift
//  Lovelace
//
//  Created by Junyang ma on 6/7/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation
import Alamofire


// Router enum is used to generate proper request depends on its value
enum Router: URLRequestConvertible {
    
    static let baseURLString = "http://csi6220-1-vm1.ucd.ie"
//    static let baseURLString = "http://127.0.0.1:5000"
    
    case RecommendTweets(Int)
    case EvaluationData(Int)
    case EvaluationResult([String:AnyObject])
    case SingleTweetFeedback([String:String])
    case UserProfile
    case UserLogout
    
    // define http method for each case
    var method: Alamofire.Method {
        switch self {
        case .RecommendTweets:
            return .GET
        case .EvaluationData:
            return .GET
        case .EvaluationResult:
            return .PUT
        case .SingleTweetFeedback:
            return .PUT
        case .UserProfile:
            return .GET
        case .UserLogout:
            return .DELETE
        }
    }
    
    // set proper endpoint for each case
    var path: String {
        switch  self {
        case .RecommendTweets:
            return ("/recommend")
        case .EvaluationData:
            return ("/evaluationData")
        case .EvaluationResult:
            return ("/evaluationResult")
        case .SingleTweetFeedback:
            return ("/singleTweetFeedback")
        case .UserProfile:
            return ("/userProfile")
        case .UserLogout:
            return ("/userLogout")
        }
    }
    
    var URLRequest: NSMutableURLRequest{
        let URL = NSURL(string: Router.baseURLString)!
        let mutableURLRequest = NSMutableURLRequest(URL: URL.URLByAppendingPathComponent(path))
        mutableURLRequest.HTTPMethod = method.rawValue
        
        
        // set parameters for each case
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
            case .SingleTweetFeedback(let feedbackParams):
                parameters = feedbackParams
                encodeing = Alamofire.ParameterEncoding.JSON
            default:
                break
            }
            
            switch self {
            case .UserProfile:
                break
            default:
                var curretnUserScreenName = ""
                CurrentUserAccountInfo.getCurrentUser{ user in
                    curretnUserScreenName = user.screenName
                    parameters["currentUserScreenName"] = curretnUserScreenName
                }
            }
            
            return encodeing.encode(mutableURLRequest, parameters: parameters).0
        }
        return mutableURLRequest
    }
}
