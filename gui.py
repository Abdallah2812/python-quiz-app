import tkinter as tk
from tkinter import messagebox, simpledialog
try:
    from questions import QuestionManager as FileQuestionManager
except Exception:
    FileQuestionManager = None
import json

# =========================================================
#               INTERNAL DATA MANAGERS (NO FILES)
# =========================================================


class QuestionManager:
    def __init__(self):
        self.questions = []
    def add_question(self, category, question, options, correct, q_type="MCQ"):
        self.questions.append({
            "category": category,
            "type": q_type,
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

        # Add a dropdown for category selection in the GUI
        self.category_label = tk.Label(self.root, text='Select Category:', bg="#1e1e2f", fg="white")
        self.category_label.pack(pady=(10, 0))

        self.category_var = tk.StringVar(self.root)
        self.category_var.set('Select Category')  # default value
        self.category_menu = tk.OptionMenu(self.root, self.category_var, 'Python', 'OOP', 'Data', 'General')
        self.category_menu.pack(pady=(0, 20))

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

    def ask_choice(self, title, prompt, choices):
        dlg = tk.Toplevel(self.root)
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.title(title)

        tk.Label(dlg, text=prompt, font=("Arial", 12)).pack(padx=20, pady=(20, 10))

        var = tk.StringVar(value=choices[0] if choices else "")
        opt = tk.OptionMenu(dlg, var, *choices) if choices else tk.Label(dlg, text="No choices available")
        opt.pack(padx=20, pady=10)

        result = {"value": None}

        def on_ok():
            result["value"] = var.get()
            dlg.destroy()

        def on_cancel():
            dlg.destroy()

        btn_frame = tk.Frame(dlg)
        tk.Button(btn_frame, text="OK", width=10, command=on_ok).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel).pack(side="left", padx=5)
        btn_frame.pack(pady=(10, 20))

        self.root.wait_window(dlg)
        return result["value"]

    # =====================================================
    #                 BUTTON FUNCTIONS
    # =====================================================

    def gui_add_question(self):
        # Build category choices from file-based questions if available,
        # otherwise fall back to common defaults.
        choices = ["Python", "OOP", "Data", "General"]
        if FileQuestionManager is not None:
            try:
                file_qm = FileQuestionManager()
                file_cats = sorted({q.get("category") for q in file_qm.questions if q.get("category")})
                if file_cats:
                    choices = file_cats
            except Exception:
                pass

        category = self.ask_choice("Category", "Select a category:", choices)
        if not category:
            return

        q = simpledialog.askstring("Add Question", "Enter the question:")
        # If user cancelled, stop. If empty string, show error naming the field
        if q is None:
            return
        if not q.strip():
            messagebox.showerror("Missing Field", "Question text is required.")
            return

        q_type = self.ask_choice("Question Type", "Select question type:", ["MCQ", "TF"])
        if not q_type:
            return

        options = []
        correct = None
        if q_type == "MCQ":
            for i in range(4):
                opt = simpledialog.askstring("Option", f"Enter option {i+1}:")
                # Cancelled -> stop flow
                if opt is None:
                    return
                if not opt.strip():
                    messagebox.showerror("Missing Field", f"Option {i+1} is required.")
                    return
                options.append(opt)

            correct = simpledialog.askinteger("Correct", "Correct option number (1-4):")
            if correct is None:
                messagebox.showerror("Missing Field", "Correct option number is required.")
                return
            if not (1 <= correct <= 4):
                messagebox.showerror("Invalid Field", "Correct option number must be between 1 and 4.")
                return
        else:  # TF
            options = ["True", "False"]
            tf_choice = self.ask_choice("Correct Answer", "Select the correct answer:", options)
            if tf_choice is None or not str(tf_choice).strip():
                messagebox.showerror("Missing Field", "Correct answer for True/False is required.")
                return
            correct = tf_choice

        self.qm.add_question(category, q, options, correct, q_type)
        messagebox.showinfo("Success", "Question added!")

    def gui_take_quiz(self):
        if not self.qm.questions:
            messagebox.showwarning("No Questions", "Add questions first!")
            return

        selected_category = self.category_var.get()
        if selected_category == 'Select Category':
            messagebox.showwarning("No Category", "Select a category first!")
            return

        score = 0
        for q in self.qm.questions:
            if q.get("category") != selected_category:
                continue  # Skip questions not in the selected category

            q_type = q.get("type", "MCQ")
            if q_type == "MCQ":
                prompt = f"{q['question']}\n\n"
                for idx, opt in enumerate(q['options'], start=1):
                    prompt += f"{idx}. {opt}\n"
                prompt += "\nYour answer (option number):"

                user_answer = simpledialog.askinteger("Quiz", prompt)
                if user_answer is None:
                    continue
                if user_answer == q["correct"]:
                    score += 1
            else:  # TF
                tf_choice = self.ask_choice("Quiz - True/False", q['question'], ["True", "False"])
                if not tf_choice:
                    continue
                if tf_choice == q["correct"]:
                    score += 1

        self.quiz.score = score
        self.quiz.total_questions = len([q for q in self.qm.questions if q.get("category") == selected_category])
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
