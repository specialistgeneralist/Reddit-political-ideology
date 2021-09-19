library(tidyverse)
library(matrix)
library(tm)
library(wordcloud)
library(patchwork)
library(ggwordcloud)

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

left_df <- CreateWFDF(econ, 'left') %>% filter_all(all_vars(!grepl("’", .)))
econ_center_df <- CreateWFDF(econ, 'center') %>% filter_all(all_vars(!grepl("’", .)))
right_df <- CreateWFDF(econ, 'right') %>% filter_all(all_vars(!grepl("’", .)))

auth_df <- CreateWFDF(social, 'auth') %>% filter_all(all_vars(!grepl("’", .)))
social_center_df <- CreateWFDF(social, 'center') %>% filter_all(all_vars(!grepl("’", .)))
lib_df <- CreateWFDF(social, 'lib') %>% filter_all(all_vars(!grepl("’", .)))

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


bar_left <- ggplot(left_df[1:20,], aes(x=reorder(factor(word), freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('') +
  ylab('') +
  theme_bw() +
  coord_flip() +
  ggtitle('economically left') 

bar_econ_center <- ggplot(econ_center_df[1:20,], aes(x=reorder(factor(word), freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('') +
  ylab('') +
  theme_bw() +
  coord_flip() +
  ggtitle('economically centrist') 

bar_right <- ggplot(right_df[1:20,], aes(x=reorder(factor(word), freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('') +
  ylab('') +
  theme_bw() +
  coord_flip() +
  ggtitle('economically right') 

(bar_left + bar_econ_center + bar_right)+ 
  plot_annotation(
    title = 'Word frequencies by economic ideology',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))
ggsave("/Users/pkitc/Desktop/Michael/Thesis/Viz/econ_word_freq.pdf", 
       width = 32, height = 20, units = "cm")


bar_lib <- ggplot(lib_df[1:20,], aes(x=reorder(factor(word), freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('') +
  ylab('') +
  theme_bw() +
  coord_flip() +
  ggtitle('socially libertarian') 

bar_social_center <- ggplot(social_center_df[1:20,], aes(x=reorder(factor(word), freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('') +
  ylab('') +
  theme_bw() +
  coord_flip() +
  ggtitle('socially centrist') 

bar_auth <- ggplot(auth_df[1:20,], aes(x=reorder(factor(word), freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('') +
  ylab('') +
  theme_bw() +
  coord_flip() +
  ggtitle('socially authoritarian') 

(bar_lib + bar_social_center + bar_auth)+ 
  plot_annotation(
    title = 'Word frequencies by social ideology',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))
ggsave("/Users/pkitc/Desktop/Michael/Thesis/Viz/social_word_freq.pdf", 
       width = 32, height = 20, units = "cm")


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

set.seed(0)
wordcloud(words = word_freq_econ$word, 
          freq = word_freq_econ$freq_r, 
          min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          scale=c(1.25,.45),
          colors = colorRampPalette(c("cyan", "magenta"))(8))

set.seed(0)
wordcloud(words = word_freq_econ$word, 
          freq = word_freq_econ$freq_l, 
          min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          scale=c(1.25,.45),
          colors = colorRampPalette(c("cyan", "magenta"))(8))

ggplot(arrange(word_freq_econ, desc(freq))[c(1:20,(6470-20):6470),], aes(x=reorder(factor(word), freq), freq)) +
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('Term') +
  ylab('Correlation') +
  theme_bw() +
  coord_flip() +
  ggtitle('Predictors of economic ideology') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

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

set.seed(0)
wordcloud(words = word_freq_social$word, 
          freq = word_freq_social$freq_a, 
          min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          scale=c(1.25,.45),
          colors = colorRampPalette(c("cyan", "magenta"))(8))

set.seed(0)
wordcloud(words = word_freq_social$word, 
          freq = word_freq_social$freq_l, 
          min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          scale=c(1.25,.45),
          colors = colorRampPalette(c("cyan", "magenta"))(8))

ggplot(arrange(word_freq_social, desc(freq))[c(1:20,(6470-20):6470),], aes(x=reorder(factor(word), freq), freq)) +
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('Term') +
  ylab('Correlation') +
  theme_bw() +
  coord_flip() +
  ggtitle('Predictors of economic ideology') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))



