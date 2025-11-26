
class ReportManager:
    def show_report(self, quiz_manager):
        print("\n=== Quiz Report ===")
        print(f"Last Quiz Score: {quiz_manager.score}/{quiz_manager.total_questions}")

        if quiz_manager.total_questions > 0:
            percentage = (quiz_manager.score / quiz_manager.total_questions) * 100
            print(f"Percentage: {percentage:.2f}%")
        else:
            print("No quiz taken yet.")
