import pandas as pd
import sqlite3
from scipy import stats


bnb_df = pd.read_csv(r"C:\Users\ketan\Downloads\airbnb_nyc.csv")
print(bnb_df.isnull().sum())


bnb_df["reviews_per_month"] = bnb_df["reviews_per_month"].fillna(0)

few_rows = bnb_df[bnb_df["price"] <=10000]
print(few_rows)

zero_price = bnb_df[bnb_df["price"] > 0]
print(zero_price)

connection = sqlite3.connect("airbnb.db")

cursor = connection.cursor()
cursor.execute("SELECT room_type, AVG(price) AS avg_price FROM listings WHERE price!= 10000 AND price!=0 GROUP BY room_type ORDER BY avg_price DESC ")
results = cursor.fetchall()
connection.close()
print(results)

clean_df = bnb_df[(bnb_df["price"]!= 10000) & (bnb_df["price"]!= 0)]

entire_home = clean_df[clean_df["room_type"] == "Entire home/apt"] ["price"]
private_room = clean_df[clean_df["room_type"] == "Private room"] ["price"]

t_stat, p_value = stats.ttest_ind(entire_home, private_room)
print("t_stat", t_stat)
print("p_value", p_value)

connection = sqlite3.connect("airbnb.db")
cursor = connection.cursor()
cursor.execute("SELECT room_type, neighbourhood_group, AVG(price) AS avg_price FROM listings WHERE price!= 10000 AND price!= 0 GROUP BY neighbourhood_group, room_type ORDER BY price")
results = cursor.fetchall()
connection.close()
print(results)

clean_df = bnb_df[(bnb_df["price"]!= 10000) & (bnb_df["price"]!= 0)]

Bronx = clean_df[clean_df["neighbourhood_group"] == "Bronx"] ["price"]
Manhattan = clean_df[clean_df["neighbourhood_group"] == "Manhattan"] ["price"]
t_stat, p_value = stats.ttest_ind(Bronx, Manhattan)
print("t_stat", t_stat)
print("p_value", p_value)

connection = sqlite3.connect("airbnb.db")
cursor = connection.cursor()
cursor.execute("SELECT COUNT(minimum_nights) AS min_nights, AVG(price) AS avg_price FROM listings WHERE price!= 10000 AND price!= 0 GROUP BY minimum_nights ORDER BY avg_price DESC")
results = cursor.fetchall()
connection.close()
print(results)

relation = clean_df["minimum_nights"].corr(clean_df["price"])
print(relation)

actual_relation = clean_df[['minimum_nights',  'minimum_nights', 'calculated_host_listings_count', 'price']].corr()
print(actual_relation)

review_relation = clean_df["number_of_reviews"].corr(clean_df["availability_365"])
print(review_relation)


# ---------------------------------------------------------------------------
# BONUS: Basic linear regression (built with AI assistance)
# Goal: quantify multiple price drivers simultaneously, controlling for each
# other, rather than testing one factor at a time as above.
# ---------------------------------------------------------------------------
from sklearn.linear_model import LinearRegression

model_df = pd.get_dummies(
    clean_df[['price', 'room_type', 'neighbourhood_group', 'minimum_nights',
              'number_of_reviews', 'availability_365']],
    columns=['room_type', 'neighbourhood_group'], drop_first=True
)

X = model_df.drop(columns=['price'])
y = model_df['price']

model = LinearRegression()
model.fit(X, y)

print("R2:", round(model.score(X, y), 4))
for name, coef in zip(X.columns, model.coef_):
    print(f"{name}: {coef:.2f}")
