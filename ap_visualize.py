from splinter import Browser
from bs4 import BeautifulSoup as soup
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

def remove_stopwords(list):
    '''Function to remove unimportant words from list of words on front page'''
    
    nltk.download('stopwords')
    nltk.download('punkt')
    # Get a list of English stopwords
    stop_words = set(stopwords.words('english'))

    # Filter out the stopwords
    filtered_words = [word for word in list if word.lower() not in stop_words]

    return filtered_words



def ap_scrape_clean_viz():
    '''Retrieves text from Associated Press webpages,
      cleans it using remove_stopwords function, and
      creates a visualization using the text.'''


    browser = Browser('chrome')
    # starts in list so we can add other links to it later, then extract data for all pages in one step
    urls = ['https://apnews.com/']
    browser.visit(urls[0])

    html = browser.html
    ap_soup = soup(html, 'html.parser')

    # initialize list for later
    link_text = []

    # extract each topic
    topics_links = ap_soup.find_all(class_ = 'AnClick-MainNav')

    # grab link for each topic
    for topic in topics_links:
        if topic['href'] in urls:
            pass
        else:
            urls.append(topic['href'])

    # visit each topic page, parse for article, image, and promo text, then adds all text to list for later
    for url in urls:
        browser.visit(url)
        html = browser.html
        ap_soup = soup(html, 'html.parser')

        # article links text contain header of news article, sometimes image header
        ap_article_links = ap_soup.find_all(class_ = 'Link')
        # text for the breaking news bar underneath website nav
        promo_text = ap_soup.findAll(class_ = ' PagePromoContentIcons-text')
        
        # take text from articles
        for link in ap_article_links:
            try:
                text = link.text.strip()
                if text:
                    link_text.append(text)
            except:
                pass
        # take text from breaking news
        for link in promo_text:
            try:
                text = link.text.strip()
                if text:
                    link_text.append(text)
            except:
                pass

    browser.quit()

    # separate and clean text
    words_list = []
    for item in link_text:
        words = (item.split(' '))
        for word in words:
            words_list.append(word)

    cleaned_list = remove_stopwords(words_list)
    cleaned_count = {}
    for word in cleaned_list:
        key = word
        if key in  cleaned_count:
            cleaned_count[key] += 1
        else:
            cleaned_count[key] = 1

    cleaned_count = {k: v for k, v in sorted(cleaned_count.items(), key=lambda item: item[1], reverse=True)}

    # visualize
    n = 20
    clean_top_words = list(cleaned_count.keys())[:n]
    clean_top_counts = [cleaned_count[word] for word in clean_top_words]

    plt.barh(clean_top_words, clean_top_counts)
    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.title('Most Used Words on Main Pages of AP Website')

    plt.savefig('ap_plot.png', format='png', bbox_inches='tight')

if __name__ == '__main__':
    ap_scrape_clean_viz()