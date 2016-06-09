//
//  APIManager.swift
//  Lovelace
//
//  Created by Junyang ma on 6/9/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import Foundation
import OAuthSwift

struct APIConstent{
    static let consumerKey = "BbTvs8T7CZguiloHMIVeRdKUO"
    static let consumerSecret = "Ji9JyeCKRrY9DUhE0ry0wWpYcVxJMHyOheqGc62VJOB4UsBXZy"
    static let requestTokenUrl = "https://api.twitter.com/oauth/request_token"
    static let authorizeUrl = "https://api.twitter.com/oauth/authenticate"
    static let accessTokenUrl = "https://api.twitter.com/oauth/access_token"
    static let callbackUrl = "https://lovelance.herokuapp.com/oauth-callback"
}

class APIManager {
    
    static let oauthSwift = OAuth1Swift(
        consumerKey: APIConstent.consumerKey, consumerSecret: APIConstent.consumerSecret ,requestTokenUrl: APIConstent.requestTokenUrl, authorizeUrl: APIConstent.authorizeUrl, accessTokenUrl: APIConstent.accessTokenUrl)
}
