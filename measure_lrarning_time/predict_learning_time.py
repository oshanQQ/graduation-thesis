import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the CSV file as a pandas DataFrame
df = pd.read_csv('learning_time_on_local.csv')

# Split the DataFrame into features (X) and target (y)
X = df[['batch_size', 'epoch']]
y = df['learning_time']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model on the test data
test_score = model.score(X_test, y_test)
print("Test Score:", test_score)
