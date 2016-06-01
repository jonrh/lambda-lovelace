---
layout: post
title:  Project Managment Tool Selection
date:   2016-05-26 21:07:00 +0100
---

For managment we wanted to keep things lite. Team members had previous experience with SCRUM but did not feel it was suitable or worth it for a 12 - 14 week program. Instead we wanted something more like a *Kanban board* where we could ideally have a *burndown chart* and *track time*. Here are the solutions we researched:

* [ZenHub](https://www.zenhub.io/) $75. Chrome extension that augments the GitHub website. Fairly extensive features. [Twitter](https://twitter.com/zenhubhq): ~1000 followers, fairly active.
* [Waffle.io](https://waffle.io/) **Free**. Kanban board for a GitHub repository. [Twitter](https://twitter.com/waffleio): ~2500 followers, active.
* [Blossom](https://www.blossom.co/) $66. [Twitter](https://twitter.com/blossom): ~3100 followers, very active.
* [HuBoard](https://huboard.com/) $72. [Twitter](https://twitter.com/huboard): ~500 followers, fairly active.
* [Jixee](https://jixee.me/) $60. Seems to be a fairly complete product. [Twitter](https://twitter.com/jixeeme): ~1300 followers, not very active, last tweet ~1.5 month ago.
* [SweepBoard](http://sweepboard.com/). [Twitter](https://twitter.com/wiredcraft): ~800 followers, active but it's the account of the company, no recent tweets on SweepBoard.
* [KanbanTool](http://kanbantool.com/) ~€100. [Twitter](https://twitter.com/kanbantool): ~1700 followers, fairly active.
* [KanbanFlow](https://kanbanflow.com/) $75. [Twitter](https://twitter.com/KanbanFlow): ~1100 followers, not very active.

Prices are estimations for how much we would have to pay for the duration of the project. To get a rough idea for the popularity of the solutions we looked at the Twitter accounts of the products.

None of the above solutions offers finely granular time tracking features (that we could see). Those sort of features seemed only to be available in solutions like [KanbanTool](http://kanbantool.com/), [KanbanFlow](https://kanbanflow.com/), and others. The problem with those solutions is they do not provide native integration with GitHub. In our research we did come across a neat service: [Zapier](https://zapier.com/app/explore). It's essentially a service to patch together with web hooks services that do not yet have native integrations. For example we did play around a bit with creating *zaps* to create a ticket in KanbanTool every time a new issue was created in the GitHub repository. It's a very powerful thing but does require some set-up.


### Evaluations

First we evaluated *Blossom*. It looked really promising but at the time automatically catching GitHub issues in the Kanban board was a work in progress feature, although the external website claimed otherwise.

Next up was *ZenHub*. This is the solution we are evaluating when this post was written. We are few days in and so far liking it very much. As mentioned earlier it's basically a Chrome extension that hijacks the GitHub webpage and adds extra features like a Kanban board, epics, story point, burndown chart, etc. This suits us very well because it eliminates the need to be managing something on a third party site. It's closer to the code where we prefer to work. 

![]({{site.baseurl}}/images/kanban_board1.png)  


On behalf of λ Lovelace  
\- *Jón Rúnar Helgason*