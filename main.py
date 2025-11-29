from questions import QuestionManager
from quiz import QuizManager
from reports import ReportManager

def main():
    question_manager = QuestionManager()
    quiz_manager = QuizManager(question_manager)
    report_manager = ReportManager()

    while True:
        print("\n=== Python Quiz Application ===")
        print("1. Add Question")
        print("2. Take Quiz")
        print("3. View Quiz Report")
        print("4. View Developers")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            question_manager.add_question()
        elif choice == "2":
            quiz_manager.take_quiz()
        elif choice == "3":
            report_manager.show_report(quiz_manager)
        elif choice == "4":
            print("\n" + "="*40)
            print("DEVELOPED BY TEAM:")
            print("="*40)
            print("• Abdallahf")
            print("• Shady")
            print("• Yassin")
            print("• Ali")
            print("="*40)
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()