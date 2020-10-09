library(dplyr)
library(tidyverse)

####This script calculates the linear and multiple regressions between 
####the age predictor Mean Tip Length and each environmental 
####predictor for Africa.

##Reading file
africa_complete <- read.csv("africa_v83.csv")
head(africa_complete)

##Removing NA values for the columns we are using
dropped_africa_complete_tip <- drop_na(africa_complete, temp_distance, 
                                       precip_distance, Bioclim_1, 
                                       Bioclim_7, Bioclim_12, Bioclim_17, 
                                       Elevation, Coarse_fragment,
                                       Ph_x_10, Sand, Organic_content, 
                                       Mean.Tip.Length)

##Filtering out values equal to 0 or below for the variables: organic content,
##elevation, coarse fragment, sand percent, and Mean.Tip.Length. Values above 
##300 were also filtered for Mean.Tip.Length.
##Filtering out values = "Inf" for the variable temperature distance.
dropped_africa_complete_filtered_tip <-dropped_africa_complete_tip %>% 
  filter(Organic_content > 0) %>% 
  filter(Elevation > 0) %>% 
  filter(Coarse_fragment > 0) %>% 
  filter(Sand > 0) %>% 
  filter(temp_distance != "Inf") %>% 
  filter(Mean.Tip.Length > 0) %>% 
  filter(Mean.Tip.Length < 300)

##Calculating correlations, plotting linear regression graphs, and 
##producing and saving summary statistics for all the variables selected:

