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
        if not category:
            print("Missing field: category is required.")
            return

        q_type = input("Enter question type (MCQ/TF): ").strip().upper()
        if not q_type:
            print("Missing field: question type is required.")
            return

        question_text = input("Enter the question: ").strip()
        if not question_text:
            print("Missing field: question text is required.")
            return

        if q_type == "MCQ":
            options = []
            for i in range(4):
                opt = input(f"Enter option {i+1}: ").strip()
                if not opt:
                    print(f"Missing field: option {i+1} is required.")
                    return
                options.append(opt)

            answer_idx = input("Enter correct option number (1-4): ").strip()
            if not answer_idx:
                print("Missing field: correct option number is required.")
                return
            if not answer_idx.isdigit():
                print("Invalid field: correct option number must be numeric (1-4).")
                return
            answer_idx = int(answer_idx)
            if not (1 <= answer_idx <= len(options)):
                print("Invalid correct option number. Must be within 1-4.")
                return

            # Store the answer as the option text to be consistent with quiz display
            answer = options[answer_idx - 1]

        elif q_type == "TF":
            options = ["True", "False"]
            answer = input("Enter answer (True/False): ").strip()
            if not answer:
                print("Missing field: TF correct answer is required.")
                return
            if answer.lower() not in ("true", "false"):
                print("Invalid field: TF answer must be 'True' or 'False'.")
                return
            # normalize
            answer = "True" if answer.lower() == "true" else "False"
        else:
            print("Invalid question type.")
            return

        question = {
            "id": len(self.questions) + 1,
            "type": q_type,
            "category": category,
            "question": question_text,
            "options": options,
            "answer": answer
        }

        self.questions.append(question)
        self.save_questions()
        print("Question added successfully.")
