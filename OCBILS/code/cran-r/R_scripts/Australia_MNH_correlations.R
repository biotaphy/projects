library(dplyr)
library(tidyverse)

####This script calculates the linear and multiple regressions between 
####the age predictor Mean Node Height and each environmental 
####predictor for Australia.

##Reading file
australia_complete <- read.csv("australia_stats_cj_mod.csv")
head(australia_complete)

##Removing NA values for the columns we are using
dropped_australia_complete <- drop_na(australia_complete, Temp_distance, 
                                      Precip_distance, Bioclim_1, 
                                      Bioclim_7, Bioclim_12, Bioclim_17, 
                                      Elevation, Coarse_fragment,
                                      Ph_x_10, Sand_percent, Organic_content, 
                                      Mean.Node.Height)

##Filtering out values equal to 0 or below for the variables: organic content,
##elevation, coarse fragment and sand percent. Filtering out values = "Inf"
##for the variable temperature distance.
dropped_australia_complete_filtered <-dropped_australia_complete %>% 
  filter(Organic_content > 0) %>% 
  filter(Elevation > 0) %>% 
  filter(Coarse_fragment > 0) %>% 
  filter(Sand_percent > 0) %>% 
  filter(Temp_distance != "Inf") 

##Calculating correlations, plotting linear regression graphs, and 
##producing and saving summary statistics for all the variables selected:

####Temp_distance
cor_Temp_dist <- cor(dropped_australia_complete_filtered$Temp_distance, 
                     dropped_australia_complete_filtered$Mean.Node.Height)

model_Temp_dist <- lm(Mean.Node.Height ~ Temp_distance, 
                      data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Temp_distance, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Temperature distance", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Temp_dist_Australia_nodes.txt")
summary(model_Temp_dist)
sink()

####Precip_distance
cor_Precip_distance <- cor(dropped_australia_complete_filtered$Precip_distance, 
                           dropped_australia_complete_filtered$Mean.Node.Height)

model_Precip_distance <- lm(Mean.Node.Height ~ Precip_distance, 
                            data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Precip_distance, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Precipitation distance", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Precip_dist_Australia_nodes.txt")
summary(model_Precip_distance)
sink()

#####Bioclim_1
cor_Bioclim_1 <- cor(dropped_australia_complete_filtered$Bioclim_1, 
                     dropped_australia_complete_filtered$Mean.Node.Height)

model_Bioclim_1 <- lm(Mean.Node.Height ~ Bioclim_1, 
                      data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Bioclim_1, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Annual Mean Temperature", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_1_Australia_nodes.txt")
summary(model_Bioclim_1)
sink()

#####Bioclim_7
cor_Bioclim_7 <- cor(dropped_australia_complete_filtered$Bioclim_7, 
                     dropped_australia_complete_filtered$Mean.Node.Height)

model_Bioclim_7 <- lm(Mean.Node.Height ~ Bioclim_7, 
                      data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Bioclim_7, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Temperature Annual Range", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_7_Australia_nodes.txt")
summary(model_Bioclim_7)
sink()

#####Bioclim_12
cor_Bioclim_12 <- cor(dropped_australia_complete_filtered$Bioclim_12, 
                      dropped_australia_complete_filtered$Mean.Node.Height)

model_Bioclim_12 <- lm(Mean.Node.Height ~ Bioclim_12, 
                       data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Bioclim_12, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Annual Precipitation", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_12_Australia_nodes.txt")
summary(model_Bioclim_12)
sink()

#####Bioclim_17
cor_Bioclim_17 <- cor(dropped_australia_complete_filtered$Bioclim_17, 
                      dropped_australia_complete_filtered$Mean.Node.Height)

model_Bioclim_17 <- lm(Mean.Node.Height ~ Bioclim_17, 
                       data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Bioclim_17, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Precipitation of Driest Quarter", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_17_Australia_nodes.txt")
summary(model_Bioclim_17)
sink()

#####Elevation
cor_Elevation <- cor(dropped_australia_complete_filtered$Elevation, 
                     dropped_australia_complete_filtered$Mean.Node.Height)

