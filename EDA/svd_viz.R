library(tidyverse)
library(patchwork)

data <- read_csv('/Users/pkitc/Desktop/Michael/Thesis/data/results/svd_data.csv') %>% 
  select(-X1) %>%
  mutate(
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

colnames(data) <- c('all',1:1000, 'econ', 'social')

#################################################################################
# ECON
#################################################################################

p1 <- data %>% 
  ggplot(aes(x=`1`, y=`2`, color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

p2 <- data %>% 
  ggplot(aes(x=`3`, y=`4`,   color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

p3 <- data %>% 
  ggplot(aes(x=`5`, y=`6`,   color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

p4 <- data %>% 
  ggplot(aes(x=`7`, y=`8`,   color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

p5 <- data %>% 
  ggplot(aes(x=`9`, y=`10`,   color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

p6 <- data %>% 
  ggplot(aes(x=`11`, y=`12`,   color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

p7 <- data %>% 
  ggplot(aes(x=`13`, y=`14`,   color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

p8 <- data %>% 
  ggplot(aes(x=`15`, y=`16`,   color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

p9 <- data %>% 
  ggplot(aes(x=`17`, y=`18`,   color =econ)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("gray",  'magenta', "cyan")) + 
  theme_bw()

(p1 + p2 + p3)/(p4 + p5 + p6)/(p7 + p8 + p9) + plot_annotation(
  title = 'Users in SVD space',
  subtitle = "Leftwing (magenta), rightwing (cyan) and centrist (grey) users from training and validation set in SVD component space"
) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        legend.position = "None",
        text = element_text(family = 'serif', face =  'bold', size = 16))

ggsave("/Users/pkitc/Desktop/Michael/Thesis/Viz/econ_svd_9.pdf", 
       width = 32, height = 32, units = "cm")

p3 + 
  xlab('SVD component 5') +
  ylab('SVD component 6') +
  plot_annotation(
    title = 'Users in SVD space',
    subtitle = "Leftwing (magenta), rightwing (cyan) and centrist (grey) users in SVD space"
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        legend.position = "None",
        text = element_text(family = 'serif', face =  'bold', size = 20))

ggsave("/Users/pkitc/Desktop/Michael/Thesis/Viz/svd_scatterplot.pdf", 
       width = 32, height = 20, units = "cm")

#################################################################################
# SOCIAL
#################################################################################

p1 <- data %>% 
  ggplot(aes(x=`1`, y=`2`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

p2 <- data %>% 
  ggplot(aes(x=`3`, y=`4`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

p3 <- data %>% 
  ggplot(aes(x=`5`, y=`6`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

p4 <- data %>% 
  ggplot(aes(x=`7`, y=`8`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

p5 <- data %>% 
  ggplot(aes(x=`9`, y=`10`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

p6 <- data %>% 
  ggplot(aes(x=`11`, y=`12`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

p7 <- data %>% 
  ggplot(aes(x=`13`, y=`14`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

p8 <- data %>% 
  ggplot(aes(x=`15`, y=`16`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

p9 <- data %>% 
  ggplot(aes(x=`17`, y=`18`,   color =social)) +
  geom_point(alpha = 0.2, shape = 18, size = 5) +
  scale_color_manual(values=c("magenta", "grey", "cyan")) + 
  theme_bw()

(p1 + p2 + p3)/(p4 + p5 + p6)/(p7 + p8 + p9) + plot_annotation(
  title = 'Users in SVD space',
  subtitle = "Authoritarian (magenta), libertarian (cyan) and centrist (grey)  users from training and validation set in SVD component space"
) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        axis.text.y = element_text(color = 'black'),
        legend.position = "None",
        text = element_text(family = 'serif', face =  'bold', size = 16))



ggsave("/Users/pkitc/Desktop/Michael/Thesis/Viz/social_svd_9.pdf", 
       width = 32, height = 32, units = "cm")
