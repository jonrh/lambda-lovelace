//
//  APIManager.swift
//  Lovelace
//
//  Created by Junyang ma on 6/9/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation
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
    
    class func authorize(sender: ViewController, success: OAuthSwift.TokenSuccessHandler, failure: OAuthSwift.FailureHandler?) {
        let oauthSwift = OAuth1Swift(
            consumerKey: APIConstent.consumerKey,
            consumerSecret: APIConstent.consumerSecret,
            requestTokenUrl: APIConstent.requestTokenUrl,
            authorizeUrl: APIConstent.authorizeUrl,
            accessTokenUrl: APIConstent.accessTokenUrl)
        oauthSwift.authorize_url_handler = SafariURLHandler(viewController: sender)
        oauthSwift.authorizeWithCallbackURL(APIConstent.callbackUrl, success: success, failure: failure)
    }
    
    
}
