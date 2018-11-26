new_american = read.csv('vegas_sme_dataset.csv')

names(new_american[31]) # review_count
names(new_american[32]) # stars
names(new_american[90]) # negative_reviews
names(new_american[91]) # neutral_reviews
names(new_american[92]) # positive_reviews

# set variable as factor except review_count, stars, negative_reviews, neutral_reviews, positive_reviews
lapply(new_american[1:30], factor)
lapply(new_american[32:89], factor)

#### 1st MODEL
#### Backward elimintation for y = review_count, but check the model is robust or not 1st ####
reviewsss = lm(review_count ~ ambience_romantic + ambience_intimate + ambience_classy
               + ambience_hipster + ambience_touristy + ambience_trendy + ambience_upscale + ambience_casual
               + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast 
               + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
               + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
               + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood, data=new_american)
plot(reviewsss)

log_reviewsss = lm(log(review_count) ~ ambience_romantic + ambience_intimate + ambience_classy
               + ambience_hipster + ambience_touristy + ambience_trendy + ambience_upscale + ambience_casual
               + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast 
               + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
               + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
               + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood, data=new_american)
plot(log_reviewsss) # better than previous

summary(log_reviewsss)
anova(log_reviewsss) # remove ambience_upscale, good_for_latenight, parking_street, noise_loud

log_reviewsss2 = lm(log(review_count) ~ ambience_romantic + ambience_intimate + ambience_classy
                   + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                   + good_for_dessert + good_for_lunch + good_for_dinner + good_for_breakfast 
                   + good_for_brunch + parking_garage + parking_validated + parking_lot + parking_valet
                   + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
                   + noise_very_loud + noise_quiet + noise_average + neighborhood, data=new_american)
anova(log_reviewsss2) # remove ambience_intimate, remove parking_validated

log_reviewsss3 = lm(log(review_count) ~ ambience_romantic + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dessert + good_for_lunch + good_for_dinner + good_for_breakfast 
                    + good_for_brunch + parking_garage + parking_lot + parking_valet
                    + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
                    + noise_very_loud + noise_quiet + noise_average + neighborhood, data=new_american)
anova(log_reviewsss3) # ambience_romantic, parking_valet, none, noise_very_loud, smoking_outdoor

log_reviewsss4 = lm(log(review_count) ~ ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dessert + good_for_lunch + good_for_dinner + good_for_breakfast 
                    + good_for_brunch + parking_garage + parking_lot
                    + full_bar + beer_and_wine + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
                    + noise_quiet + noise_average + neighborhood, data=new_american)
anova(log_reviewsss4) # remove full_bar, beer_and_wine

log_reviewsss5 = lm(log(review_count) ~ ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dessert + good_for_lunch + good_for_dinner + good_for_breakfast 
                    + good_for_brunch + parking_garage + parking_lot
                    + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
                    + noise_quiet + 
                      
                      noise_average + neighborhood, data=new_american)
anova(log_reviewsss5)
summary(log_reviewsss5) ### FINAL MODEL
plot(log_reviewsss5)



#### 2nd MODEL
#### Backward elimintation for y = stars, but check the model is robust or not 1st ####
stars_reviews = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                   + ambience_hipster + ambience_touristy + ambience_trendy + ambience_upscale + ambience_casual
                   + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast + review_count
                   + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
                   + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
                   + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood + negative_reviews 
                   + neutral_reviews + positive_reviews, data=new_american)
plot(stars_reviews)
summary(stars_reviews) # can we fit a better model?

log_stars_reviews = lm(log(stars) ~ ambience_romantic + ambience_intimate + ambience_classy
                       + ambience_hipster + ambience_touristy + ambience_trendy + ambience_upscale + ambience_casual
                       + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast + review_count
                       + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
                       + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
                       + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood + negative_reviews 
                       + neutral_reviews + positive_reviews, data=new_american)
plot(log_stars_reviews)
summary(log_stars_reviews) # do not employ!

squared_root_stars_reviews = lm(stars^0.5 ~ ambience_romantic + ambience_intimate + ambience_classy
                                + ambience_hipster + ambience_touristy + ambience_trendy + ambience_upscale + ambience_casual
                                + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast + review_count
                                + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
                                + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
                                + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood + negative_reviews 
                                + neutral_reviews + positive_reviews, data=new_american)
plot(squared_root_stars_reviews) # do not employ!
summary(squared_root_stars_reviews)


anova(stars_reviews) # remove wifi_no, neutral_reviews

stars_reviews2 = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_upscale + ambience_casual
                    + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
                    + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_paid
                    + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood + negative_reviews 
                    + positive_reviews, data=new_american)
