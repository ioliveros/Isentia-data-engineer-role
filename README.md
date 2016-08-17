# Coding Sample for Isentia Data Engineer Position

## REST API

**Search articles**
----
  Search articles which was scraped from theguardian.com by keywords.

  The search behavior would perform the logical conjunction between keywords.
* ****

  `http://ec2-54-206-48-181.ap-southeast-2.compute.amazonaws.com/search`

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
        "content": "blah"
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
