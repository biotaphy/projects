library(dplyr)
library(tidyverse)

####This script calculates the linear and multiple regressions between 
####the age predictor Mean Node Height and each environmental 
####predictor for South America.

##Reading file
samerica_complete <- read.csv("south_america_stats_cj_mod.csv")
head(samerica_complete)

##Removing NA values for the columns we are using
dropped_samerica_complete <- drop_na(samerica_complete, Temp_distance, 
                                     Precip_distance, Bioclim_1, 
                                     Bioclim_7, Bioclim_12, Bioclim_17, 
                                     Elevation, Coarse_fragment,
                                     Soil_ph, Sand_content,Organic_carbon, 
                                     Mean.Node.Height)

##Filtering out values equal to 0 or below for the variables: organic content,
##elevation, coarse fragment and sand percent. Filtering out values = "Inf"
##for the variable temperature distance.
dropped_samerica_complete_filtered <-dropped_samerica_complete %>% 
  filter(Organic_carbon > 0) %>% 
  filter(Elevation > 0) %>% 
  filter(Coarse_fragment > 0) %>% 
  filter(Sand_content > 0) %>% 
  filter(Temp_distance != "Inf") 

##Calculating correlations, plotting linear regression graphs, and 
##producing and saving summary statistics for all the variables selected:

####Temp_distance
cor_Temp_dist <- cor(dropped_samerica_complete_filtered$Temp_distance, 
                     dropped_samerica_complete_filtered$Mean.Node.Height)

model_Temp_dist <- lm(Mean.Node.Height ~ Temp_distance, 
                      data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Temp_distance, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Temperature distance", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Temp_dist_SAmerica_nodes.txt")
summary(model_Temp_dist)
sink()

####Precip_distance
cor_Precip_distance <- cor(dropped_samerica_complete_filtered$Precip_distance, 
                           dropped_samerica_complete_filtered$Mean.Node.Height)

model_Precip_distance <- lm(Mean.Node.Height ~ Precip_distance, 
                            data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Precip_distance, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Precipitation distance", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Precip_dist_SAmerica_nodes.txt")
summary(model_Precip_distance)
sink()

#####Bioclim_1
cor_Bioclim_1 <- cor(dropped_samerica_complete_filtered$Bioclim_1, 
                     dropped_samerica_complete_filtered$Mean.Node.Height)

model_Bioclim_1 <- lm(Mean.Node.Height ~ Bioclim_1, 
                      data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Bioclim_1, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Annual Mean Temperature", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_1_SAmerica_nodes.txt")
summary(model_Bioclim_1)
sink() 

#####Bioclim_7
cor_Bioclim_7 <- cor(dropped_samerica_complete_filtered$Bioclim_7, 
                     dropped_samerica_complete_filtered$Mean.Node.Height)

model_Bioclim_7 <- lm(Mean.Node.Height ~ Bioclim_7, 
                      data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Bioclim_7, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Temperature Annual Range", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_7_SAmerica_nodes.txt")
summary(model_Bioclim_7)
sink()

#####Bioclim_12
cor_Bioclim_12 <- cor(dropped_samerica_complete_filtered$Bioclim_12, 
                      dropped_samerica_complete_filtered$Mean.Node.Height)

model_Bioclim_12 <- lm(Mean.Node.Height ~ Bioclim_12, 
                       data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Bioclim_12, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Annual Precipitation", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_12_SAmerica_nodes.txt")
summary(model_Bioclim_12)
sink()

#####Bioclim_17
cor_Bioclim_17 <- cor(dropped_samerica_complete_filtered$Bioclim_17, 
                      dropped_samerica_complete_filtered$Mean.Node.Height)

model_Bioclim_17 <- lm(Mean.Node.Height ~ Bioclim_17, 
                       data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Bioclim_17, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Precipitation of Driest Quarter", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Bioclim_17_SAmerica_nodes.txt")
summary(model_Bioclim_17)
sink()

#####Elevation
cor_Elevation <- cor(dropped_samerica_complete_filtered$Elevation, 
                     dropped_samerica_complete_filtered$Mean.Node.Height)

model_Elevation <- lm(Mean.Node.Height ~ Elevation, 
                      data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Elevation, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Elevation", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Elevation_SAmerica_nodes.txt")
