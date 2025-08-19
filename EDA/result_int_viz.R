library(tidyverse)
library(patchwork)

all_class <- read_csv('all_int_results.csv') %>%
  rename(model_name = X1)
all_class <- as_tibble(cbind(nms = colnames(all_class ), t(all_class)))
colnames(all_class ) <- all_class [1,] 
all_class  <- all_class  %>% 
  select(-model) %>%
  slice(-1) %>%
  rename(acc = accuracy) %>%
  mutate(acc = as.numeric(acc),
         auc = as.numeric(auc),
         model_name = case_when(
           model_name == 'multinomial_l1' ~ 'Multinomial w L1',
           model_name == 'multinomial' ~ 'Multinomial',
           model_name == 'ovr_logreg_l1' ~ 'OVR logistic w L1',
           model_name == 'ovr_logreg' ~ 'OVR logistic',
           model_name == 'adaboost' ~ 'AdaBoost',
           model_name == 'rf' ~ 'Random forest',
           model_name == 'ovr_rf' ~ 'OVR Random forest',
           model_name == 'zero_r' ~ 'Zero R'
         )
  )


econ_class <- read_csv('econ_int_results.csv') %>%
  rename(model_name = X1)
econ_class <- as_tibble(cbind(nms = colnames(econ_class ), t(econ_class)))
colnames(econ_class ) <- econ_class [1,] 
econ_class  <- econ_class  %>% 
  select(-model) %>%
  slice(-1) %>%
  rename(acc = accuracy) %>%
  mutate(acc = as.numeric(acc),
         auc = as.numeric(auc),
         model_name = case_when(
           model_name == 'multinomial_l1' ~ 'Multinomial w L1',
           model_name == 'multinomial' ~ 'Multinomial',
           model_name == 'ovr_logreg_l1' ~ 'OVR logistic w L1',
           model_name == 'ovr_logreg' ~ 'OVR logistic',
           model_name == 'adaboost' ~ 'AdaBoost',
           model_name == 'rf' ~ 'Random forest',
           model_name == 'ovr_rf' ~ 'OVR Random forest',
           model_name == 'zero_r' ~ 'Zero R'
         )
  )

social_class <- read_csv('social_int_results.csv') %>%
  rename(model_name = X1)
social_class <- as_tibble(cbind(nms = colnames(social_class ), t(social_class)))
colnames(social_class ) <- social_class [1,] 
social_class  <- social_class  %>% 
  select(-model) %>%
  slice(-1) %>%
  rename(acc = accuracy) %>%
  mutate(acc = as.numeric(acc),
         auc = as.numeric(auc),
         model_name = case_when(
           model_name == 'multinomial_l1' ~ 'Multinomial w L1',
           model_name == 'multinomial' ~ 'Multinomial',
           model_name == 'ovr_logreg_l1' ~ 'OVR logistic w L1',
           model_name == 'ovr_logreg' ~ 'OVR logistic',
           model_name == 'adaboost' ~ 'AdaBoost',
           model_name == 'rf' ~ 'Random forest',
           model_name == 'ovr_rf' ~ 'OVR Random forest',
           model_name == 'zero_r' ~ 'Zero R'
         )
  )

# **************************** Nine-class user int *****************************

p1 <- all_class %>% filter(model_name != 'Zero R') %>% 
  ggplot(aes(x=reorder(model_name, -acc ), y=acc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = as.numeric(all_class[1,2]), linetype = "dashed", size = 1.5, color = "red") +
  ylab('Accuracy') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

p2 <- all_class %>% filter(model_name != 'Zero R') %>% 
  ggplot(aes(x=reorder(model_name, -auc ), y=auc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = 0.5, linetype = "dashed", color = "red", size = 1.5) +
  ylab('ROC-AUC') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

(p1 +  p2) + 
  plot_annotation(
    title = 'All Class Classification',
    subtitle = 'Accuracy and weighted ROC-AUC for models in the nine class problem',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

ggsave("~/Desktop/WORK/Monash/Thesis/Data collection/EDA/nine_int_acc_auc.pdf", 
       width = 32, height = 20, units = "cm")

# **************************** econ user int *****************************

p3 <- econ_class %>% filter(model_name != 'Zero R') %>% 
  ggplot(aes(x=reorder(model_name, -acc ), y=acc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = as.numeric(econ_class[1,2]), linetype = "dashed", color = "red", size = 1.5) +
  ylab('Accuracy') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

p4 <- econ_class %>% filter(model_name != 'Zero R') %>% 
  ggplot(aes(x=reorder(model_name, -auc ), y=auc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = 0.5, linetype = "dashed", color = "red", size = 1.5) +
  ylab('ROC-AUC') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

(p3 +  p4) + 
  plot_annotation(
    title = 'Economic Classification',
    subtitle = 'Accuracy and weighted ROC-AUC for models in the economic problem',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

ggsave("econ_int_acc_auc.pdf", 
       width = 32, height = 20, units = "cm")

# **************************** social user int *****************************

p5 <- social_class %>% filter(model_name != 'Zero R') %>% 
  ggplot(aes(x=reorder(model_name, -acc ), y=acc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = as.numeric(social_class[1,2]), linetype = "dashed", color = "red", size = 1.5) +
  ylab('Accuracy') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

p6 <- social_class %>% filter(model_name != 'Zero R') %>% 
  ggplot(aes(x=reorder(model_name, -auc ), y=auc)) +
  geom_col(, color="black", fill = "cyan") +
  geom_hline(yintercept = 0.5, linetype = "dashed", color = "red", size = 1.5) +
  ylab('ROC-AUC') +
  xlab('') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

(p5 +  p6) + 
  plot_annotation(
    title = 'Social Classification',
    subtitle = 'Accuracy and weighted ROC-AUC for models in the economic problem',
  ) &
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,  color = 'black'),
        text = element_text(family = 'serif', face =  'bold', size = 20, color = 'black'))

ggsave("social_int_acc_auc.pdf", 
       width = 32, height = 20, units = "cm")
