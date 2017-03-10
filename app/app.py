import subprocess as sp
from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html', container=container())

def container():
  statement = ['cat','/proc/self/cgroup']
  p = sp.Popen(statement,stdout=sp.PIPE,stderr=sp.PIPE)
  out,err = p.communicate()
  out = out.split("\n")[0].split('/')[-1]
  return out
