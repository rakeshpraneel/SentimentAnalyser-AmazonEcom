import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word

'''
1.) reading data from csv file
2.) removing non data values and filling the empty review content rows with their repective review title
3.) removing stop words
4.) lematizing the content
5.) sentiment analysing and providing feedback
'''

# Function for sentiment analyser
def Senti_analyser():
    # Getting I/P filename from the user
    print("Enter the input csv filename with path if it is present in different directory. "
          "If it is present in current directory, Please enter the filename alone.\n")
    filename = input("Please enter the input filename: ")
    Data_frame = pd.read_csv(filename)
    print(Data_frame.shape)
    print(Data_frame.index)
    print(Data_frame['CONTENT'])

    # Replacing the special characters, non word character, new line, return, tab
    Data_frame['CONTENT'] = Data_frame['CONTENT'].str.replace('[^\w\s]',"")
    Data_frame['CONTENT'] = Data_frame['CONTENT'].str.replace('\n', " ")
    print(Data_frame['CONTENT'][0:15])

    # Here We are going to replace the empty rows with respective title values
    # Replacing empty rows with NAN
    Data_frame['CONTENT'].replace('', np.nan)
    print(Data_frame['CONTENT'][0:15])

    # Replacing NAN values with respective Title values
    #Data_frame.dropna(subset=["CONTENT"], inplace=True)
    Data_frame['CONTENT'].fillna(Data_frame['TITLE'], inplace=True)
    print(Data_frame['CONTENT'][0:15])

    # Removing the stop words
    stope = stopwords.words('english')
    Data_frame['CONTENT'] = Data_frame['CONTENT'].apply(lambda a: " ".join(a for a in str(a).split() if a not in stope))
    print(Data_frame['CONTENT'][0:15])

    # Lemitaizing the data
    Data_frame['CONTENT'] = Data_frame['CONTENT'].apply(lambda b: " ".join([Word(word).lemmatize() for word in b.split()]))
    print(Data_frame['CONTENT'][0:15])
    Reviews = Data_frame['CONTENT']

    # Sentiment analysing
    postive_rating = 0
    negative_rating = 0
    neutral = 0
    Total_polarity = 0
    for r in Reviews:
        Results = TextBlob(r)
        print(Results.polarity)
        Total_polarity+=Results.polarity
        if Results.polarity > 0:
            postive_rating+=1
        elif Results.polarity < 0:
            negative_rating+=1
        else:
            neutral+=1
    print("++++"*25)
    print(f"Total Reviews analysed: {len(Reviews)}")
    print(f"Total polarity about the product: {Total_polarity}")
    if Total_polarity > 0:
        print("Most of the people like this product")
    elif Total_polarity < 0:
        print("Most of the people dislike this product")
    else:
        print("People have a balanced view about this product")
    print(f"Total postive rating: {postive_rating}\n"
          f"Total Negative rating: {negative_rating}\n"
          f"Total neutral rating: {neutral}")



# Main function
if __name__ == '__main__':
    Senti_analyser()