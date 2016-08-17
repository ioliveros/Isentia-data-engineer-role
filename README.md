# Coding Sample for Isentia Data Engineer Position

## How to install

### Platform
- ubuntu 16.04

### Prerequisites
- Python >= 3.4
- python3-dev(required by Falcon)
- lxml(required by Scrapy)
- Pip
- Virtualenv

```bash
git clone https://github.com/Bernardzzz/Isentia-data-engineer-role.git
cd Isentia-data-engineer-role
Python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

1. Create `config.ini` at root directory
2. Put MongoDB connection link and Readability Parser API token in the file

For example,
```ini
[mongodb]
host=[your MongoDB connection link, including username and password]

[readability]
app=[your app name]
token=[your parser token]
```

## Crawler

MongoDB is deployed on [Compose](https://app.compose.io/pilgrimz) as required. If you need access, please feel free to contact me.

### How to run

```bash
cd src/crawler
scrapy crawl guardian
```

The crawler scrapes news articles from theguardian.com

## REST API

### How to run

```bash
cd src
gunicorn app:app
```
### How to use

**Search articles**
----
  Search articles which was scraped from theguardian.com by keywords.
``
  The search behavior would perform the logical conjunction between keywords.
* ****

  [http://ec2-54-206-48-181.ap-southeast-2.compute.amazonaws.com/search](http://ec2-54-206-48-181.ap-southeast-2.compute.amazonaws.com/search)

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `keyword=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json
    {
      "[article-id]": {
        "title": "blah",
        "url": "blah",
        "content": "blah",
        "author": "blah"
      }
    }
    ```
* **Error Response:**

  * **Code** 404 Not Found <br />
    **Reason** Cannot find matching articles by the given keyword(s)

  * **Code:** 400 Missing Parameter <br />
    **Content:**
    ```json
    {
      "title": "Missing parameter",
      "description": "The \"keyword\" parameter is required"
    }
    ```
  * **Code:** 500 Internal Error <br />
    **Content:**
    ```json
    {
      "title": "[Error title]",
      "description": "[Error Reason]"
    }
    ```

* **Sample Call:**

  /search?keyword=Australia&keyword=Olympics

## Test

```bash
cd [root directory]
python -m unittest tests/test_search.py
```
