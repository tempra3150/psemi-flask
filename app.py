from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    details = db.Column(db.String(100))

@app.route("/")
def index():
    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)
@app.route("/create", methods=["POST"])
def create():
    title = request.form.get("title")
    details = request.form.get("details")
    new_task = Todo(title=title, details=details)

    db.session.add(new_task)
    db.session.commit()
    return redirect("/")
@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get(id)

    db.session.delete(delete_task)
    db.session.commit()
    return redirect('/')

## TODO
## /update/1のような遷移先を作成する
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    ## idをもとにデータベースからタスクを取得する
    update_task = Todo.query.get(id)
    ## GETのときはupdate.htmlを表示する
    ## update.htmlには元々のタスクの情報を表示したい
    if request.method == 'GET':
        return render_template('update.html', task=update_task)
    
    ## POSTのときはデータベースを更新して/にリダイレクトする
    ## データベースを更新するときは、タスクを取得→取得したタスクの内容を更新→保存する
    elif request.method == 'POST':
        update_task.title = request.form.get('title')
        update_task.details = request.form.get('details')

        db.session.commit()
        return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)