model_Elevation <- lm(Mean.Node.Height ~ Elevation, 
                      data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Elevation, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Elevation", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Elevation_Australia_nodes.txt")
summary(model_Elevation)
sink()

#####Coarse_fragment
cor_Coarse_fragment <- cor(dropped_australia_complete_filtered$Coarse_fragment, 
                           dropped_australia_complete_filtered$Mean.Node.Height)

model_Coarse_fragment <- lm(Mean.Node.Height ~ Coarse_fragment, 
                            data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Coarse_fragment, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Coarse fragment", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Coarse_fragment_Australia_nodes.txt")
summary(model_Coarse_fragment)
sink()

#####Ph_x_10
cor_Ph_x_10 <- cor(dropped_australia_complete_filtered$Ph_x_10, 
                   dropped_australia_complete_filtered$Mean.Node.Height)

model_Ph_x_10 <- lm(Mean.Node.Height ~ Ph_x_10, 
                    data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Ph_x_10, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Soil pH", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Soil_ph_Australia_nodes.txt")
summary(model_Ph_x_10)
sink()

#####Sand_percent
cor_Sand_percent <- cor(dropped_australia_complete_filtered$Sand_percent, 
                        dropped_australia_complete_filtered$Mean.Node.Height)

model_Sand_percent <- lm(Mean.Node.Height ~ Sand_percent, 
                         data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Sand_percent, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Sand percent", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Sand_percent_Australia_nodes.txt")
summary(model_Sand_percent)
sink()

#####Organic_content
cor_Organic_content <- cor(dropped_australia_complete_filtered$Organic_content, 
                           dropped_australia_complete_filtered$Mean.Node.Height)

model_Organic_content <- lm(Mean.Node.Height ~ Organic_content, 
                            data = dropped_australia_complete_filtered)

ggplot(dropped_australia_complete_filtered, aes(Organic_content, 
                                                Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Organic carbon", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12)) +
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Organic_content_Australia_nodes.txt")
summary(model_Organic_content)
sink()


###Multiple regression
##Calculating mulitple regression correlations and saving summary statistics 
##for the 4 combinations of variables selected:

###Mean Node Height for all variables
model_Mean.Node.Height <- lm(Mean.Node.Height ~ Temp_distance + Precip_distance + Bioclim_1 * 
                               Bioclim_7 * Bioclim_12 * Bioclim_17 + Coarse_fragment * 
                               Organic_content * Ph_x_10 * Sand_percent + Elevation,
                             data = dropped_australia_complete_filtered)

sink("model_Mean.Node.Height_Australia.txt")
summary(model_Mean.Node.Height)
sink()
AIC_model_Mean.Node.Height <- AIC(model_Mean.Node.Height)


###Mean Node Height for climate distance variables
model_MND_climate <- lm(Mean.Node.Height ~ Temp_distance + Precip_distance,
                        data = dropped_australia_complete_filtered)

sink("model_Mean.Node.Height_climate_Australia.txt")
summary(model_MND_climate)
sink()
AIC_model_MND_climate <- AIC(model_MND_climate)


###Mean Node Height for Bioclim variables
model_MND_Bioclim <- lm(Mean.Node.Height ~ Bioclim_1 * Bioclim_7 * Bioclim_12 * 
                          Bioclim_17, data = dropped_australia_complete_filtered)

sink("model_Mean.Node.Height_Bioclim_Australia.txt")
summary(model_MND_Bioclim)
sink()
AIC_model_MND_Bioclim <- AIC(model_MND_Bioclim)


###Mean Node Height for soil variables
model_MND_soil <- lm(Mean.Node.Height ~ Coarse_fragment * Organic_content * 
                       Ph_x_10 * Sand_percent, 
                     data = dropped_australia_complete_filtered)

sink("model_Mean.Node.Height_soil_Australia.txt")
summary(model_MND_soil)
sink()
AIC_model_MND_soil <- AIC(model_MND_soil)
