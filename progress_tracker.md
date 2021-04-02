# Progress Tracker 

## Tuesday March 30

* Created user_flair_scraper_draft.py, a script which goes through the most recent posts on the PCM subreddit and looks at each comment. For each comment it records the username and user flair of the comment's author (if the comment has a flair). It saves these to a csv. 

* Created user_flair_scraper_draft.py, a script that contains a function that can record the entire post and comment history of a specified reddit user. We can loop through a list of users to create a csv file that contains the entire post/comment history of multiple users. Each row of the output csv has the following columns:
* username | interaction_type (post or comment) | title (if it is a post) | body (text) | score (of the post) | time (of creation) | subreddit


## Thursday April 1 

* Github repo created, user_flair_scraper_draft.py and user_history_scraper_draft.py uploaded to repo

* To get a sense of how long it takes to scrape user names and flairs from the comments on the posts in the PCM subreddit, I ran user_flair_scraper_draft.py  several times, each time specifying that it stop after collecting usernames and flairs for a certain number of users.
* The results are as follows: 
    * 1000 users | 71.79 seconds
    * 2000 users | 114.6 seconds
    * 3000 users | 215.34 seconds
    * 4000 users | 293.65 seconds
    * 5000 users | 368.24 seconds
    * 6000 users | 558.32 seconds
    
* Updated user_flair_scraper_draft so that it scrapes 1000 user/flair pairs at a time and then adds each user/pair as a row to an existing .csv file. This way, if the computer doing the scraping is turned off while the script is running or something else terminates the script, most of the scraped data will still be saved and available.

## Friday April 2

* Started running the updated 'user_flair_scraper_draft.py' scraper. The limit of user observations to record is 500,000. I think it is unlikely that this number will be reached (there may not even be this number of flaired users who have made comments). Fortunately, the script saves every 1000 observations to a .csv so it will be no huge loss if some limiations cause an error and the script to stop running. I plan to keep this running over the break. In the meantime, I will start to get stuck into the literature review. 

* I have had some issues with the scraper. It turns out that PRAW has a limit of 1000 requsts. as such the 'posts in pcm.new(limit=None)' that we are looping through in order to view the comments (and by extension, the author of the comments and the author's flair). I have a few ideas that may allow us to work around this problem:
   1. Nest the 'for post in pcm.new(limit=None)' loop (the loop that goes through most recent posts) within a 'while len(users_unique) < 500000' loop (a loop that starts the for loop again if we have less than the desired ammount of users). One issue here is that there are likely not many new posts with lots of comment (from unique authors) being created inbetween running the initial for loop and running it again. As such this could be very slow as each iteration of the foor loop may yeild a few new comments from flaired users who we have not already recorded.
   2. At the moment the script only loops through first level comments (comments that are direct replies to the post). Obviously there are many more comments that branch through these comments that may be authored by flaired users who are not currently in our .csv file. As such the script should be ammended to go through ALL the comments of a post in search of unrecorded user/flair combinations. This approach is applicable no matter what list of posts we end up searching through. I am not sure how this will impact the time given the various request limits.
   3. Instead of going through the most recent posts, we can loop through the top (most popular) posts of all time (or of the week, month, year, etc.) These will presumably have a greater number of comments on them. As such the unique user/flair pairs yeilded from 1000 of the best posts of all time is likely to be much higher than through looping the 1000 most recent comments.
   4. We can loop through new comment, the top comments (of the week, year, etc.) seperately and then merge the files together. There will undoubtably be duplicates but it will be easy to remove duplicates from the merged data using R or Python.

* I will try various combinations of these possible workarounds and then update the user flair script in this repo.

