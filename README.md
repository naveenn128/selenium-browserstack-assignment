#  El País Web Scraper - Selenium & BrowserStack
This project demonstrates web scraping, API integration, and text processing using Selenium and BrowserStack.The script:

Navigates to the El País website.

Accepts the cookie consent pop-up.

Extracts first five article titles from the Opinión section.

Translates titles from Spanish to English using Google Translate Web API (via deep_translator).

If images are available,it downloads and saves the cover image of each article.

Identifies frequently repeated words across translated headlines.

Runs tests across multiple browsers/devices on BrowserStack.

## Prerequisite
```
python3 should be installed
```

## Setup

``` 
* Install necessary packages and do the environment setup.
```

```

## Configure BrowserStack Credentials
* Add your BrowserStack username and access key in the `browserstack.yml` config fle.
* You can also export them as environment variables, `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY`:

  #### For Linux/MacOS
    ```
    export BROWSERSTACK_USERNAME=<browserstack-username>
    export BROWSERSTACK_ACCESS_KEY=<browserstack-access-key>
    ```
  #### For Windows
    ```
    setx BROWSERSTACK_USERNAME=<browserstack-username>
    setx BROWSERSTACK_ACCESS_KEY=<browserstack-access-key>
    ```

## Running tests
* Run Tests Locally:
  - To run the sample test without BrowserStack, execute:
    ```
    python test.py
    ``` 
* Run Tests on BrowserStack:
  - To execute tests across multiple browsers/devices on BrowserStack
    ```
    browserstack-sdk python ./tests/test.py
    ``` 
