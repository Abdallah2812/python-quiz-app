import random
import time
from colorama import Fore, Back, Style

class QuizManager:
    def __init__(self, question_manager):
        self.question_manager = question_manager
        self.score = 0
        self.total_questions = 0

    def take_quiz(self):
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.YELLOW + Style.BRIGHT + "🎯 QUIZ MODE ACTIVATED")
        print(Fore.CYAN + "="*50)
        
        categories = set(q["category"] for q in self.question_manager.questions)
        if categories:
            print(Fore.BLUE + "Available categories:", ", ".join(categories))
        else:
            print(Fore.YELLOW + "No categories found. Using all questions.")
        
        category = input(Fore.WHITE + "Enter category (or press Enter for all): ").strip()
        
        if category:
            filtered_questions = [
                q for q in self.question_manager.questions
                if q["category"].lower() == category.lower()
            ]
            if not filtered_questions:
                print(Fore.RED + f"❌ No questions found in '{category}' category!")
                return
        else:
            filtered_questions = self.question_manager.questions
        
        if not filtered_questions:
            print(Fore.RED + "❌ No questions available. Please add questions first.")
            return

        TIME_LIMIT = 30
        
        while True:
            try:
                num_q = input(Fore.WHITE + f"How many questions? (1-{len(filtered_questions)}): ").strip()
                if not num_q:
                    num_questions = min(5, len(filtered_questions))
                    break
                num_questions = int(num_q)
                if 1 <= num_questions <= len(filtered_questions):
                    break
                print(Fore.RED + f"❌ Please enter between 1-{len(filtered_questions)}")
            except ValueError:
                print(Fore.RED + "❌ Please enter a valid number!")

        questions = random.sample(filtered_questions, num_questions)
        
        self.score = 0
        self.total_questions = len(questions)
        
        print(Fore.CYAN + f"\n{'='*50}")
        print(Fore.GREEN + f"📝 Starting Quiz: {num_questions} questions")
        print(Fore.YELLOW + f"⏰ Time per question: {TIME_LIMIT} seconds")
        print(Fore.CYAN + f"{'='*50}")

        for i, q in enumerate(questions, 1):
            print(Fore.CYAN + f"\n{'='*50}")
            print(Fore.BLUE + f"Question {i}/{self.total_questions}")
            print(Fore.MAGENTA + f"Category: {q['category']}")
            print(Fore.YELLOW + f"⏰ Time remaining: {TIME_LIMIT} seconds")
            print(Fore.CYAN + f"{'='*50}")
            
            print(Fore.WHITE + f"\n{q['question']}")
            
            if q["type"] == "MCQ":
                print(Fore.CYAN + "\nOptions:")
                for idx, opt in enumerate(q["options"], start=1):
                    print(Fore.WHITE + f"  {idx}. {opt}")
            
            start_time = time.time()
            ans = input(Fore.YELLOW + f"\n⏳ Your answer (you have {TIME_LIMIT}s): ").strip()
            elapsed = time.time() - start_time
            
            if elapsed > TIME_LIMIT:
                print(Fore.RED + f"\n⏰ TIME'S UP! ({elapsed:.1f} seconds)")
                print(Fore.GREEN + f"✅ Correct answer: {q['answer']}")
                continue
            
            print(Fore.CYAN + f"⏱️ Time taken: {elapsed:.1f} seconds")
            
            correct = False
            if q["type"] == "MCQ":
                correct = (ans == q["answer"])
            elif q["type"] == "TF":
                correct = (ans.lower() == q["answer"].lower())
            
            if correct:
                print(Fore.GREEN + "✅ CORRECT!")
                self.score += 1
                if elapsed < 10:
                    print(Fore.YELLOW + "⚡ Quick thinking! Answered in under 10 seconds!")
            else:
                print(Fore.RED + f"❌ INCORRECT")
                print(Fore.GREEN + f"✅ Correct answer: {q['answer']}")
        
        print(Fore.CYAN + f"\n{'='*50}")
        print(Fore.YELLOW + Style.BRIGHT + "🎯 QUIZ COMPLETED!")
        print(Fore.CYAN + f"{'='*50}")
        print(Fore.BLUE + f"Total Questions: {self.total_questions}")
        print(Fore.BLUE + f"Correct Answers: {self.score}")
        
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            print(Fore.GREEN + f"Score: {percentage:.1f}%")
            
            if percentage >= 80:
                print(Fore.GREEN + Style.BRIGHT + "🏆 EXCELLENT! You're a quiz master!")
            elif percentage >= 60:
                print(Fore.YELLOW + "👍 GOOD JOB! Keep practicing!")
            else:
                print(Fore.CYAN + "💪 KEEP PRACTICING! You'll get better!")
        
        print(Fore.CYAN + f"{'='*50}")
