import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# new dataframe to store data on listings marked as sold
sold_df = pd.read_csv('SoldBuilding.csv', index_col=0, thousands=',')
sold_df
# no.of missing values for each variable 
sold_df.isnull().sum()
# replacing missing values inplace with the column's mean 
sold_df['sold_price'].fillna((sold_df['sold_price'].mean()), inplace=True)
sold_df['redfin_estimates'].fillna((sold_df['redfin_estimates'].mean()), inplace=True)
# drop rows with irrelevant property_type values
sold_df.drop(sold_df.loc[sold_df['property_type']=='Yes'].index, inplace=True)
sold_df.drop(sold_df.loc[sold_df['property_type']=='No'].index, inplace=True)

# average sold price
sold_df.sold_price.mean()
# average price per property type
sold_df.groupby("property_type").sold_price.mean()
# visualize avg sold price across property types 
sns.catplot(x="sold_price", y="property_type", 
            kind='bar', data=sold_df).fig.suptitle("Average Selling Price across Property Types", y=1);
# examining relationship between transit score & sold price, with bivariate & univariate graphs
sns.jointplot(x="transit_score", y="sold_price", data=sold_df, kind="reg", 
              color='forestgreen').fig.suptitle("Correlation: Transit Score & Sold Price", y=1);
# examining relationship between bike score & sold price
sns.jointplot(x="bike_score", y="sold_price", data=sold_df, kind="reg", 
              color='red').fig.suptitle("Correlation: Biking Score & Sold Price", y=1.0);
# examining relationship between walking score & sold price
sns.jointplot(x="walking_score", y="sold_price", data=sold_df, kind="reg", 
              color='blue').fig.suptitle("Correlation: Walking Score & Sold Price", y=1);

# visualize avg sold price by location
sns.catplot(x="sold_price", y="building_location", 
            kind='bar', data=sold_df).fig.suptitle("Average Selling Price across Locations", y=1.05);

# histogram to look at distribution of sold price
sold_df['sold_price'].plot(figsize=(10,3), kind="hist", title="Sold Price Distribution", grid=True);
# histogram to look at distribution of redfin estimates
sold_df['redfin_estimates'].plot(figsize=(10,3), kind="hist", title="Redfin Estimates Distribution", grid=True);
# kde plots for estimates & sold price
sns.kdeplot(sold_df.redfin_estimates, 
            label='Redfin Estimates');
sns.kdeplot(sold_df.sold_price, 
            label="Sold Price").set_title("Comparison: KDE Plots for Estimates and Sold Price", y=1.1);
plt.legend(loc='upper right', 
           labels=['Redfin Estimates', 'Sold Price']);

# kde plots comparing distributions of 3 diff. property types 
sns.kdeplot(sold_df.sold_price[sold_df.property_type=='Single Family Residential'], 
            label='Single Family Residential');
sns.kdeplot(sold_df.sold_price[sold_df.property_type=="Multi-Family (2-4 Unit)"], 
            label="Multi-Family (2-4 Unit)");
sns.kdeplot(sold_df.sold_price[sold_df.property_type=="Condo/Co-op"], 
            label="Condo/Co-op").set_title("Comparison: KDE Plots for Selected Property Types", y=1.1);
plt.legend(title='Property Type', loc='upper right', 
           labels=['Single Family Residential', 'Multi-Family (2-4 Unit)', "Condo/Co-op"]);
