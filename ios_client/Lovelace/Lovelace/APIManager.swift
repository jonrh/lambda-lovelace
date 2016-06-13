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

struct APIConstent{
    static let consumerKey = "BbTvs8T7CZguiloHMIVeRdKUO"
    static let consumerSecret = "Ji9JyeCKRrY9DUhE0ry0wWpYcVxJMHyOheqGc62VJOB4UsBXZy"
    static let requestTokenUrl = "https://api.twitter.com/oauth/request_token"
    static let authorizeUrl = "https://api.twitter.com/oauth/authenticate"
    static let accessTokenUrl = "https://api.twitter.com/oauth/access_token"
    static let callbackUrl = NSURL(string:"https://lovelance.herokuapp.com/oauth-callback")!
}

class APIManager {
    
    
    
    static private var oauth_token: String?;
    static private var oauth_token_secret: String?;
    
    class var hasOAuthToken: Bool {
        return oauth_token != nil && oauth_token_secret != nil
    }
    
    static let oauthSwift = OAuth1Swift(
            consumerKey: APIConstent.consumerKey,
            consumerSecret: APIConstent.consumerSecret,
            requestTokenUrl: APIConstent.requestTokenUrl,
            authorizeUrl: APIConstent.authorizeUrl,
            accessTokenUrl: APIConstent.accessTokenUrl)
    
    class func authorize(viewControllerForOpeningWebView viewControllerForOpeningWebView: ViewController) {
        oauthSwift.authorize_url_handler = SafariURLHandler(viewController: viewControllerForOpeningWebView)
        oauthSwift.authorizeWithCallbackURL(APIConstent.callbackUrl,
                                            success: { (credential, response, parameters) in
                                                oauth_token = credential.oauth_token
                                                oauth_token_secret = credential.oauth_token_secret
            },
                                            failure: { (error) in
                                                print("error")
                                                print(error.localizedDescription)
            }
        )
    }
    
    class func getHomeLine(){
        Alamofire.request(Router.Tweets)
            .responseJSON { response in
                guard response.result.error == nil else {
                    print(response.result.error)
                    return
                }
                if let value = response.result.value {
                    print(value)
                    let tweets = JSON(value)
                    for tweet in tweets {
                        print( tweet)
                    }
                }
        }
    }
    
    class func getOAuthTokenAndTokenSecret() -> (oauth_token: String, oauth_token_secret: String){
        guard hasOAuthToken else {
            return ("","")
        }
        return (oauth_token!,oauth_token_secret!)
    }
    
}
