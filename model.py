import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv("Crop_recommendation (1).csv")
print(df.head())
x = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']
labels = df['label']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=50)
# Instantiate the model
classifier = RandomForestClassifier()

# Fit the model
classifier.fit(X_train, y_train)

# Make pickle file of our model
pickle.dump(classifier, open("model.pkl", "wb"))