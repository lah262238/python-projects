from pdf2docx import Converter

pdf_file = "input.pdf"      # your PDF file name
docx_file = "output.docx"   # output Word file name

cv = Converter(pdf_file)
cv.convert(docx_file, start=0, end=None)
cv.close()

print("Conversion completed successfully!")
