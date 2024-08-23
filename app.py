from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import csv
import time
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_questions_from_csv(csv_file, num_questions=10):
    questions = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append({
                "question": row["Question"],
                "options": [row["A"], row["B"], row["C"], row["D"]],
                "correct": row["Right Answer"],
                "image": row.get("Image", "")
            })
    random_questions = random.sample(questions, min(len(questions), num_questions))
    return random_questions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'POST':
        session['questions'] = load_questions_from_csv('questions.csv', 10)
        session['current_question'] = 0
        session['correct_answers'] = 0
        session['start_time'] = time.time()
        return redirect(url_for('next_question'))
    return render_template('index.html')

@app.route('/next_question', methods=['GET', 'POST'])
def next_question():
    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        question_index = session['current_question']
        questions = session['questions']

        if selected_answer:
            correct_answer = questions[question_index]['correct']
            session['questions'][question_index]['selected'] = selected_answer
            if selected_answer == correct_answer:
                session['correct_answers'] += 1
            session['current_question'] += 1

        if session['current_question'] >= len(questions):
            return redirect(url_for('results'))

    current_question = session['questions'][session['current_question']]
    progress = int((session['current_question'] / len(session['questions'])) * 100)
    time_passed = int(time.time() - session['start_time'])

    return render_template('quiz.html', question=current_question, question_number=session['current_question'] + 1,
                           total_questions=len(session['questions']), progress=progress, time_passed=time_passed)

@app.route('/get_time')
def get_time():
    time_passed = int(time.time() - session['start_time'])
    minutes = time_passed // 60
    seconds = time_passed % 60
    return jsonify(minutes=minutes, seconds=seconds)

@app.route('/results')
def results():
    correct_answers = session.get('correct_answers', 0)
    total_questions = len(session['questions'])
    time_taken = time.time() - session['start_time']
    return render_template('results.html', correct_answers=correct_answers, total_questions=total_questions,
                           time_taken=f"{int(time_taken // 60)}m {int(time_taken % 60)}s")

if __name__ == '__main__':
    app.run(debug=True, port=5001)

