from fpdf import FPDF

def write_file_to_pdf(filename):
  
    # save FPDF() class into 
    # a variable pdf
    pdf = FPDF()   
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font 
    # that you want in the pdf
    pdf.set_font("Arial", size = 15)
    
    # open the text file in read mode
    f = open(filename, "r")
    
    # insert the texts in pdf
    for x in f:
        pdf.cell(200, 10, txt = x, ln = 1)
    
    # save the pdf with name .pdf
    pdf.output(f"{filename}_history.pdf")   


write_file_to_pdf("w.txt")