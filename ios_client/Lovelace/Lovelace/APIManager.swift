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
    static let callbackUrl = NSURL(string:"https://lovelance.herokuapp.com/oauth-callback")!
}

struct NSUserDefaultKeys{
    static let oauthTokenKey = "oauthToken"
    static let oauthTokenSecretKey = "oauthSecretToken"
}

protocol APIDataRefreshDelegate: class {
    func apiDataRefresh()
}

class APIManager {
    
    weak static var dataRefreshDelegate: APIDataRefreshDelegate?
    
    static private var oauth_token: String? {
        didSet{
           dataRefreshDelegate?.apiDataRefresh()
        }
    }
    static private var oauth_token_secret: String?;
    
    static var reqestingAccessToken = false
    
    class var hasOAuthToken: Bool {
        return oauth_token != nil && oauth_token_secret != nil
    }
    
    static let oauthSwift = OAuth1Swift(
            consumerKey: APIConstents.consumerKey,
            consumerSecret: APIConstents.consumerSecret,
            requestTokenUrl: APIConstents.requestTokenUrl,
            authorizeUrl: APIConstents.authorizeUrl,
            accessTokenUrl: APIConstents.accessTokenUrl)
    
    class func initOAuthTokenAndSecret(viewControllerForOpeningWebView viewControllerForOpeningWebView: UIViewController, dataRefreshDelegate: APIDataRefreshDelegate){
        self.dataRefreshDelegate = dataRefreshDelegate
        
        let defaults = NSUserDefaults.standardUserDefaults()
        
        if let oauthToken = defaults.stringForKey(NSUserDefaultKeys.oauthTokenKey){
            if let oauthTokenSecret = defaults.stringForKey(NSUserDefaultKeys.oauthTokenSecretKey){
                oauth_token = oauthToken
                oauth_token_secret = oauthTokenSecret
            }
        } else {
            // user first loggin will direct to twitter loggin website
            authorize(viewControllerForOpeningWebView: viewControllerForOpeningWebView)
        }
        
    }
    
    class func authorize(viewControllerForOpeningWebView viewControllerForOpeningWebView: UIViewController) {
        reqestingAccessToken = true
        oauthSwift.authorize_url_handler = SafariURLHandler(viewController: viewControllerForOpeningWebView)
        oauthSwift.authorizeWithCallbackURL(APIConstents.callbackUrl,
                                            success: { (credential, response, parameters) in
                                                successfullyReceiveAccessToken(credential)
            },
                                            failure: { (error) in
                                                print("error")
                                                print(error.localizedDescription)
                                                reqestingAccessToken = false
            }
        )
    }
    
    private class func successfullyReceiveAccessToken(credential: OAuthSwiftCredential){
        let defaults = NSUserDefaults.standardUserDefaults()
        defaults.setObject(credential.oauth_token, forKey: NSUserDefaultKeys.oauthTokenKey)
        defaults.setObject(credential.oauth_token_secret, forKey: NSUserDefaultKeys.oauthTokenSecretKey)
        
        oauth_token = credential.oauth_token
        oauth_token_secret = credential.oauth_token_secret
        
        reqestingAccessToken = false
    }
    
    class func getHomeLine(callback: (JSON)->Void) {
        Alamofire.request(Router.Tweets)
            .responseJSON { response in
                guard response.result.error == nil else {
                    print(response.result.error)
                    return
                }
                if let value = response.result.value {
                    let tweets = JSON(value)
                    // get response data
                    callback(tweets)
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
