from flask import Flask,request,abort
from route.IndexRoute import indexRoute
from route.UploadRoute import uploadRoute
from route.MonthRoute import monthRoute
from route.DetailRoute import detailRoute
from service import InitService
from util import Log

app = Flask(__name__)
app.register_blueprint(indexRoute)
app.register_blueprint(uploadRoute)
app.register_blueprint(monthRoute)
app.register_blueprint(detailRoute)

@app.route('/')
def login():
    return app.send_static_file("index.html")

Log.init()
InitService.init()
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 50*1024*1024

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8020)

