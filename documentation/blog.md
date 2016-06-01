# λ Lovelace - Blog

Part of our project is to write a blog post at least every week. Here are instructions on how to post a blog post or change the blog in any way.

**Blog URL**: [http://jonrh.github.io/lambda-lovelace/](http://jonrh.github.io/lambda-lovelace/)

The blog is essentially [Jekyll](http://jekyllrb.com/) hosted on GitHub Pages. Jekyll is a Ruby project the "*convention over configuration*" mantra. It may be nescisary to read up on some of the Jekyll documentation because a lot of things are inferred implicitly. But things should mostly be set up by now so there shouldn't be much to worry about, mostly just adding blogs pots.

## Setup

1. Clone the [`gh-pages`](https://github.com/jonrh/lambda-lovelace/tree/gh-pages) branch to a seperate folder *ll-blog/* (or some other name you may prefer).
	
	```
	// Go to the folder you want to keep the blog folder.

	git clone https://github.com/jonrh/lambda-lovelace.git ll-blog/
	cd ll-blog
	git checkout -b gh-pages origin/gh-pages
	```

2. Make sure you got the latest version of [Ruby](https://www.ruby-lang.org/en/). When this was written the newest version was 2.3.1: `ruby --version`. One way is [rvm](https://rvm.io/) (doesn't work on Windows):
	
	```
	# Assuming rvm has been installed
	rvm install 2.3.1
	```

3. Install bundler and fetch the blog dependencies ([github-pages](https://github.com/github/pages-gem))
	
	```
	gem install bundler
	bundle install
	```
	
4. To start writing a blog locally:
	
	```
	bundle exec jekyll serve
	```
	
	Then open in a browser: [http://localhost:4000/lambda-lovelace/](http://localhost:4000/lambda-lovelace/)

5. To create a new blog post create a new GitHub Flavoured Markdown file (.md) in the **_posts/** folder. Follow the example of previous blog posts and make sure the file name matches the date convention.

6. Once you've written your blog post and you want to publish it to the web, simply commit and push the changes to the `gh-pages` branch:
	
	```
	# In the ll-blog/ folder
	git add _posts/name_of_your_new_blog_post.md
	git commit -m "A bombastic Git commit message of what you did"
	git push
	```