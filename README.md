# WebScraper

## Project Implementation Steps

### stages 1-3

1. Provide url of the product's opinions page
2. send a request to provided URL (from the client to the web servers using protacals)
3. Fetch necessery information (e.g. product name, all opinions)
4. Parse opinions/information to extract requierd data
5. Check for multiple pages of oppinions(check for link for next page with opinions) 
6. and if so, repete steps 1 to 5 for all pages with opinions about the product
7. save acuiered opinions to a file database

## Project Inputs

### Product codes
- 39747497
- 88404566
- 116421227
- 172765143
- 11309799
- 57480155
- 1335235566
- 90558892
- 174130671

### Opinion structure Structure
|components|name|selector|
|----------|----|--------|
|opinion ID|opinion_id|[data-entry-id]|
|opinion’s author|author|span.user-post__author-name|
|author’s recommendation|recomendations|span.user-post__author-recomendation > em|
|score expressed in number of stars|score|span.user-post__score-count|
|opinion’s content|content|div.user-post__text|
|list of product advantages|pros|div.review-feature__item--positive|
|list of product disadvantages|cons|div.review-feature__item--negative|
|how many users think that opinion was helpful|helpfull|button.vote.yes > span|
|how many users think that opinion was unhelpful|unhelpfull|button.vote.no > span|
|publishing date|publishing_date|span.user-post__published > time:nth-child(1)[datetime]|
|purchase date|purchese_date|span.user-post__published > time:nth-child(2)[datetime]|

