library(tidyverse)
library(Matrix)
library(tm)
library(wordcloud)
library(patchwork)
library(ggwordcloud)
library(wordcloud)
library(tidytext)
library(gridExtra)
library(gridGraphics)
library(ggplotify)

################################################################################
# FREQUENCIES
################################################################################

data = read_csv('nlp_concat_data.csv') %>% 
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

ggsave("word_freq.pdf", 
       width = 32, height = 20, units = "cm")
  

################################################################################
# WORDCLOUD
################################################################################

raw_data <- read_csv('tf_idf_matrix.csv')

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

econ_df <- data %>%
  select(-c(X1, `user.flair`, `social.flair`)) %>% 
  relocate(econ.flair) 

word_freq_econ <- as_tibble(cbind(colnames(econ_df)[-1] ,cor(econ_df[-1], econ_df$econ.flair)))
colnames(word_freq_econ) <- c('word', 'freq')
word_freq_econ$freq <- as.numeric(word_freq_econ$freq)
word_freq_econ <- word_freq_econ %>% 
  mutate(freq_r = freq,
         freq_l = -1*freq)

social_df <- data %>%
  select(-c(X1, `user.flair`, `econ.flair`)) %>% 
  relocate(social.flair) 

word_freq_social <- as_tibble(cbind(colnames(social_df)[-1] ,cor(social_df[-1], social_df$social.flair)))
colnames(word_freq_social) <- c('word', 'freq')
word_freq_social$freq <- as.numeric(word_freq_social$freq)
word_freq_social <- word_freq_social %>% 
  mutate(freq_a = freq,
         freq_l = -1*freq)


# Econ right
set.seed(0)
plot1 <- wordcloud(words = word_freq_econ$word, freq = word_freq_econ$freq_r, min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          scale = c(3, 3*(1/30)),
          colors = colorRampPalette(c("cyan", "magenta"))(8))
grid.echo()
p1 <- as.ggplot(grid.grab()) + ggtitle("economic - right")  + theme(plot.title = element_text(hjust = 0.5, size = 20))

# Econ left
set.seed(0)
plot2 <- wordcloud(words = word_freq_econ$word, freq = word_freq_econ$freq_l, min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          scale = c(2, 2*(1/30)),
          colors = colorRampPalette(c("cyan", "magenta"))(8))
grid.echo()
p2 <- as.ggplot(grid.grab()) + ggtitle("economic - left")  + theme(plot.title = element_text(hjust = 0.5, size = 20))



# Social auth
set.seed(0)
plot3 <- wordcloud(words = word_freq_social$word, freq = word_freq_social$freq_a, min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          scale = c(2, 2*(1/30)),
          colors = colorRampPalette(c("cyan", "magenta"))(8))
grid.echo()
p3 <- as.ggplot(grid.grab()) + ggtitle("social - auth")  + theme(plot.title = element_text(hjust = 0.5, size = 20))


# Social lib
set.seed(0)
plot4 <- wordcloud(words = word_freq_social$word, freq = word_freq_social$freq_l, min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          scale = c(2, 2*(1/30)),
          colors = colorRampPalette(c("cyan", "magenta"))(8))
grid.echo()
p4 <- as.ggplot(grid.grab()) + ggtitle("social - lib") + theme(plot.title = element_text(hjust = 0.5, size = 20))


(p1 + p2)/(p3+p4) + 
  plot_annotation(
    title = 'Textual predictors of ideology',
  ) &
  theme(
        text = element_text(size = 20, color = 'black'))
ggsave("wordclouds.pdf", 
       width = 40, height = 40, units = "cm")
