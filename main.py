from flask import Flask, render_template, request, redirect, url_for
from peewee import SqliteDatabase, Model, CharField, IntegerField
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

db = SqliteDatabase('sports.db')

class BaseModel(Model):
    class Meta:
        database = db

class SportData(BaseModel):
    name = CharField()
    players = IntegerField()
    popularity = IntegerField()

db.connect()
db.create_tables([SportData], safe=True)

app = Flask(__name__)

@app.route('/')
def index():
    data = SportData.select()
    return render_template('index.html', data=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                SportData.create(name=row['name'], players=row['players'], popularity=row['popularity'])
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/visualize')
def visualize():
    data = pd.DataFrame(list(SportData.select().dicts()))
    if not data.empty:
        plt.figure(figsize=(8, 5))
        sns.barplot(x='name', y='popularity', data=data)
        plt.xticks(rotation=45)
        plt.savefig('static/popularity.png')
        plt.close()
    return render_template('visualize.html')

if __name__ == '__main__':
    app.run(debug=True)
