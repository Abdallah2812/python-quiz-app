
import random

class QuizManager:
    def __init__(self, question_manager):
        self.question_manager = question_manager
        self.score = 0
        self.total_questions = 0

    def take_quiz(self):
        print("\n--- Choose Quiz Category ---")
        category = input("Enter category (Python/OOP/Data/General): ").strip()
        filtered_questions = [
            q for q in self.question_manager.questions
            if q["category"].lower() == category.lower()
        ]
        if not filtered_questions:
            print("No questions found in this category!")
            return

        if not self.question_manager.questions:
            print("No questions available. Please add questions first.")
            return

        questions = random.sample(filtered_questions, min(5, len(filtered_questions)))


        self.score = 0
        self.total_questions = len(questions)

        for q in questions:
            print("\nCategory:", q["category"])
            print(q["question"])


            if q["type"] == "MCQ":
                for idx, opt in enumerate(q["options"], start=1):
                    print(f"{idx}. {opt}")

                ans = input("Enter the option number: ").strip()
                if ans == q["answer"]:
                    print("Correct!")
                    self.score += 1
                else:
                    print(f"Wrong! Correct answer: {q['answer']}")

            elif q["type"] == "TF":
                ans = input("Enter True/False: ").strip()
                if ans.lower() == q["answer"].lower():
                    print("Correct!")
                    self.score += 1
                else:
                    print(f"Wrong! Correct answer: {q['answer']}")

        print(f"\nQuiz finished! Your score: {self.score}/{self.total_questions}")
