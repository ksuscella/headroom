import tornado.escape
import tornado.ioloop
import tornado.web
import os
import logging

from WikipediaQuery_Location import WikiQueryLoc
from NOAAQuery_Location import NOAAQueryLoc
from WikipediaQuery_Id import WikiQueryId

# Simple web server that serves html content from /Users/kirk/Documents/GoMaxGo/headroom/web/
# url http://localhost:8889/web/index.html
# heroku logs --app headroom
from tornado.log import enable_pretty_logging
enable_pretty_logging() 

#static_path = "/Users/kirk/Documents/GoMaxGo/headroom/web/" #-Removed hard path
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"web")

class RESTHandler(tornado.web.RequestHandler):
    def get(self):
        a=''
        #Determine REST service
        if self.get_argument('type') == 'geo':
            #Geo Service
            lat = self.get_argument('getLat')
            lng = self.get_argument('getLng')
            logging.info("RESTHandler Request - geo")
            logging.info(lat + ", " + lng)
            a = WikiQueryLoc(lat, lng)
            
        if self.get_argument('type') == 'weather':
            #Geo Service
            lat = self.get_argument('getLat')
            lng = self.get_argument('getLng')
            logging.info("RESTHandler Request - weather")
            logging.info(lat + ", " + lng)
            a = NOAAQueryLoc(lat, lng)
            
        if self.get_argument('type') == 'pageid':
            #PageID Service
            page_id = self.get_argument('getPageID')
            logging.info("RESTHandler Request - pageid")
            a = WikiQueryId(page_id)
        
        self.write(a.getResults())
        
def main():
    application = tornado.web.Application([
        (r"/", RESTHandler),
        (r"/web/(.*)",tornado.web.StaticFileHandler, {"path": static_path}) 
    ])
    #application.listen(8889)
    #tornado.ioloop.IOLoop.instance().start()

    #Match
    #http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    main()