from requests_html import HTMLSession
import pandas as pd
from datetime import datetime

'''
Base url: https://www.amazon.in/Apple-New-iPhone-12-128GB/dp/B08L5TNJHG/
add to url: /ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent
'''

# Function to load the csv file
def load_csv(logfilename, filename, output_dict):
    try:
        output_data = pd.DataFrame(output_dict)
        output_data.to_csv(filename, index=False)
        print(f'<<< {filename} Created >>>')
        with open(logfilename, 'a') as f:
            f.write(f'<<< {filename} Created >>>\n')
        return 1
    except Exception as arg:
        print("Some exception has occured!!! Please check")
        print(arg)
        with open(logfilename, 'a') as f:
            f.write("Some exception has occured!!! Please check\n")
            f.write(str(arg))
            f.write("\n")
        return 0

# Function to scrap the data
def Amazon_pr_review_scraper():
    # Fetching current UTC time to name the log & Output file
    dt = datetime.now()
    hour = dt.hour
    minute = dt.minute
    seconds = dt.second
    UTC = str(hour) + '_' + str(minute) + '_' + str(seconds)
    date = dt.strftime("%d") + '-' + dt.strftime("%m") + '-' + str(dt.year)
    Logfile_name = 'Logfile-pr-review_' + date + '_' + UTC + '.txt'
    OutputFile_name = 'ProductReviews_' + date + '_' + UTC + '.csv'
    with open(Logfile_name, 'w') as f:
        f.write(f"Application started at <<< {date} {UTC} >>>\n")

    # Initializing the review dictionary to store the data
    Url_list = []
    reviews_dict = {
        'TITLE': [],
        'COLOUR': [],
        'SIZE': [],
        'CONTENT': [],
        'VERIFIED': []
    }
    terminate = 0

    try:
        # Reading the urls from the file
        with open('url.txt','r') as f:
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
        with open(Logfile_name,'a') as f:
            f.write("Below exception has occured while reading the url.txt file.\n")
            f.write(str(arg))
            f.write('\n')

    # Checking whether to proceed or not
    if terminate == 1:
        for url in Url_list:
            if url.find('/dp/'):
                url = url.replace('/dp/', '/product-reviews/')
                url = url + '/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber='
                #header = {
                #    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

                # Initializing a session
                session = HTMLSession()
                with open(Logfile_name,'a') as f:
                    f.write(f"URL framed is {url}\n")
                # Looping through all the pages
                for i in range(1, 20):
                    print(f"Url: {url+str(i)}")
                    with open(Logfile_name, 'a') as f:
                        f.write(f"Scrapping page no: {str(i)}\n")
                    print(f"Scrapping page no: {str(i)}")
                    Response = session.get(url + str(i))
                    print('The Response of the url: ', Response)
                    print("\n")

                    # Scraping the reviews. When no reviews are found terminating the loop
                    if not Response.html.find('div[data-hook=review]'):
                        print("No reviews are found")
                        break
                    else:
                        Reviews = Response.html.find('div[data-hook=review]')
                        # Looping through the reviews list
                        for review in Reviews:
                            # Checking for the Review title
                            try:
                                review_title = review.find('a[data-hook=review-title] span', first=True).text
                            except:
                                review_title = ''
                            # Checking for the Product specification
                            try:
                                Product_specs = review.find('a[data-hook=format-strip]', first=True).text.split(':')
                                Product_colour = str(Product_specs[1]).replace('(PRODUCT)','')
                                Product_colour = Product_colour.replace('Size name','').strip()
                                Product_size = str(Product_specs[2]).replace('Pattern name','').strip()
                            except:
                                Product_colour = ''
                                Product_size = ''
                            # Checking for the Review Content
                            try:
                                review_content = review.find('span[data-hook=review-body] span', first=True).text
                            except:
                                review_content = ''
                            # Checking for the Verified customer
                            if not review.find('span[data-hook=avp-badge]'):
                                Verified_purchase = "No"
                            else:
                                Verified_purchase = "Yes"
                            # Appending the collected data to the dictionary
                            reviews_dict['TITLE'].append(review_title)
                            reviews_dict['COLOUR'].append(Product_colour)
                            reviews_dict['SIZE'].append(Product_size)
                            reviews_dict['CONTENT'].append(review_content)
                            reviews_dict['VERIFIED'].append(Verified_purchase)
                            print(f"Title: {review_title}")
                            print(f"Product colour: {Product_colour}")
                            print(f"Product size: {Product_size}")
                            print(f"Review: {review_content}")
                            print(f"Verfied purchase: {Verified_purchase}")
                            print("===="*25)
                    print("####"*25)
            print("URL Completed")
        # Passing values to the load csv function to create outputfile
        Load_output = load_csv(Logfile_name, OutputFile_name, reviews_dict)
        print("Program completed successfully") if Load_output else print("Some excpetion has occured")
    else:
        print("Closing the application due to error. Please check!!!")

# Main Function
if __name__ == '__main__':
    # Calling the scraper function
    Amazon_pr_review_scraper()
