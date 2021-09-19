library(tidyverse)
library(patchwork)
library(arrow)

data <- read_parquet('~/Desktop/WORK/Monash/Thesis/Data collection/Complete Data/eda_prop.parquet')

################################################################################
# Barplots
################################################################################

# Mental health themed visualizations 

mh_1 <- data %>% 
  select('user.flair','depression') %>% 
  ggplot(aes(x=reorder(user.flair, -depression), y = depression)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/depression') +
  xlab('') +
  theme_bw()

mh_2 <- data %>% 
  select('user.flair','Anxiety') %>% 
  ggplot(aes(x=reorder(user.flair, -Anxiety), y = Anxiety)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/Anxiety') +
  xlab('') +
  theme_bw()

mh_3 <- data %>% 
  select('user.flair','OCD') %>% 
  ggplot(aes(x=reorder(user.flair, -OCD), y = OCD)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/OCD') +
  xlab('') +
  theme_bw()

(mh_1 + mh_2 + mh_3) + plot_annotation(
  title = 'Proportion of comments in mental health subreddits by ideology',
) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/mh_eda.pdf", 
       width = 32, height = 20, units = "cm")

#  Might expect to be right

bitcoin <- data %>% 
  select('user.flair','Bitcoin') %>% 
  ggplot(aes(x=reorder(user.flair, -Bitcoin), y = Bitcoin)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/Bitcoin') +
  xlab('') +
  theme_bw()

wsb <- data %>% 
  select('user.flair','wallstreetbets') %>% 
  ggplot(aes(x=reorder(user.flair, -wallstreetbets), y = wallstreetbets)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/wallstreetbets') +
  xlab('') +
  theme_bw()

cons <- data %>% 
  select('user.flair','conspiracy') %>% 
  ggplot(aes(x=reorder(user.flair, -conspiracy), y = conspiracy)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/conspiracy') +
  xlab('') +
  theme_bw()


(bitcoin + wsb + cons)  + plot_annotation(
  title = 'Proportion of comments in subreddits you may associate with conservative views',
) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/rightwing_eda.pdf", 
       width = 32, height = 20, units = "cm")

# Might expect to be left wing 

lgbt <- data %>% 
  select('user.flair','lgbt') %>% 
  ggplot(aes(x=reorder(user.flair, -lgbt), y = lgbt)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/lgbt') +
  xlab('') +
  theme_bw()

ahsr <- data %>% 
  select('user.flair','AgainstHateSubreddits') %>% 
  ggplot(aes(x=reorder(user.flair, -AgainstHateSubreddits), y = AgainstHateSubreddits)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/AgainstHateSubreddits') +
  xlab('') +
  theme_bw()

twox <-data %>% 
  select('user.flair','TwoXChromosomes') %>% 
  ggplot(aes(x=reorder(user.flair, -TwoXChromosomes), y = TwoXChromosomes)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/TwoXChromosomes') +
  xlab('') +
  theme_bw()

(lgbt + ahsr +twox) + plot_annotation(
  title = 'Proportion of comments in subreddits you may associate with progressive views',
) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/leftwing_eda.pdf", 
       width = 32, height = 20, units = "cm")

# Random interests 

movies <- data %>% 
  select('user.flair','movies') %>% 
  ggplot(aes(x=reorder(user.flair, -movies), y = movies)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/movies') +
  xlab('') +
  theme_bw()

gaming <- data %>% 
  select('user.flair','gaming') %>% 
  ggplot(aes(x=reorder(user.flair, -gaming), y = gaming)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/gaming') +
  xlab('') +
  theme_bw()

sports <- data %>% 
  select('user.flair','sports') %>% 
  ggplot(aes(x=reorder(user.flair, -sports), y = sports)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/sports') +
  xlab('') +
  theme_bw()

(movies + gaming + sports) + 
  plot_annotation(
    title = 'Proportion of comments in hobby related subreddits',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/interests_eda.pdf", 
       width = 32, height = 20, units = "cm")
