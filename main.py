from azul import AzulGrabber
from flask import Flask, render_template, request
from latam import LatamGrabber
from smiles import SmilesGrabber
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
grabber_azul = AzulGrabber()
grabber_latam = LatamGrabber()
grabber_smiles = SmilesGrabber()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ida = request.form['ida']
        volta = request.form['volta']
        data = request.form['data']
        voos_azul = grabber_azul.grab_info(ida, volta, data)
        voos_latam = grabber_latam.grab_info(ida, volta, data)
        voos_smiles = grabber_smiles.grab_info(ida, volta, data)
        voos = voos_azul + voos_latam + voos_smiles
        return render_template('index.html', voos=voos)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

