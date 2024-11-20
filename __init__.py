from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from collections import Counter
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)  
                                                                                                                
@app.route('/')
def hello_world():
    return render_template('hello.html')  
                                                                                                                                     
@app.route('/contact/')
def MaPremiereApi():
    return render_template('contact.html')  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
@app.route("/historigramme/")
def historigramme():
    return render_template("historigramme.html")
@app.route('/commits/')
def commits():
    # URL de l'API GitHub
    api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    # Récupérer les données des commits
    response = urlopen(api_url)
    commits_data = json.loads(response.read().decode('utf-8'))

    # Extraire les minutes des dates des commits
    commit_minutes = []
    for commit in commits_data:
        try:
            date_string = commit['commit']['author']['date']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            commit_minutes.append(date_object.minute)
        except KeyError:
            continue  # Ignorer les commits malformés

    # Compter les commits par minute
    commit_counts = Counter(commit_minutes)

    # Convertir les données au format JSON utilisable par Google Charts
    chart_data = [["Minute", "Commits"]]
    for minute in range(60):
        chart_data.append([str(minute), commit_counts.get(minute, 0)])

    # Passer les données au template HTML
    return render_template('commits.html', chart_data=json.dumps(chart_data))

if __name__ == "__main__":
  app.run(debug=True)
