import random
import time

class QuizManager:
    def __init__(self, question_manager):
        self.question_manager = question_manager
        self.score = 0
        self.total_questions = 0

    def take_quiz(self):
        print("\n" + "="*40)
        print("QUIZ MODE ACTIVATED")
        print("="*40)
        
        categories = set(q["category"] for q in self.question_manager.questions)
        if categories:
            print("Available categories:", ", ".join(categories))
        else:
            print("No categories found. Using all questions.")
        
        category = input("Enter category (or press Enter for all): ").strip()
        
        if category:
            filtered_questions = [
                q for q in self.question_manager.questions
                if q["category"].lower() == category.lower()
            ]
            if not filtered_questions:
                print(f"No questions found in '{category}' category!")
                return
        else:
            filtered_questions = self.question_manager.questions
        
        if not filtered_questions:
            print("No questions available. Please add questions first.")
            return

        TIME_LIMIT = 30
        
        while True:
            try:
                num_q = input(f"How many questions? (1-{len(filtered_questions)}): ").strip()
                if not num_q:
                    num_questions = min(5, len(filtered_questions))
                    break
                num_questions = int(num_q)
                if 1 <= num_questions <= len(filtered_questions):
                    break
                print(f"Please enter between 1-{len(filtered_questions)}")
            except ValueError:
                print("Please enter a valid number!")

        questions = random.sample(filtered_questions, num_questions)
        
        self.score = 0
        self.total_questions = len(questions)
        
        print(f"\n{'='*50}")
        print(f"Starting Quiz: {num_questions} questions")
        print(f"Time per question: {TIME_LIMIT} seconds")
        print(f"{'='*50}")

        for i, q in enumerate(questions, 1):
            print(f"\n{'='*50}")
            print(f"Question {i}/{self.total_questions}")
            print(f"Category: {q['category']}")
            print(f"Time remaining: {TIME_LIMIT} seconds")
            print(f"{'='*50}")
            
            print(f"\n{q['question']}")
            
            if q["type"] == "MCQ":
                print("\nOptions:")
                for idx, opt in enumerate(q["options"], start=1):
                    print(f"  {idx}. {opt}")
            
            start_time = time.time()
            ans = input(f"\nYour answer (you have {TIME_LIMIT}s): ").strip()
            elapsed = time.time() - start_time
            
            if elapsed > TIME_LIMIT:
                print(f"\nTIME'S UP! ({elapsed:.1f} seconds)")
                print(f"Correct answer: {q['answer']}")
                continue
            
            print(f"Time taken: {elapsed:.1f} seconds")
            
            correct = False
            if q["type"] == "MCQ":
                correct = (ans == q["answer"])
            elif q["type"] == "TF":
                correct = (ans.lower() == q["answer"].lower())
            
            if correct:
                print("CORRECT!")
                self.score += 1
                if elapsed < 10:
                    print("Quick thinking! Answered in under 10 seconds!")
            else:
                print(f"INCORRECT")
                print(f"Correct answer: {q['answer']}")
        
        print(f"\n{'='*50}")
        print("QUIZ COMPLETED!")
        print(f"{'='*50}")
        print(f"Total Questions: {self.total_questions}")
        print(f"Correct Answers: {self.score}")
        
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            print(f"Score: {percentage:.1f}%")
            
            if percentage >= 80:
                print("EXCELLENT! You're a quiz master!")
            elif percentage >= 60:
                print("GOOD JOB! Keep practicing!")
            else:
                print("KEEP PRACTICING! You'll get better!")
        
        print(f"{'='*50}")
