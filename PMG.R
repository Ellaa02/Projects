#load library
library(tidyverse)
library(dplyr)
library(ggplot2)
library(scales)

#rm(list)

setwd("C:/Users/ella1/Desktop") 
pricing <- read_csv("Pricing.csv") %>% drop_na()
# drop empty strings in performance
performance <- read.csv("Performance.csv", na.strings = c('', "NA")) %>% drop_na()

# clean numeric columns
performance <- performance %>%
  mutate(
    Impressions = as.numeric(gsub(",", "", Impressions)),
    Clicks = as.numeric(gsub(",", "", Clicks)),
    Cost = as.numeric(gsub(",", "", Cost)),
    Revenue = as.numeric(gsub(",", "", Revenue)),
    Profit = Revenue - Cost
  )
#sapply(performance, class)

#"How does performance of the Non-Fiction category compare to the Fiction 
#category? What data did you use to determine this? Finally, What would you
#recommend the company do with this information? Please put your written
#answer and the data you used to answer below.  
fiction <- performance %>% filter (Category.2 == "Fiction")
non_fiction <- performance %>% filter (Category.2 == "Non-Fiction")

fiction_avg <- fiction %>% summarise(across(c("Impressions", "Clicks", "Cost", "Revenue"),mean))
non_fiction_avg <- non_fiction %>% summarise(across(c("Impressions", "Clicks", "Cost", "Revenue"),mean))

comparison_avg <- bind_rows(
  Fiction = fiction_avg,
  Non_Fiction = non_fiction_avg,
  .id = "Category"
)

print(comparison_avg)

# Reshape for plotting
comparison_long <- comparison_avg %>%
  pivot_longer(cols = c("Impressions", "Clicks", "Cost", "Revenue"),
               names_to = "Metric",
               values_to = "Average")

comparison_scaled <- comparison_long %>%
  group_by(Metric) %>%
  mutate(Scaled = Average / max(Average))
comparison_scaled


ggplot(comparison_scaled, aes(x = Metric, y = Scaled, fill = Category)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Scaled Performance: Fiction vs Non-Fiction",
       y = "Scaled Value (0–1)") +
  theme_minimal()










category3_summary <- performance %>%
  group_by(Category.3) %>%
  summarise(
    Avg_Impressions = mean(Impressions, na.rm = TRUE),
    Avg_Clicks = mean(Clicks, na.rm = TRUE),
    Avg_Profit = mean(Profit, na.rm = TRUE),
    CTR = mean(Clicks / Impressions, na.rm = TRUE),
    ROAS = mean(Revenue / Cost, na.rm = TRUE)
  ) %>%
  arrange(desc(ROAS))

print(category3_summary)

# ---- 1) Impressions (log scale) ----
p_impr <- ggplot(category3_summary,
                 aes(x = reorder(Category.3, Avg_Impressions),
                     y = Avg_Impressions)) +
  geom_col(fill = "#00BFC4") +
  scale_y_log10(labels = label_comma()) +
  labs(title = "Average Impressions by Category.3 (log scale)",
       x = "Category 3",
       y = "Avg Impressions (log10 scale)") +
  theme_minimal()

# ---- 2) Clicks (log scale) ----
p_clicks <- ggplot(category3_summary,
                   aes(x = reorder(Category.3, Avg_Clicks),
                       y = Avg_Clicks)) +
  geom_col(fill = "#00BFC4") +
  scale_y_log10(labels = label_comma()) +
  labs(title = "Average Clicks by Category.3 (log scale)",
       x = "Category 3",
       y = "Avg Clicks (log10 scale)") +
  theme_minimal()


# ---- 3) Profit (diverging bars with zero line) ----
category3_profit <- category3_summary %>%
  mutate(ProfitFlag = if_else(Avg_Profit >= 0, "Positive", "Negative"))

