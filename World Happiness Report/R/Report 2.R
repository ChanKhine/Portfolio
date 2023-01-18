library(tidyverse)
library(ggplot2)
library(dplyr)
library(hrbrthemes)
library(viridis)
library(directlabels)
library(readxl)

# read data
df <- read_excel('/Users/cmk/Desktop/Viz/Report/Output with Immigration Data.xlsx')
summary(df)
str(df)

df$Total_Inflows_of_Migration <- as.integer(df$Total_Inflows_of_Migration) 
str(df)

Clean_Data_WHR <- read_excel('/Users/cmk/Desktop/Viz/Report/Clean Data WHR.xlsx')

#bar chart
ggplot(df, aes(x=Years, y=Total_Inflows_of_Migration,fill=Years))+ 
  geom_bar(stat='identity', position="dodge")
ggplot(df, aes(x=Years, y=Happiness_Score,fill=Years))+ 
  geom_bar(stat='identity', position="dodge")

#Scatterplot 
ggplot(df, aes(x=Foreign_born_Men_Employment_Rate, y=Happiness_Score, colour="orange")) + 
  geom_point(stat='identity') +
  geom_smooth()
ggplot(df, aes(x=Foreign_born_Women_Employment_Rate, y=Happiness_Score, colour="orange")) + 
  geom_point(stat='identity') +
  geom_smooth()

# boxplot
Clean_Data_WHR %>%
  ggplot( aes(x=Years, y=GDP_per_Capita, fill=Years)) +
  geom_boxplot() +
  scale_fill_viridis(discrete = TRUE, alpha=0.6, option="A") +
  theme(
    legend.position="none",
    plot.title = element_text(size=11)
  ) +
  ggtitle("GDP per Capita Distribution from 2015 to 2019") +
  xlab("") +
geom_jitter(color="black", size=0.4, alpha=0.9) 

# histogram & Facet
p <- Clean_Data_WHR %>%
  ggplot( aes(x=Happiness_Score, color=Years, fill=Years)) +
  geom_histogram(alpha=0.6, binwidth = 0.1) +
  scale_fill_viridis(discrete=TRUE) +
  scale_color_viridis(discrete=TRUE) +
  theme(
    legend.position="none",
    panel.spacing = unit(0.1, "lines"),
    strip.text.x = element_text(size = 8)
  ) +
  xlab("") +
  ylab("") +
  facet_wrap(~Years) +
  ggtitle("Happiness Score distribution from 2015 to  2019")
p


# line chart
l <- ggplot(df, aes(Years ,Happiness_Score ,group=Country,
                    color=Total_Inflows_of_Migration))+geom_line()+ 
  labs(title="Happiness Score and Total Inflow of Migration From 2015 to 2019", 
       x ="Years", y = "Happiness Score",color='Total Inflow of Migration')+
  geom_dl(aes(label = Country), method = list(dl.trans(x = x + 0.2), "last.points", cex = 0.8)) +
  geom_dl(aes(label = Country), method = list(dl.trans(x = x - 0.2), "first.points", cex = 0.8)) + theme_classic() 
l

# Violin 
v1 <- ggplot(df, aes(x=Years, y=Foreign_born_Men_Employment_Rate,color=Years)) + 
  geom_violin(trim=FALSE)+ stat_summary(fun=mean, geom="point", shape=23, size=2,color="black")+
  labs(title="Foreign-Born Men Employment Rate From 2015 to 2019", 
       x ="Years", y = "Foreign-Born Men Employment Rate") + theme_classic()+theme(legend.position = "none")
v1

v2 <- ggplot(df, aes(x=Years, y=Foreign_born_Women_Employment_Rate,color=Years)) + 
  geom_violin(trim=FALSE)+ stat_summary(fun=mean, geom="point", shape=23, size=2,color="black")+
  labs(title="Foreign-Born Women Employment Rate From 2015 to 2019", 
       x ="Years", y = "Foreign-Born Women Employment Rate") + theme_classic() +theme(legend.position = "none")
v2

# Split Violin
df2 <- df %>% select(Years,Foreign_born_Men_Employment_Rate)
df2$Gender <- "M"
names(df2)[2] <- "Foreign_born_Employment_Rate"

df3 <- df %>% select(Years,Foreign_born_Women_Employment_Rate)
df3$Gender <- "F"
names(df3)[2] <- "Foreign_born_Employment_Rate"

df4 <- rbind(df2,df3)
v3 <- ggplot(df4, aes(x=Years, y=Foreign_born_Employment_Rate,color=Gender)) + 
  geom_violin(trim=FALSE)+ stat_summary(fun=mean, geom="crossbar")+
  labs(title="Foreign-Born People Employment Rate From 2015 to 2019", 
       x ="Years", y = "Foreign-Born People Employment Rate") + theme_classic() 
v3


##Ellipse Plot
df <- read_excel("/Users/cmk/Desktop/Viz/Report/Group data.xlsx")
head(df)
ggplot(df,aes(x=Happiness_score,y=GDP_per_Capita,color=Group))+
  stat_ellipse(level=0.95,alpha=0.7)+theme_bw()+scale_color_manual(values=c("red","blue","green"))
       