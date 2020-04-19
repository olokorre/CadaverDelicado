from flask import Flask, send_from_directory, render_template, request, redirect
import random

app = Flask(__name__)

def jota(pal):
	if len(pal) == 1: return 1
	else: return len(pal) - 1

palavras = ["artigo", "substantivo", "verbo", "adverbio"]
palavra = None
user = None
palavraUser = None

@app.route('/', methods = ('GET', 'POST')) # rota principal
def index():
	global user, palavra, palavraUser
	if request.method == 'GET':
		palavraUser = random.randint(0, (len(palavras) - 1))
		palavra = palavras[palavraUser]
	elif request.method == 'POST':
		user = request.form['aa']
		return redirect('/respostas')
		
	return render_template("index.html", pedir = palavra)

@app.route('/respostas')
def responder():
	frase = ""
	for i in palavras:
		if i == palavras[palavraUser]:
			frase += user + " "
		else:
			arquivo = open("Palavras/" + i + ".txt", "r")
			previas = arquivo.readlines()
			frase += previas[random.randint(0, jota(previas))] + " "
			arquivo.close()

	return render_template("respostas.html", resp = frase)

# rotas auxiliares
@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('static/css', path)

@app.route('/image/<path:path>')
def send_image(path):
	return send_from_directory('static/image', path)

# inicializador
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=6956)