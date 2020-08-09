from datetime import time


def documento_equivalente(nombre, cedula, celular, cantidad, valor_unitario, id_detalle, total):

    from PyPDF2 import PdfFileWriter, PdfFileReader
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from datetime import datetime
    import os

    os.chdir('C:/Users/ydmar/OneDrive/Documentos/Proyectos/Gold/backend')
    # Carga de fuente
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

    # Fecha de hoy

    anno = datetime.now().year
    dia = datetime.now().day
    mes = datetime.now().month

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    # Nombre
    can.drawString(95, 680, nombre)
    # CC
    can.drawString(100, 658, str(cedula))
    #Vereda
    #can.drawString(106, 636, vereda)
    #tel
    can.drawString(400, 636, str(celular))
    #can.drawString(225, 590, "1216722806")
    #can.drawString(329, 590, "1216722806")
    #Cantidad
    can.drawString(225, 567, str(cantidad))
    #Valor unitario
    can.drawString(329, 567, str(valor_unitario))
    # valor total
    #can.drawString(450, 567, cantidad*valor_unitario)
    #can.drawString(450, 590, "1216722806")

    #Base
    #can.drawString(465, 530, "126722806")
    # Regalias
    #can.drawString(465, 507, "126722806")
    # Total
    can.drawString(465, 480, str(total))
    # cambio tipo de letra
    can.setFont('Arial', 18)
    # Poner dia
    can.drawString(443, 698, str(dia))
    # Poner mes
    can.drawString(500, 698, str(mes))
    # Poner año
    can.drawString(540, 698, str(anno))
    # Numero
    can.drawString(500, 740, str(id_detalle))


    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("pdfs/EQUIVALENTE-editado.pdf", "rb"))
    # Cambiar directorio
    os.chdir('pdfs')
    try:
    # crear carpeta
        os.mkdir('documento_equivalente')
    # cambiar ruta
    except:
        pass
    os.chdir('documento_equivalente')
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("documento_equivalente_{}_{}.pdf".format((str(anno))+'-'+str(mes)+'-'+str(dia), cedula), "wb")
    output.write(outputStream)
    outputStream.close()
    os.chdir('../..')

def abrir_documento_equivalente(cedula):
    import os
    import time
    os.chdir('pdfs/documento_equivalente/')
    cedulas = [str(cedula)]
    documentos = [v for v in os.listdir() if v[31:].split('.')[0] in (cedulas)]
    os.startfile(documentos[0])
    os.chdir('../..')




def unir_documento_equivalente():
    from PyPDF2 import PdfFileMerger, PdfFileReader
    import os
    import time
    import shutil
    os.chdir('pdfs/documento_equivalente/')
    # Call the PdfFileMerger
    mergedObject = PdfFileMerger()
    documentos = os.listdir()
    for documento in documentos:
        mergedObject.append(PdfFileReader(documento, 'rb'))
    mergedObject.write("documento_equivalente_join.pdf")
    os.startfile('documento_equivalente_join.pdf')
    time.sleep(10)
    os.chdir('..')
    shutil.rmtree("documento_equivalente")
    os.chdir('..')
