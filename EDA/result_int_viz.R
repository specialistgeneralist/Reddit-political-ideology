library(tidyverse)
library(patchwork)

# **************************** Nine-class user int *****************************

nine_class <- tibble(
  `model` = c('OVR random forest', 'Random forest', 'AdaBoost', 'OVR logistic w. L1',
           'Multinomial w. L1', 'OVR logistic', 'Multinomial','Zero R'),
  `acc` = c(0.294, 0.283, 0.27, 0.245, 0.244, 0.243, 0.235, 0.206),
  `auc` = c( 0.675, 0.657, 0.651, 0.677, 0.672, 0.68, 0.686, NA))

p1 <- nine_class %>% filter(model != 'Zero R') %>% 
  ggplot(aes(x=reorder(model, -acc ), y=acc)) +
  geom_col(, color="black", fill = "green") +
  geom_hline(yintercept = 0.206, linetype = "dashed", color = "red") +
  ylab('Accuracy') +
  xlab('Model') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

p2 <- nine_class %>% filter(model != 'Zero R') %>% 
  ggplot(aes(x=reorder(model, -auc ), y=auc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = 0.5, linetype = "dashed", color = "magenta") +
  ylab('ROC-AUC') +
  xlab('Model') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

p1 + p2

# **************************** econ user int *****************************

econ_class <- tibble(
  `model` = c('OVR logistic w L1','OVR logistic', 'Multinomial w L1',	'Multinomial',	'OVR Random forest',	
  'Random forest',	'AdaBoost',	'Zero R'),
  `acc` = c(0.52,	0.52,	0.519,	0.518,	0.505,	0.502,	0.499,	0.363),
  `auc` = c(0.713,	0.713,	0.713,	0.713,	0.693,	0.687,	0.683, NA))

p3 <- econ_class %>% filter(model != 'Zero R') %>% 
  ggplot(aes(x=reorder(model, -acc ), y=acc)) +
  geom_col(, color="black", fill = "green") +
  geom_hline(yintercept = 0.363, linetype = "dashed", color = "red") +
  ylab('Accuracy') +
  xlab('Model') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

p4 <- econ_class %>% filter(model != 'Zero R') %>% 
  ggplot(aes(x=reorder(model, -auc ), y=auc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = 0.5, linetype = "dashed", color = "magenta") +
  ylab('ROC-AUC') +
  xlab('Model') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))


p3 +  p4

# **************************** social user int *****************************

social_class <- tibble(
  `model` = c('OVR Random forest',	'Random forest',	'AdaBoost',	'Zero R', 'OVR logistic with L1',	'OVR logistic',
    'Multinomial w L1',	'Multinomial'),
  `acc` = c(0.538,	0.537,	0.536,	0.523,	0.469,	0.446,	0.439,	0.438),
  `auc` = c(0.636,	0.627,	0.616,  NA,		0.641,	0.643,	0.641,	0.639))

p5 <- social_class %>% filter(model != 'Zero R') %>% 
  ggplot(aes(x=reorder(model, -acc ), y=acc)) +
  geom_col(, color="black", fill = "green") +
  geom_hline(yintercept = 0.523, linetype = "dashed", color = "red") +
  ylab('Accuracy') +
  xlab('Model') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))

p6 <- social_class %>% filter(model != 'Zero R') %>% 
  ggplot(aes(x=reorder(model, -auc ), y=auc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = 0.5, linetype = "dashed", color = "magenta") +
  ylab('ROC-AUC') +
  xlab('Model') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 16, color = 'black'))


p5 + p6











