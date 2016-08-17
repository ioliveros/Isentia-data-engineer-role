# Coding Sample for Isentia Data Engineer Position

## REST API

**Search articles**
----
  Search articles which was scraped from theguardian.com by keyword

* ****

  `http://ec2-54-206-48-181.ap-southeast-2.compute.amazonaws.com/search`

* **Method:**

  `GET`

*  **URL Params**

  **Required:**

   `keyword=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`

* **Error Response:**


  * **Code:** 401 UNAUTHORIZED <br />
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

  OR

  * **Code:** 422 UNPROCESSABLE ENTRY <br />
    **Content:** `{ error : "Email Invalid" }`

* **Sample Call:**

  /search?keyword=hello&keyword=world
