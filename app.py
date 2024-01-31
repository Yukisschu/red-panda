from flask import Flask, request, jsonify, render_template
import utils
from flask import Flask as _Flask,jsonify
from flask import request
from flask import render_template
import decimal
import utils
import string
import emotion_score

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/time')
def get_time():
    return utils.get_time()

@app.route('/todaysum')
def get_today_sum_data():
    post = utils.get_posts_today()
    comment = utils.get_comments_today()
    valence_score = emotion_score.get_emotion_score(utils.get_selftext_today())["Valence"]
    valence = round(valence_score.mean(), 2)
    arousal_score = emotion_score.get_emotion_score(utils.get_selftext_today())["Arousal"]
    arousal = round(arousal_score.mean(), 2)

    ups = utils.get_ups_today()
    downs = utils.get_downs_today()
    # result_dict = {
    #     "post": post,
    #     "arousal": arousal,
    #     "valence": valence,
    #     "comment": comment,
    #     "ups": ups,
    #     "downs": downs
    # }
    # return jsonify(result_dict)
    # return post, arousal, valence, comment, ups, downs
    return jsonify({"post": post, "comment": comment, "valence": valence, "arousal": arousal, "ups": ups,
                    "downs": downs})

@app.route('/engagement')
def get_engagement_data():
    comments_per_hour = utils.get_comments_per_hour()
    ups_per_hour = utils.get_ups_per_hour()
    downs_per_hour = utils.get_downs_per_hour()
    comments = [0 if k is None else k for k in comments_per_hour]
    ups = [0 if k is None else k for k in ups_per_hour]
    downs = [0 if k is None else k for k in downs_per_hour]

    return jsonify({"comments": comments, "ups": ups, "downs": downs})


if __name__ == '__main__':
    app.run(debug=True)