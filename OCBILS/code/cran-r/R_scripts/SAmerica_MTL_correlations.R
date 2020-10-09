library(dplyr)
library(tidyverse)

####This script calculates the linear and multiple regressions between 
####the age predictor Mean Tip Length and each environmental 
####predictor for South America.

##Reading file
samerica_complete <- read.csv("south_america_stats_cj_mod.csv")
head(samerica_complete)

##Removing NA values for the columns we are using
dropped_samerica_complete_tip <- drop_na(samerica_complete, Temp_distance, 
                                     Precip_distance, Bioclim_1, 
                                     Bioclim_7, Bioclim_12, Bioclim_17, 
                                     Elevation, Coarse_fragment,
                                     Soil_ph, Sand_content,Organic_carbon, 
                                     Mean.Tip.Length)

##Filtering out values equal to 0 or below for the variables: organic content,
##elevation, coarse fragment and sand percent. Filtering out values = "Inf"
##for the variable temperature distance.
dropped_samerica_complete_filtered_tip <-dropped_samerica_complete_tip %>% 
  filter(Organic_carbon > 0) %>% 
  filter(Elevation > 0) %>% 
  filter(Coarse_fragment > 0) %>% 
  filter(Sand_content > 0) %>% 
  filter(Temp_distance != "Inf")

##Calculating correlations, plotting linear regression graphs, and 
##producing and saving summary statistics for all the variables selected:

