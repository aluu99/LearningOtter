import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import csv

web_data = pd.read_csv('docs/web_data.csv')
user_data = pd.read_csv('docs/dummy_data.csv')  # Replace 'sentiment_data.csv' with your dataset file

def train_from_csv(data):
    # Load and preprocess the data
    X = data['example']
    y = data['difficulty']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a TF-IDF vectorizer to convert text into numerical features
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    # Train a support vector machine (SVM) classifier with neutral category
    svm = SVC(kernel='linear')
    svm.fit(X_train, y_train)

    # Predict the sentiment labels for the test set
    y_pred = svm.predict(X_test)

    # Evaluate the performance of the model
    print(classification_report(y_test, y_pred))

    return svm, vectorizer

def add_to_csv(text, sentiment):
    with open('user_sentiment.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        field = [text, sentiment]
        writer.writerow(field)

def get_random_article(df):

    random_index = df.sample().index.item()
    random_article = df.loc[random_index, 'example']
    df = df.drop(random_index)

    return random_article, df

def update_user_data(df, svm, vectorizer):
    # add another row to web_data called predicted_difficulty based on AI model
    def predict(article, vectorizer):

        # Preprocess the new text using the same vectorizer used during training
        new_text_vec = vectorizer.transform([article])

        # Use the trained model to predict the sentiment of the new text
        prediction = svm.predict(new_text_vec)[0]


        return prediction
    
    # Add a new column for sentiment predictions
    df['Sentiment'] = ''

    # Iterate over each row and predict sentiment
    for index, row in df.iterrows():
        text = row['example']
        sentiment = predict(text, vectorizer)
        df.at[index, 'Sentiment'] = sentiment


    return df

def get_suggested_articles(web_data, user_data):
    # returns first a user defined article 
    # if all of them run out, suggest a new article based on predicted_difficulty
    #if user_data.empty() is False:
    
    if not user_data.empty:
        user_data = user_data[user_data['difficulty'] == 'just right']
        article, user_data = get_random_article(user_data)
    elif not web_data.empty:
        user_data = user_data[user_data['difficulty'] == 'just right']
        article, user_data = get_random_article(user_data)
    else:
        article = "No more articles"

    return article

while True:
    article, web_data = get_random_article(web_data)
    print(article)
    user_input = input("\n [1] Too Easy, [2] Just Right, [3] Too Hard, [4] Read, [5] Stop: ")

    if user_input == "4":
        svm, vectorizer = train_from_csv(user_data)
        web_data = update_user_data(user_data, svm, vectorizer)

        while True:
            sug_article = get_suggested_articles(web_data, user_data)

            print(sug_article)

            user_input = input("\n [1] New Article [2] Stop: ")

            if user_input == "1":
                sug_article = get_suggested_articles(web_data, user_data)
            else:
                break
    elif user_input == "1":
        add_to_csv(article, "too easy")
    elif user_input == "2":
        add_to_csv(article, "just right")
    elif user_input == "3":
        add_to_csv(article, "too hard")
    else:
        break


