library(tidyverse) 
library(ggplot2)  
library(readxl)
library(viridis)
library(Rserve)
library(mvoutlier)
library(factoextra)
library(car)
library(lmtest)
library(sandwich)



Rserve(args="--save")

df <- read_excel('Output with Immigration Data.xlsx')
df$Total_Inflows_of_Migration <- as.integer(df$Total_Inflows_of_Migration) 
str(df)

df2 <- na.omit(df) 

Clean_Data_WHR <- read_xlsx("Clean Data WHR.xlsx")

hist(df2$Generosity)
hist(df2$Happiness_Score)
hist(df2$GDP_per_Capita)
hist(df2$Life_Expectancy)
hist(df2$Freedom)
hist(df2$Government_Corruption)
hist(df2$Total_Inflows_of_Migration)
hist(df2$Foreign_born_Men_Employment_Rate)
hist(df2$Foreign_born_Women_Employment_Rate)


outliers1 <- sign2(cbind(df2$wfinal01,df2$Total_Inflows_of_Migration,df2$Happiness_Score))
outliers1$wfinal01

o1 <- ggplot(df2, aes(Happiness_Score,Total_Inflows_of_Migration ,group=outliers1$wfinal01,
                    color=outliers1$wfinal01))+geom_point()+
  labs(title="Happiness Score and Total Inflow of Migration", 
       x ="Happiness Score", y = "Total Inflow of Migration")+
    theme_classic() +theme(legend.position = "none")
o1

outliers2 <- sign2(cbind(df$wfinal01,df$Foreign_born_Men_Employment_Rate,df$Happiness_Score))
outliers2$wfinal01
o2 <- ggplot(df, aes(Happiness_Score,Foreign_born_Men_Employment_Rate ,
                     group=outliers2$wfinal01,
                      color=outliers2$wfinal01))+geom_point()+
  labs(title="Happiness Score and Foreign Born Men Employment Rate", 
       x ="Happiness Score", y = "Foreign Born Men Employment Rate")+
  theme_classic() +theme(legend.position = "none")
o2

outliers3 <- sign2(cbind(df$wfinal01,df$Foreign_born_Women_Employment_Rate,df$Happiness_Score))
outliers3$wfinal01
o3 <- ggplot(df, aes(Happiness_Score,Foreign_born_Women_Employment_Rate ,
                     group=outliers3$wfinal01,
                     color=outliers3$wfinal01))+geom_point()+
  labs(title="Happiness Score and Foreign Born Women Employment Rate", 
       x ="Happiness Score", y = "Foreign Born Women Employment Rate")+
  theme_classic() +theme(legend.position = "none")
o3

#clustering

df3 <- df %>% select(Happiness_Score,Total_Inflows_of_Migration)
df3 <- na.omit(df3)
fviz_nbclust(df3,kmeans,method="wss")

km1 <- kmeans(df3,3,iter=10)
km1  
print(km1)
c <-ggplot(df3, aes(Happiness_Score,Total_Inflows_of_Migration,
                   group=km1$cluster,
                   color=km1$cluster))+geom_point() +
  labs(title="Happiness Score and Total Inflow of Migration Cluster Plot", 
       x ="Happiness Score", y = "Total Inflow of Migration")+theme_classic() +
  theme(legend.position = "none")+scale_color_viridis(option = "viridis")
c
outliers5 <- sign2(cbind(df3$wfinal01,df3$Total_Inflows_of_Migration,df3$Happiness_Score))
outliers5$wfinal01
df3$outliers_mv <- outliers5$wfinal01
df6 <- df3 %>% filter(df3$outliers_mv>0) %>% select(Happiness_Score,Total_Inflows_of_Migration)
fviz_nbclust(df6,kmeans,method="wss")
km3 <- kmeans(df6,3,iter=10)
km3 
print(km3)

c3 <-ggplot(df6, aes(Happiness_Score,Total_Inflows_of_Migration,
                    group=km3$cluster,
                    color=km3$cluster))+geom_point() +
  labs(title="Happiness Score and Total Inflow of Migration Cluster Plot", 
       x ="Happiness Score", y = "Total Inflow of Migration")+theme_classic() +
  theme(legend.position = "none")+scale_color_viridis(option = "viridis")
c3

km4 <- kmeans(df6,2,iter=10)
km4
print(km4)

