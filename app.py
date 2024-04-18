from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def metodo_euler(f, x0, y0, h, iteraciones, solucion_exacta=None):
    puntos_x = [x0]
    puntos_y = [y0]
    errores = []
    for i in range(iteraciones):
        y_nueva = y0 + h * f(x0, y0)
        x0, y0 = x0 + h, y_nueva
        puntos_x.append(x0)
        puntos_y.append(y_nueva)
        if solucion_exacta:
            error_actual = abs(solucion_exacta(x0) - y_nueva) / abs(solucion_exacta(x0)) * 100 if solucion_exacta(x0) != 0 else 0
            errores.append(error_actual)
        else:
            errores.append(None)
    return puntos_x, puntos_y, errores

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            f = eval('lambda x, y: ' + request.form['funcion'])
            x0 = float(request.form['x0'])
            y0 = float(request.form['y0'])
            h = float(request.form['h'])
            iteraciones = int(request.form['iteraciones'])
            solucion_exacta = eval('lambda x: ' + request.form['solucion_exacta']) if request.form['solucion_exacta'] else None

            xs, ys, errores = metodo_euler(f, x0, y0, h, iteraciones, solucion_exacta)
            plot_url = create_plot(xs, ys)
            puntos = list(zip(xs, ys, errores))
            solucion_exacta_provided = bool(request.form['solucion_exacta'])
            return render_template('index.html', plot_url=plot_url, puntos=puntos, solucion_exacta_provided=solucion_exacta_provided)
        except Exception as e:
            return f"Error en cálculo: {e}", 400
    else:
        return render_template('index.html')

def create_plot(xs, ys):
    plt.figure()
    plt.plot(xs, ys, marker='o', linestyle='-', color='blue')
    plt.title('Aproximación por Método de Euler')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

if __name__ == '__main__':
    app.run(debug=True)
