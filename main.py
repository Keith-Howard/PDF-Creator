from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, TableStyle, Frame, Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
import datetime


def put_frame(canvas_doc, x_position, y_position, len_width, len_height,
              left_padding, bottom_padding, right_padding, top_padding, id, show_boundary):
    f = Frame(x_position * canvas_inch, y_position * canvas_inch, len_width * canvas_inch, len_height * canvas_inch,
              leftPadding=left_padding, bottomPadding=bottom_padding, rightPadding=right_padding,
              topPadding=top_padding, id=id, showBoundary=show_boundary)
    f.drawBoundary(canvas_doc, __boundary__=None)
    return len_width, len_height


def put_paragraph(canvas_doc, x_position, y_position,
                  avail_width, avail_height, text, font_size, alignment):
    paragraph_style = ParagraphStyle('Normal', alignment=alignment, fontSize=font_size, leading=font_size * 1.20)
    paragraph = Paragraph(text, style=paragraph_style)
    width_pts_used, height_pts_used = paragraph.wrapOn(canvas_doc, avail_width * canvas_inch, avail_height * canvas_inch)
    paragraph.drawOn(canvas_doc, x_position * canvas_inch, y_position * canvas_inch)
    return width_pts_used / canvas_inch, height_pts_used / canvas_inch


def put_picture(canvas_doc, x_position, y_position, len_width, len_height,
                image_filename, scaling_percent):
    canvas_doc.drawImage(image_filename, x_position * canvas_inch, y_position * canvas_inch,
                         len_width * canvas_inch * scaling_percent, len_height * canvas_inch * scaling_percent)
    return len_width * scaling_percent, len_height * scaling_percent


def put_table(canvas_doc, x_position, y_position, avail_width, avail_height, col_width, row_height, font_size, table_data,
              background_color, text_color, box_color):
    f = Table(table_data, colWidths=col_width * canvas_inch, rowHeights=row_height * canvas_inch,)
    f.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), background_color),
                           ('TEXTCOLOR', (0, 0), (-1, -1), text_color),
                           ('INNERGRID', (0, 0), (-1, -1), 1, box_color),
                           ('FONTSIZE', (0, 0), (-1, -1), font_size),
                           ('LEADING', (0, 0), (-1, -1), font_size * 1.20),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('BOX', (0, 0), (-1, -1), 1, box_color)]))
    (width_used, height_used) = f.wrapOn(c, avail_width * canvas_inch, avail_height * canvas_inch)
    f.drawOn(canvas_doc, x_position * canvas_inch, y_position * canvas_inch)
    return width_used / canvas_inch, height_used / canvas_inch


canvas_inch = 72.0
date = str(datetime.datetime.today()).split()[0]
output_pdf = r"outputFolder/drivers_license.pdf"
c = canvas.Canvas(output_pdf, pagesize=letter)
image = r'images/licensePhoto.jpeg'
data = [['Doe'],
        ['John'],
        ['555 Main Street'],
        ['Your City, NY 11111']]
p = 'My name is John Doe. I am 26 years old and live in Your City NY. I have lived in New York for ' \
    '1 and a half years. I have been driving since I was 16. Photo from https://depositphotos.com/,' \
    ' royalty free images.'

c.setFont('Times-Bold', 60)
put_paragraph(c, .5, 6, 7, 2, "John Doe's Drivers License", 60, TA_CENTER)

c.showPage()

frame_width_and_height = put_frame(c, .25, .25, 8, 10.5, 0, 0, 0, 0, None, 1)
# print('frame_width_and_height', frame_width_and_height)

put_paragraph(c, .5, 8.75, 7, 2, "New York State", 60, TA_CENTER)
put_paragraph(c, 1, 8, 6.5, 1, "Driver License", 45, TA_CENTER)

picture_width_and_height = put_picture(c, 1, 4.55, 3.25, 2.5, image, 1)
# print('picture_width_and_height', picture_width_and_height)
table_width_and_height = put_table(c, 3.75, 4.55, 1.5, 3, 3.75, .75, 24, data, colors.yellow, colors.black, colors.red)
# print("table_width_and_height", table_width_and_height)
paragraph_width_and_height = put_paragraph(c, 1, 3.25, 6.5, .5, p, 12, TA_LEFT)
# print("paragraph_width_and_height", paragraph_width_and_height)
put_paragraph(c, 6, 1, 3, 1, date, 10, TA_LEFT)
c.save()
print("Location of the PDF ", output_pdf)

