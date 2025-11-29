import json

class QuestionManager:
    FILE = "questions.json"

    def __init__(self):
        self.questions = self.load_questions()

    def load_questions(self):
        try:
            with open(self.FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_questions(self):
        with open(self.FILE, "w") as f:
            json.dump(self.questions, f, indent=4)

    def add_question(self):
        category = input("Enter category (Python/OOP/Data/General): ").strip()
        q_type = input("Enter question type (MCQ/TF): ").strip().upper()
        question_text = input("Enter the question: ")

        if q_type == "MCQ":
            options = []
            for i in range(4):
                opt = input(f"Enter option {i+1}: ")
                options.append(opt)
            answer = input("Enter correct option number (1-4): ")
        elif q_type == "TF":
            options = ["True", "False"]
            answer = input("Enter answer (True/False): ")
        else:
            print("Invalid question type.")
            return

        question = {
            "id": len(self.questions) + 1,
            "type": q_type,
            "category":category,
            "question": question_text,
            "options": options,
            "answer": answer
        }

        self.questions.append(question)
        self.save_questions()
        print("Question added successfully.")
