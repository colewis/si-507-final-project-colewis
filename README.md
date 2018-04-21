# si-507-final-project-colewis
Your GitHub repo must contain a README.md file that gives an overview of your project, including:

I used data from the American Kennel Club website, starting at http://www.akc.org/dog-breeds/ and scraping and crawling that page and the pages for all of the subcategories for the categories listed on the left side of the page. I only ended up caching the data for the first 15 dogs because my cache file was too big to handle when I was scraping all 265 breeds, but that was what I was doing originally.

Significant data processing functions:

1. scrape_breed_names -- scrapes the http://www.akc.org/dog-breeds/ page and any subcategory pages to get the breed names that appear on those pages/in those subcategories -- takes a list of URLs and returns a list of breed names
2. crawl_urls -- takes the string for a category and a specific subcategory and appends those URLs to a specified list, which I then entered into scrape_breed_names -- I had it taking page numbers too, but since I ended up only doing the first 15 dogs, I didn't need to go past the first page for each subcategory

Code is structured by first establishing my caching code, then defining the above functions, then calling these functions for a multitude of categories/subcategories, then appending the information to a dictionary in which each breed name was assigned a dictionary value, within which each category was a key and the specific subcategories for that dog were assigned to the appropriate keys. I then made a CSV file from the dictionary, and from the CSV file I created my main database (breeds). After creating the database I created separate tables for each category to assign IDs to in order to establish a primary/foreign key relationship with the breeds table. I then define my class, which returns all of the breeds in the list, from which I selected the top five to incorporate into my flask app. I then wrote code for my flask app that linked to individual templates for each page on the site.

All you need to do to run the program is open the virtual environment, puppy_power, and follow the installation instructions in the requirements.txt, then run the program, and choose your paths on the flask site.
