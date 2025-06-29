import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Sample labeled data — descriptions and their categories
data = {
    "description": [
        "grocery store",
        "bus ticket",
        "monthly rent",
        "movie ticket",
        "electricity bill",
        "restaurant dinner",
        "taxi fare",
        "salary payment",
        "coffee shop",
        "gym membership"
    ],
    "category": [
        "Groceries",
        "Transport",
        "Rent",
        "Entertainment",
        "Utilities",
        "Food",
        "Transport",
        "Salary",
        "Food",
        "Health"
    ]
}

df = pd.DataFrame(data)

# Vectorize text descriptions
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['description'])

# Train a simple classifier
model = MultinomialNB()
model.fit(X, df['category'])

# Save model and vectorizer
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully.")
