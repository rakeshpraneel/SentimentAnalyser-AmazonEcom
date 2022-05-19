from requests_html import HTMLSession
from datetime import datetime
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word

# Function to analyse the view about the product
def Sentiment_analyse(Content):

    # Replacing the special characters, non word character, new line, return, tab
    Content = Content.replace('[^\w\s]', "")
    Content = Content.replace('\n', " ")
    #print(Content)

    # Removing the stop words
    stope = stopwords.words('english')
    Content = " ".join(c for c in Content.split() if c not in stope)
    #print(Content)

    # Lemitaizing the data
    Content = " ".join([Word(word).lemmatize() for word in Content.split()])
    #print(Content)

    # Sentiment analysing
    Result = TextBlob(Content)
    print(f"Polarity of this review: {Result.polarity}")
    if Result.polarity > 0:
        print("This review is postive")
    elif Result.polarity < 0:
        print("This review is negative")
    else:
        print("This review is neutral")

# Function to scrape the data
def data_scraper():
    # Fetching current UTC time to name the log & Output file
    dt = datetime.now()
    hour = dt.hour
    minute = dt.minute
    seconds = dt.second
    UTC = str(hour) + '_' + str(minute) + '_' + str(seconds)
    date = dt.strftime("%d") + '-' + dt.strftime("%m") + '-' + str(dt.year)
    Logfile_name = 'Logfile-single-senti-analyser_' + date + '_' + UTC + '.txt'
    with open(Logfile_name, 'w') as f:
        f.write(f"Application started at <<< {date} {UTC} >>>\n")

    # Initializing the review dictionary to store the data
    Url_list = []
    terminate = 0

    try:
        # Reading the urls from the file
        with open('url.txt', 'r') as f:
            f_content = f.readlines()
        if f_content:
            terminate = 1
            for content in f_content:
                Url_list.append(content.strip())
        else:
            print("File is Empty.")
            with open(Logfile_name, 'a') as f:
                f.write("url.txt file is EMPTY!!!\n")
                f.write("Please check it.\n")
    except Exception as arg:
        print(f"Some exception has occured. {arg}")
        with open(Logfile_name, 'a') as f:
            f.write("Below exception has occured while reading the url.txt file.\n")
            f.write(str(arg))
            f.write('\n')
    # Checking whether to proceed or not
    if terminate == 1:
        for url in Url_list:
            if url.find('/dp/'):
                url = url.replace('/dp/', '/product-reviews/')
                url = url + '/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent'
                #header = {
                #    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

                # Initializing a session
                session = HTMLSession()
                with open(Logfile_name,'a') as f:
                    f.write(f"URL framed is {url}\n")
                Response = session.get(url)
                print('The Response of the url: ', Response)
                print("\n")

                # Scraping the reviews. When no reviews are found terminating the loop
                if not Response.html.find('div[data-hook=review]'):
                    print("No reviews are found")
                    break
                else:
                    Reviews = Response.html.find('div[data-hook=review]')
                    # Using the first Review present as the order is in by recent
                    review = Reviews[0]
                    # Checking for the Review title
                    try:
                        review_title = review.find('a[data-hook=review-title] span', first=True).text
                    except:
                        review_title = ''
                    # Checking for the Review Content
                    try:
                        review_content = review.find('span[data-hook=review-body] span', first=True).text
                    except:
                        review_content = ''
                    # If review content is empty then review title is taken into consideration
                    if review_content == '':
                        review_content = review_title
                    print(f"Review posted: \n{review_content}",)
                    Sentiment_analyse(review_content)
            print("URL Completed")
    else:
        print("Closing the application due to error. Please check!!!")

# Main Function
if __name__ == '__main__':
    data_scraper()