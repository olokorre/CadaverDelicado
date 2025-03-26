from flask import Flask, send_from_directory, render_template, request, redirect
import random

app = Flask(__name__)

def espaco(lista, index):
	n = 0
	for i in lista:
		if index == i: break
		else: n += 1
	if len(lista) - 1 == n: return ""
	else: return " "

palavras = ["substantivo próprio", "verbo", "adverbio de intensidade", "artigo", "substantivo"]
palavra = None
palavraEscolhida = None

@app.route('/', methods = ('GET', 'POST')) # rota principal
def index():
	global palavraEscolhida, palavra
	if request.method == 'GET':
		palavra = random.choice(palavras)
	elif request.method == 'POST':
		palavraEscolhida = request.form['palavra-escolhida']
		if palavraEscolhida == "myon": return redirect("/video/myon.mp4")
		return redirect('/respostas')

	return render_template("index.html", pedir = palavra)

@app.route('/respostas')
def responder():
	global palavra
	if palavra == None: return redirect('/')
	frase = ""
	for i in palavras:
		if i == palavra: frase += palavraEscolhida
		else:
			arquivo = open("static/palavras/" + i + ".txt", "r")
			previas = arquivo.readlines()
			frase += random.choice(previas)
			arquivo.close()
		frase += espaco(palavras, i)
	frase += "."
	palavra = None
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

@app.route('/video/<path:path>')
def send_video(path):
	return send_from_directory('static/video', path)

# inicializador
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=6956)
