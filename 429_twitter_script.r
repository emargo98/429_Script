# MAY HAVE TO "install.packages("<name>")" these
library(tidyverse)
library(twitteR)
library(tidytext)
library(glue)
library(stringr)
library(lubridate)
# If needed
# install.packages("vader")
library(vader)
library(SentimentAnalysis)

# Twitter Auth
setup_twitter_oauth(consumer_key    = "vDhzMo5yo1lIdRsSMFQkCWKmb", 
                    consumer_secret  = "<INSERT SECRET KEY>",
                    access_token     = "90768200-Qsi1DK0lOceLq3wkqoh6v7Nxdmu9DJIVDh3z4bPZz",
                    access_secret    = "<INSERT SECRET KEY>")

## CHANGE THIS
# List of users to track
users <- c("BillSimmons", "AdamSchefter", "wojespn", "mortreport", "realmikewilbon", "darrenrovell", "stoolpresidente", "stephenasmith", "RealSkipBayless","jemelehill")

# Output tab;e
responses = NULL
# Loop through users
for(i in 1:length(users)){
  # Get query string for mention
  queryString = paste0("to:", users[i])
  # Get Tweets and convert to DF
  rply = searchTwitter(queryString, sinceID = Id, n=150,  retryOnRateLimit=10) 
  rply = twListToDF(rply) %>% mutate(respond = users[i])
  # Append it to overal response table
  responses = rbind(responses, rply)
}
responses <- responses %>% mutate(respond = as.factor(respond))

# Function to get sentiment score of text string
GetSent <- function(text){
  # Strip text and reformat as data frame with one word in each row
  #d <- strsplit(gsub("[^[:alnum:] ]", "", text), " +")[[1]] %>% as.data.frame()
  # Rename column to allow for inner join
  #names(d)[1] = "word"
  # Return frame with sentiment score for text string
  #sent <- d %>% inner_join(get_sentiments("afinn"))
  
  # VADER
  x <- get_vader(text)
  return(as.numeric(x[2]))
}

# Vector to store sentiment scores
sent_scores <- c()
# Loop through replies data frame
for(i in 1:nrow(responses)){
  # Get sentiment data frame
  sents <- GetSent(responses[i,1])
  # Get score from individual response
  # score <- sum(sents$value)
  # Append it to the sentiment score vector
  sent_scores <- append(sent_scores, sents)
}
# Add Sentiment scores to data table
responses_w_sent <- responses %>% cbind(sent_score = sent_scores) %>% mutate(created=ymd_hms(created))




# Ploting Data
scatter <- ggplot(data=responses_w_sent) + geom_jitter(mapping=aes(x=created, y=sent_score, color=respond)) + labs(x="Date", y= "Sentiment Score", color="Twitter Handle") + ggtitle("Sentiment Analysis - Recent Mentions of Sports Journalists")

box <- ggplot(data=responses_w_sent) + geom_boxplot(mapping=aes(x=respond, y=sent_score)) +coord_flip()
#responses_w_sent %>% summary()


# Saving Data
write_csv(responses_w_sent, "recent_mentions.csv")
ggsave("recent_mentions_sentiment_scatter.jpg", plot=scatter)
ggsave("recent_mentions_sentiment_box.jpg", plot=box)

