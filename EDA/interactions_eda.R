library(tidyverse)
library(patchwork)
library(arrow)
library(tidytext) 

data <- read_parquet('~/Desktop/WORK/Monash/Thesis/Data collection/Complete Data/eda_prop.parquet')

################################################################################
# Barplots
################################################################################

data %>% 
  select(c('user.flair','depression','Anxiety','OCD',
           'Bitcoin', 'wallstreetbets', 'conspiracy',
           'lgbt', 'AgainstHateSubreddits', 'TwoXChromosomes',
           'movies', 'gaming', 'sports')) %>%
  pivot_longer(c('depression','Anxiety','OCD',
                 'Bitcoin', 'wallstreetbets', 'conspiracy',
                 'lgbt', 'AgainstHateSubreddits', 'TwoXChromosomes',
                 'movies', 'gaming', 'sports'), names_to = "subreddit",
               values_to = "value") %>%
  mutate(subreddit = paste('r/', subreddit, sep = ""),
         subreddit = factor(subreddit, 
                            levels = c('r/depression','r/Anxiety','r/OCD',
                                      'r/Bitcoin', 'r/wallstreetbets', 'r/conspiracy',
                                       'r/lgbt', 'r/AgainstHateSubreddits', 'r/TwoXChromosomes',
                                        'r/movies', 'r/gaming', 'r/sports'))) %>% 
  ggplot(aes(x=reorder_within(user.flair, -value, subreddit), y=value))+
  geom_col(color = 'black', fill = 'cyan') +
  theme_bw() + 
  facet_wrap(~subreddit, scales = "free", ncol = 3) +
  scale_x_reordered() +
  ggtitle('Proportion of comments in subreddits by ideology') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1, size = 20),
        plot.title  = element_text(size = 20),
        strip.text.x = element_text(size = 20)) +
  xlab("") +
  ylab("")

ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/interactions_eda.pdf", 
       width = 32, height = 40, units = "cm")
