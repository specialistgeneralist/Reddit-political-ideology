library(tidyverse)
library(Matrix)
library(tm)
library(wordcloud)
library(patchwork)
library(ggwordcloud)
library(tidytext)

data = read_csv('/Volumes/Elements/Text/nlp_concat_data.csv') %>% 
  select(-X1) %>% 
  mutate(
    `user.flair` = case_when(
      user.flair == ':CENTG: - Centrist' ~  'centrist',
      user.flair == ':centrist: - Centrist' ~  'centrist',
      user.flair == ':centrist: - Grand Inquisitor' ~  'centrist',
      user.flair == ':left: - Left' ~  'left',
      user.flair == ':libright: - LibRight' ~  'libright',
      user.flair == ':libright2: - LibRight' ~  'libright',
      user.flair == ':right: - Right' ~  'right',
      user.flair == ':libleft: - LibLeft' ~  'libleft',
      user.flair == ':lib: - LibCenter' ~  'libcenter',
      user.flair == ':auth: - AuthCenter' ~  'authcenter',
      user.flair == ':authleft: - AuthLeft' ~  'authleft',
      user.flair == ':authright: - AuthRight' ~  'authright'),
    
    econ = case_when(
      user.flair == 'centrist' ~ 'center',
      user.flair == 'left' ~ 'left',
      user.flair == 'libright' ~ 'right',
      user.flair == 'right' ~ 'right',
      user.flair == 'libleft' ~ 'left',
      user.flair == 'libcenter' ~ 'center',
      user.flair == 'authcenter' ~ 'center',
      user.flair == 'authleft' ~ 'left',
      user.flair == 'authright' ~ 'right' 
    ),
    
    social = case_when(
      user.flair == 'centrist' ~ 'center',
      user.flair == 'left' ~ 'center',
      user.flair == 'libright' ~ 'lib',
      user.flair == 'right' ~ 'center',
      user.flair == 'libleft' ~ 'lib',
      user.flair == 'libcenter' ~ 'lib',
      user.flair == 'authcenter' ~ 'auth',
      user.flair == 'authleft' ~ 'auth',
      user.flair == 'authright' ~ 'auth'
    )
  ) %>%
  rename(all = `user.flair`)

CreateWFDF <- function(problem, ideology){
  
  problem <- enquo(problem)
  
  docs <- Corpus(VectorSource(filter(data, !!problem == ideology)$comment)) %>% 
    tm_map(removeNumbers) %>%
    tm_map(removePunctuation) %>%
    tm_map(stripWhitespace) %>% 
    tm_map(content_transformer(tolower)) %>%
    tm_map(removeWords, stopwords("english"))
  
  dtm <- removeSparseTerms(TermDocumentMatrix(docs), sparse = 0.99)
  matrix <- as.matrix(dtm)
  words <- sort(rowSums(matrix), decreasing = TRUE)
  df <- data.frame(word = names(words), freq = words) 
  
  return(df)
}

left_df <- CreateWFDF(econ, 'left') %>% filter_all(all_vars(!grepl("’", .))) %>% mutate(ideology = 'left')
econ_center_df <- CreateWFDF(econ, 'center') %>% filter_all(all_vars(!grepl("’", .))) %>% mutate(ideology = 'econ center')
right_df <- CreateWFDF(econ, 'right') %>% filter_all(all_vars(!grepl("’", .))) %>% mutate(ideology = 'right')
auth_df <- CreateWFDF(social, 'auth') %>% filter_all(all_vars(!grepl("’", .))) %>% mutate(ideology = 'auth')
social_center_df <- CreateWFDF(social, 'center') %>% filter_all(all_vars(!grepl("’", .))) %>% mutate(ideology = 'social center')
lib_df <- CreateWFDF(social, 'lib') %>% filter_all(all_vars(!grepl("’", .))) %>% mutate(ideology = 'lib') 

rbind(left_df[1:20,], 
      econ_center_df[1:20,],
      right_df[1:20,],
      auth_df[1:20,],
      social_center_df[1:20,],
      lib_df[1:20,]
      ) %>%
  mutate(ideology = factor(ideology, levels =
                             c('left', 'econ center', 'right',
                               'lib', 'social center', 'auth')),
         word = factor(word)) %>% 
  group_by(ideology) %>% 
  ggplot(aes(x=reorder_within(word, freq, ideology), y=freq)) +
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  theme_bw() +
  coord_flip() +
  facet_wrap(~ideology, scales = "free") +
  ggtitle('Word frequencies by ideology') +
  scale_x_reordered() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1, size = 10, color = 'black'),
        axis.text.y = element_text(size = 13, color = 'black'),
        plot.title  = element_text(size = 20, color = 'black'),
        strip.text.x = element_text(size = 20, color = 'black')) +
  xlab("") +
  ylab("")

ggsave("/Users/pkitc/Desktop/Michael/Thesis/Viz/word_freq.pdf", 
       width = 32, height = 20, units = "cm")
  


################################################################################
# Econ - WF

# set.seed(0)
# wordcloud(words = left_df$word, freq = left_df$freq, min.freq = 1,
#           max.words = 200,
#           random.order = FALSE,
#           rot.per = 0.35,
#           colors = brewer.pal(8, "Dark2"))
# 
# set.seed(0)
# wordcloud(words = econ_center_df$word, freq = econ_center_df$freq, min.freq = 1,
#           max.words = 200,
#           random.order = FALSE,
#           rot.per = 0.35,
#           colors = brewer.pal(8, "Dark2")) 
# 
# set.seed(0)
# wordcloud(words = right_df$word, freq = right_df$freq, min.freq = 1,
#           max.words = 200,
#           random.order = FALSE,
#           rot.per = 0.35,
#           colors = brewer.pal(8, "Dark2"))



