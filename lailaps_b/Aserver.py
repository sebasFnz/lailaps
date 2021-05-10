from tornado import web,ioloop,httpclient,escape
import routes

application = web.Application([
    ("/instagram",routes.instagramHandler),
    ("/tiktok",routes.tiktokHandler)
],debug=True)

if __name__ == '__main__':
    port = 8888
    print("Listen at port {0}".format(port))
    try:
        application.listen(port)
        ioloop.IOLoop.current().start()

    except KeyboardInterrupt:
        ioloop.IOLoop.current().stop()
