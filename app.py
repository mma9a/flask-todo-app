from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for tasks (in a real app, you'd use a database)
class Task:
    def __init__(self, id, content, completed=False):
        self.id = id
        self.content = content
        self.completed = completed

# List to store tasks
tasks = []
next_id = 1

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    global next_id
    task_content = request.form['task']
    if task_content.strip():
        tasks.append(Task(next_id, task_content))
        next_id += 1
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)