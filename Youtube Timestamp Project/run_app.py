from flask import Flask, render_template, request
import main
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def return_home():
    return render_template('index.html')

@app.route('/indexRender', methods=['GET', 'POST'])
def indexRender():
    query = request.args.get('query')
    args = {
        'input': query
    }
    top_10_docs = main.run_search(query)
    videos = []
    for title, link in top_10_docs.items():
        temp = {}
        temp['title'] = title
        temp['link'] = link
        
        # calculate point in video
        seconds = int(link.split('&t=')[-1])
        minutes = math.floor(seconds / 60)
        seconds = seconds % 60
        temp['time'] = f'{minutes}:{seconds}'
        
        videos.append(temp)
    args['videos'] = videos

    return render_template('indexRender.html', **args)

if __name__ == '__main__':
    app.run(debug=True)