c4 <-ggplot(df6, aes(Happiness_Score,Total_Inflows_of_Migration,
                     group=km4$cluster,
                     color=km4$cluster))+geom_point() +
  labs(title="Happiness Score and Total Inflow of Migration Cluster Plot", 
       x ="Happiness Score", y = "Total Inflow of Migration")+theme_classic() +
  theme(legend.position = "none")+scale_color_viridis(option = "viridis")
c4

df4 <- df %>% select(Foreign_born_Men_Employment_Rate,Foreign_born_Women_Employment_Rate)
df4 <- na.omit(df4)
fviz_nbclust(df4,kmeans,method="wss")

km2 <- kmeans(df4,5,algorithm=c("Lloyd"),iter.max=10)
km2  
print(km2)
c2 <-ggplot(df4, aes(Foreign_born_Men_Employment_Rate,Foreign_born_Women_Employment_Rate,
                     group=km2$cluster,
                     color=km2$cluster))+geom_point() +
  labs(title="Foreign Born Men and Women Employment Rate", 
       x ="Foreign Born Men Employment Rate", y = "Foreign Born Women Employment Rate")+
  theme_classic() +theme(legend.position = "none")+scale_color_viridis(option = "viridis")
c2

# Linear Regression
l1<-lm(Happiness_Score~Generosity+GDP_per_Capita+Life_Expectancy+
          Freedom+Government_Corruption,df)
summary(l1)
coeftest(l1,vcov=vcovHC,type="HC1")
avPlots(l1,se=TRUE)

l2<-lm(Happiness_Score~Generosity+Life_Expectancy+
         Freedom+Government_Corruption,df)
coeftest(l2,vcov=vcovHC,type="HC1")
avPlots(l2,se=TRUE)

# lm without outliers
outliers4 <- sign2(cbind(df$wfinal01,df$Happiness_Score,df$Generosity,
                         df$GDP_per_Capita,df$Life_Expectancy,
                           df$Freedom,df$Government_Corruption))
outliers4$wfinal01

o4 <- ggplot(df, aes(Happiness_Score,Generosity+GDP_per_Capita+Life_Expectancy+Freedom+Government_Corruption,group=outliers4$wfinal01,
                      color=outliers4$wfinal01))+geom_point()+
  labs(title="Happiness Score and Other Variables", 
       x ="Happiness Score", y = "Other Variables")+
  theme_classic() +theme(legend.position = "none")
o4

df$outliers_mv <- outliers4$wfinal01
df5 <- df %>% filter(df$outliers_mv>0)



l3<-lm(Happiness_Score~Generosity+GDP_per_Capita+Life_Expectancy+
         Freedom+Government_Corruption,df5)
summary(l3)
coeftest(l3,vcov=vcovHC,type="HC1")
avPlots(l3,se=TRUE)

l4<-lm(Happiness_Score~Generosity+Life_Expectancy+
         Freedom+Government_Corruption,df5)
summary(l4)
coeftest(l4,vcov=vcovHC,type="HC1")
avPlots(l4,se=TRUE)

# boxplot
Clean_Data_WHR <- read_excel('/Users/cmk/Desktop/Viz/Report/Clean Data WHR.xlsx')
Clean_Data_WHR %>%
  ggplot( aes(x=Years, y=GDP_per_Capita, fill=Years)) +
  geom_boxplot(notch = TRUE,
               outlier.colour="red", 
               outlier.fill="red",
               outlier.size=2,
               notchwidth = 0.5
               ) +
  scale_fill_viridis(discrete = TRUE, alpha=0.6, option="A") +
  theme(
    legend.position="none",
    plot.title = element_text(size=11)
  ) +
  ggtitle("GDP per Capita Distribution from 2015 to 2019 (Boxplot with Outliers)") +
  xlab("") + 
  geom_jitter(color="black", size=0.4, alpha=0.9)

## Remove Outliers
Clean_Data_WHR %>%
  ggplot( aes(x=Years, y=GDP_per_Capita, fill=Years)) +
  geom_boxplot(notch = TRUE,
               outlier.colour="red", 
               outlier.fill="red",
               outlier.size=2,
               notchwidth = 0.5,
               outlier.shape = NA
  ) +
  scale_fill_viridis(discrete = TRUE, alpha=0.6, option="A") +
  theme(
    legend.position="none",
    plot.title = element_text(size=11)
  ) +
  ggtitle("GDP per Capita Distribution from 2015 to 2019 (Boxplot without Outliers)") +
  xlab("") + 
  coord_cartesian(ylim=c(0.0, 1.8)) + 
  geom_jitter(color="black", size=0.4, alpha=0.9)

