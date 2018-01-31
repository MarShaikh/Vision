import os
import random
import sqlite3
from flask import Flask, render_template, request, url_for
import cv2
from werkzeug.utils import secure_filename
from darkflow.net.build import TFNet

app = Flask(__name__)

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def select_link(conn, label):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE name=?", (label,))
    rows = cur.fetchall()
    return rows;        

@app.route("/", methods = ['GET', 'POST'])
def main():
    path = []
    tags = []
    dic = {}
    if request.method == 'POST':

        f = request.files['file']
        if f:
            options = {
                'model': 'cfg/yolo.cfg',
                'load': 'bin/yolo.weights',
                'threshold': 0.3,
            }
            tfNet = TFNet(options)
            f.save(secure_filename(f.filename))
            img = cv2.imread(f.filename);
            result = tfNet.return_predict(img);
            conn = sqlite3.connect('new.db')
            for i in range(len(result)):
                if result[i]['label'] not in tags:
                    tags.append(result[i]['label'])
                    names = os.listdir(os.path.join(app.static_folder, os.path.join('data',result[i]['label'])));
                    for name in names:
                        path.append(url_for('static', filename=os.path.join('data', os.path.join(result[i]['label'],name))))
                    cur = conn.cursor()
                    cur.execute("SELECT link FROM projects WHERE name=?", (result[i]['label'],))
                    links =cur.fetchall()
                    for link in links:
                        dic[result[i]['label']]=link[0];
    return render_template('index.html', tags= tags,path=path,dic=dic);


if __name__ == "__main__":
    app.run(debug=True)