p_profit <- ggplot(category3_profit,
                   aes(x = reorder(Category.3, Avg_Profit),
                       y = Avg_Profit,
                       fill = ProfitFlag)) +
  geom_hline(yintercept = 0, linewidth = 0.6) +
  geom_col() +
  coord_flip() +
  scale_y_continuous(labels = dollar) +
  scale_fill_manual(values = c("Positive" = "#00BFC4", "Negative" = "#F8766D")) +
  labs(title = "Average Profit by Category.3",
       x = "Category 3",
       y = "Avg Profit",
       fill = NULL) +
  theme_minimal() +
  theme(legend.position = "top")

# Print the three charts
p_impr
p_clicks
p_profit






library(lubridate)

# Create a new dataset for day-of-week CTR analysis
performance_day <- performance %>%
  mutate(
    date = as.Date(date, format = "%m/%d/%Y"),
    DayOfWeek = wday(date, label = TRUE, abbr = FALSE)
  )

# Summarize average CTR by day of week
day_summary <- performance_day %>%
  group_by(DayOfWeek) %>%
  summarise(
    Avg_Impressions = mean(Impressions, na.rm = TRUE),
    Avg_Clicks = mean(Clicks, na.rm = TRUE),
    CTR = mean(Clicks / Impressions, na.rm = TRUE),
    ROAS = mean(Profit, na.rm = TRUE)
  ) %>%
  arrange(desc(CTR))

print(day_summary)

