from uuid import uuid4

from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.exceptions import NotFound
from todos.utils import (
      error_for_list_title,
      find_list_by_id,
      error_for_todo_title,
      find_todo_by_id,
      delete_todo_by_id,
      mark_all_completed,
)

app = Flask(__name__)
app.secret_key='secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

# Redirect to view all lists
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

# Add new list
@app.route("/lists", methods=["POST"])
def create_list():
    title = request.form["list_title"].strip()

    error = error_for_list_title(title, session["lists"])
    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)

    session['lists'].append({
          'id': str(uuid4()),
          'title': title,
          'todos': [],
    })

    flash("The list has been created.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

# Show single list
@app.route("/lists/<list_id>")
def show_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")

    return render_template('list.html', lst=lst)

# Add todo to a list
@app.route("/lists/<list_id>/todos", methods=["POST"])
def add_todo(list_id):
    title = request.form['todo'].strip()
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")

    error = error_for_todo_title(title)
    if error:
        flash(error, "error")
        return render_template('list.html', lst=lst)

    lst['todos'].append({
      'title': title,
      'completed': False,
      'id': str(uuid4())
    })

    flash("The todo has been added.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

# Complete or incomplete single todo
@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=["POST"])
def toggle(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")

    todo = find_todo_by_id(todo_id, lst['todos'])
    if not todo:
        raise NotFound(description="Todo not found")

    completed_status = request.form['completed']
    new_status = completed_status == 'True'

    if new_status:
        flash(f"{todo['title']} has been completed.", "success")
    else:
        flash(f"{todo['title']} has been marked incomplete.", "success")

    todo['completed'] = new_status
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

# Delete a todo
@app.route("/lists/<list_id>/todos/<todo_id>/delete", methods=["POST"])
def delete_todo(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")

    todo = find_todo_by_id(todo_id, lst['todos'])
    if not todo:
        raise NotFound(description="Todo not found")

    delete_todo_by_id(todo_id, lst)
    flash("Todo has been deleted.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

# Complete all todos
@app.route("/lists/<list_id>/complete_all", methods=["POST"])
def complete_all(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")

    mark_all_completed(lst)

    flash("All todos have been completed.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

# View Edit list page
@app.route("/lists/<list_id>/edit")
def edit_list(list_id):
    lst = find_list_by_id(list_id, session["lists"])
    if not lst:
        raise NotFound(description="List not found")

    title = lst['title']
    return render_template('edit_list.html', title=title, lst=lst)

# Submit a new list title
@app.route("/lists/<list_id>", methods=["POST"])
def submit_list(list_id):
    lst = find_list_by_id(list_id, session["lists"])
    if not lst:
        raise NotFound(description="List not found")

    title = request.form["list_title"].strip()

    error = error_for_list_title(title, session["lists"])
    if error:
        flash(error, "error")
        return render_template('edit_list.html', title=title, lst=lst)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