anova(stars_reviews2) # remove smoking_no, ambience_upscale


stars_reviews3 = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
                    + none + full_bar + beer_and_wine + smoking_outdoor + smoking_yes + wifi_free + wifi_paid
                    + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood + negative_reviews 
                    + positive_reviews, data=new_american)
anova(stars_reviews3) # remove parking_validated, smoking_outdoor, noise_loud, noise_very_loud

stars_reviews4 = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_lot + parking_valet
                    + none + full_bar + beer_and_wine + smoking_yes + wifi_free + wifi_paid
                    + noise_quiet + noise_average + neighborhood + negative_reviews 
                    + positive_reviews, data=new_american)
anova(stars_reviews4) # remove beer_and_wine, wifi_paid

stars_reviews5 = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_lot + parking_valet
                    + none + full_bar + smoking_yes + wifi_free
                    + noise_quiet + noise_average + neighborhood + negative_reviews 
                    + positive_reviews, data=new_american)
anova(stars_reviews5) # remove good_for_dessert, none, positive_reviews

stars_reviews6 = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_lot + parking_valet
                    + full_bar + smoking_yes + wifi_free + noise_quiet + noise_average 
                    + neighborhood + negative_reviews, data=new_american)
anova(stars_reviews6) # remove good_for_lunch

stars_reviews7 = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_latenight + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_lot + parking_valet
                    + full_bar + smoking_yes + wifi_free + noise_quiet + noise_average 
                    + neighborhood + negative_reviews, data=new_american)
anova(stars_reviews7) # good_for_latenight

stars_reviews8 = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_lot + parking_valet
                    + full_bar + smoking_yes + wifi_free + noise_quiet + noise_average 
                    + neighborhood + negative_reviews, data=new_american)
anova(stars_reviews8) # remoce noise_average

stars_reviews9 = lm(stars ~ ambience_romantic + ambience_intimate + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_lot + parking_valet
                    + full_bar + smoking_yes + wifi_free + noise_quiet 
                    + neighborhood + negative_reviews, data=new_american)
anova(stars_reviews9) # rmove ambience_intimate

stars_reviews10 = lm(stars ~ ambience_romantic + ambience_classy
                    + ambience_hipster + ambience_touristy + ambience_trendy + ambience_casual
                    + good_for_dinner + good_for_breakfast + review_count
                    + good_for_brunch + parking_garage + parking_street + parking_lot + parking_valet
                    + full_bar + smoking_yes + wifi_free + noise_quiet 
                    + neighborhood + negative_reviews, data=new_american)
anova(stars_reviews10) # rmove ambience_touristy, parking_valet, wifi_free

stars_reviews11 = lm(stars ~ ambience_romantic + ambience_classy
                     + ambience_hipster + ambience_trendy + ambience_casual
                     + good_for_dinner + good_for_breakfast + review_count
                     + good_for_brunch + parking_garage + parking_street + parking_lot
                     + full_bar + smoking_yes + noise_quiet 
                     + neighborhood + negative_reviews, data=new_american)
anova(stars_reviews11) # rmove good_for_dinner

stars_reviews12 = lm(stars ~ ambience_romantic + ambience_classy
                     + ambience_hipster + ambience_trendy + ambience_casual
                     + good_for_breakfast + review_count
                     + good_for_brunch + parking_garage + parking_street + parking_lot
                     + full_bar + smoking_yes + noise_quiet 
                     + neighborhood + negative_reviews, data=new_american)
anova(stars_reviews12) # remove full_bar, smoking_yes

stars_reviews12 = lm(stars ~ ambience_romantic + ambience_classy + ambience_hipster + ambience_trendy 
                     + ambience_casual + good_for_breakfast + review_count + good_for_brunch 
                     + parking_garage + parking_street + parking_lot + noise_quiet 
                     + neighborhood + negative_reviews, data=new_american)
anova(stars_reviews12) # FINAL MODEL
summary(stars_reviews12) # Adjusted R-squared:  0.3018 

######################################################
#### Model y = stars, x = 3 other type of reviews ####
star_review_type = lm(stars ~ negative_reviews + neutral_reviews + positive_reviews, data = new_american)
summary(star_review_type) # adjusted R-squared: 0.2343 # not linear
plot(star_review_type)

log_star_review_type = lm(log(stars) ~ negative_reviews + neutral_reviews + positive_reviews, data = new_american)
plot(log_star_review_type) # worse
summary(log_star_review_type)

sqdrt_star_review_type = lm(stars^0.5 ~ negative_reviews + neutral_reviews + positive_reviews, data = new_american)
plot(sqdrt_star_review_type)  # worse

