import falcon
from Resources.Search import Search

app = falcon.API()

app.add_route('/search', Search())
