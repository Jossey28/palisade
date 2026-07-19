from fpdf import FPDF
from datetime import datetime

class MemoPDF(FPDF):
    def header(self):
        # 1. Add the Logo on the top right
        try:
            # Parameters: image_path, x, y, width
            self.image("Overleaf-logo.jpg", x=140, y=10, w=60)
        except FileNotFoundError:
            # Fallback if image isn't there yet so the script doesn't crash
            self.set_font("Helvetica", "I", 10)
            self.set_text_color(150, 150, 150)
            self.text(140, 20, "[Logo Missing: Overleaf-logo.jpg]")
        
        # Move cursor below logo height for the metadata header
        self.set_y(35)

    def draw_memo_header(self, memo_to, memo_from, subject, date_str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        
        # Construct the metadata block grid
        headers = [
            ("TO:", memo_to),
            ("FROM:", memo_from),
            ("SUBJECT:", subject),
            ("DATE:", date_str)
        ]
        
        for label, val in headers:
            self.set_font("Helvetica", "B", 11)
            self.cell(25, 7, label, ln=0)
            self.set_font("Helvetica", "", 11)
            self.cell(0, 7, val, ln=1)
            
        # Draw a clean horizontal rule divider line (like the LaTeX template)
        self.ln(4)
        self.set_draw_color(180, 180, 180) # Light grey line
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8) # Space below line

def create_memo_pdf(output_filename="memo_output.pdf"):
    # Create PDF instance: Portrait, millimeters, A4 page size
    pdf = MemoPDF(orientation="P", unit="mm", format="A4")
    
    # Set page margins (10mm left/right, 15mm top)
    pdf.set_margins(10, 15, 10)
    pdf.add_page()
    
    # 2. Populate the Metadata Header
    today_date = datetime.today().strftime('%B %d, %Y')
    pdf.draw_memo_header(
        memo_to="Professor X",
        memo_from="John",
        subject="New memo template available via Python",  # <-- Change memosubject to subject
        date_str=today_date
    )

    # 3. Add Main Body Text (Replacing \lipsum)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    
    body_text_p1 = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Satius autem sapientia "
        "aliquid hoc dubitandum fuerit, utrumne certamen honestum an turpe sit. Duo Reges: "
        "constructio interrete. Quid Zeno torqueat? Torquem detraxit hosti. Et quidem, inquit, "
        "appetitum animi, quem Graeci impetum vocant, aut pactionem."
    )
    
    body_text_p2 = (
        "Quis istum dolorem timet? Non quaerere, inquam, hoc illud Torquati dedecebit, "
        "commodo tueri naturae! Hanc quoque iucunditatem, si vis, transfer in animum; "
        "Atque hoc loco similitudines eas, quibus illi uti solent, dissimillimas proferebas."
    )
    
    # multi_cell automatically handles word wrapping at margins
    # Parameters: width (0 means match margin), line_height, text
    pdf.multi_cell(0, 6, body_text_p1)
    pdf.ln(5) # Paragraph spacing
    pdf.multi_cell(0, 6, body_text_p2)
    
    # Save the output file
    pdf.output(output_filename)
    print(f"Successfully generated pure Python PDF: {output_filename}")

if __name__ == "__main__":
    create_memo_pdf("overleaf_memo_clean.pdf")