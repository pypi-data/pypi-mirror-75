"""

@author: Edward R Jones
@version 1.26
@copyright 2020 - Edward R Jones, all rights reserved.
"""

import sys
import warnings
import pandas as pd

import re
import requests  # install using conda install requests

from time import time
from datetime import date

try:
    import newspaper # install using conda install newspaper3k
    from newspaper import Article
except:
    warnings.warn("AdvancedAnalytics.Scrape.newspaper_stories "+\
                  "missing NEWSPAPER3K package")
try:
# newsapi requires tiny\segmenter:  pip install tinysegmenter==0.3
# Install newsapi using:  pip install newsapi-python
    from newsapi import NewsApiClient # Needed for using API Feed
except:
    warnings.warn("AdvancedAnalytics.Scrape.newsapi_get_urls "+\
                  "missing NEWSAPI package")
   
class scrape(object):
        
    def newspaper_stories(words, search_type='or', search_level=0, urls=None, 
                      display=True):
        if urls == None:
           news_urls = {
                'huffington': 'http://huffingtonpost.com', 
                'reuters':    'http://www.reuters.com', 
                'cbs-news':   'http://www.cbsnews.com',
                'usa-today':  'http://usatoday.com',
                'cnn':        'http://cnn.com',
                'npr':        'http://www.npr.org',
                'abc-news':   'http://abcnews.com',
                'us-news':    'http://www.usnews.com',
                'msn':        'http://msn.com',
                'pbs':        'http://www.pbs.org',
                'nbc-news':   'http://www.nbcnews.com',
                'fox':        'http://www.foxnews.com'}
        else:
            news_urls = urls
        
        print("\nSearch Level {:<d}:".format(search_level), end="")
        if search_level==0:
            print(" Screening URLs for search words")
            print("   URLs must contain one or more of:", end="")
        else:
            print(" No URL Screening")
            print("   Deep Search for Articles containing: ", 
                  end="")
        i=0
        for word in words:
            i += 1
            if i < len(words):
                if search_type == 'or':
                    print(word+" or ", end="")
                else:
                    print(word+" & ", end="")
            else:
                print(word)
                    
        df_articles = pd.DataFrame(columns=['agency', 'url', 'length', 
                                            'keywords', 'title', 'summary', 
                                            'story'])
        n_articles  = {}
        today       = str(date.today())
        for agency, url in news_urls.items():
            paper   = newspaper.build(url, memoize_articles=False, \
                                   fetch_images=False, request_timeout=20)
            if display:
                print("\n{:>6d} Articles available from {:<s} on {:<10s}:".
                      format(paper.size(), agency.upper(), today))
            article_collection = []
            for article in paper.articles:
                url_lower = article.url.lower()
                # Exclude articles that are in a language other then en
                # or contains mostly video or pictures
                # search_level 0 only downloads articles with at least
                # one of the key words in its URL
                # search_level 1 download all articles that appear to be
                # appear to be in English and are not mainly photos or
                # videos.
                # With either search level, if an article is downloaded
                # it is scanned to see if it contains the search words
                # It is also compared to other articles to verify that
                # it is not a duplicate of another article.
                
                 # Special Filters for some Agencies
                if agency=='cbs-news':
                    if  url_lower.find('.com') >=0 :
                        # secure-fly are duplicates of http
                        if article.url.find('secure-fly')>=0:
                            continue
                if agency=='usa-today':
                    if url_lower.find('tunein.com') >= 0:
                        continue
                if agency=='huffington':
                    # Ignore huffington if it's not .com
                    if url_lower.find('.com') < 0:
                        continue
                    
                # Filter Articles that are primarily video, film or not en
                if url_lower.find('.video/')   >=0 or \
                   url_lower.find('/video')    >=0 or \
                   url_lower.find('/picture')  >=0 or \
                   url_lower.find('.pictures/')>=0 or \
                   url_lower.find('/photo')    >=0 or \
                   url_lower.find('.photos/')  >=0 or \
                   url_lower.find('espanol')   >=0 or \
                   url_lower.find('.mx/' )     >=0 or \
                   url_lower.find('/mx.' )     >=0 or \
                   url_lower.find('.fr/' )     >=0 or \
                   url_lower.find('/fr.' )     >=0 or \
                   url_lower.find('.de/' )     >=0 or \
                   url_lower.find('/de.' )     >=0 or \
                   url_lower.find('.it/' )     >=0 or \
                   url_lower.find('/it.' )     >=0 or \
                   url_lower.find('.gr/' )     >=0 or \
                   url_lower.find('/gr.' )     >=0 or \
                   url_lower.find('.se/' )     >=0 or \
                   url_lower.find('/se.' )     >=0 or \
                   url_lower.find('.es/' )     >=0 or \
                   url_lower.find('/es.' )     >=0 :
                       continue
               
                # Filter if search_level == 0, URL quick search
                if search_level == 0:
                    # Verify url contains at least one of the key words
                    found_it = False
                    for word in words:
                        j = url_lower.find(word)
                        if j>= 0:
                            found_it = True
                            break
                    if found_it:
                        # Article contains words and passes filters
                        # Save this article for full review
                        article_collection.append(article.url)
                else:
                    #  No URL screening, Save for full review
                    article_collection.append(article.url)
            n_to_review = len(article_collection)
            if display:
                print("{:>6d} Selected for download".format(n_to_review))
            
            for article_url in article_collection:
                article = Article(article_url)
                article.download()
                n = 0
                # Allow for a maximum of 5 download failures
                stop_sec=1 # Initial max wait time in seconds
                while n<2:
                    try:
                        article.parse()
                        n = 99
                    except:
                        n += 1
                        # Initiate download again before new parse attempt
                        article.download()
                        # Timeout for 5 seconds waiting for download
                        t0 = time()
                        tlapse = 0
                        while tlapse<stop_sec:
                            tlapse = time()-t0
                        # Double wait time if needed for next exception
                        stop_sec = stop_sec+1
                if n != 99:
                    if display:
                        print("Cannot download:", article_url[0:79])
                    n_to_review -= 1
                    continue
                article.nlp()
                keywords = article.keywords
                title    = article.title
                summary  = article.summary
                story    = article.text
                story_lower_case = story.lower()
                if search_type == 'or':
                    found_it = False
                    # Verify the url contains at least one of the key words
                    for word in words:
                        j = story_lower_case.find(word)
                        if j>= 0:
                            found_it = True
                            break
                else: 
                    # search type 'and'
                    found_it = True
                    for word in words:
                        j = story_lower_case.find(word)
                        if j < 0:
                            found_it = False
                            break
                if found_it:
                    # Article contains words and passes filters
                    # Save this article for later full review
                    length   = len(story)
                    df_story = pd.DataFrame([[agency, url, length, keywords,
                                              title, summary, story]], 
                                columns=['agency', 'url', 'length', 'keywords',
                                             'title', 'summary', 'story'])
                    # Check for an identical already in the file
                    if df_articles.shape[0]==0:
                        df_articles  = df_articles.append(df_story)
                    else:
                        # Verify this story is not already in df_articles
                        same_story = False
                        for i in range(df_articles.shape[0]):
                            if story==df_articles['story'].iloc[i]:
                                same_story   = True
                                n_to_review -= 1
                                continue
                        if not(same_story):
                            df_articles  = df_articles.append(df_story)
                else:
                    n_to_review -= 1
                    
                print("=", end='')
            n_articles[agency] = [n_to_review, len(article_collection)]
        if display:
            print("\n\nArticles Selected by Agency:")
            for agency in news_urls:
                ratio = str(n_articles[agency][0]) + "/" + \
                        str(n_articles[agency][1])
                ratio = ratio
                print("{:>10s} Articles from {:<s}".
                      format(ratio, agency.upper()))
            print("\nArticles Collected on "+today+":", 
                      df_articles.shape[0],'from', 
                      df_articles['agency'].nunique(), "Agencies.")
            print("\nSize    Agency    Title")
            print("*{:->78s}*".format("-"))
            for i in range(df_articles.shape[0]):
                k = len(df_articles['title'].iloc[i])
                if k > 63:
                    for j in range(25):
                        k = 63-j
                        if df_articles['title'].iloc[i][k] == " ":
                            break
                
                    print("{:>5d} {:<10s} {:<63s}".
                          format(df_articles['length'].iloc[i], 
                                 df_articles['agency'].iloc[i],
                                 df_articles['title' ].iloc[i][0:k]))
                    if len(df_articles['title'].iloc[i])>63:
                        print("                {:<60s}".
                              format(df_articles['title'].iloc[i][k:120]))
                else:
                    print("{:>5d} {:<10s} {:<s}".
                          format(df_articles['length'].iloc[i], 
                                 df_articles['agency'].iloc[i],
                                 df_articles['title' ].iloc[i]))
                print("")
            print("*{:->78s}*".format("-"))
        return df_articles

    def clean_html(html):
        # First we remove inline JavaScript/CSS:
        pg = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        pg = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", pg)
        # Next we can remove the remaining tags:
        pg = re.sub(r"(?s)<.*?>", " ", pg)
        # Finally, we deal with whitespace
        pg = re.sub(r"&nbsp;", " ", pg)
        pg = re.sub(r"&rsquo;", "'", pg)
        pg = re.sub(r"&#x27;", "'", pg)
        pg = re.sub(r"&ldquo;", '"', pg)
        pg = re.sub(r"&rdquo;", '"', pg)
        pg = re.sub(r"&quot;", '"', pg)
        pg = re.sub(r"&amp;", '&', pg)
        pg = re.sub(r"\n", " ", pg)
        pg = re.sub(r"\t", " ", pg)
        pg = re.sub(r"/>", " ", pg)
        pg = re.sub(r'/">', " ", pg)
        k = 1
        m = len(pg)
        while k>0:
            pg = re.sub(r"  ", " ", pg)
            k = m - len(pg)
            m = len(pg)
        return pg.strip()

    def newsapi_get_urls(search_words, key, urls=None):
        if urls==None:
            agency_urls = {
            'abc-news': 'https://abcnews.go.com',
            'al-jazeera-english': 'http://www.aljazeera.com',
            'ars-technica': 'http://arstechnica.com',
            'associated-press': 'https://apnews.com/',
            'axios': 'https://www.axios.com',
            'bleacher-report': 'http://www.bleacherreport.com',
            'bloomberg': 'http://www.bloomberg.com',
            'breitbart-news': 'http://www.breitbart.com',
            'business-insider': 'http://www.businessinsider.com',
            'buzzfeed': 'https://www.buzzfeed.com',
            'cbs-news': 'http://www.cbsnews.com',
            'cnbc': 'http://www.cnbc.com',
            'cnn': 'http://us.cnn.com',
            'crypto-coins-news': 'https://www.ccn.com',
            'engadget': 'https://www.engadget.com',
            'entertainment-weekly': 'http://www.ew.com',
            'espn': 'http://espn.go.com',
            'espn-cric-info': 'http://www.espncricinfo.com/',
            'fortune': 'http://fortune.com',
            'fox-news': 'http://www.foxnews.com',
            'fox-sports': 'http://www.foxsports.com',
            'google-news': 'https://news.google.com',
            'hacker-news': 'https://news.ycombinator.com',
            'ign': 'http://www.ign.com',
            'mashable': 'http://mashable.com',
            'medical-news-today': 'http://www.medicalnewstoday.com',
            'msnbc': 'http://www.msnbc.com',
            'mtv-news': 'http://www.mtv.com/news',
            'national-geographic': 'http://news.nationalgeographic.com',
            'national-review': 'https://www.nationalreview.com/',
            'nbc-news': 'http://www.nbcnews.com',
            'new-scientist': 'https://www.newscientist.com/section/news',
            'newsweek': 'http://www.newsweek.com',
            'new-york-magazine': 'http://nymag.com',
            'next-big-future': 'https://www.nextbigfuture.com',
            'nfl-news': 'http://www.nfl.com/news',
            'nhl-news': 'https://www.nhl.com/news',
            'politico': 'https://www.politico.com',
            'polygon': 'http://www.polygon.com',
            'recode': 'http://www.recode.net',
            'reddit-r-all': 'https://www.reddit.com/r/all',
            'reuters': 'http://www.reuters.com',
            'techcrunch': 'https://techcrunch.com',
            'techradar': 'http://www.techradar.com',
            'the-american-conservative': 
                        'http://www.theamericanconservative.com/',
            'the-hill': 'http://thehill.com',
            'the-huffington-post': 'http://www.huffingtonpost.com',
            'the-new-york-times': 'http://www.nytimes.com',
            'the-next-web': 'http://thenextweb.com',
            'the-verge': 'http://www.theverge.com',
            'the-wall-street-journal': 'http://www.wsj.com',
            'the-washington-post': 'https://www.washingtonpost.com',
            'the-washington-times': 'https://www.washingtontimes.com/',
            'time': 'http://time.com',
            'usa-today': 'http://www.usatoday.com/news',
            'vice-news': 'https://news.vice.com',
            'wired': 'https://www.wired.com'}
        else:
            agency_urls = urls
        if len(search_words)==0 or agency_urls==None:
            return None
        print("Searching agencies for pages containing:", search_words)
       
        # Get your NEWSAPI key from https://newsapi.org/account
        try:
            api = NewsApiClient(api_key=key)
        except:
            raise RuntimeError("***Call to request_pages invalid.\n"+\
                               " api key was not accepted.")
            sys.exit()
            
        api_urls  = []
        # Iterate over agencies and search words to pull more url's
        # Limited to 1,000 requests/day - Likely to be exceeded 
        for agency in agency_urls:
            domain = agency_urls[agency].replace("http://", "")
            print(agency, domain)
            for word in search_words:
                # Get articles with q= in them, Limits to 20 URLs
                try:
                    articles = api.get_everything(q=word, language='en',\
                                        sources=agency, domains=domain)
                except:
                    print("--->Unable to pull news from:", agency, "for", word)
                    continue
                # Pull the URL from these articles (limited to 20)
                d = articles['articles']
                for i in range(len(d)):
                    url = d[i]['url']
                    api_urls.append([agency, word, url])
        df_urls  = pd.DataFrame(api_urls, columns=['agency', 'word', 'url'])
        n_total  = len(df_urls)
        # Remove duplicates
        df_urls  = df_urls.drop_duplicates('url')
        n_unique = len(df_urls)
        print("\nFound a total of", n_total, " URLs, of which", n_unique,\
              " were unique.")
        return df_urls
    
    def request_pages(df_urls):
        try:
            if df_urls.shape[0]==0:
                return None
        except:
            raise RuntimeError("***Call to request_pages invalid.")
            sys.exit()
            
        web_pages = []
        for i in range(len(df_urls)):
            u   = df_urls.iloc[i]
            url = u[2]
            k = len(url)
            short_url = url[0:k]
            short_url = short_url.replace("https://", "")
            short_url = short_url.replace("http://", "")
            k = len(short_url)
            if k>70:
                k=70
            short_url = short_url[0:k]
            n = 0
            # Allow for a maximum of 3 download attempts
            stop_sec=3 # Max wait time per attempt
            while n<2:
                try:
                    r = requests.get(url, timeout=(stop_sec))
                    if r.status_code == 408:
                        print("-->HTML ERROR 408", short_url)
                        raise ValueError()
                    if r.status_code == 200:
                        print(short_url)
                    else:
                        print("-->Web page: "+short_url+" status code:", \
                                  r.status_code)
                    n=99
                    continue # Skip this page
                except:
                    n += 1
                    # Timeout waiting for download
                    t0 = time()
                    tlapse = 0
                    print("Waiting", stop_sec, "sec")
                    while tlapse<stop_sec:
                        tlapse = time()-t0
            if n != 99:
                # download failed skip this page
                continue
            # Page obtained successfully
            html_page = r.text
            page_text = scrape.clean_html(html_page)
            web_pages.append([url, page_text])
        df_www  = pd.DataFrame(web_pages, columns=['url', 'text'])
        n_total  = len(df_www)
        print("Attempted to download", len(df_urls), "web pages.", \
              " Obtained", n_total, ".")
        return df_www
    