####Temp_distance
cor_Temp_dist_tip <- cor(dropped_africa_complete_filtered_tip$temp_distance, 
                         dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Temp_dist_tip <- lm(Mean.Tip.Length ~ temp_distance, 
                          data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(temp_distance, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Temperature distance", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Temp_dist_Africa_tips_updated_2.txt")
summary(model_Temp_dist_tip)
sink()

####Precip_distance
cor_Precip_distance_tip <- cor(dropped_africa_complete_filtered_tip$precip_distance, 
                               dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Precip_distance_tip <- lm(Mean.Tip.Length ~ precip_distance, 
                                data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(precip_distance, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Precipitation distance", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Precip_distance_Africa_tips_updated_2.txt")
summary(model_Precip_distance_tip)
sink()

#####Bioclim_1
cor_Bioclim_1_tip <- cor(dropped_africa_complete_filtered_tip$Bioclim_1, 
                         dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_1_tip <- lm(Mean.Tip.Length ~ Bioclim_1, 
                          data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Bioclim_1, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Annual Mean Temperature", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_1_Africa_tips_updated_2.txt")
summary(model_Bioclim_1_tip)
sink()

#####Bioclim_7
cor_Bioclim_7_tip <- cor(dropped_africa_complete_filtered_tip$Bioclim_7, 
                         dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_7_tip <- lm(Mean.Tip.Length ~ Bioclim_7, 
                          data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Bioclim_7, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Temperature Annual Range", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_7_Africa_tips_updated_2.txt")
summary(model_Bioclim_7_tip)
sink()

#####Bioclim_12
cor_Bioclim_12_tip <- cor(dropped_africa_complete_filtered_tip$Bioclim_12, 
                          dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_12_tip <- lm(Mean.Tip.Length ~ Bioclim_12, 
                           data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Bioclim_12, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Annual Precipitation", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_12_Africa_tips_updated_2.txt")
summary(model_Bioclim_12_tip)
sink()

#####Bioclim_17
cor_Bioclim_17_tip <- cor(dropped_africa_complete_filtered_tip$Bioclim_17, 
                          dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_17_tip <- lm(Mean.Tip.Length ~ Bioclim_17, 
                           data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Bioclim_17, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Precipitation of Driest Quarter", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_17_Africa_tips_updated_2.txt")
summary(model_Bioclim_17_tip)
sink()

#####Elevation
cor_Elevation_tip <- cor(dropped_africa_complete_filtered_tip$Elevation, 
                         dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Elevation_tip <- lm(Mean.Tip.Length ~ Elevation, 
                          data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Elevation, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Elevation", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Elevation_Africa_tips_updated_2.txt")
summary(model_Elevation_tip)
sink()

#####Coarse_fragment
cor_Coarse_fragment_tip <- cor(dropped_africa_complete_filtered_tip$Coarse_fragment, 
                               dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Coarse_fragment_tip <- lm(Mean.Tip.Length ~ Coarse_fragment, 
                                data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Coarse_fragment, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Coarse fragment", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Coarse_fragment_Africa_tips_updated_2.txt")
summary(model_Coarse_fragment_tip)
sink()

#####Soil_ph
cor_Soil_ph_tip <- cor(dropped_africa_complete_filtered_tip$Ph_x_10, 
                       dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Soil_ph_tip <- lm(Mean.Tip.Length ~ Ph_x_10, 
                        data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Ph_x_10, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Soil pH", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Soil_ph_Africa_tips_updated_2.txt")
summary(model_Soil_ph_tip)
sink()

#####Sand_content
cor_Sand_percent_tip <- cor(dropped_africa_complete_filtered_tip$Sand, 
                            dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Sand_content_tip <- lm(Mean.Tip.Length ~ Sand, 
                             data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Sand, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Sand percent", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Sand_content_Africa_tips_updated_2.txt")
summary(model_Sand_content_tip)
sink()

#####Organic_carbon
cor_Organic_carbon_tip <- cor(dropped_africa_complete_filtered_tip$Organic_content, 
                              dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Organic_carbon_tip <- lm(Mean.Tip.Length ~ Organic_content, 
                               data = dropped_africa_complete_filtered_tip)

ggplot(dropped_africa_complete_filtered_tip, aes(Organic_content, 
                                                 Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Organic carbon", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12)) +
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Organic_carbon_Africa_tips_updated_2.txt")
summary(model_Organic_carbon_tip)
sink()


###Multiple regression
##Calculating mulitple regression correlations and saving summary statistics 
##for the 4 combinations of variables selected:

###Mean Tip Length for all variables
model_Mean.Tip.Length_Africa_tips <- lm(Mean.Tip.Length ~ temp_distance + precip_distance + Bioclim_1 * 
                                          Bioclim_7 * Bioclim_12 * Bioclim_17 + Coarse_fragment * 
                                          Organic_content * Ph_x_10 * Sand + Elevation,
                                        data = dropped_africa_complete_filtered_tip)

sink("model_Mean.Tip.Length_Africa_tips_updated_2.txt")
summary(model_Mean.Tip.Length_Africa_tips)
sink()
AIC_model_Mean.Tip.Length_Africa_tips <- AIC(model_Mean.Tip.Length_Africa_tips)

###Mean Tip Length for climate distance variables
model_Mean.Tip.Length_climate_Africa_tips <- lm(Mean.Tip.Length ~ temp_distance + precip_distance,
                                                data = dropped_africa_complete_filtered_tip)

sink("model_Mean.Tip.Length_climate_Africa_tips_updated_2.txt")
summary(model_Mean.Tip.Length_climate_Africa_tips)
sink()
AIC_model_Mean.Tip.Length_climate_Africa_tips <- AIC(model_Mean.Tip.Length_climate_Africa_tips)

###Mean Tip Length for Bioclim variables
model_Mean.Tip.Length_Bioclim_Africa_tips <- lm(Mean.Tip.Length ~ Bioclim_1 * Bioclim_7 * Bioclim_12 * 
                                                  Bioclim_17, data = dropped_africa_complete_filtered_tip)

sink("model_Mean.Tip.Length_Bioclim_Africa_tips_updated_2.txt")
summary(model_Mean.Tip.Length_Bioclim_Africa_tips)
sink()
AIC_model_Mean.Tip.Length_Bioclim_Africa_tips <- AIC(model_Mean.Tip.Length_Bioclim_Africa_tips)

###Mean Tip Length for soil variables
model_Mean.Tip.Length_soil_Africa_tips <- lm(Mean.Tip.Length ~ Coarse_fragment * Organic_content * 
                                               Ph_x_10 * Sand, 
                                             data = dropped_africa_complete_filtered_tip)

sink("model_Mean.Tip.Length_soil_Africa_tips_updated_2.txt")
summary(model_Mean.Tip.Length_soil_Africa_tips)
sink()
AIC_model_Mean.Tip.Length_soil_Africa_tips <- AIC(model_Mean.Tip.Length_soil_Africa_tips)
