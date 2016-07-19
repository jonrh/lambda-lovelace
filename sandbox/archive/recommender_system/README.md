# λ Lovelace - Recommender System

This folder contains code relating to the recommender system of the project.

There are several forms of recommendation provided, which ultimately results in a collection of tweets for the user.

The recommender system takes the users own timeline to create a term-frequency document, which is used in the following ways:

1. Filtering: Tweets containing more often-occurring terms in the term-frequency document are prioritised over others containing fewer.
2. Recommendation: Tweets from accounts not followed by the user are searched for using the hashtag function with the term-frequency document.
3. Weighting: Term weightings are appended to both sets of tweets, with higher ranking tweets (Ones containing more high-ranking terms from the
term-frequency document) appearing higher on the list.
4. The list of tweets is returned to the iOS app via flask.