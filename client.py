from flask import Flask, redirect, render_template, request, jsonify
import requests
import json
import tempfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('filters.html')


@app.route('/test_submit', methods=['POST'])
def test_submit():
    filters = []
    if request.form['region'] != "any":
        filters.append(dict(name='school__region', op='has', val=request.form['region']))
    if request.form['area'] != "":
        filters.append(dict(name='school', op='has', val={"name":"area","op":"ilike","val":"%"+request.form['area']+"%"}))
    if request.form['school__name'] != "":
        filters.append(dict(name='school', op='has', val={"name":"name","op":"ilike","val":"%"+request.form['school__name']+"%"}))
    if request.form['school__type'] != "any":
        filters.append(dict(name='school__type', op='has', val=request.form['school__type']))
    if request.form['year'] != "any":
        filters.append(dict(name='year', op='eq', val=int(request.form['year'])))
    if request.form['subject'] != "any":
        filters.append(dict(name='subject', op='eq', val=request.form['subject']))

    url = 'http://127.0.0.1:5000/api/v2/results'
    headers = {'Content-Type': 'application/json'}

    params = dict(q=json.dumps(dict(filters=filters)))
    response = requests.get(url, params=params, headers=headers)

    if request.form['output'] == 'json':
        temp = response.json()
        return jsonify(temp)
    else:
        fig = plt.figure(figsize=(5,5),dpi=100)
        avg = [0,0,0,0,0, 0,0,0,0,0]
        axes = fig.add_subplot(2,1,1)
        average = fig.add_subplot(2,1,2)
        for obj in response.json()['objects']:
            y = obj['abs_scores']
            x = range(len(y))
            avg = [sum(x) for x in zip(avg, y)]
            axes.plot(x,y,'-')

        # axes.set_xlabel('intervals')
        axes.set_ylabel('students')
        axes.set_title("Plots")
        # average.set_xlabel('intervals')
        average.set_ylabel('students')
        # average.set_title("Average Plot")
        average.plot(range(len(avg)), avg, '-')
        f = tempfile.NamedTemporaryFile(
        dir='C:\\Users\\Vlad\\PycharmProjects\\untitled1\\static\\temp',
        suffix='.png', delete=False)
        plt.savefig(f)
        f.close()
        plotPng = f.name.split('\\')[-1]
        return render_template('results2.html', objects=response.json()['objects'], plotPng=plotPng)

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5010)
