# DATA

The data used to model ideology as a function of digital footprint was scrapped from the ‘r/PoliticalCompassMemes/’ subreddit using Python and PRAW (Python Reddit API wrapper). There were two steps to collating the data:

1. Creating a list of usernames and the ideology signaling flair associated with said username. 
2. Creating a list of the 1000 (** may not actually be 1000 due to PRAW limit **) most recent comments and posts made by said user storing the title of the post (if applicable), the body of text, the score of the post, the time of creation and the subreddit its was created in. 

## Creating a list of usernames and ideology signaling flairs 

The process of creating a list of usernames and the associated ideology signaling flair was achieved through running a Python script that cycled through the top 1000 most popular posts of all time in the ‘r/PoliticalCompassMemes/’ subreddit. For each post, we looped through all the available comments. If the author of the comment was not already in a list of users who’s ideology we had recorded and their comment was flared with an ideology, we added the username and their flair as a row to the data set. The username was also added to the list of users who’s ideology we had recorded to avoid doubling up. 

This resulted in a dataset of 91,100 username and flair combinations. The data set looked like this:

[ TABLE ]

This data is central to the creation of a predictive model that can classify the ideology of reddit users’ based on their digital footprints. The flairs signal the ideology of users which served as our dependent or response variable. With this information at hand, the next step in the process was to obtain comprehensive digital footprints for all of the users for whom we have knowledge of their ideology. Comprehensive digital footprints can be converted to set of predictor variables for each user in a number of ways, allowing us to model ideology (as signaled by flair) as a function of digital footprint. 

There is no guarantee that each username in our dataset corresponds to a unique person; one individual could have two or more different reddit accounts. However, this is unlikely to be a prevalent behaviour and should have a negligible effect on the dataset at best. It is also possible that an account’s flair may n to truly represent the ideology of the person behind the account. This could be due to users mistakenly assuming that they subscribe to a particular ideology without having taken the test. We assume the vast majority of users in the ‘r/PoliticalCompassMemes/’ subreddit to have completed the test in order to determine their flair. It is also possible that some users create accounts flaired with opposing ideologies  in order to post unpopular views or stereotypes associated with that ideology in an effort to satirize the beliefs of their ideological opponents. We do not consider this to be a substantive issue in our dataset. 

It should also be noted that the limit of 1000 posts/comments/etc. is not arbitrary. PRAW limits requests to 1000 objects of a given time;  i.e.  if we are looping through a particular subreddit’s top posts we can at most request 1000 post ‘objects’ from PRAW. It was on this basis that we elected to gather usernames and flairs through the top posts since these are likely to have many comments and hence more user/flair combinations to record. It should also be noted that there may not be exactly 1000 objects returned from any request since deleted posts may be returned and contribute to the request limit despite being of no use to us. 

It would be possible to obtain a larger dataset through several workarounds (looping through different sets of posts and combining the results) but this would be tedious and our dataset is large enough to represent a substantive step forward from other work done in this area. 

The proportions of each ideology from our sample are discussed in the results section. 

## Collecting the digital footprints of flaired users 

As mentioned, the next step was to obtain the digital footprints of all the users who’s flairs were known so that we could extract a set of predictive features from them. For each user, we loop through the 1000 most recent posts and 1000 most recent comments. Each post or comment was stored as a row in a dataset with the following columns: 

username | interaction_type (post or comment) | title (if it is a post) | body (text) | score (of the post) | time (of creation) | subreddit

Resulting in a data frame looking like this:

[TABLE] 

As noted, we are limited to, at most, 1000 posts and 1000 comments for each user. Many users do not have this many posts or comments however some do and as such we are not collecting the entirety of their digital footprint. We choose to take the 1000 most recent posts and comments since these are presumably most reflective of the users’ most current attitudes and interests. 

The various ways in which this data was converted into a set of predictors for each user is detailed in the methodology section. 


One risk is that an individuals ideology has changed over time. If we collected a user’s ideology as signaled by flair in time t1 and later scraped the most recent comments at t2 such that t2 > t1.

Ideology can certainly change over time. However, the ‘r/PoliticalCompassMemes/’ subreddit has not been popular for a particularly long time and 

[][] put in screenshots from  https://subredditstats.com/r/politicalcompassmemes [][]


[][][ confirm we actually are getting most recent posts ] [][][]

[][][] risk users ideology has changed over time with our data collection [][][]

[][] add notes  from meeting [][][]

[][] sample non-rep - people post alot and may post in politically centered forums [][]
