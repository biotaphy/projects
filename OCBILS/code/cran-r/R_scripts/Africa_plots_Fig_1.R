library(dplyr)
library(tidyverse)
library(ggplot2)
library(cowplot)

####This Script produces Figure 1 of the manuscript, containing the most
####meaningful linear correlations between both age metrics (MTL and MNH)
####and the environmental predictors investigated.

##Reading file used for both tip and node plots
africa_complete <- read.csv("africa_v83.csv")
head(africa_complete)

##NODE ANALYSES
##Removing NA values for the columns we are using
dropped_africa_complete <- drop_na(africa_complete, temp_distance, 
                                   precip_distance, Bioclim_1, 
                                   Bioclim_7, Bioclim_12, Bioclim_17, 
                                   Elevation, Coarse_fragment,
                                   Ph_x_10, Sand,Organic_content, 
                                   Mean.Node.Height)

##Filtering out values equal to 0 or below for the variables: organic content,
##elevation, coarse fragment, sand percent, and Mean.Node.Height. 
##Filtering out values = "Inf" for the variable temperature distance.
dropped_africa_complete_filtered <-dropped_africa_complete %>% 
  filter(Organic_content > 0) %>% 
  filter(Elevation > 0) %>% 
  filter(Coarse_fragment > 0) %>% 
  filter(Sand > 0) %>% 
  filter(temp_distance != "Inf") %>% 
  filter(Mean.Node.Height > 0)

##Calculating correlations and plotting linear regression graphs
##for the 3 most meaningful variables (NODE ANALYSES):
cor_Bioclim_1 <- cor(dropped_africa_complete_filtered$Bioclim_1, 
                     dropped_africa_complete_filtered$Mean.Node.Height)

model_Bioclim_1 <- lm(Mean.Node.Height ~ Bioclim_1, 
                      data = dropped_africa_complete_filtered)

cor_Elevation <- cor(dropped_africa_complete_filtered$Elevation, 
                     dropped_africa_complete_filtered$Mean.Node.Height)

model_Elevation <- lm(Mean.Node.Height ~ Elevation, 
                      data = dropped_africa_complete_filtered)

cor_Ph_x_10 <- cor(dropped_africa_complete_filtered$Ph_x_10, 
                   dropped_africa_complete_filtered$Mean.Node.Height)

model_Ph_x_10 <- lm(Mean.Node.Height ~ Ph_x_10, 
                    data = dropped_africa_complete_filtered)

##TIP ANALYSES
##Removing NA values for the columns we are using
dropped_africa_complete_tip <- drop_na(africa_complete, temp_distance, 
                                       precip_distance, Bioclim_1, 
                                       Bioclim_7, Bioclim_12, Bioclim_17, 
                                       Elevation, Coarse_fragment,
                                       Ph_x_10, Sand,Organic_content, 
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

##Calculating correlations and plotting linear regression graphs
## for the 3 meaningful variables (TIP ANALYSES):
cor_Bioclim_12_tip <- cor(dropped_africa_complete_filtered_tip$Bioclim_12, 
                          dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Bioclim_12_tip <- lm(Mean.Tip.Length ~ Bioclim_12, 
                           data = dropped_africa_complete_filtered_tip)

cor_Elevation_tip <- cor(dropped_africa_complete_filtered_tip$Elevation, 
                         dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Elevation_tip <- lm(Mean.Tip.Length ~ Elevation, 
                          data = dropped_africa_complete_filtered_tip)

cor_Ph_x_10_tip <- cor(dropped_africa_complete_filtered_tip$Ph_x_10, 
                       dropped_africa_complete_filtered_tip$Mean.Tip.Length)

model_Ph_x_10_tip <- lm(Mean.Tip.Length ~ Ph_x_10, 
                        data = dropped_africa_complete_filtered_tip)

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
Ph_x_10 <- ggplotRegression(model_Ph_x_10)
Ph_x_10_2 <- Ph_x_10 + 
  labs(x= "Soil pH", y= "Mean Node Height")

Elevation <- ggplotRegression(model_Elevation)
Elevation_2 <- Elevation + 
  labs(x= "Elevation", y= "Mean Node Height")

Bioclim_1 <- ggplotRegression(model_Bioclim_1)
Bioclim_1_2 <- Bioclim_1 + 
  labs(x= "Annual Mean Temperature", y= "Mean Node Height")

Ph_x_10_tip <- ggplotRegression(model_Ph_x_10_tip)
Ph_x_10_tip_2 <- Ph_x_10_tip + 
  labs(x= "Soil pH", y= "Mean Tip Length")

Bioclim_12_tip <- ggplotRegression(model_Bioclim_12_tip)
Bioclim_12_tip_2 <- Bioclim_12_tip + 
  labs(x= "Annual Precipitation", y= "Mean Tip Length")

Elevation_tip <- ggplotRegression(model_Elevation_tip)
Elevation_tip_2 <- Elevation_tip + 
  labs(x= "Elevation", y= "Mean Tip Length")


##Plotting all the graphs to the same grid:
plot_grid(Ph_x_10_2, Elevation_2, Bioclim_1_2, 
          Ph_x_10_tip_2, Elevation_tip_2, Bioclim_12_tip_2,
          labels = "AUTO", 
          ncol = 3, nrow = 2)