####Temp_distance
cor_Temp_dist_tip <- cor(dropped_samerica_complete_filtered_tip$Temp_distance, 
                     dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Temp_dist_tip <- lm(Mean.Tip.Length ~ Temp_distance, 
                      data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Temp_distance, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Temperature distance", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Temp_dist_SAmerica_tips.txt")
summary(model_Temp_dist_tip)
sink()

####Precip_distance
cor_Precip_distance_tip <- cor(dropped_samerica_complete_filtered_tip$Precip_distance, 
                           dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Precip_distance_tip <- lm(Mean.Tip.Length ~ Precip_distance, 
                            data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Precip_distance, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Precipitation distance", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Precip_distance_SAmerica_tips.txt")
summary(model_Precip_distance_tip)
sink()

#####Bioclim_1
cor_Bioclim_1_tip <- cor(dropped_samerica_complete_filtered_tip$Bioclim_1, 
                     dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_1_tip <- lm(Mean.Tip.Length ~ Bioclim_1, 
                      data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Bioclim_1, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Bioclim 1", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_1_SAmerica_tips.txt")
summary(model_Bioclim_1_tip)
sink()

#####Bioclim_7
cor_Bioclim_7_tip <- cor(dropped_samerica_complete_filtered_tip$Bioclim_7, 
                     dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_7_tip <- lm(Mean.Tip.Length ~ Bioclim_7, 
                      data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Bioclim_7, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Bioclim 7", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_7_SAmerica_tips.txt")
summary(model_Bioclim_7_tip)
sink()

#####Bioclim_12
cor_Bioclim_12_tip <- cor(dropped_samerica_complete_filtered_tip$Bioclim_12, 
                      dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_12_tip <- lm(Mean.Tip.Length ~ Bioclim_12, 
                       data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Bioclim_12, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Bioclim 12", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_12_SAmerica_tips.txt")
summary(model_Bioclim_12_tip)
sink()

#####Bioclim_17
cor_Bioclim_17_tip <- cor(dropped_samerica_complete_filtered_tip$Bioclim_17, 
                      dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_17_tip <- lm(Mean.Tip.Length ~ Bioclim_17, 
                       data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Bioclim_17, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Bioclim 17", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_17_SAmerica_tips.txt")
summary(model_Bioclim_17_tip)
sink()

#####Elevation
cor_Elevation_tip <- cor(dropped_samerica_complete_filtered_tip$Elevation, 
                     dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Elevation_tip <- lm(Mean.Tip.Length ~ Elevation, 
                      data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Elevation, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Elevation", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Elevation_SAmerica_tips.txt")
summary(model_Elevation_tip)
sink()

#####Coarse_fragment
cor_Coarse_fragment_tip <- cor(dropped_samerica_complete_filtered_tip$Coarse_fragment, 
                           dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Coarse_fragment_tip <- lm(Mean.Tip.Length ~ Coarse_fragment, 
                            data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Coarse_fragment, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Coarse fragment", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Coarse_fragment_SAmerica_tips.txt")
summary(model_Coarse_fragment_tip)
sink()

#####Soil_ph
cor_Soil_ph_tip <- cor(dropped_samerica_complete_filtered_tip$Soil_ph, 
                   dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Soil_ph_tip <- lm(Mean.Tip.Length ~ Soil_ph, 
                    data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Soil_ph, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Soil pH", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Soil_ph_SAmerica_tips.txt")
summary(model_Soil_ph_tip)
sink()

#####Sand_content
cor_Sand_percent_tip <- cor(dropped_samerica_complete_filtered_tip$Sand_content, 
                        dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Sand_content_tip <- lm(Mean.Tip.Length ~ Sand_content, 
                         data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Sand_content, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Sand percent", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Sand_content_SAmerica_tips.txt")
summary(model_Sand_content_tip)
sink()

#####Organic_carbon
cor_Organic_carbon_tip <- cor(dropped_samerica_complete_filtered_tip$Organic_carbon, 
                          dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Organic_carbon_tip <- lm(Mean.Tip.Length ~ Organic_carbon, 
                           data = dropped_samerica_complete_filtered_tip)

ggplot(dropped_samerica_complete_filtered_tip, aes(Organic_carbon, 
                                                   Mean.Tip.Length)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Organic carbon", y= "Mean Tip Length") +
  theme(axis.title = element_text(size = 12)) +
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Organic_carbon_SAmerica_tips.txt")
summary(model_Organic_carbon_tip)
sink()


###Multiple regression
##Calculating mulitple regression correlations and saving summary statistics 
##for the 4 combinations of variables selected:

###Mean Tip Length for all variables
model_Mean.Tip.Length_SAmerica_tips <- lm(Mean.Tip.Length ~ Temp_distance + Precip_distance + Bioclim_1 * 
                               Bioclim_7 * Bioclim_12 * Bioclim_17 + Coarse_fragment * 
                               Organic_carbon * Soil_ph * Sand_content + Elevation,
                             data = dropped_samerica_complete_filtered_tip)

sink("model_Mean.Tip.Length_SAmerica_tips.txt")
summary(model_Mean.Tip.Length_SAmerica_tips)
sink()
AIC_model_Mean.Tip.Length_SAmerica_tips <- AIC(model_Mean.Tip.Length_SAmerica_tips)


###Mean Tip Length for climate distance variables
model_Mean.Tip.Length_climate_SAmerica_tips <- lm(Mean.Tip.Length ~ Temp_distance + Precip_distance,
                        data = dropped_samerica_complete_filtered_tip)

sink("model_Mean.Tip.Length_climate_SAmerica_tips.txt")
summary(model_Mean.Tip.Length_climate_SAmerica_tips)
sink()
AIC_model_Mean.Tip.Length_climate_SAmerica_tips <- AIC(model_Mean.Tip.Length_climate_SAmerica_tips)


###Mean Tip Length for Bioclim variables
model_Mean.Tip.Length_Bioclim_SAmerica_tips <- lm(Mean.Tip.Length ~ Bioclim_1 * Bioclim_7 * Bioclim_12 * 
                          Bioclim_17, data = dropped_samerica_complete_filtered_tip)

sink("model_Mean.Tip.Length_Bioclim_SAmerica_tips.txt")
summary(model_Mean.Tip.Length_Bioclim_SAmerica_tips)
sink()
AIC_model_Mean.Tip.Length_Bioclim_SAmerica_tips <- AIC(model_Mean.Tip.Length_Bioclim_SAmerica_tips)


###Mean Tip Length for soil variables
model_Mean.Tip.Length_soil_SAmerica_tips <- lm(Mean.Tip.Length ~ Coarse_fragment * Organic_carbon * 
                       Soil_ph * Sand_content, 
                     data = dropped_samerica_complete_filtered_tip)

sink("model_Mean.Tip.Length_soil_SAmerica_tips.txt")
summary(model_Mean.Tip.Length_soil_SAmerica_tips)
sink()
AIC_model_Mean.Tip.Length_soil_SAmerica_tips <- AIC(model_Mean.Tip.Length_soil_SAmerica_tips)
