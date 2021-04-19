# Literature Review Notes

## Broad Notes

The literature review could look at research in several different areas:
  1. Research in predicting traits from digital footprints.
  2. Research done into the determinants of ideology/predicting ideology 
  3. Research into classification/learning techniques for sparse, high dimensional datasets (obviously we are not coming up with new techniques but these might guide good models).
  4. Research into NLP techniques to gauge political sentiment (again, in order to find techniques to apply to the second stage of the project).
  5. Research on how different ideologies respond to different sorts of events (to see if our results cohere or not).

## Private traits and attributes are predictable from digital records of human behavior - Michal Kosinski, David Stillwell, and Thore Graepel

See: https://www.pnas.org/content/110/15/5802

Article has the following tags:
social networks | computational social science | machine learning | big data | data mining | psychological assessment

**Abstract:** *We show that easily accessible digital records of behavior, Facebook Likes, can be used to automatically and accurately predict a range of highly sensitive personal attributes including: sexual orientation, ethnicity, religious and political views, personality traits, intelligence, happiness, use of addictive substances, parental separation, age, and gender. The analysis presented is based on a dataset of over 58,000 volunteers who provided their Facebook Likes, detailed demographic profiles, and the results of several psychometric tests. The proposed model uses dimensionality reduction for preprocessing the Likes data, which are then entered into logistic/linear regression to predict individual psychodemographic profiles from Likes. The model correctly discriminates between homosexual and heterosexual men in 88% of cases, African Americans and Caucasian Americans in 95% of cases, and between Democrat and Republican in 85% of cases. For the personality trait “Openness,” prediction accuracy is close to the test–retest accuracy of a standard personality test. We give examples of associations between attributes and Likes and discuss implications for online personalization and privacy.*

