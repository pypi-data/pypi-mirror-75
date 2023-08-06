from app import app

from flask_boiler.context import Context as CTX
application = CTX.services.engine.wrap(app)

if __name__ == '__main__':
    import os
    PORT = int(os.environ['LEANCLOUD_APP_PORT'])

    # 只在本地开发环境执行的代码
    from gevent.pywsgi import WSGIServer
    from werkzeug.serving import run_with_reloader
    from werkzeug.debug import DebuggedApplication

    @run_with_reloader
    def run():
        global application
        app.debug = True
        application = DebuggedApplication(application, evalex=True)
        server = WSGIServer(('0.0.0.0', PORT), application)
        server.serve_forever()

    run()

