library(dplyr)
library(tidyverse)
library(ggplot2)
library(cowplot)

####This Script produces Figure 2 of the manuscript, containing the most
####meaningful linear correlations between both age metrics (MTL and MNH)
####and the environmental predictors investigated.

##Reading file used for both tip and node plots
samerica_complete <- read.csv("south_america_stats_cj_mod.csv")
head(samerica_complete)

##NODE ANALYSES
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

##Calculating correlations and plotting linear regression graphs
## for the 3 most meaningful variables (NODE ANALYSES):
cor_Coarse_fragment <- cor(dropped_samerica_complete_filtered$Coarse_fragment, 
                           dropped_samerica_complete_filtered$Mean.Node.Height)

model_Coarse_fragment <- lm(Mean.Node.Height ~ Coarse_fragment, 
                            data = dropped_samerica_complete_filtered)

sum_Coarse_fragment <- summary(model_Coarse_fragment)

cor_Elevation <- cor(dropped_samerica_complete_filtered$Elevation, 
                     dropped_samerica_complete_filtered$Mean.Node.Height)

model_Elevation <- lm(Mean.Node.Height ~ Elevation, 
                      data = dropped_samerica_complete_filtered)

cor_Bioclim_1 <- cor(dropped_samerica_complete_filtered$Bioclim_1, 
                     dropped_samerica_complete_filtered$Mean.Node.Height)

model_Bioclim_1 <- lm(Mean.Node.Height ~ Bioclim_1, 
                      data = dropped_samerica_complete_filtered)

##TIP ANALYSES
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

##Calculating correlations and plotting linear regression graphs
## for the 3 most meaningful variables (TIP ANALYSES):
cor_Coarse_fragment_tip <- cor(dropped_samerica_complete_filtered_tip$Coarse_fragment, 
                               dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Coarse_fragment_tip <- lm(Mean.Tip.Length ~ Coarse_fragment, 
                                data = dropped_samerica_complete_filtered_tip)

cor_Elevation_tip <- cor(dropped_samerica_complete_filtered_tip$Elevation, 
                         dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Elevation_tip <- lm(Mean.Tip.Length ~ Elevation, 
                          data = dropped_samerica_complete_filtered_tip)

cor_Bioclim_1_tip <- cor(dropped_samerica_complete_filtered_tip$Bioclim_1, 
                         dropped_samerica_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_1_tip <- lm(Mean.Tip.Length ~ Bioclim_1, 
                          data = dropped_samerica_complete_filtered_tip)


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
coarse_frag <- ggplotRegression(model_Coarse_fragment)
coarse_frag_2 <- coarse_frag + 
  labs(x= "Coarse fragment", y= "Mean Node Height")

elevation <- ggplotRegression(model_Elevation)
elevation_2 <- elevation + 
  labs(x= "Elevation", y= "Mean Node Height")

bioclim1 <- ggplotRegression(model_Bioclim_1)
bioclim1_2 <- bioclim1 + 
  labs(x= "Annual Mean Temperature", y= "Mean Node Height")

coarse_frag_tip <- ggplotRegression(model_Coarse_fragment_tip)
coarse_frag_tip_2 <- coarse_frag_tip + 
  labs(x= "Coarse fragment", y= "Mean Tip Length")

elevation_tip <- ggplotRegression(model_Elevation_tip)
elevation_tip_2 <- elevation_tip + 
  labs(x= "Elevation", y= "Mean Tip Length")

bioclim1_tip <- ggplotRegression(model_Bioclim_1_tip)
bioclim1_tip_2 <- bioclim1_tip + 
  labs(x= "Annual Mean Temperature", y= "Mean Tip Length")


##Plotting all the graphs to the same grid:
plot_grid(coarse_frag_2, elevation_2, bioclim1_2, 
          coarse_frag_tip_2, elevation_tip_2, bioclim1_tip_2,
          labels = "AUTO", 
          ncol = 3, nrow = 2)
