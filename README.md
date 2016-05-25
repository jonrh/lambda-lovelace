# λ Lovelace

A collaborative recommender system for tweets. A 30 ECTS group project, summer 2016 at University College Dublin.



## Project Scope

**Summary**: A collaborative recommender system for tweets. A user with a Twitter account signs up and uses our iOS mobile client. Tweets from followers not of interest are filtered out (or deferred to later) while interesting tweets are prioritised. Tweets from non-followers may be suggested. The iOS client makes observations of the users engagements (opening, liking, time in focus, etc) and sends it to the recommender back-end for further formulation of recommendations.

Earlier our project scope was to create a general recommendation system for all sorts of media: news, tweets, blogs, videos, etc. However given professor's feedback we decided to focus the idea on Twitter. We believe that doing so will allow us to deliver a more refined and complete solution. However if things go exceedingly well we may revisit this idea for further expansion.

For the 





## Minimum Viable Product

Given the description we gave for the Personalised News project a minimum viable product would be a recommender system + mobile client for Twitter. I guess we’d have to detail a bit further what exactly that is.

A recommender system 



## Evaluation Method

There are two evaluations that come to mind:

- Quality / Accuracy of recommender system
- Usability of mobile client

A cornerstone of the project will be to recommend something the user finds relevant. The recommender system can be evaluated in two ways:

- **Evaluation on a static dataset**. Static datasets constructed from existing Twitter accounts. Something we can test over and over to benchmark ourselves. Sort of like unit tests. Try to predict likes for example. This evaluation is more intended to aid us during development.
- **User evaluation**.  One idea we had though was to present to the user pairs of unseen tweets and have the user select which tweet is more interesting or relevant.
  - Present pairs of unseen tweets from a users timeline. User selects which tweet is more interesting or relevant. With t
  - v
  - True evaluations from live users. This is more fuzzy, we have users try our system with their Twitter account and report how accurate the predictions are.

Not sure how we would test the usability of the mobile app, but there are probably well known ways to do it : )



## Technical Decisions

Here below are some of the technical descisions we've made so far. Please note that we do not consider them binding. That is, we are fully prepared to switch languages, stacks mid project if we believe it will suit us better.

- **Mobile**: iOS 9 + Swift 2.2
- **Recommender System**: Python 3
- **Back-end web service**: Python 3 or 2, [Flask](http://flask.pocoo.org/) (or [Bottle](http://bottlepy.org/docs/dev/index.html))
- **Database**: *undecided*

For the backend we'll strive to use Python 3 as much as we can but for some parts it may be nescisary to use Python 2.7. For the recommender system we aim to use Python 3 data scicence libraries as much as we can. However Python is not the fastest language on the block so we've pondered the possibility to dip into [Rust](https://www.rust-lang.org/) for performance critical parts, but we'll see.

### Story Points

**1**:    ~30m easy work, e.g. testing for the other team
**2**:    1 - 2 hours of work, simple but requires effort
**3**:    half a day of work
**5**:    full day of work
**8**:    2 days of work, not easy
**13**:  3 - 5 days of work, very complex may require multiple people



## Team members

- Jón Rúnar Helgason, [jonrh](https://github.com/jonrh), [jonrh@jonrh.is](jonrh@jonrh.is)
- Xinqi Li, [XinqiLi1992](https://github.com/XinqiLi1992), [xinqi.li@ucdconnect.ie](xinqi.li@ucdconnect.ie)
- Marc Laffan, [Marc5690](https://github.com/Marc5690), marclaffan@gmail.com
- Junyang Ma, [specter4mjy](https://github.com/specter4mjy), specter4mjy@gmail.com
- Eazhilarasi Manivannan, [Eazhilarasi](https://github.com/Eazhilarasi), [eazhilarasi.manivannan@ucdconnect.ie](eazhilarasi.manivannan@ucdconnect.ie)