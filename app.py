import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer


ps=PorterStemmer()

tfidf = pickle.load(open("vectorizer.pkl",'rb'))

model = pickle.load(open("model.pkl",'rb'))

st.title("Email/SMS Spam Classifier")


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():  # removing special characters
            y.append(i)

    text = y.copy()
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:  # removing stopwords and punctuation
            y.append(i)

    text = y.copy()
    y.clear()

    for i in text:
        y.append(ps.stem(i))  # stemming

    return " ".join(y)  # converting output to a string


input_sms = st.text_area('Enter the message')

if st.button('Predict'):
    #1.Transform

    transformed_sms = transform_text(input_sms)

    #2.Vectorization

    vector_input = tfidf.transform([transformed_sms])

    #3.Predict

    result = model.predict(vector_input)[0]

    #4.Display

    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")




