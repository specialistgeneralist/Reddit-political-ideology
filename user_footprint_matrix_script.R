library(tidyverse)
setwd('~/Desktop/WORK/Monash/Thesis/Data collection')

user_records <- read_csv('user_records.csv') %>% filter(subreddit != 'PoliticalCompassMemes')

# not distinguishing between posts and comments, recording total posts/comments
# (that were found in the scrape) found in each  subreddit
user_records  %>% 
  select(-interaction, -title, -body, -time, -score) %>% 
  mutate(freq=1) %>%
  group_by(user, subreddit) %>%
  summarize(freq = sum(freq)) %>% 
  pivot_wider(names_from = subreddit, values_from = freq, values_fill = 0)

# not distinguishing between posts and comments, recording if posts/comments
# (that were found in the scrape) were found in each  subreddit
user_records  %>% 
  select(-interaction, -title, -body, -time, -score) %>% 
  mutate(freq=1) %>%
  group_by(user, subreddit) %>%
  summarize(freq = max(freq)) %>% 
  pivot_wider(names_from = subreddit, values_from = freq, values_fill = 0)
  
# not distinguishing between posts and comments, recording total karma of posts/comments
# (that were found in the scrape) found in each  subreddit
user_records  %>% 
  select(-interaction, -title, -body, -time) %>% 
  group_by(user, subreddit) %>%
  summarize(score = sum(score)) %>% 
  pivot_wider(names_from = subreddit, values_from = score, values_fill = 0)

# not distinguishing between posts and comments, recording average karma of posts/comments
# (that were found in the scrape) found in each  subreddit
user_records  %>% 
  select(-interaction, -title, -body, -time) %>% 
  group_by(user, subreddit) %>%
  summarize(score = mean(score)) %>% 
  pivot_wider(names_from = subreddit, values_from = score, values_fill = 0)





