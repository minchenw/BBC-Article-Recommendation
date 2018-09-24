# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)


@app.route("/")
def articles():
    """Show a list of article titles"""
    return render_template('articles.html', articles=articles)


@app.route("/article/<topic>/<filename>")
def article(topic, filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    for a in articles:
        if a[0] == topic+'/'+filename:
            title = a[1]
            text = a[2]
            paragraphs = text.split('\n\n')
            break
    recommend_articles = recommended(a, articles, 5)
    return render_template('article.html', title=title, paragraphs=paragraphs,recommend=recommend_articles)




# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[1]
articles_dirname = sys.argv[2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)

