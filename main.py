from colorama import init, Fore, Back, Style
init(autoreset=True)

from questions import QuestionManager
from quiz import QuizManager
from reports import ReportManager
from analytics import Analytics

def main():
    question_manager = QuestionManager()
    quiz_manager = QuizManager(question_manager)
    report_manager = ReportManager()
    analytics = Analytics()

    while True:
        print(Fore.CYAN + "\n" + "="*40)
        print(Fore.YELLOW + Style.BRIGHT + "🎯 PYTHON QUIZ APPLICATION")
        print(Fore.CYAN + "="*40)
        print(Fore.GREEN + "1. Add Question")
        print(Fore.GREEN + "2. Take Quiz")
        print(Fore.GREEN + "3. View Quiz Report")
        print(Fore.CYAN + "4. View Analytics Dashboard")
        print(Fore.BLUE + "5. View Developers")
        print(Fore.MAGENTA + "6. Export Analytics Data")
        print(Fore.RED + "7. Exit")

        choice = input(Fore.WHITE + "Enter your choice: ")

        if choice == "1":
            question_manager.add_question()
        elif choice == "2":
            quiz_manager.take_quiz()
        elif choice == "3":
            report_manager.show_report(quiz_manager)
        elif choice == "4":
            analytics.show_stats()
        elif choice == "5":
            print(Fore.CYAN + "\n" + "="*40)
            print(Fore.YELLOW + "DEVELOPED BY TEAM:")
            print(Fore.CYAN + "="*40)
            print(Fore.GREEN + "• Yassin (Team Leader)")
            print(Fore.GREEN + "• Abdallah")
            print(Fore.GREEN + "• Shady")
            print(Fore.GREEN + "• Ali")
            print(Fore.CYAN + "="*40)
        elif choice == "6":
            analytics.export_to_csv()
        elif choice == "7":
            print(Fore.MAGENTA + "Exiting... Goodbye! 👋")
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
