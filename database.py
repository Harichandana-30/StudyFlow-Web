import sqlite3


def create_database():
    conn = sqlite3.connect("studyflow.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        subject TEXT NOT NULL,
        deadline TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    conn.commit()
    conn.close()


def add_task(task, subject, deadline):
    conn = sqlite3.connect("studyflow.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks (task, subject, deadline)
    VALUES (?, ?, ?)
    """, (task, subject, deadline))

    conn.commit()
    conn.close()


def get_tasks():
    conn = sqlite3.connect("studyflow.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def complete_task(task_id):
    conn = sqlite3.connect("studyflow.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect("studyflow.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

def search_tasks(subject):
    conn = sqlite3.connect("studyflow.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE subject LIKE ?",
        ('%' + subject + '%',)
    )

    tasks = cursor.fetchall()

    conn.close()

    return tasks