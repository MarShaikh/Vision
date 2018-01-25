from flask import Flask, render_template, request
import cv2
from werkzeug.utils import secure_filename
from darkflow.net.build import TFNet

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def main():
    tags = []
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

            for i in range(len(result)):
                if result[i]['label'] not in tags:
                    tags.append(result[i]['label'])
            return render_template('tem.html', tags= tags);
        else:
            return render_template('tem.html',tags= tags)
    else:
        return render_template('tem.html', tags = tags)


if __name__ == "__main__":
    app.run(debug=True)