# Visualization
ggplot(day_summary, aes(x = DayOfWeek, y = CTR, fill = DayOfWeek)) +
  geom_col() +
  labs(
    title = "Average Click-Through Rate (CTR) by Day of Week",
    x = "Day of Week",
    y = "Average CTR"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

ggplot(performance_day, aes(x = DayOfWeek, y = Impressions)) +
  geom_boxplot(fill = "#00BFC4") +
  labs(title = "CTR Distribution by Day of Week", y = "Impressions")





# --- Outlier Detection Function ---
detect_outlier <- function(x) {
  q1 <- quantile(x, probs = 0.25, na.rm = TRUE)
  q3 <- quantile(x, probs = 0.75, na.rm = TRUE)
  iqr <- q3 - q1
  upper <- q3 + 1.5 * iqr
  lower <- q1 - 1.5 * iqr
  return(x < lower | x > upper)
}

# --- Outlier Removal Function ---
remove_outlier <- function(df, columns = names(df)) {
  df_clean <- df
  for (col in columns) {
    if (is.numeric(df_clean[[col]])) {   # only apply to numeric columns
      outliers <- detect_outlier(df_clean[[col]])
      df_clean <- df_clean[!outliers, ]  # remove rows with outliers
    }
  }
  return(df_clean)
}

performance_day <- performance %>%
  mutate(
    date = as.Date(date, format = "%m/%d/%Y"),
    DayOfWeek = wday(date, label = TRUE, abbr = FALSE),
    CTR = Clicks / Impressions,
    Avg_Profit = mean(Profit, na.rm = TRUE),
  )

# Remove outliers based on CTR only (you can add more columns if needed)
performance_day_clean <- remove_outlier(performance_day, columns = c("CTR"))

# --- Summarize and plot again ---
day_summary_clean <- performance_day_clean %>%
  group_by(DayOfWeek) %>%
  summarise(
    Avg_Impressions = mean(Impressions, na.rm = TRUE),
    Avg_Clicks = mean(Clicks, na.rm = TRUE),
    CTR = mean(CTR, na.rm = TRUE),
    ROAS = mean(Revenue / Cost, na.rm = TRUE)
  )

print(day_summary_clean)

# --- Replot after removing outliers ---
ggplot(day_summary_clean, aes(x = DayOfWeek, y = ROAS, fill = DayOfWeek)) +
  geom_col() +
  labs(
    title = "Average ROAS by Day of Week (Outliers Removed)",
    x = "Day of Week",
    y = "Average ROAS"
  ) +
  theme_minimal() +
  theme(legend.position = "none")









merged <- performance %>%
  left_join(pricing, by = "ID") %>%
  mutate(
    Units_Sold = if_else(!is.na(Price) & Price > 0, Revenue / Price, NA_real_),
    CTR = Clicks / Impressions
  )

# --- 3. Summarize by Category.2 and Category.3 ---
category_summary <- merged %>%
  group_by(Category.2, Category.3, ID) %>%
  summarise(
    Price          = first(Price),
    Avg_Impressions = mean(Impressions, na.rm = TRUE),
    Avg_Clicks     = mean(Clicks, na.rm = TRUE),
    Total_Units    = sum(Units_Sold, na.rm = TRUE),
    Avg_Profit     = mean(Profit, na.rm = TRUE),
    CTR            = mean(CTR, na.rm = TRUE)
  )

print(category_summary)

# --- 4. Visualization (optional) ---
ggplot(category_summary, aes(x = reorder(Category.3, Total_Units), y = Total_Units, fill = Category.2)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Unit Sold By Category.2",
    x = "Category 3",
    y = "Unit Sold"
  ) +
  theme_minimal()


category2_summary <- merged %>%
  group_by(Category.2) %>%
  summarise(
    Total_Impressions = sum(Impressions, na.rm = TRUE),
    Total_Clicks      = sum(Clicks, na.rm = TRUE),
    Total_Profit      = sum(Profit, na.rm = TRUE),
    Total_Units_Sold  = sum(Revenue / Price, na.rm = TRUE),
    CTR               = mean(Clicks / Impressions, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(Total_Units_Sold))

# Print the comparison table
print(category2_summary)

# --- Optional: Visualization ---
ggplot(category2_summary, aes(x = reorder(Category.2, Total_Units_Sold), y = Total_Units_Sold, fill = Category.2)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Category 2 Comparison: Total Units Sold",
    x = "Category 2",
    y = "Total Units Sold"
  ) +
  theme_minimal()












# --- Merge Pricing and Performance ---
merged <- performance %>%
  left_join(pricing %>% mutate(Price = as.numeric(Price)), by = "ID") %>%
  mutate(
    Units_Sold = if_else(!is.na(Price) & Price > 0, Revenue / Price, NA_real_)
  )

# --- Summarize by Category.2 (Fiction vs Non-Fiction) ---
category_summary <- merged %>%
  group_by(Category.2) %>%
  summarise(
    Total_Units = sum(Units_Sold, na.rm = TRUE),
    CTR = mean(Clicks / Impressions, na.rm = TRUE),
    ROAS = mean(Revenue / Cost, na.rm = TRUE)
  ) %>%
  arrange(desc(CTR))

Overall_summary <- merged %>%
  group_by(Category.2) %>%
  summarise(
    Total_Units = sum(Units_Sold, na.rm = TRUE),
    clicks = mean(Clicks, na.rm = TRUE),
    impression = mean(Impressions, na.rm = TRUE),
    revenue = mean(Revenue, na.rm = TRUE),
    cost =mean(Cost,na.rm = TRUE)
  ) 

Impressions = as.numeric(gsub(",", "", Impressions)),
Clicks = as.numeric(gsub(",", "", Clicks)),
Cost = as.numeric(gsub(",", "", Cost)),
Revenue = as.numeric(gsub(",", "", Revenue)),

print(category_summary)

# --- Visualization: CTR vs ROAS ---
ggplot(category_summary, aes(x = CTR, y = ROAS, color = Category.2, size = Total_Units)) +
  geom_point(alpha = 0.7) +
  geom_text(aes(label = Category.2), vjust = -0.7, size = 3) +
  scale_size_continuous(range = c(2, 8)) +
  coord_cartesian(clip = "off") +
  labs(
    title = "Category Performance: CTR vs ROAS",
    subtitle = "Bubble size represents Total Units Sold",
    x = "Click-Through Rate (Engagement Efficiency)",
    y = "Return on Ad Spend (Financial Efficiency)"
  ) +
  theme_minimal() +
  theme(legend.position = "right")
