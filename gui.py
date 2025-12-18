import tkinter as tk
from tkinter import messagebox, simpledialog

# =========================================================
#               INTERNAL DATA MANAGERS (NO FILES)
# =========================================================

class QuestionManager:
    def __init__(self):
        self.questions = []

    def add_question(self, question, options, correct):
        self.questions.append({
            "question": question,
            "options": options,
            "correct": correct
        })


class QuizManager:
    def __init__(self, question_manager):
        self.qm = question_manager
        self.score = 0
        self.total_questions = 0


class ReportManager:
    def generate_report(self, quiz_manager):
        return (
            f"Quiz Report\n"
            f"Score: {quiz_manager.score}/{quiz_manager.total_questions}\n"
            f"Percentage: {quiz_manager.score / quiz_manager.total_questions * 100:.2f}%"
            if quiz_manager.total_questions > 0 else
            "No quiz taken yet."
        )


class Analytics:
    def __init__(self):
        self.attempts = []  # [(score, total), ...]

    def add_attempt(self, score, total):
        self.attempts.append((score, total))

    def get_stats(self):
        if not self.attempts:
            return "No analytics available yet."

        avg = sum(s for s, _ in self.attempts) / len(self.attempts)
        return (
            f"Attempts: {len(self.attempts)}\n"
            f"Average Score: {avg:.2f}"
        )

    def export_to_csv(self):
        with open("analytics.csv", "w") as f:
            f.write("Score,Total Questions\n")
            for score, total in self.attempts:
                f.write(f"{score},{total}\n")


# =========================================================
#                        GUI APP
# =========================================================

class QuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz Application")
        self.root.geometry("500x550")
        self.root.configure(bg="#1e1e2f")

        self.qm = QuestionManager()
        self.quiz = QuizManager(self.qm)
        self.report = ReportManager()
        self.analytics = Analytics()

        self.build_interface()

    def build_interface(self):
        title = tk.Label(
            self.root,
            text="🎯 PYTHON QUIZ APPLICATION",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1e1e2f"
        )
        title.pack(pady=20)

        buttons = [
            ("Add Question", self.gui_add_question),
            ("Take Quiz", self.gui_take_quiz),
            ("View Quiz Report", self.gui_view_report),
            ("Analytics Dashboard", self.gui_analytics),
            ("Developers", self.gui_developers),
            ("Export Analytics CSV", self.gui_export_csv),
            ("Exit", self.root.quit)
        ]

        for text, cmd in buttons:
            tk.Button(
                self.root,
                text=text,
                width=25,
                height=2,
                font=("Arial", 14),
                bg="#2d2d44",
                fg="white",
                activebackground="#3c3c5c",
                command=cmd
            ).pack(pady=10)

    # =====================================================
    #                 BUTTON FUNCTIONS
    # =====================================================

    def gui_add_question(self):
        q = simpledialog.askstring("Add Question", "Enter the question:")
        if not q:
            return

        options = []
        for i in range(4):
            opt = simpledialog.askstring("Option", f"Enter option {i+1}:")
            options.append(opt)

        correct = simpledialog.askinteger("Correct", "Correct option number (1-4):")

        self.qm.add_question(q, options, correct)
        messagebox.showinfo("Success", "Question added!")

    def gui_take_quiz(self):
        if not self.qm.questions:
            messagebox.showwarning("No Questions", "Add questions first!")
            return

        score = 0

        for q in self.qm.questions:
            user_answer = simpledialog.askinteger(
                "Quiz",
                f"{q['question']}\n"
                f"1. {q['options'][0]}\n"
                f"2. {q['options'][1]}\n"
                f"3. {q['options'][2]}\n"
                f"4. {q['options'][3]}\n\n"
                f"Your answer:"
            )

            if user_answer == q["correct"]:
                score += 1

        self.quiz.score = score
        self.quiz.total_questions = len(self.qm.questions)
        self.analytics.add_attempt(score, len(self.qm.questions))

        messagebox.showinfo(
            "Quiz Finished",
            f"Score: {score}/{len(self.qm.questions)}"
        )

    def gui_view_report(self):
        report = self.report.generate_report(self.quiz)
        messagebox.showinfo("Report", report)

    def gui_analytics(self):
        stats = self.analytics.get_stats()
        messagebox.showinfo("Analytics Dashboard", stats)

    def gui_developers(self):
        messagebox.showinfo(
            "Developers",
            "Developed by:\n"
            "• Yassin\n"
            "• Abdallah\n"
            "• Shady\n"
            "• Ali"
        )

    def gui_export_csv(self):
        self.analytics.export_to_csv()
        messagebox.showinfo("Exported", "Analytics saved to analytics.csv")


# =========================================================
#                    RUN THE APPLICATION
# =========================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()
