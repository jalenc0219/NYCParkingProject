# =============================================================================
# Parking Violations Analysis Jalen Casey
# Data: https://www.kaggle.com/datasets/davinascimento/nyc-parking-violations-issued
# =============================================================================



import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm as cm



# =============================================================================
# 1. Load Data
# =============================================================================

df = pd.read_csv('Parking_Violations_Issued.csv', delimiter=',', on_bad_lines='skip')
df.head()


# =============================================================================
# 2. Top 5 Violation Types
# =============================================================================

# Violation code reference:
#   21 = NO PARKING - STREET CLEANING
#   38 = FAIL TO DSPLY MUNI METER RECPT
#   14 = NO STANDING - DAY/TIME LIMITS
#    7 = FAILURE TO STOP AT RED LIGHT
#   37 = EXPIRED MUNI METER

COLORS = ['purple', 'red', 'green', 'blue', 'orange']

violation_counts = df['Violation Code'].value_counts().head(5)
top_5_violations = violation_counts.head(5)

print(violation_counts)

# Bar plot: top 5 violations by count
plt.figure(figsize=(10, 6))
sns.barplot(x=top_5_violations.index, y=top_5_violations.values, palette=COLORS)
plt.xlabel("Violation Code")
plt.ylabel("Number of Violations")
plt.title("Top 5 Violations")
plt.legend([], [], frameon=False)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# =============================================================================
# 3. Top 5 Violations by Total Revenue
# =============================================================================

price_mapping = {7: 50, 14: 115, 21: 65, 37: 65, 38: 65}
df['Violation Price'] = df['Violation Code'].map(price_mapping).fillna(0)

violation_amounts = df.groupby('Violation Code')['Violation Price'].sum()
top_5_violations_amount = violation_amounts.nlargest(5)

# Bar plot: top 5 violations by total revenue
plt.figure(figsize=(10, 6))
sns.barplot(x=top_5_violations_amount.index, y=top_5_violations_amount.values, palette=COLORS)
plt.xlabel("Violation Code")
plt.ylabel("Total Revenue ($)")
plt.title("Top 5 Violations by Total Revenue")
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# =============================================================================
# 4. Do Older Cars Receive More Parking Violations?
# =============================================================================

# Preview unique vehicle years for binning decisions
df['Vehicle Year'].unique()

bin_edges  = [1970, 1980, 1990, 2000, 2010, 2020, 2030]
bin_labels = ['1970-1979', '1980-1989', '1990-1999', '2000-2009', '2010-2019', '2020-2030']

df['Year Range'] = pd.cut(
    df['Vehicle Year'],
    bins=bin_edges,
    labels=bin_labels,
    include_lowest=True
)

df.head(10)

yr_counts = df['Year Range'].value_counts().sort_index()

# Bar plot: violation frequency by vehicle decade
plt.figure(figsize=(10, 6))
yr_counts.plot(kind='bar', color='skyblue')
plt.title('Frequency of Vehicles by Decade')
plt.xlabel('Year Range')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# =============================================================================
# 5. State Distribution Analysis
# =============================================================================

parking_violations = pd.read_csv("Parking_Violations_Issued.csv")
parking_violations.head()
parking_violations.info()

# Overview of states represented
unique_states = parking_violations['Registration State'].nunique()
states_list   = parking_violations['Registration State'].unique()
state_counts  = parking_violations['Registration State'].value_counts()

print(f"Number of different states in the dataset: {unique_states}")
print(f"States represented in the dataset: {states_list}")
print("State counts:\n", state_counts)

# --- Top 10 states (excluding NY, NJ, and placeholder '99') ---

filtered_state_counts = (
    parking_violations[~parking_violations['Registration State'].isin(['NY', 'NJ', '99'])]
    ['Registration State']
    .value_counts()
)
top_10_filtered_state_counts = filtered_state_counts.head(10)

plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(
    x=top_10_filtered_state_counts.index,
    y=top_10_filtered_state_counts.values,
    palette='coolwarm'
)

for i, value in enumerate(top_10_filtered_state_counts.values):
    bar_plot.text(i, value + 0.5, str(value), ha='center', fontsize=10)