summary(model_Elevation)
sink()

#####Coarse_fragment
cor_Coarse_fragment <- cor(dropped_samerica_complete_filtered$Coarse_fragment, 
                           dropped_samerica_complete_filtered$Mean.Node.Height)

model_Coarse_fragment <- lm(Mean.Node.Height ~ Coarse_fragment, 
                            data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Coarse_fragment, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Coarse fragment", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Coarse_fragment_SAmerica_nodes.txt")
summary(model_Coarse_fragment)
sink()

#####Soil_ph
cor_Soil_ph <- cor(dropped_samerica_complete_filtered$Soil_ph, 
                   dropped_samerica_complete_filtered$Mean.Node.Height)

model_Soil_ph <- lm(Mean.Node.Height ~ Soil_ph, 
                    data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Soil_ph, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Soil pH", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Soil_ph_SAmerica_nodes.txt")
summary(model_Soil_ph)
sink()

#####Sand_content
cor_Sand_percent <- cor(dropped_samerica_complete_filtered$Sand_content, 
                        dropped_samerica_complete_filtered$Mean.Node.Height)

model_Sand_content <- lm(Mean.Node.Height ~ Sand_content, 
                         data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Sand_content, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Sand percent", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12))+
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Sand_content_SAmerica_nodes.txt")
summary(model_Sand_content)
sink()

#####Organic_carbon
cor_Organic_carbon <- cor(dropped_samerica_complete_filtered$Organic_carbon, 
                          dropped_samerica_complete_filtered$Mean.Node.Height)

model_Organic_carbon <- lm(Mean.Node.Height ~ Organic_carbon, 
                           data = dropped_samerica_complete_filtered)

ggplot(dropped_samerica_complete_filtered, aes(Organic_carbon, 
                                               Mean.Node.Height)) +
  theme(axis.text.x = element_text(size = 12)) +
  theme(axis.text.y = element_text(size = 12)) +
  labs(x= "Organic carbon", y= "Mean Node Height") +
  theme(axis.title = element_text(size = 12)) +
  geom_point(size=0.5)+
  stat_smooth(method = lm)

sink("model_Organic_content_SAmerica_nodes.txt")
summary(model_Organic_carbon)
sink()


###Multiple regression
##Calculating mulitple regression correlations and saving summary statistics 
##for the 4 combinations of variables selected:

###Mean Node Height for all variables
model_Mean.Node.Height <- lm(Mean.Node.Height ~ Temp_distance + Precip_distance + Bioclim_1 * 
                               Bioclim_7 * Bioclim_12 * Bioclim_17 + Coarse_fragment * 
                               Organic_carbon * Soil_ph * Sand_content + Elevation,
                             data = dropped_samerica_complete_filtered)

sink("model_Mean.Node.Height_SAmerica.txt")
summary(model_Mean.Node.Height)
sink()
AIC_model_Mean.Node.Height <- AIC(model_Mean.Node.Height)


###Mean Node Height for climate distance variables
model_MND_climate <- lm(Mean.Node.Height ~ Temp_distance + Precip_distance,
                        data = dropped_samerica_complete_filtered)

sink("model_Mean.Node.Height_climate_SAmerica.txt")
summary(model_MND_climate)
sink()
AIC_model_MND_climate <- AIC(model_MND_climate)


###Mean Node Height for Bioclim variables
model_MND_Bioclim <- lm(Mean.Node.Height ~ Bioclim_1 * Bioclim_7 * Bioclim_12 * 
                          Bioclim_17, data = dropped_samerica_complete_filtered)

sink("model_Mean.Node.Height_Bioclim_SAmerica.txt")
summary(model_MND_Bioclim)
sink()
AIC_model_MND_Bioclim <- AIC(model_MND_Bioclim)


###Mean Node Height for soil variables
model_MND_soil <- lm(Mean.Node.Height ~ Coarse_fragment * Organic_carbon * 
                       Soil_ph * Sand_content, 
                     data = dropped_samerica_complete_filtered)

sink("model_Mean.Node.Height_soil_SAmerica.txt")
summary(model_MND_soil)
sink()
AIC_model_MND_soil <- AIC(model_MND_soil)
