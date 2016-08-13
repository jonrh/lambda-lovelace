# λ Lovelace
Recommender system for tweets; a more personalised tweet stream. This is a repository for a final project in the 30 ECTS credit module COMP47250 Team Software Project 2016. Submitted to the School of Computer Science \& Informatics in partial fulfilment of the requirements for the degree of Masters of Science in Computer Science (Negotiated Learning) at University College Dublin. Summer 2016.

**Blog**: [https://jonrh.github.io/lambda-lovelace/](http://jonrh.github.io/lambda-lovelace/)


## Getting Started
Here are instructions on how to get started developing for the project.

**Quick Start**:

1. Install the [ZenHub Chrome extension](https://chrome.google.com/webstore/detail/zenhub-for-github/ogcgkffhplmphkaahpmffcafajaocjbd). See [Project Managment](#project-managmnent) for more details.
2. Clone `master` and `gh-pages` brances into seperate local repositories (folders)

There are two main branches: `master` (code & docs) and `gh-pages` (blog). It's best to clone both branches in a seperate folder because they do not share any common code.

```
// Go to the folder you want to keep the GitHubCode/ folder

mkdir GitHubCode
cd GitHubCode/

// Clone the master branch into the folder lambda-lovelace/
git clone https://github.com/jonrh/lambda-lovelace.git

// If you're not going to be working with the blow the blow can be skipped
// Clone the gh-pages branch into the folder ll-blog/
git clone https://github.com/jonrh/lambda-lovelace.git ll-blog/
cd ll-blog
git checkout -b gh-pages origin/gh-pages
```

## Project
**Summary**: A recommender system for tweets; a more personalised tweet stream.

The theme of 2016 for the group project module is *Future Of News*. The premise for our project is the asumption (or observation) that people are experiencing an information overload. Years or decades ago news or content creators were few (print, television, radio) compared to today. Now everyone with a computer or a smartphone can be a content creator. We believe that the future of news is going to be filtering and delivering personalised news to people. We see our project to be a stepping stone in that direction, starting with Twitter.

### Scope
On a very high level there are two main components to the project:

* **Front-end**: iOS Twitter mobile app
* **Back-end**: Collaborative recommender system

A Twitter user uses our iOS mobile client and grants us API access. Uninteresting tweets are filtered out (or deferred to later) while interesting tweets are prioritised in the timeline. Tweets from non-followers may be suggested as well. Essentially we hope to create a better, more personalised timeline of tweets than what Twitter provides by default. Our iOS app will make observations of the users engagements (opening, liking, time in focus, etc) and sends the information to the recommender back-end for further recommendations.

The mobile app is required in order to collect additional user preference information to refine the recommendations. For example, if a user clicks a link in a tweet, likes a tweet, retweets, or engages in conversations. Another potential passive observation mechanishm would be to have the client measure the amount of time a tweet is visible. Thinking being if a tweet is in focus for longer it might be of more interest than a tweet that is scrolled past quickly.

Our contributions or novelty if you will are as follows:

1. Filter out uninteresting tweets (or defer to later)
2. Collect additional user preferences in a mobile app
3. Show interesting tweets from non-followers

These are ordered by priority, that is we will first strive to implement tweet filtering, then data collection in the mobile app and if things go well we will try to introduce outsider tweets that might be of interest to the user.

In the beginning our project scope was to create a general recommendation system for all sorts of media: news, tweets, blogs, videos, etc. However given professor's feedback we decided to focus the idea on Twitter. We believe that doing so will allow us to deliver a more refined and complete solution. However if things go exceedingly well we may revisit this idea for further expansion.


## Technical Decisions
Here below are some of the technical descisions we've made so far. Please note that we do not consider them binding. That is, we are fully prepared to switch languages, stacks mid project if we believe it will suit us better.

- **Mobile**: iOS 9 + Swift 2.2
- **Recommender System**: Python 2.7, 
- **Back-end web service**: Python 2.7 and [Flask](http://flask.pocoo.org/) 
- **Database**: Undecided. Maybe [PostGres](https://www.postgresql.org/) for general storage, and a document database to store a cache of tweets.


## Project Managment

For project managment we keep it loose & lean. We use [ZenHub](https://www.zenhub.io/) to augment GitHub so we get a Kanban style board for issues and burndown charts to track milestone progresses. To use it you will have to install a [Chrome extension](https://chrome.google.com/webstore/detail/zenhub-for-github/ogcgkffhplmphkaahpmffcafajaocjbd). After the extension is installed you simply go to the GitHub [repository](https://github.com/jonrh/lambda-lovelace) and the extra features will be there on the page.

For issues we use the following story point estimations:

| Story Points | Description |
|:------------:|:------------|
| **1**        | ~30m easy work, e.g. testing for the other team |
| **2**        | 1 - 2 hours of work, simple but requires effort |
| **3**        | half a day of work |
| **5**        | full day of work |
| **8**        | 2 days of work, not easy |
| **13**       | 3 - 5 days of work, very complex may require multiple people | 


### Schedule & Deliverables
~~2016-05-17		Lecture 1 (10:00 - 16:00)~~  
~~2016-05-24		Lecture 2 (13:00 - 16:00)~~  
~~2016-05-31		Week 3 Lab (13:00 - 16:00)~~  
~~**2016-06-10		Week 4: Project Plan** (17:00)~~  
~~2016-06-14		Week 5 Lab (13:00 - 16:00)~~  
~~**2016-06-21		Mid-term presentations** (10:00 - 17:00)~~  
~~**2016-06-24		Mid-term report**~~  
2016-07-05		Week 8 Lab (13:00 - 16:00)  
**2016-07-15		User evaluation report**  
2016-07-19		Week 10 Lab (13:00 - 16:00)  
2016-08-02		Week 12 Lab (13:00 - 16:00)  
**2016-08-09		Final presentations** (10:00 - 17:00)  
**2016-08-19		Final Report & Code**  


### Week Calendar
|             |    M    |    T    |    W    |    T    |    F    |    S    |    S    | Month     |
|------------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:----------|
| **Week 1**  | 16      | 17      | 18      | 19      | 20      | 21      | 22      | May       |
| **Week 2**  | 23      | 24      | 25      | 26      | 27      | 28      | 29      | May       |
| **Week 3**  | 30      | *31*    | 1       | 2       | 3       | 4       | 5       | May/June  |
| **Week 4**  | 6       | 7       | 8       | 9       | **10**  | 11      | 12      | June      |
| **Week 5**  | 13      | *14*    | 15      | 16      | 17      | 18      | 19      | June      |
| **Week 6**  | 20      | **21**  | 22      | 23      | **24**  | 25      | 26      | June      |
| **Week 7**  | 27      | 28      | 29      | 30      | 1       | 2       | 3       | June/July |
| **Week 8**  | 4       | *5*     | 6       | 7       | 8       | 9       | 10      | July      |
| **Week 9**  | 11      | 12      | 13      | 14      | **15**  | 16      | 17      | July      |
| **Week 10** | 18      | *19*    | 20      | 21      | 22      | 23      | 24      | July      |
| **Week 11** | 25      | 26      | 27      | 28      | 29      | 30      | 31      | July      |
| **Week 12** | 1       | *2*     | 3       | 4       | 5       | 6       | 7       | August    |
| **Week 13** | 8       | **9**   | 10      | 11      | 12      | 13      | 14      | August    |
| **Week 14** | 15      | 16      | 17      | 18      | **19**  | 20      | 21      | August    |

**Bold**: Deliverable or presentation  
*Italic*: Show & Tell


### Blog and Show'n'tell
Moodle Deadlines:

* **Blog post**: 17:00 on the Monday before
* **Show & Tell slides**: 12:00 on Tuesday

|             |     Blog    |    Show & Tell    |
|------------:|:------------|:------------------|
| **Week 3**  | Jón Rúnar   | Jón Rúnar         |
| **Week 4**  | Xinqi       |                   |
| **Week 5**  | Marc        | Marc              |
| **Week 6**  |             |                   |
| **Week 7**  |             |                   |
| **Week 8**  | Eazhilarasi | Eazhilarasi       |
| **Week 9**  | Jón Rúnar   |                   |
| **Week 10** | Junyang     | Junyang           |
| **Week 11** | Marc        |                   |
| **Week 12** | Xinqi       | Xinqi             |

A tally of past jobs as well as scheduled ones:

|             | Blog posts | Show & Tell |
|:-----------:|:----------:|:-----------:|
| Xinqi       | 2          | 1           |
| Marc        | 2          | 1           |
| Junyang     | 1          | 1           |
| Jón Rúnar   | 2          | 1           |
| Eazhilarasi | 1          | 1           |


## Team members

- Jón Rúnar Helgason, [jonrh](https://github.com/jonrh), <jonrh@jonrh.is>
- Xinqi Li, [XinqiLi1992](https://github.com/XinqiLi1992), <xinqi.li@ucdconnect.ie>
- Marc Laffan, [Marc5690](https://github.com/Marc5690), <marclaffan@gmail.com>
- Junyang Ma, [specter4mjy](https://github.com/specter4mjy), <specter4mjy@gmail.com>
- Eazhilarasi Manivannan, [Eazhilarasi](https://github.com/Eazhilarasi), <eazhilarasi.manivannan@ucdconnect.ie>

Project roles:

* **Project Managment**: Marc
* **User Experience**: Eazhilarasi
* **Software Development**: Specter & Xinxqi
* **Evaluation & Communications**: Jón Rúnar