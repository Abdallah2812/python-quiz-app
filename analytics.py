from colorama import Fore, Style
import csv
from datetime import datetime

class Analytics:
    def __init__(self):
        self.quiz_history = []
    
    def add_quiz_result(self, score, total, category, time_taken):
        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "total": total,
            "category": category,
            "percentage": (score/total)*100 if total > 0 else 0,
            "time_taken": time_taken
        }
        self.quiz_history.append(result)
        self._save_to_csv()
    
    def _save_to_csv(self):
        try:
            with open("quiz_history.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["date", "score", "total", "category", "percentage", "time_taken"])
                writer.writeheader()
                writer.writerows(self.quiz_history)
        except:
            pass
    
    def show_stats(self):
        if not self.quiz_history:
            print(Fore.YELLOW + "📊 No quiz history available.")
            return
        
        total_quizzes = len(self.quiz_history)
        avg_score = sum(r["percentage"] for r in self.quiz_history) / total_quizzes
        best_score = max(r["percentage"] for r in self.quiz_history)
        
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.YELLOW + Style.BRIGHT + "📊 QUIZ ANALYTICS DASHBOARD")
        print(Fore.CYAN + "="*50)
        print(Fore.GREEN + f"Total Quizzes Taken: {total_quizzes}")
        print(Fore.BLUE + f"Average Score: {avg_score:.1f}%")
        print(Fore.MAGENTA + f"Best Score: {best_score:.1f}%")
        
        categories = {}
        for quiz in self.quiz_history:
            cat = quiz["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        print(Fore.CYAN + "\n📈 Category Breakdown:")
        for cat, count in categories.items():
            print(Fore.WHITE + f"  {cat}: {count} quizzes")
        
        print(Fore.CYAN + "="*50)
    
    def export_to_csv(self):
        if not self.quiz_history:
            print(Fore.RED + "❌ No data to export.")
            return
        
        self._save_to_csv()
        print(Fore.GREEN + f"✅ Data exported to quiz_history.csv ({len(self.quiz_history)} records)")