class Metrics:
    # Function for calculating loss and confusion matrix
    def binary_loss(y, y_predict, fn_cost, fp_cost, display=True):
        loss     = [0, 0]       #False Neg Cost, False Pos Cost
        conf_mat = [[0, 0], [0, 0]] #tn, fp, fn, tp
        for j in range(len(y)):
            if y[j]==0:
                if y_predict[j]==0:
                    conf_mat[0][0] += 1 #True Negative
                else:
                    conf_mat[0][1] += 1 #False Positive
                    loss[1] += fp_cost[j]
            else:
                if y_predict[j]==1:
                    conf_mat[1][1] += 1 #True Positive
                else:
                    conf_mat[1][0] += 1 #False Negative
                    loss[0] += fn_cost[j]
        if display:
            fn_loss = loss[0]
            fp_loss = loss[1]
            total_loss = fn_loss + fp_loss
            misc    = conf_mat[0][1] + conf_mat[1][0]
            misc    = misc/len(y)
            print("{:.<23s}{:10.4f}".format("Misclassification Rate", misc))
            print("{:.<23s}{:10.0f}".format("False Negative Loss", fn_loss))
            print("{:.<23s}{:10.0f}".format("False Positive Loss", fp_loss))
            print("{:.<23s}{:10.0f}".format("Total Loss", total_loss))
        return loss, conf_mat
