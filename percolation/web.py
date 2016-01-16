from flask import Flask
import rdflib_web.lod import lod

app = Flask(__name__)
@app.route("/banana/")
def hello():
        return "Hello World!"
app.config['graph'] = my_rdflib_graph
app.register_blueprint(lod)
