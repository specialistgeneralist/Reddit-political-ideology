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
      user.flair == 'authright' ~ 'right',      
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
      user.flair == 'authright' ~ 'auth',
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

set.seed(0)
wordcloud(words = left_df$word, freq = left_df$freq, min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          colors = brewer.pal(8, "Dark2"))

set.seed(0)
wordcloud(words = econ_center_df$word, freq = econ_center_df$freq, min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          colors = brewer.pal(8, "Dark2")) 

set.seed(0)
wordcloud(words = right_df$word, freq = right_df$freq, min.freq = 1,
          max.words = 200,
          random.order = FALSE,
          rot.per = 0.35,
          colors = brewer.pal(8, "Dark2"))


bar_left <- ggplot(left_df[1:20,], aes(x=reorder(factor(word), -freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('Term') +
  ylab('Frequency') +
  theme_bw() +
  ggtitle('Economically left wing users') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

bar_econ_center <- ggplot(econ_center_df[1:20,], aes(x=reorder(factor(word), -freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('Term') +
  ylab('Frequency') +
  theme_bw() +
  ggtitle('Economically centrist users') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

bar_right <- ggplot(right_df[1:20,], aes(x=reorder(factor(word), -freq), freq)) +     
  geom_col(position = 'dodge', color = 'black', fill = 'cyan') +
  xlab('Term') +
  ylab('Frequency') +
  theme_bw() +
  ggtitle('Economically right wing users') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

(bar_left + bar_econ_center + bar_right)+ 
  plot_annotation(
    title = 'Word Frequencies by economic ideology',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))























set.seed(0)
ggplot(
  left_df,
  aes(label = word, size = freq, color = freq)
) +
  geom_text_wordcloud_area() +
  scale_size_area(max_size = 24) +
  theme_bw() +
  scale_color_gradient(low = 'cyan', high = 'magenta')


ggwordcloud(left_df$word, left_df$freq)


install.packages('ggwordcloud')

output <- wordcloud(words = df$word, freq = df$freq, min.freq = 1,
                    max.words = 200,
                    random.order = FALSE,
                    rot.per = 0.35,
                    colors = brewer.pal(8, "Dark2"))




WordCloud <- function(problem, ideology){
  
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
  
  set.seed(0)
  
  output <- wordcloud(words = df$word, freq = df$freq, min.freq = 1,
            max.words = 200,
            random.order = FALSE,
            rot.per = 0.35,
            colors = brewer.pal(8, "Dark2"))
  
  return(output)
}


WC_left <- WordCloud(econ, 'left')
WC_cent <- WordCloud(econ, 'center')
WC_right <- WordCloud(econ, 'right')











