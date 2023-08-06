# bizbuzz
Bizz Buzz is a news aggregator service which provides users with all the latest news or ‘buzz’ about their favorite businesses. Our website uses Python's Beautiful Soup framework to scrape four different news sources and accumulates scraped article titles, urls, and summaries to a SQLite database. Users of our website can create an account and subcribe to any combination of the 14 companies our website supports. Changing a users company subscriptions will change the news that is displayed on the home page. Our front end was built using Python's Django framework and allows users to seemlessly login, signup, and make changes to their preferences. In addition, the home page displays each news article in a card format which upon being clicked will navigate users to the full article.

Link to project GitHub: https://github.com/andrewbriceno/bizbuzz

Package name on PyPI: pip install bizzbuzz==0.0.6

****Before running executable line, please cd into the directory that holds manage.py****

Executable line: bizzbuzz

Navigate to 127.0.0.1:8000/bizzbuzz in your browser and our project should be running!
