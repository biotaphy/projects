library(dplyr)
library(tidyverse)
library(ggplot2)
library(cowplot)

####This Script produces Figure 3 of the manuscript, containing the most
####meaningful linear correlations between both age metrics (MTL and MNH)
####and the environmental predictors investigated.

##Reading file used for both tip and node plots
australia_complete <- read.csv("australia_stats_cj_mod.csv")
head(australia_complete)

##NODE ANALYSES
##Removing NA values for the columns we are using
dropped_australia_complete <- drop_na(australia_complete, Temp_distance, 
                                      Precip_distance, Bioclim_1, 
                                      Bioclim_7, Bioclim_12, Bioclim_17, 
                                      Elevation, Coarse_fragment,
                                      Ph_x_10, Sand_percent,Organic_content, 
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

##Calculating correlations and plotting linear regression graphs
## for the 3 most meaningful variables (NODE ANALYSES):
cor_Bioclim_12 <- cor(dropped_australia_complete_filtered$Bioclim_12, 
                      dropped_australia_complete_filtered$Mean.Node.Height)

model_Bioclim_12 <- lm(Mean.Node.Height ~ Bioclim_12, 
                       data = dropped_australia_complete_filtered)

cor_Sand_percent <- cor(dropped_australia_complete_filtered$Sand_percent, 
                        dropped_australia_complete_filtered$Mean.Node.Height)

model_Sand_percent <- lm(Mean.Node.Height ~ Sand_percent, 
                         data = dropped_australia_complete_filtered)

cor_Ph_x_10 <- cor(dropped_australia_complete_filtered$Ph_x_10, 
                   dropped_australia_complete_filtered$Mean.Node.Height)

model_Ph_x_10 <- lm(Mean.Node.Height ~ Ph_x_10, 
                    data = dropped_australia_complete_filtered)

##TIP ANALYSES
##Removing NA values for the columns we are using
dropped_australia_complete_tip <- drop_na(australia_complete, Temp_distance, 
                                          Precip_distance, Bioclim_1, 
                                          Bioclim_7, Bioclim_12, Bioclim_17, 
                                          Elevation, Coarse_fragment,
                                          Ph_x_10, Sand_percent,Organic_content, 
                                          Mean.Tip.Length)

##Filtering out values equal to 0 or below for the variables: organic content,
##elevation, coarse fragment and sand percent. Filtering out values = "Inf"
##for the variable temperature distance.
dropped_australia_complete_filtered_tip <-dropped_australia_complete_tip %>% 
  filter(Organic_content > 0) %>% 
  filter(Elevation > 0) %>% 
  filter(Coarse_fragment > 0) %>% 
  filter(Sand_percent > 0) %>% 
  filter(Temp_distance != "Inf")

##Calculating correlations and plotting linear regression graphs
## for the 3 most meaningful variables (TIP ANALYSES):
cor_Bioclim_12_tip <- cor(dropped_australia_complete_filtered_tip$Bioclim_12, 
                          dropped_australia_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_12_tip <- lm(Mean.Tip.Length ~ Bioclim_12, 
                           data = dropped_australia_complete_filtered_tip)

cor_Sand_percent_tip <- cor(dropped_australia_complete_filtered_tip$Sand_percent, 
                            dropped_australia_complete_filtered_tip$Mean.Tip.Length)

model_Sand_content_tip <- lm(Mean.Tip.Length ~ Sand_percent, 
                             data = dropped_australia_complete_filtered_tip)

cor_Soil_ph_tip <- cor(dropped_australia_complete_filtered_tip$Ph_x_10, 
                       dropped_australia_complete_filtered_tip$Mean.Tip.Length)

model_Soil_ph_tip <- lm(Mean.Tip.Length ~ Ph_x_10, 
                        data = dropped_australia_complete_filtered_tip)

##Plotting the graphs for each of the six analyses above 
##(3 for tip and 3 for node):
ggplotRegression <- function (fit) {
  
  require(ggplot2)
  
  ggplot(fit$model, aes_string(x = names(fit$model)[2], y = names(fit$model)[1])) + 
    theme(axis.text.x = element_text(size = 12)) +
    theme(axis.text.y = element_text(size = 12)) +
    theme(axis.title = element_text(size = 12))+
    theme(plot.margin = unit(c(2,4,2,4), "mm"))+
    geom_point(size=0.5) +
    stat_smooth(method = "lm")
}

##Add the appropriate labels to each graph:
bioclim12 <- ggplotRegression(model_Bioclim_12)
bioclim12_2 <- bioclim12 + 
  labs(x= "Annual Precipitation", y= "Mean Node Height")

sand_percent <- ggplotRegression(model_Sand_percent)
sand_percent_2 <- sand_percent + 
  labs(x= "Sand percent", y= "Mean Node Height")

soil_pH <- ggplotRegression(model_Ph_x_10)
soil_pH_2 <- soil_pH + 
  labs(x= "Soil pH", y= "Mean Node Height")

bioclim12_tip <- ggplotRegression(model_Bioclim_12_tip)
bioclim12_tip_2 <- bioclim12_tip + 
  labs(x= "Annual Precipitation", y= "Mean Tip Length")

sand_percent_tip <- ggplotRegression(model_Sand_content_tip)
sand_percent_tip_2 <- sand_percent_tip + 
  labs(x= "Sand percent", y= "Mean Tip Length")

soil_pH_tip <- ggplotRegression(model_Soil_ph_tip)
soil_pH_tip_2 <- soil_pH_tip + 
  labs(x= "Soil pH", y= "Mean Tip Length")

##Plotting all the graphs to the same grid:
plot_grid(bioclim12_2, sand_percent_2, soil_pH_2, 
          bioclim12_tip_2, sand_percent_tip_2, soil_pH_tip_2,
          labels = "AUTO", 
          ncol = 3, nrow = 2)