* Kosinski notes that human activity frequnetly occurs via digital devices which leave records of an individuals' digital interactions.
* Notes that though some information on an individuals behaviour/actions is explicitly recorded through their digital activities, there is other information that can be statistically predicted from records of digital activities. 
* Notes that it has been shown that age, gender, occupation, education level and personality can be predicted from web browing logs. 
* Aimed at illustrating the possibility of estimating private personal attributes with a basic set of digital records, Kosinski et al. attempt to build predictive models of an individuals' private traits (sexual orientation, ethnic origin, political views, religion, personality, intelligence, satisfaction with life, drug use, alcohol use, tobacco use, maritial status of parents, age, gender, relationship status. and size and density of friendship network) based on said individuals' facebook likes. 
* Most relevant are the predictive models of personality and political views.
* Model of five factor model personality scores (20 item IPIP test) was trained on a set of 54,373 facebook users and their likes.
* Individuals are those for which 1 <= x ?<= 700 likes were available, median likes = 68.
* Model of political views (liberal/conservative') was trained on a a set of 9,752 facebook users and their likes (65% of samples liberal).
* Data is obtainde from volunteers via the myPersonality facebook app. Kosinski represented a users' digital footprint on facebook as a user-like matrix. Each row represents a user and each column represents a facebook page. A particular cell is assigned a value of 1 if the relevant user has liked the relevant facebook page and a value of 0 otherwise. Resulting in a sparse data matrix. 
* Kosinkski used SVD decomposition to reduce the dimensions of the user-like matrix. For personality and political views the top 100 SVD components were used as independent variables. 
* Political ideology was modelled using logistic regression. 
* Scores on 5 factors were modelled using linear regression.
* 10-fold CV used.
* Dems vs Republicans (I assume this is what liberal/conservative refered to) predicted with 0.85 AUC (10-fold CV).
* For the personality measures, the predictions were assesed on the basis of the pearson correlation between actual and predicted values.
* Openness r=0.43, extraversion r=0.4, agreeableness r=0.3, emotional stability r=0.3, conscientiousness r=0.29
* Kosinkski also ran predictive models based on randomly selected subsets of likes from 1 to 300 (subsetting observations to only include users with 300 or more likes). They illustrated that knowing likes increases accuracy with diminishing returns. 

**Direct notes on methodology:** (All direct quotes)

* "For the purpose of building a predictive model, Likes associated with fewer than 20 users, as well as users with fewer than two Likes, were removed from the sample. The remaining 58,466 users and 55,814 unique liked objects were arranged in a sparse matrix (user–Like matrix), the columns of which represent Likes and the rows of which represent users. The entries were set to 1 if there existed an association between a user and a Like and 0 otherwise. The matrix contained roughly 10 million associations between users and Likes. To facilitate the predictive analysis, the dimensionality of the user–Like matrix was reduced using singular-value decomposition (SVD) (6) such that each user is represented by a vector of k component scores."
* "We used the first k = 100 SVD components, which explained 28% of the variance in the user–Like matrix."
* Like this works' supporting docs, we could create tables that illustrate the relative popularity of certain subreddit interactions within different ideological subsets of our users (see: https://www.pnas.org/content/pnas/suppl/2013/03/07/1218772110.DCSupplemental/pnas.201218772SI.pdf) 

**Relevant notes from this paper:**

Kosinkski notes that the sample is limited: *"Individuals who declare their political and religious views, relationship status, and sexual orientation on their profile may be different from nondeclaring members of those groups; they may associate with distinct Likes, which may lead to an overestimate of prediction accuracies for these groups."

We can directly extend this study in many ways with reddit data:
* 1. many more samples for look into political views.
* 2. many more choices than just liberal/conservative, more complex 2-dimensional model of ideology.
* 3. more complicated methods than just logistic/linear regression can be used
* 4. we can extend user-like matrix to user-subreddit_interact, user-subreddit_freq, user-subreddit_totalscore, user-subreddit_averagescore




## Personality, Gender, and Age in the Language of Social Media: The Open-Vocabulary Approach - H. Andrew Schwartz, Johannes C. Eichstaedt,Margaret L. Kern,Lukasz Dziurzynski,Stephanie M. Ramones,Megha Agrawal,Achal Shah,Michal Kosinski,David Stillwell,Martin E. P. Seligman,Lyle H. Ungar

See: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0073791

**Abstract:** *We analyzed 700 million words, phrases, and topic instances collected from the Facebook messages of 75,000 volunteers, who also took standard personality tests, and found striking variations in language with personality, gender, and age. In our open-vocabulary technique, the data itself drives a comprehensive exploration of language that distinguishes people, finding connections that are not captured with traditional closed-vocabulary word-category analyses. Our analyses shed new light on psychosocial processes yielding results that are face valid (e.g., subjects living in high elevations talk about the mountains), tie in with other research (e.g., neurotic people disproportionately use the phrase ‘sick of’ and the word ‘depressed’), suggest new hypotheses (e.g., an active life implies emotional stability), and give detailed insights (males use the possessive ‘my’ when mentioning their ‘wife’ or ‘girlfriend’ more often than females use ‘my’ with ‘husband’ or 'boyfriend’). To date, this represents the largest study, by an order of magnitude, of language and personality.*

* Open-vocabulary analysis; looks at distinctive words and phrases as functions of traits by corellating individuals language used with their attributes. Rather than considering relationships between a pre-determined set of words and phrases and traits (closed-vocabulary analysis), the data itself drives the set of words and phrases which are linked to traits. 
* Differential language analysis (an open-vocabulary methodology) is used to find bits of language in social media posts that are indicative of different traits. 
* Words, phrases and topics are correlated with traits. 

* Personality characterised by the five factor model. 

* Overview of closed-vocabulary techniques to gain insight into psychology/other domains:
* Typical approach to analyzing language: count word useage for an apriori chosen set (words within a set contribute to score for that set).
* Commonly used typical approach is the linguistic inquiry and word count LIWC; it contains 64 different sets (categories of language). 
* This has a long history in psychology: Pennebaker & King analysed the diaries, writting assignments, etc. of people with different personalities and found the following:
    * agreeable people use more articles
    * neurotic people use more negative emotion words
* People have explored frequencies between democratic vs. republican speeches using Bayesian models w/ regularization and shrinkage (priors on word use).

* Research has also been done seeking to predict psychological (and other) outcomes based on language use:
* These predictive owrks are typicallynot concerned with 'individually distinguishing pieces of language' and are instead focussed on predictive accuracy.
* Words that are highly colinear with other words typically have htier weights penalised. 
* This paper is not soley focussed on a preditctive model and wishes to understand all the words that are correlated with personality in order to gain insight into personality types.

![image](https://user-images.githubusercontent.com/81718822/114502301-ea874000-9c6e-11eb-85a1-3885ada90196.png)

* From a set of social media messages they extract 'linguistic features' including both words and phrases (sequences of length 1-3) (24,530 features) and topics (derived from words using unsupervised learning) (500).
* Then each linguistic features is regressed on each dependent variable (trait).

* Closed vocabulary: counting words in a priori defined categories of language. 
* percentage of participants word in a given category is equal to the ratio of:
  * sum of the times ths subject has mentioned a word in the category AND
  * sum of frequency of all words used by the subject
* OLS is used to analyse the linkage between word category use and subject traits: trait ~ LIWC_1 + LIWC_2 + .... + controlling covariates(i.e. gender, age)
* Coeffecient of target explanatory variable is considered to represent the strength of the relationship. 

* Differential language analysis:
* Linguistic feature extraction:
* words determined by tokenizer. 
* phrases determined to PMI: log of ratio of joint probability of phrase (p(word1, word2, word 3) ?) and. indpendent probability of the phrase (p(word1)*p(word2)* p(word3))
* phrases with PMI > 2*length (length. := number of words in phrase) were kept


## FINISH THIS OFF!


DIRECT QUOTES:

"One should always be careful generalizing new results outside of the domain they were found as language is often dependent on context [40]"

"In other works, ideologies of political figures (i.e. conservative to liberal) have been predicted based on language using supervised techniques [58] or unsupervised inference of ideological space [59], [60]."


* Predictive model of ideology could form the basis of large scale inquiries into the language used by people of different ideologies: "Burger et al. scaled up the gender prediction over 184,000 Twitter authors by using automatically guessed gender based-on gender-specific keywords in profiles." 

* Might be working using this open vocab approach to exploring tthe differences betwteen political groups.

# PSYCH - DETERMINANTS OF PERSONALITY

## Personality and politics: The role of the HEXACO model of personality in predicting ideology and voting. - Antonio Chirumbolo, Luigi Leone

See: https://www.sciencedirect.com/science/article/pii/S0191886910001182

**Abstract:** *This paper investigates the impact of the HEXACO model of personality structure in predicting political ideology and voting. Five-hundred and seventeen participants provided responses for measures of the HEXACO and the Five Factor Models, ideological orientation, and past voting. Results showed that Conscientiousness was linked to voting for right-wing parties, whereas Honesty–Humility, Agreeableness and Openness were related to voting for left-wing parties. Ideological orientation mediated the relationship between personality traits and voting. Hierarchical tests indicated that the HEXACO outperformed the Five Factor Model in predicting ideological orientation.*

* Using a sample of 517 Italian adults, Chirumbolo and Leone demonstrate that the HEXACO model of personality and the Five Factor model of personality can be used to predict, or rather,  explain variation in,  an individual's ideology and voting behaviour. They note that a hierarchical regression model where HEXACO traits are added as additional predictors to the Five Factor Model contributes to a substantial increase in explained variance whilst the converse does not. 
* They found that honesty-humility, agreeableness and openess were more associated with left wing ideologies whilst consciensiousness was associated with conservative ideologies. Simmilar results were found for voting behaviour.
* Note that studies into psychological the determinatns of ideology are plagued by poor sample sizes and lack of statistical power - studies have demonstrated inconsistent results. 

* Ideology was modelled by the response to a 7-point q uestionaire with values ranging from 1: extreme left, to 7: extreme right. 
* Voting modelled as a binary variable (left wing or right wing vote) 


## Political conservatism as motivated social cognition - Jost, J. T., Glaser, J., Kruglanski, A. W., & Sulloway, F. J. 

See:https://psycnet.apa.org/record/2003-00782-003

**Abstract:** *Analyzing political conservatism as motivated social cognition integrates theories of personality (authoritarianism, dogmatism-intolerance of ambiguity), epistemic and existential needs (for closure, regulatory focus, terror management), and ideological rationalization (social dominance, system justification). A meta-analysis (88 samples, 12 countries, 22,818 cases) confirms that several psychological variables predict political conservatism: death anxiety (weighted mean r=.50); system instability (.47); dogmatism-intolerance of ambiguity (.34); openness to experience (-.32); uncertainty tolerance (-.27); needs for order, structure, and closure (.26); integrative complexity (-.20); fear of threat and loss (.18); and self-esteem (-.09). The core ideology of conservatism stresses resistance to change and justification of inequality and is motivated by needs that vary situationally and dispositionally to manage uncertainty and threat. (PsycINFO Database Record (c) 2016 APA, all rights reserved)*

* Jost etc. perform a meta-analysis of research into conservatism as a function of social cognition.
* They find that the following psychological traits have predictive power for conservatism: death anxiety, system instability, dogmatism-intolerance of ambiguity, openess to experience, uncertainity tolerance, needs for order, structure and closure, integrative compelxity, fear of threat and loss and self-esteem.

* Make sure to cover definitons of all the above traits. 
* These hobbies/interests may be reflective of these traits (i.e. people with trait X like hobby Y) providing a mechanism through which ideology is linked to digital footprint on reddit.

## Openness to Experience and Boundaries in the Mind: Relationships with Cultural and Economic Conservative Beliefs - Alain Van Hiel  Ivan Mervielde

See: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.0022-3506.2004.00276.x

**Abstract:** *The present research investigates whether Openness to Experience and Boundaries in the mind are related to conservatism. In the first study, significant relationships between several scales of the Boundaries in the mind questionnaire and indicators of conservative beliefs were obtained in an adult sample (N=78) as well as in a sample of political party activists (N=44). In the second study, these negative relationships between conservatism and thin boundaries were replicated in an adult sample (N=225). Moreover, two dimensions representing Boundaries in the mind were identified, one positively related to Openness to Experience and negatively to conservatism and the second showing high positive correlations with Neuroticism. The exceptionally strong correlations between conservatism and the Boundaries in the mind facet scales Opinions about organizations, Opinions about beauty, truth, Edges, lines, clothing and Opinions about peoples, nations, groups are discussed, as well as the weak relationships between economic conservatism and Openness to Experience.*

* Van Hiel and Mervielde illustrate that the results of Hartmann's Boundaries questionnaire can be used to predict conservatism.
* Some results expected, i.e. conservativism can be predicted by preference for clearly defined social structures but also some 'unexpected' results: conservatism positively associated with a preference for art with blurred edges and soft lines. 
* Looks at cultural conservatism and economic conservatism (in general, weaker correlations for economic conservatism with openess)

## Personality correlates of party preference: The Big Five in five big European countries - MicheleVecchioneaHaraldSchoenbJosé Luis GonzálezCastrocJanCieciuchdVassilisPavlopouloseGian VittorioCapraraa

See: https://www.sciencedirect.com/science/article/pii/S0191886911002911

**Abstract:** *The Big Five Model was used to assess the role of personality traits in orienting voting choice across five European countries (n = 1288). Findings from Italy, Spain, Germany, Greece, and Poland showed that the Big Five were linked to party preference in theoretically consistent ways. Traits had substantial effects on voting, whereas the socio-demographic characteristics of gender, age, income, and educational level had weaker influences. In each country, voters’ traits are seemingly congruent with the policies of their preferred party. The Openness trait has been shown to be the most generalizable predictor of party preference across the examined cultures. Conscientiousness was also a valid predictor, although its effect was less robust and replicable. Similarities and differences across countries were discussed and linked to the nature of the respective political discourses.*

* More powerful predictor than demographic traits
* Openess predicts liberal and left-wing views, conscientiousness predicts conservative and right-wing political views.
* "In a nutshell, vote choice is rooted in personality traits since citizens vote for parties whose ideological and policy stances fit their ideological preferences, that in turn are affected by basic personality dispositions."
* Openness - tolerance of new ideas, relates negatively with preferecnes for hierarhcy and oscial conformity - expected to increased likelihood of left wing.
* Consceintiousness - adherence to social rules, predicted to associated with support of right wing parties.
* Shows relationships between voting and demographics, gender, age and education are shown to be significantly correlated in some but not all countries. Openess correlated in most countries, conscientiousness only in germany.
* Fit logistic regression (hierarchical, demographic -> psychometric), change in pseudo R^2 due to adding traits varies a lot.
* Multinomial logistic regression used for third parties.
* Openness pretty robustly predicts left wing votes as does conscientiousness.
* end result: personality can be linked to voting in theoretically consistent manner,  socio-demographic features largely insignificant. 
* "Taken together, these findings suggest that the Big Five factors of personality may underlie citizens’ support for different parties, based on the policy issues they advocated."


* Conscientiousness and Openess are typically the most powerful predictors.

* Samples of conveniance 




* reserach is an extension as it doesn't focus on 'conservative/liberal' dichotomy but instead contains 2-axis (except Van Hiel and Mervielde).












