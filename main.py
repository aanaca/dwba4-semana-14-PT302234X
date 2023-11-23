import flask
from replit import db

app = flask.Flask(__name__)

@app.errorhandler(500)
def internal_server_error(e: str):
    return flask.jsonify(error=str(e)), 500

@app.route('/', methods=['GET', 'POST'])
def cadastroContatos():
    try:
        contatos = db.get('contatos', {})
        if flask.request.method == "POST":      
            contatos[flask.request.form['email']] = {
                'nome': flask.request.form['nome'],
                'telefone': flask.request.form['telefone'],
                'assunto': flask.request.form['assunto'],
                'mensagem': flask.request.form['mensagem'],
                'resposta': flask.request.form['resposta']
            }
        db['contatos'] = contatos
        return flask.render_template('contatos.html', contatos=contatos)
    except Exception as e:
        flask.abort(500, description=str(e))
      
@app.route('/limparBanco', methods=['POST'])
def limparBanco():
    try:
        del db["contatos"]
        return flask.render_template('contatos.html')
    except Exception as e:
        return flask.render_template('contatos.html')

@app.route('/eliminarRegistro/<email>', methods=['POST'])
def deletar_contato(email):
    try:
        contatos = db.get('contatos', {})
        if email in contatos:
            del contatos[email]
            db['contatos'] = contatos
        return flask.redirect(flask.url_for('cadastroContatos'))
    except Exception as e:
        flask.abort(500, description=str(e))

app.run('0.0.0.0')
