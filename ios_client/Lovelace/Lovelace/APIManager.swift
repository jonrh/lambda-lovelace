//
//  APIManager.swift
//  Lovelace
//
//  Created by Junyang ma on 6/9/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation
import Alamofire
import SwiftyJSON
import OAuthSwift
import SafariServices

struct APIConstents{
    static let consumerKey = "BbTvs8T7CZguiloHMIVeRdKUO"
    static let consumerSecret = "Ji9JyeCKRrY9DUhE0ry0wWpYcVxJMHyOheqGc62VJOB4UsBXZy"
    static let requestTokenUrl = "https://api.twitter.com/oauth/request_token"
    static let authorizeUrl = "https://api.twitter.com/oauth/authenticate"
    static let accessTokenUrl = "https://api.twitter.com/oauth/access_token"
    static let callbackUrl = NSURL(string:"http://csi6220-1-vm1.ucd.ie/oauth-callback")!
}

struct NSUserDefaultKeys{
    static let oauthTokenKey = "oauthToken"
    static let oauthTokenSecretKey = "oauthSecretToken"
}

protocol APIDataRefreshDelegate: class {
    func apiDataRefresh()
}


class APIManager {
    
    weak static var apiDataRefreshDelegate: APIDataRefreshDelegate?
    
    static private var oauth_token: String?
    
    static private var oauth_token_secret: String?
    
    static var isRequestingOAuthToken = false
    
    class var hasOAuthToken: Bool {
        return oauth_token != nil && oauth_token_secret != nil
    }
    
    static let oauthSwift = OAuth1Swift(
            consumerKey: APIConstents.consumerKey,
            consumerSecret: APIConstents.consumerSecret,
            requestTokenUrl: APIConstents.requestTokenUrl,
            authorizeUrl: APIConstents.authorizeUrl,
            accessTokenUrl: APIConstents.accessTokenUrl)
    
    
    class func LoadLocalOAuthToken() -> Bool{
        
        let defaults = NSUserDefaults.standardUserDefaults()
        
        if let oauthToken = defaults.stringForKey(NSUserDefaultKeys.oauthTokenKey){
            if let oauthTokenSecret = defaults.stringForKey(NSUserDefaultKeys.oauthTokenSecretKey){
                oauth_token = oauthToken
                oauth_token_secret = oauthTokenSecret
                return true
            }
        }
        return false
        
    }
    
    
    class func getOAuthTokenAndTokenSecret() -> (oauth_token: String, oauth_token_secret: String){
        guard hasOAuthToken else {
            return ("","")
        }
        return (oauth_token!,oauth_token_secret!)
    }
    
    
    class func authorize(vcForOpeningWebView vcForOpeningWebView: UIViewController) {
        isRequestingOAuthToken = true
        oauthSwift.authorize_url_handler = SafariURLHandler(viewController: vcForOpeningWebView)
        oauthSwift.authorizeWithCallbackURL(APIConstents.callbackUrl,
                                            success: { (credential, response, parameters) in
                                                print("get oauth token successfully")
                                                successfullyReceiveAccessToken(credential)
                                                isRequestingOAuthToken = false
            },
                                            failure: { (error) in
                                                print("request oauth token error")
                                                print(error.localizedDescription)
                                                isRequestingOAuthToken = false
            }
        )
    }
    
    private class func successfullyReceiveAccessToken(credential: OAuthSwiftCredential){
        let defaults = NSUserDefaults.standardUserDefaults()
        defaults.setObject(credential.oauth_token, forKey: NSUserDefaultKeys.oauthTokenKey)
        defaults.setObject(credential.oauth_token_secret, forKey: NSUserDefaultKeys.oauthTokenSecretKey)
        defaults.synchronize()
        
        oauth_token = credential.oauth_token
        oauth_token_secret = credential.oauth_token_secret
        apiDataRefreshDelegate?.apiDataRefresh()
    }
    
    
    
    class func getRecommendTweetsWithPage(page: Int, callback: (JSON)->Void) {
        Alamofire.request(Router.RecommendTweets(page))
            .responseJSON { response in
                guard response.result.error == nil else {
                    print(response.result.error)
                    return
                }
                if let value = response.result.value {
                    let tweets = JSON(value)
                    callback(tweets)
                }
        }
    }
    
    
    class func getEvaluationDataWithPage(page: Int, callback: (JSON)->Void) {
        Alamofire.request(Router.EvaluationData(page))
            .responseJSON { response in
                guard response.result.error == nil else {
                    print(response.result.error)
                    return
                }
                if let value = response.result.value {
                    let tweets = JSON(value)
                    callback(tweets)
                }
        }
    }
    
    class func postEvaluationResult(resultParams: [String: AnyObject]){
        Alamofire.request(Router.EvaluationResult(resultParams))
            .response { request, response, data, error in
                print(request)
        }
        
    }
    
    
}
