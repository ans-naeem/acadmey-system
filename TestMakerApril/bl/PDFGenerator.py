import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class PDFGenerator:
    def __init__(self, username):
        self.username=username
        self.template_dir = "pdfTemplates"
        self.template_path = os.path.join(self.template_dir, f"{self.username}_template.pdf")

    def generate_pdf(self, questions):
        c = canvas.Canvas(self.template_path, pagesize=letter)

        self.draw_template(c, "firstpage")
        self.add_questions(c, questions)
        c.save()
        print(f"PDF generated: {self.template_path}")

    def draw_template(self, c, page_type):
        # Draw header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, 750, f"{self.username}'s Test - {page_type}")
        # Draw footer
        c.setFont("Helvetica", 10)
        c.drawString(72, 30, f"Page {c.getPageNumber()}")

    def add_questions(self, c, questions):
        y = 700
        for i, question in enumerate(questions, start=1):
            if y < 72:
                c.showPage()
                self.draw_template(c, "secondpage")  # Call to draw_template
                y = 700
            c.setFont("Helvetica", 12)
            c.drawString(72, y, f"Q{i}: {question}")
            y -= 36