plt.xlabel('State')
plt.ylabel('Number of Occurrences')
plt.title('Top 10 States by Number of Violations (Excluding NY and NJ)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# =============================================================================
# 6. Most Common Vehicle Color by State
# =============================================================================

# Initial check before cleaning
popular_color_by_state = (
    parking_violations
    .groupby('Registration State')['Vehicle Color']
    .agg(lambda x: x.value_counts().idxmax())
)
print("Most popular vehicle color by state (pre-clean):")
print(popular_color_by_state)

# Clean vehicle color column
parking_violations['Vehicle Color'] = (
    parking_violations['Vehicle Color']
    .str.strip()
    .str.lower()
    .replace({'wh': 'white', 'bl': 'black'})
)
print("Unique vehicle colors after cleaning:", parking_violations['Vehicle Color'].unique())

# Remove rows still containing raw 'wh' or 'bl' abbreviations
parking_violations = parking_violations[~parking_violations['Vehicle Color'].isin(['wh', 'bl'])]

# Most popular color by state (post-clean)
popular_color_by_state = (
    parking_violations
    .groupby('Registration State')['Vehicle Color']
    .agg(lambda x: x.value_counts().idxmax())
    .reset_index()
)
popular_color_by_state.columns = ['State', 'Most Popular Color']

color_counts = popular_color_by_state['Most Popular Color'].value_counts()

# Bar plot: most popular vehicle color by state
plt.figure(figsize=(12, 6))
bar_plot = sns.barplot(x=color_counts.index, y=color_counts.values, palette='tab20')

for i, value in enumerate(color_counts.values):
    plt.text(i, value + 0.5, str(value), ha='center', fontsize=10)

plt.xlabel('Vehicle Color')
plt.ylabel('Number of States')
plt.title('Most Popular Vehicle Color by State')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Which state has yellow as the most popular color?
yellow_state = popular_color_by_state[popular_color_by_state['Most Popular Color'] == 'yellow']
print(yellow_state)


# =============================================================================
# 7. Vehicle Color Heatmap by State (Excluding NY, NJ)
# =============================================================================

filtered_data = parking_violations[
    ~parking_violations['Vehicle Color'].isin(['wh', 'bl']) &
    ~parking_violations['Registration State'].isin(['NY', 'NJ'])
]

top_10_colors = filtered_data['Vehicle Color'].value_counts().head(10).index
top_10_color_data = filtered_data[filtered_data['Vehicle Color'].isin(top_10_colors)]

vehicle_color_heatmap_data = top_10_color_data.pivot_table(
    index='Registration State',
    columns='Vehicle Color',
    aggfunc='size',
    fill_value=0
)

plt.figure(figsize=(12, 8))
sns.heatmap(vehicle_color_heatmap_data, cmap='YlGnBu', cbar=True, linewidths=0.5)
plt.xlabel('Vehicle Color')
plt.ylabel('Registration State')
plt.title('Top 10 Vehicle Colors by State (Excluding wh, bl, NY, and NJ)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =============================================================================
# 8. Tickets by Subdivision and County
# =============================================================================

ticket_counts_by_subdivision = parking_violations['Sub Division'].value_counts()
print(ticket_counts_by_subdivision)

ticket_counts_by_county = parking_violations['Violation County'].value_counts()
print(ticket_counts_by_county)

# Bar plot: tickets across the five NYC boroughs
borough_codes = ['NY', 'K', 'Q', 'BX', 'R']
filtered_df = parking_violations[parking_violations['Violation County'].isin(borough_codes)]
ticket_counts_by_county = filtered_df['Violation County'].value_counts()

plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(
    x=ticket_counts_by_county.index,
    y=ticket_counts_by_county.values,
    palette='viridis'
)

for i, value in enumerate(ticket_counts_by_county.values):
    plt.text(i, value + 0.5, str(value), ha='center', fontsize=10)

plt.xlabel('County')
plt.ylabel('Number of Tickets')
plt.title('Parking Violations by NYC Borough')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Most common out-of-state registration by borough (excluding NY, NJ, PA)
filtered_df = parking_violations[
    parking_violations['Violation County'].isin(['K', 'Q', 'BX', 'R']) &
    ~parking_violations['Registration State'].isin(['NY', 'NJ', 'PA'])
]

most_common_state_by_county = (
    filtered_df
    .groupby('Violation County')['Registration State']
    .agg(lambda x: x.mode()[0])
    .reset_index()
)
most_common_state_by_county.columns = ['County', 'Most Common State']
print(most_common_state_by_county)


# =============================================================================
# 9. Most Common Vehicle Year, Make, and Body Type by State
# =============================================================================

most_common_vehicle_by_state = parking_violations.groupby('Registration State').agg(
    Vehicle_Year      = ('Vehicle Year',      lambda x: x.mode()[0]),
    Vehicle_Make      = ('Vehicle Make',      lambda x: x.mode()[0]),
    Vehicle_Body_Type = ('Vehicle Body Type', lambda x: x.mode()[0])
).reset_index()
print(most_common_vehicle_by_state)

# Most common vehicle make by state
most_common_make_by_state = (
    parking_violations
    .groupby('Registration State')['Vehicle Make']
    .agg(lambda x: x.mode()[0])
    .reset_index()
)
most_common_make_by_state.columns = ['State', 'Most Common Vehicle Make']
print(most_common_make_by_state)

make_counts = most_common_make_by_state['Most Common Vehicle Make'].value_counts()

plt.figure(figsize=(12, 6))
bar_plot = sns.barplot(x=make_counts.index, y=make_counts.values, palette='tab10')

for i, value in enumerate(make_counts.values):
    plt.text(i, value + 0.5, str(value), ha='center', fontsize=10)

plt.xlabel('Vehicle Make')
plt.ylabel('Number of States')
plt.title('Most Common Vehicle Make by State')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =============================================================================
# 10. Vehicle Make Distribution Heatmap by State (Excluding NY, NJ)
# =============================================================================

vehicle_makes_by_state = (
    parking_violations
    .groupby(['Registration State', 'Vehicle Make'])
    .size()
    .unstack(fill_value=0)
    .drop(['NY', 'NJ'], errors='ignore')
)

top_states = vehicle_makes_by_state.sum(axis=1).nlargest(10).index
top_makes  = vehicle_makes_by_state.sum(axis=0).nlargest(10).index
filtered_makes_data = vehicle_makes_by_state.loc[top_states, top_makes]

plt.figure(figsize=(12, 8))
sns.heatmap(filtered_makes_data, cmap='YlGnBu', annot=True, fmt='d', cbar=True, linewidths=0.5)
plt.xlabel('Vehicle Make')
plt.ylabel('Registration State')
plt.title('Vehicle Make Distribution by State (Excluding NY and NJ — Top 10 Each)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =============================================================================
# 11. Violation Location vs. Registration State (Scatter)
# =============================================================================

plt.figure(figsize=(12, 8))
sns.scatterplot(data=parking_violations, x='Violation Location', y='Registration State')
plt.title('Violation Location vs. Registration State')
plt.xlabel('Violation Location')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# =============================================================================
# 12. County-Level Deep Dive & Population Comparison
# =============================================================================

# NOTE: This CSV is ~1.6 GB — loading may take a moment.
df = pd.read_csv("Parking_Violations_Issued.csv")
df.head()

# Standardise county names (abbreviations → full names)
county_mapping = {
    'NY':    'NEW YORK COUNTY',
    'NYC':   'NEW YORK COUNTY',
    '103':   'NEW YORK COUNTY',   # 103rd St. mis-entry
    'K':     'KINGS',
    'Q':     'QUEENS',
    'QUEEN': 'QUEENS',
    'BX':    'BRONX',
    'R':     'RICHMOND',
    'RC':    'RICHMOND',
    'RICH':  'RICHMOND',
}
df['Violation County'] = df['Violation County'].replace(county_mapping)
df['Violation County'].value_counts()

# Correlation between county (one-hot) and violation code
df_onehot = pd.get_dummies(df['Violation County'])
print(df_onehot.corrwith(df['Violation Code']))

# Top 5 violation codes per county
for county in df['Violation County'].unique():
    if pd.isnull(county):
        continue
    print(f"\n{county}")
    print(df[df['Violation County'] == county]['Violation Code'].value_counts().head(5))

# Violations per year by county
df['Year'] = pd.to_datetime(df['Issue Date']).dt.year
df_yearly = df.groupby(['Year', 'Violation County']).size().reset_index(name='Count')
df_yearly.head()

for year in df_yearly['Year'].unique():
    print(f"\n{year}")
    print(df_yearly[df_yearly['Year'] == year].groupby('Violation County')['Count'].sum())

# Sanity-check: unexpected years in dataset
print("Unique years in dataset:", df['Year'].unique())


# --- Violations vs. Population by County ---

# Total violations per county
df_county = df.groupby('Violation County').size().reset_index(name='Count')
total_violations = df_county['Count'].sum()
df_county['Percentage'] = df_county['Count'] / total_violations
df_county = df_county.sort_values('Percentage', ascending=False)

# 2024 census population data — source: worldpopulationreview.com
population = {
    'NEW YORK COUNTY': 1_600_359,
    'KINGS':           2_532_919,
    'QUEENS':          2_225_834,
    'BRONX':           1_331_144,
    'RICHMOND':          490_016,
}
total_population = sum(population.values())
percent_pop = {county: pop / total_population for county, pop in population.items()}
percent_pop = dict(sorted(percent_pop.items(), key=lambda item: item[1], reverse=True))

print("Violation percentage by county:")
print(df_county)
print("\nPopulation percentage by county:")
for county, pct in percent_pop.items():
    print(f"  {county:<20}: {pct:.4f}")


# Bar plot: violations by county
cm = plt.get_cmap("viridis_r")
percentages = np.array(list(percent_pop.values()))
normalized  = (percentages - percentages.min()) / (percentages.max() - percentages.min())
colors      = cm(normalized)

plt.figure(figsize=(10, 5))
plt.bar(df_county['Violation County'], df_county['Percentage'], color=colors)
plt.title("Violations by County")
plt.xlabel("County")
plt.ylabel("Percentage")
plt.xticks(rotation=45, ha='right')

for i in range(len(df_county)):
    plt.text(i, df_county['Percentage'].iloc[i], df_county['Count'].iloc[i], ha='center', va='bottom')

plt.tight_layout()
plt.savefig("violation_by_county.png")
plt.show()


# Bar plot: population by county
plt.figure(figsize=(10, 5))
plt.bar(percent_pop.keys(), percent_pop.values(), color=colors)
plt.title("Population Percentage by County")
plt.xlabel("County")
plt.ylabel("Percentage")
plt.xticks(rotation=45, ha='right')

for i, county in enumerate(percent_pop):
    plt.text(i, percent_pop[county], population[county], ha='center', va='bottom')

plt.tight_layout()
plt.savefig("population_by_county.png")
plt.show()
