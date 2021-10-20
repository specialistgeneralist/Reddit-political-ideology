library(tidyverse)
library(viridis)  
library(kableExtra)
library(patchwork)

# set working directory
setwd('~/Desktop/WORK/Monash/Thesis/Data collection/Complete Data')

# load  data
user_flair <- read_csv('user_flair.csv') 

# get a sense of how many duplicate flairs
unique(user_flair$flair)  

# rename flairs  in a more simple way and combine duplicates
user_flair$flair <- recode(user_flair$flair, `:CENTG: - Centrist` =  "centrist")
user_flair$flair <- recode(user_flair$flair, `:centrist: - Centrist` =  "centrist")
user_flair$flair <- recode(user_flair$flair, `:centrist: - Grand Inquisitor` =  "centrist")
user_flair$flair <- recode(user_flair$flair, `:left: - Left` =  "left")
user_flair$flair <- recode(user_flair$flair, `:libright: - LibRight` =  "libright")
user_flair$flair <- recode(user_flair$flair, `:libright2: - LibRight` =  "libright")
user_flair$flair <- recode(user_flair$flair, `:right: - Right` =  "right")
user_flair$flair <- recode(user_flair$flair, `:libleft: - LibLeft` =  "libleft")
user_flair$flair <- recode(user_flair$flair, `:lib: - LibCenter` =  "libcenter")
user_flair$flair <- recode(user_flair$flair, `:auth: - AuthCenter` =  "authcenter")
user_flair$flair <- recode(user_flair$flair, `:authleft: - AuthLeft` =  "authleft")
user_flair$flair <- recode(user_flair$flair, `:authright: - AuthRight` =  "authright")

# check we have  removed all duplicates
unique(user_flair$flair)  

# create function to order classes by freq
reorder_size <- function(x) {
  factor(x, levels = names(sort(table(x), decreasing = TRUE)))
}

# create  a frequency  table
table(reorder_size(user_flair$flair)) %>% t() %>%
  kable("latex", caption = "Idelogy frequency in sample (n = 91,000)") %>%
  kable_styling(full_width = FALSE)

# create a proportion table
prop.table(table(reorder_size(user_flair$flair))) %>% t() %>%
  kable("latex", caption = "Idelogy frequency in sample (n = 91,000)", digits  = 2) %>%
  kable_styling(full_width = FALSE)

# create ordered barcharts of frequency and proportion
# create chart for frequency
freq_ideology_barchart  <- ggplot(user_flair, aes(x = reorder_size(flair))) +
  geom_bar(fill = 'cyan',color='black') +
  xlab("Ideology") +
  ylab('Frequency')  +
  theme_bw() +
  plot_annotation(
    title = 'Frequency of ideology',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text( size = 20, color = 'black'))
ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/response_freq.pdf", 
       width = 32, height = 20, units = "cm")
