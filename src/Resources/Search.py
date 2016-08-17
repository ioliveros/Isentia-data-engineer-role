import falcon
import pymongo
import configparser
import json


class Search(object):

    def on_get(self, req, resp):
        keywords = req.params.get('keyword')
        if keywords is None:
            raise falcon.HTTPMissingParam('keyword')

        config = configparser.ConfigParser()
        config.read('../config.ini')
        db_host = config.get('mongodb', 'host')
        try:
            client = pymongo.MongoClient(host=db_host)
            db = client.get_database('guardian')
        except pymongo.errors as e:
            raise falcon.HTTPInternalServerError(
                title="Database Error",
                description="Cannot connect to database"
            )
        result = search(keywords, db.news)
        client.close()
        if result is None:
            raise falcon.HTTPNotFound()
        else:
            resp.body = json.dumps(result)


def search(keywords, collection):
    if isinstance(keywords, str):
        search_str = "\"" + keywords + "\""
    elif isinstance(keywords, list):
        search_str = ''
        for keyword in keywords:
            search_str = search_str + "\"" + keyword + "\" "
    else:
        return None
    try:
        cursor = collection.find(
            {
                "$text": {
                    "$search": search_str
                }
            }
        )
    except pymongo.errors as e:
        raise falcon.HTTPInternalServerError(
            title="Database error",
            description="Cannot query database.")
    result = {}
    if cursor.count() == 0:
        return None
    for doc in cursor:
        article_id = str(doc['_id'])
        result[article_id] = {}
        result[article_id]['title'] = doc['title']
        result[article_id]['author'] = doc['author']
        result[article_id]['content'] = doc['content']
        result[article_id]['url'] = doc['url']
    return result
