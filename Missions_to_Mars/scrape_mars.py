# Import dependencies 
from bs4 import BeautifulSoup 
import pandas as pd 
from time import sleep
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    ## 1. SCRAPING MARS NEWS

    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # Convention to let the script we are running sleep to allow everything to load 
    sleep(1)

    # Create a BeautifulSoup object and parse as lxml
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Obtain the latest news title 
    latest_news_titles = soup.find_all("div", class_="content_title")
    news_title = latest_news_titles[1].text

    # Obtain the paragraph (description) attached to the title above 
    latest_news_paragraphs = soup.find_all("div", class_="article_teaser_body")
    news_paragraph = latest_news_paragraphs[0].text



    ## 2. SCRAPING JPL MARS SPACE IMAGES JPL 

    # Page URL that we are going to scrape
    images_url = " "
    browser.visit(images_url)

    # Convention to let the script we are running sleep to allow everything to load 
    sleep(1)

    # Interact with the 'FULL IMAGE' button in the browser to get to the featured image
    browser.click_link_by_id('full_image')

    # Interact with the 'more info' button in the browser to access the larger image size 
    browser.click_link_by_partial_text('more info')

    # Create a BeautifulSoup object and parse as lxml
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Obtain the specific path to the larger image size 
    lg_image_url = soup.find(class_="main_image")["src"]

    # Combine the base url and path to image 
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + lg_image_url



    ## 3. SCRAPE MARS FACTS

    # Page URL that we are going to scrape
    facts_url = "https://space-facts.com/mars/"

    # use the read_html function in Pandas to obtain the data on the page in HTML 
    tables = pd.read_html(facts_url)
    print(tables)

    # Obtain the table that contains info on: Diameter, Mass, etc.
    df = tables[0]

    # Rename columns
    df.columns = ['Description', 'Mars']

    # Set the Description as index
    df.set_index('Description', inplace=True)

    # Convert the dataframe above to an HTML string
    html_table = df.to_html()
  
    # Save the html table 
    df.to_html('table.html')



    ## 4. SCRAPE MARS HEMISPHERE

    # Page URL that we are going to scrape
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    # Convention to let the script we are running sleep to allow everything to load 
    sleep(0.5)

    # Create a BeautifulSoup object and parse as lxml
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Create a list to store the dictionaries (for each hemisphere)
    hemisphere_image_urls = list()

    # Retrieve all the hemisphere link titles
    link_titles = soup.find_all('h3')
    for title in link_titles:
        print(title.text)

    # Loop through the link titles 
    for title in link_titles:
        
        # Click the next link that has the next title in link_titles
        browser.click_link_by_partial_text(title.text)
        sleep(0.5)
        
        # HTML object
        html = browser.html
        
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        
        
        # Retrieve the specific hemisphere name from the link titles 
        hem_name = title.text.split('Enhanced')[0]
        
        # Retrieve the full resolution image URL 
        img_path = soup.find("li")
        lg_img_url = img_path.a['href']
        
        # Append each dictionary to the list 
        hemisphere_image_urls.append({
            "title": hem_name,
            "img_url": lg_img_url
        })
        
        # Go back to the home page before loop repeats
        browser.visit(hemisphere_url)
        sleep(0.5)


    # Store all scraped data into a Python dictionary 
    data_on_mars = {
        "news_title": news_title,
        "news_paragraph": news_paragraph, 
        "featured_image_url": featured_image_url,
        "mars_fact_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls

    }

    # Quit browser
    browser.quit()
 
    return data_on_mars


# if running from command line, show the scraped data results
if __name__ == "__main__":
    result = scrape()
    print(result)

