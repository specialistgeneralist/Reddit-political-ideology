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
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

mh_2 <- data %>% 
  select('user.flair','Anxiety') %>% 
  ggplot(aes(x=reorder(user.flair, -Anxiety), y = Anxiety)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/Anxiety') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

mh_3 <- data %>% 
  select('user.flair','OCD') %>% 
  ggplot(aes(x=reorder(user.flair, -OCD), y = OCD)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/OCD') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

(mh_1 + mh_2 + mh_3) + plot_annotation(
  title = 'Proportion of comments in mental health subreddits by ideology',
) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/mh_eda.pdf", 
       width = 32, height = 20, units = "cm")

#  Might expect to be right

bitcoin <- data %>% 
  select('user.flair','Bitcoin') %>% 
  ggplot(aes(x=reorder(user.flair, -Bitcoin), y = Bitcoin)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/Bitcoin') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

wsb <- data %>% 
  select('user.flair','wallstreetbets') %>% 
  ggplot(aes(x=reorder(user.flair, -wallstreetbets), y = wallstreetbets)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/wallstreetbets') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

cons <- data %>% 
  select('user.flair','conspiracy') %>% 
  ggplot(aes(x=reorder(user.flair, -conspiracy), y = conspiracy)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/conspiracy') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))


(bitcoin + wsb + cons)  + plot_annotation(
  title = 'Proportion of comments in subreddits you may associate with conservative views',
) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/rightwing_eda.pdf", 
       width = 32, height = 20, units = "cm")

# Might expect to be left wing 

lgbt <- data %>% 
  select('user.flair','lgbt') %>% 
  ggplot(aes(x=reorder(user.flair, -lgbt), y = lgbt)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/lgbt') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

ahsr <- data %>% 
  select('user.flair','AgainstHateSubreddits') %>% 
  ggplot(aes(x=reorder(user.flair, -AgainstHateSubreddits), y = AgainstHateSubreddits)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/AgainstHateSubreddits') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

twox <-data %>% 
  select('user.flair','TwoXChromosomes') %>% 
  ggplot(aes(x=reorder(user.flair, -TwoXChromosomes), y = TwoXChromosomes)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/TwoXChromosomes') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

(lgbt + ahsr +twox) + plot_annotation(
  title = 'Proportion of comments in subreddits you may associate with progressive views',
) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/leftwing_eda.pdf", 
       width = 32, height = 20, units = "cm")

# Random interests 

movies <- data %>% 
  select('user.flair','movies') %>% 
  ggplot(aes(x=reorder(user.flair, -movies), y = movies)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/movies') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

gaming <- data %>% 
  select('user.flair','gaming') %>% 
  ggplot(aes(x=reorder(user.flair, -gaming), y = gaming)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/gaming') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

sports <- data %>% 
  select('user.flair','sports') %>% 
  ggplot(aes(x=reorder(user.flair, -sports), y = sports)) + 
  geom_col(color = 'black', fill = 'cyan') +
  ylab('r/sports') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

(movies + gaming + sports) + 
  plot_annotation(
    title = 'Proportion of comments in hobby related subreddits',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/interests_eda.pdf", 
       width = 32, height = 20, units = "cm")

################################################################################
# Density plots
################################################################################

data <- read_parquet('~/Desktop/WORK/Monash/Thesis/Data collection/Complete Data/eda_dist.parquet')

d1 <- data %>% select('user.flair','Bitcoin') %>%
  mutate(user.flair = case_when(
    user.flair == 'centrist' ~ 'center',
    user.flair == 'libcenter' ~ 'center',
    user.flair == 'authcenter' ~ 'center',
    user.flair == 'left' ~ 'left',
    user.flair == 'authleft' ~ 'left',
    user.flair == 'libleft' ~ 'left',
    user.flair == 'right' ~ 'right',
    user.flair == 'libright' ~ 'right',
    user.flair == 'authright' ~ 'right'),
    log_bitcoin = log(Bitcoin)) %>% 
  filter(user.flair != 'center') %>% 
  ggplot(aes(x=log_bitcoin, y=3*(..density..)/sum(..density..), fill = user.flair)) +
  geom_density(alpha = 1/3) +
  ylab('') +
  xlab('Log comments in R/Bitcoin') +
  scale_fill_manual(values=c('cyan', 'cyan'), name = 'Ideology') + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

d2 <- data %>% select('user.flair','movies') %>%
  mutate(user.flair = case_when(
    user.flair == 'centrist' ~ 'center',
    user.flair == 'libcenter' ~ 'lib',
    user.flair == 'authcenter' ~ 'auth',
    user.flair == 'left' ~ 'center',
    user.flair == 'authleft' ~ 'auth',
    user.flair == 'libleft' ~ 'lib',
    user.flair == 'right' ~ 'center',
    user.flair == 'libright' ~ 'lib',
    user.flair == 'authright' ~ 'auth'),
    log_movies = log(movies)) %>% 
  filter(user.flair != 'center') %>% 
  ggplot(aes(x=log_movies, y=3*(..density..)/sum(..density..), fill = user.flair)) +
  geom_density(alpha = 1/2) +
  ylab('') +
  xlab('Log comments in R/movies') +
  scale_fill_manual(values=c('cyan', 'cyan'), name = 'Ideology') + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

d1 + d2


data %>% select('user.flair','Bitcoin') %>%
  mutate(user.flair = case_when(
    user.flair == 'centrist' ~ 'center',
    user.flair == 'libcenter' ~ 'center',
    user.flair == 'authcenter' ~ 'center',
    user.flair == 'left' ~ 'left',
    user.flair == 'authleft' ~ 'left',
    user.flair == 'libleft' ~ 'left',
    user.flair == 'right' ~ 'right',
    user.flair == 'libright' ~ 'right',
    user.flair == 'authright' ~ 'right'),
    log_bitcoin = log(Bitcoin)) %>% 
  ggplot( aes(x= user.flair, y = log_bitcoin, fill = user.flair)) +
  geom_boxplot()

data %>% 
  mutate(
    log = log(Bitcoin)) %>% 
  ggplot( aes(x= user.flair, y = log, fill = user.flair)) +
  geom_boxplot(fill = 'cyan')+ 
  ylab('') +
  xlab('Log comments in R/movies') +
  scale_fill_manual(values=c('cyan', 'cyan'), name = 'Ideology') + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black')) + 
  plot_annotation(
    title = 'Box plot of log comments in hobby related subreddits',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

