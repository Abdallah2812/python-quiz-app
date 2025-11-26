
import random

class QuizManager:
    def __init__(self, question_manager):
        self.question_manager = question_manager
        self.score = 0
        self.total_questions = 0

    def take_quiz(self):
        if not self.question_manager.questions:
            print("No questions available. Please add questions first.")
            return

        questions = random.sample(
            self.question_manager.questions, 
            min(5, len(self.question_manager.questions))
        )

        self.score = 0
        self.total_questions = len(questions)

        for q in questions:
            print("\n" + q["question"])

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
