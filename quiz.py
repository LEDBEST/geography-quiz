import csv
import os
import random


class QuizApp:
    def __init__(self, csv_file, images_folder):
        self.images_folder = images_folder
        self.total_questions = 10
        self.correct_answers = 0
        self.results = []
        self.all_questions = self.load_questions_from_csv(csv_file)
        self.questions = random.sample(self.all_questions, self.total_questions)

    def load_questions_from_csv(self, csv_file):
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
        return questions

    def get_question(self, index):
        question = self.questions[index]
        options_with_labels = []
        for i, option in enumerate(question["options"]):
            label = f"{chr(65 + i)}:"  # A:, B:, C:, D:
            options_with_labels.append({"label": label, "text": option})

        image_path = os.path.join(self.images_folder, question["image"]) if question["image"] else None
        if image_path and not os.path.exists(image_path):
            print(f"Image not found at: {image_path}")
            image_path = None

        return {
            "question": question["question"],
            "options": options_with_labels,
            "image": image_path
        }

    def answer_question(self, answer, index):
        correct_answer_label = self.questions[index]["correct"]  # A, B, C, D
        if correct_answer_label not in ["A", "B", "C", "D"]:
            raise ValueError(
                f"Invalid correct answer '{correct_answer_label}' for question {index + 1}. Must be one of 'A', 'B', 'C', 'D'.")

        correct_text = self.questions[index]["options"][["A", "B", "C", "D"].index(correct_answer_label)]
        selected_text = self.questions[index]["options"][ord(answer) - 65]

        result = "Correct" if selected_text == correct_text else "Incorrect"
        if result == "Correct":
            self.correct_answers += 1

        self.results.append({
            "question_number": index + 1,
            "question": self.questions[index]["question"],
            "selected": selected_text,
            "correct": correct_text,
            "result": result
        })

    def get_results(self):
        return self.results

    def get_progress(self, index):
        return {
            "current": index + 1,
            "total": self.total_questions
        }

    def to_dict(self):
        return {
            "questions": self.questions,
            "results": self.results,
            "correct_answers": self.correct_answers,
            "total_questions": self.total_questions,
            "images_folder": self.images_folder
        }

    @classmethod
    def from_dict(cls, data):
        quiz = cls.__new__(cls)
        quiz.questions = data["questions"]
        quiz.results = data["results"]
        quiz.correct_answers = data["correct_answers"]
        quiz.total_questions = data["total_questions"]
        quiz.images_folder = data["images_folder"]
        return quiz
