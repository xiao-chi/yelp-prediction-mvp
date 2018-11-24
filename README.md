# yelp-prediction-mvp
MVP for a Yelp product that provides suggestions to small businesses (restaurants) in Las Vegas, NV to improve their Yelp rating by at least 1 star. 

Authors:  
Apostolis Gnardellis  
Bhagya Sharma  
Faizal Masrol  
Kacy Chou  
Xiao Chi Tu  
Yizhe Xu  

Steps  
Run yelpBusinessFeatureRestructure to perform feature engineering on all business features provided by Yelp. This file requires 'yelp_academic_dataset_business.json' to be present in dataset folder. (For access to this file, ask a team member)

Run yelpAmericanReviewSentiment Analysis to perform sentiment analysis and calculate number of postive/negative/netural reviews per business. This file requires 'american_reviews.csv' to be present in dataset folder. (For access to this file, ask a team member)

Run yelpFinalBusinessFeatureSetWithSentimentAnalysis to combine results from previous 2 steps. This file runs on csv files created from previous 2 steps.
