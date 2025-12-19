import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, score, total, category, time_taken):
        self.score = score
        self.total = total
        self.category = category
        self.time_taken = time_taken
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def calculate_percentage(self):
        return (self.score / self.total) * 100 if self.total > 0 else 0
    
    def get_grade(self):
        percentage = self.calculate_percentage()
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
    
    def generate_text_report(self):
        report = f"""
        📊 QUIZ REPORT
        {'=' * 40}
        Date: {self.timestamp}
        Category: {self.category}
        {'=' * 40}
        Score: {self.score}/{self.total}
        Percentage: {self.calculate_percentage():.1f}%
        Grade: {self.get_grade()}
        Time Taken: {self.time_taken} seconds
        {'=' * 40}
        """
        return report
    
    def save_report(self, filename="quiz_report.txt"):
        report = self.generate_text_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ Report saved to {filename}")
        return report
    
    def display_report(self):
        print(self.generate_text_report())

# Example usage
if __name__ == "__main__":
    # Test the report generator
    report = ReportGenerator(
        score=8,
        total=10,
        category="Python Basics",
        time_taken=150
    )
    report.display_report()
    report.save_report()
