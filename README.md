# NYC Parking Violations Analysis

This project analyzes parking violations issued in New York City using Python, pandas, and seaborn.
It explores violation types, vehicle demographics, state and county distributions, and visualizes trends using plots and heatmaps. 

## Dataset 
- Source: [Kaggle NYC Parking Violations](https://www.kaggle.com/datasets/davinascimento/nyc-parking-violations-issued)
- Size: ~1.6 GB CSV
- Note: The file is not included in the repository.

## Features / Analysis
### Top 5 Violation Types
   <img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/94c9728d-507c-47cc-902e-fa5745dc9e29" />
   This bar chart shows the 5 most common parking violations in NYC.
   Violation code 21 (No Parking - Street Cleaning) is the most common infraction type.
   Understaning these trends can help city planners target enforcement and educational campaigns. 

### Top 5 Violations by Total Revenue 
  <img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/d7080bbf-f734-4370-a7a4-4dc8aaf4b088" />
  This bar chart shows the 5 parking violations that generate the most revenue for NYC.
  Violation code 14 (No Standing - Day/Time Limits) brings in the most revenue to the city, even though it is not always the most frequent violation.
  In contrast, violation code 21 occurs more often but contributes less to total revenue due to lower fines. 
  This analysis helps identify which violations have the greatest financial impact on the city.

### Vehicle Age Analysis
   <img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/3e68a79a-da2c-48ec-8965-7d333bff8307" />
   This bar chart shows the number of vehicles receiving tickets by their manufacturing decade.
   Older vehicles (1970-1989) and the newest vehicles (2020+) appear less frequently in the dataset, while vehicles from 2000-2009 receieve the most violations.
   The analysis suggests that the majority of tickets are issued to relatively newer vehicles, likely reflecting the vehicle population in NYC. 

### State Distribution Analysis
  <img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/abb05c10-ee2c-4e88-a4c6-f1fba7a97aac" />
  This bar chart displays the top 10 states with out of state vehicles receiving NYC parking tickets, excluding NY and NJ.
  Pennsylvania, Connecticut, and Florida are the top 3 out of state vehicles receiving tickets, indicating a significant number of tickets issued to vehicles registered out of state.
  This insight can help NYC traffic authorities understand non-local vehicle patterns. 
   
### Tickets by Subdivision and County (NYC Boroughs)
  <img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/ea701a76-e782-4a4e-b258-1fd2f3d8af42" />
  This bar chart displays parking tickets across NYC boroughs: Manhattan/New York County, The Bronx, Kings County, Queens, and Staten Island/Richmond County.
  Manhattan and Brooklyn received the highest number of violations, consistent with their population density and traffic volume. 
  This analysis helps identify boroughs with the most enforcement activity. 


## Notes
- Dataset is large (~1.6 GB). Processing may take several minutes.
- Some cleaning was done: vehicle colors standardized, old vehicle years binned.
- CSV is not included in the repo due to size. 
