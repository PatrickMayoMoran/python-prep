from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key='secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo_list():
    return render_template("new_list.html")

# Render the list of todo lists
@app.route("/lists")
def get_lists():
    return render_template('lists.html', lists=session['lists'])

if __name__ == "__main__":
    app.run(debug=True, port=5003)