################################################################################
################################################################################
# PRED
################################################################################
################################################################################

library(tidyverse)
library(wordcloud)
library(wordcloud2)

raw_data <- read_csv('/Volumes/Elements/Text/tf_idf_matrix.csv')

data <- raw_data %>% 
  mutate(
    econ.flair = case_when(
      user.flair == 'centrist' ~ 0,
      user.flair == 'left' ~ -1,
      user.flair == 'libright' ~ 1,
      user.flair == 'right' ~ 1,
      user.flair == 'libleft' ~  -1,
      user.flair == 'libcenter' ~ 0,
      user.flair == 'authcenter' ~ 0,
      user.flair == 'authleft' ~ -1,
      user.flair == 'authright' ~ 1),
    
    social.flair = case_when(
      user.flair == 'centrist' ~ 0,
      user.flair == 'left' ~ 0,
      user.flair == 'libright' ~ -1,
      user.flair == 'right' ~ 0,
      user.flair == 'libleft' ~ -1,
      user.flair == 'libcenter' ~ -1,
      user.flair == 'authcenter' ~ 1,
      user.flair == 'authleft' ~ 1,
      user.flair == 'authright' ~ 1)
  )

################################################################################
# ECON
################################################################################

econ_df <- data %>%
  select(-c(X1, `user.flair`, `social.flair`)) %>% 
  relocate(econ.flair) 

word_freq_econ <- as_tibble(cbind(colnames(econ_df)[-1] ,cor(econ_df[-1], econ_df$econ.flair)))
colnames(word_freq_econ) <- c('word', 'freq')
word_freq_econ$freq <- as.numeric(word_freq_econ$freq)
word_freq_econ <- word_freq_econ %>% 
  mutate(freq_r = freq,
         freq_l = -1*freq)


col_econ <- ggplot(arrange(word_freq_econ, desc(freq))[c(1:20,(6470-20):6470),], aes(x=reorder(factor(word), freq), freq)) +
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('Term') +
  ylab('Correlation') +
  theme_bw() +
  coord_flip() +
  ggtitle('predictors of economic ideology') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))


wc_econ_right <- arrange(word_freq_econ, desc(freq_r))[1:200,] %>% 
  ggplot(aes(label = word, size = freq_r^0.5, color = freq_r)) +
  geom_text_wordcloud_area(rm_outside = TRUE,
                           max_steps = 1,
                           grid_size = 1, 
                           eccentricity = .9,
                           seed = 0) +
  theme_minimal() +
  scale_color_gradient(low = "cyan", high = "magenta") + 
  ggtitle('right wing')

wc_econ_left <- arrange(word_freq_econ, desc(freq_l))[1:200,] %>% 
  ggplot(aes(label = word, size = freq_l^0.5, color = freq_l)) +
  geom_text_wordcloud_area(rm_outside = TRUE,
                           max_steps = 1,
                           grid_size = 1, 
                           eccentricity = .9,
                           seed = 0) +
  theme_minimal() +
  scale_color_gradient(low = "cyan", high = "magenta") + 
  ggtitle('left wing')

((wc_econ_right / wc_econ_left + plot_layout(guides = 'auto')) | col_econ) + 
  plot_annotation(
    title = 'Textual predictors of economic ideology',
  ) &
  theme(axis.text.x = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))
ggsave("/Users/pkitc/Desktop/Michael/Thesis/Viz/tf_idf_econ.pdf", 
       width = 32, height = 32, units = "cm")


################################################################################
# SOCIAL
################################################################################


social_df <- data %>%
  select(-c(X1, `user.flair`, `econ.flair`)) %>% 
  relocate(social.flair) 

word_freq_social <- as_tibble(cbind(colnames(social_df)[-1] ,cor(social_df[-1], social_df$social.flair)))
colnames(word_freq_social) <- c('word', 'freq')
word_freq_social$freq <- as.numeric(word_freq_social$freq)
word_freq_social <- word_freq_social %>% 
  mutate(freq_a = freq,
         freq_l = -1*freq)

col_social <- ggplot(arrange(word_freq_social, desc(freq))[c(1:20,(6470-20):6470),], aes(x=reorder(factor(word), freq), freq)) +
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('Term') +
  ylab('Correlation') +
  theme_bw() +
  coord_flip() +
  ggtitle('predictors of social ideology') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))


wc_social_auth <- arrange(word_freq_social, desc(freq_a))[1:200,] %>% 
  ggplot(aes(label = word, size = freq_a^0.5, color = freq_a)) +
  geom_text_wordcloud_area(rm_outside = TRUE,
                           max_steps = 1,
                           grid_size = 1, 
                           eccentricity = .9,
                           seed = 0) +
  theme_minimal() +
  scale_color_gradient(low = "cyan", high = "magenta") + 
  ggtitle('authoritarian')

wc_social_lib <- arrange(word_freq_social, desc(freq_l))[1:200,] %>% 
  ggplot(aes(label = word, size = freq_l^0.5, color = freq_l)) +
  geom_text_wordcloud_area(rm_outside = TRUE,
                           max_steps = 1,
                           grid_size = 1, 
                           eccentricity = .9,
                           seed = 0) +
  theme_minimal() +
  scale_color_gradient(low = "cyan", high = "magenta") + 
  ggtitle('libertarian')

((wc_social_auth / wc_social_lib + plot_layout(guides = 'auto')) | col_social) + 
  plot_annotation(
    title = 'Textual predictors of social ideology',
  ) &
  theme(axis.text.x = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))
ggsave("/Users/pkitc/Desktop/Michael/Thesis/Viz/tf_idf_social.pdf", 
       width = 32, height = 32, units = "cm")