##################################################################################################
#### Backward elimintation for y = negative_reviews, but check the model is robust or not 1st ####
neg_reviews = lm(negative_reviews ~ ambience_romantic + ambience_intimate + ambience_classy
                   + ambience_hipster + ambience_touristy + ambience_trendy + ambience_upscale + ambience_casual
                   + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast 
                   + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
                   + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
                   + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood, data=new_american)
plot(neg_reviews)
anova(neg_reviews)
summary(neg_reviews)

#log_neg_reviews = lm(negative_reviews ~ exp(ambience_romantic + ambience_intimate + ambience_classy
#                     + ambience_hipster + ambience_touristy + ambience_trendy + ambience_upscale + ambience_casual
#                     + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast 
#                     + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
#                     + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no + wifi_paid
#                     + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood), data=new_american)
#plot(log_neg_reviews)

neg_reviews2 = lm(negative_reviews ~ ambience_romantic + ambience_intimate + ambience_classy
                 + ambience_touristy + ambience_trendy + ambience_casual
                 + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast 
                 + good_for_brunch + parking_garage + parking_street + parking_validated + parking_lot + parking_valet
                 + none + full_bar + beer_and_wine + smoking_outdoor + smoking_no + smoking_yes + wifi_free + wifi_no
                 + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood, data=new_american)
anova(neg_reviews2)

neg_reviews3 = lm(negative_reviews ~ ambience_romantic + ambience_intimate + ambience_classy
                  + ambience_touristy + ambience_trendy + ambience_casual
                  + good_for_dessert + good_for_latenight + good_for_lunch + good_for_dinner + good_for_breakfast 
                  + parking_garage + parking_street + parking_lot + parking_valet
                  + none + full_bar + smoking_outdoor + smoking_no + smoking_yes + wifi_no
                  + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood, data=new_american)
anova(neg_reviews3)

neg_reviews4 = lm(negative_reviews ~ ambience_romantic + ambience_intimate + ambience_classy
                  + ambience_touristy + ambience_trendy + ambience_casual
                  + good_for_dessert + good_for_lunch + good_for_dinner + good_for_breakfast 
                  + parking_garage + parking_street + parking_lot + 
                  + full_bar + smoking_outdoor + smoking_no + smoking_yes + wifi_no
                  + noise_very_loud + noise_loud + noise_quiet + noise_average + neighborhood, data=new_american)
anova(neg_reviews4)

neg_reviews5 = lm(negative_reviews ~ ambience_romantic + ambience_intimate
                  + ambience_touristy + ambience_trendy + ambience_casual
                  + good_for_dessert + good_for_lunch + good_for_dinner + good_for_breakfast 
                  + parking_garage + parking_street + parking_lot + 
                  + full_bar + smoking_outdoor + smoking_yes + wifi_no
                  + noise_very_loud + noise_quiet + noise_average + neighborhood, data=new_american)
anova(neg_reviews5)

neg_reviews6 = lm(negative_reviews ~ ambience_romantic
                  + ambience_touristy + ambience_casual
                  + good_for_dessert + good_for_lunch + good_for_dinner 
                  + parking_garage + parking_street + parking_lot + 
                  + full_bar + smoking_outdoor + smoking_yes + wifi_no
                  + noise_quiet + neighborhood, data=new_american)
anova(neg_reviews6)

neg_reviews7 = lm(negative_reviews ~ ambience_touristy + ambience_casual
                  + good_for_lunch + good_for_dinner + parking_garage
                  + full_bar + smoking_outdoor + smoking_yes + wifi_no
                  + noise_quiet + neighborhood, data=new_american)
anova(neg_reviews7)

neg_reviews8 = lm(negative_reviews ~ ambience_touristy + ambience_casual
                  + good_for_lunch + good_for_dinner + parking_garage
                  + full_bar + smoking_yes + wifi_no
                  + noise_quiet + neighborhood, data=new_american)
anova(neg_reviews8)

neg_reviews9 = lm(negative_reviews ~ ambience_touristy + ambience_casual
                  + good_for_lunch + good_for_dinner + parking_garage
                  + smoking_yes + wifi_no
                  + noise_quiet + neighborhood, data=new_american)
anova(neg_reviews9)

neg_reviews10 = lm(negative_reviews ~ ambience_touristy + ambience_casual
                  + good_for_lunch + parking_garage + smoking_yes
                  + noise_quiet + neighborhood, data=new_american)
anova(neg_reviews10)
summary(neg_reviews10) # Adjusted R-squared:  0.1715 
plot(neg_reviews10)
