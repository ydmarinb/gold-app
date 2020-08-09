def camara_compra(idDetalle):
    import PySimpleGUI as sg
    from datetime import date
    import cv2

    camara = cv2.VideoCapture(0)

    sg.theme('DarkGreen5')
    # Definimos los elementos de la interfaz grafica
    layout = [[sg.Image(filename='', key='-image-')],
              [sg.Button('Tomar Fotografia'), sg.Button('Salir')]]
    # Creamos la interfaz grafica
    window = sg.Window('Camara',
                       layout,
                       no_titlebar=False,
                       location=(0, 0))

    image_elem = window['-image-']

    numero = 0
    while camara.isOpened() and numero < 1:
        # Obtenemos informacion de la interfaz grafica y video
        event, values = window.read(timeout=0)
        ret, frame = camara.read()

        # Si salimos
        if event == 'Salir':
            window.close()
            break

        # Si tomamos foto
        elif event == 'Tomar Fotografia':
            cv2.imwrite('fh/foto_compra/'+str(idDetalle)+".png", frame)
            numero += 1
            window.close()

        if not ret:
            break

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        image_elem.update(data=imgbytes)

    camara.release()


######################################################

def camara_cliente(cedula):
    import PySimpleGUI as sg
    from datetime import date
    import cv2

    camara = cv2.VideoCapture(0)

    sg.theme('DarkGreen5')
    # Definimos los elementos de la interfaz grafica
    layout = [[sg.Image(filename='', key='-image-')],
              [sg.Button('Tomar Fotografia'), sg.Button('Salir')]]
    # Creamos la interfaz grafica
    window = sg.Window('Camara',
                       layout,
                       no_titlebar=False,
                       location=(0, 0))

    image_elem = window['-image-']

    numero = 0
    while camara.isOpened() and numero < 1:
        # Obtenemos informacion de la interfaz grafica y video
        event, values = window.read(timeout=0)
        ret, frame = camara.read()

        # Si salimos
        if event == 'Salir':
            window.close()
            break

        # Si tomamos foto
        elif event == 'Tomar Fotografia':
            cv2.imwrite('fh/foto_ingreso/'+str(cedula)+".png", frame)
            numero += 1
            window.close()

        if not ret:
            break

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        image_elem.update(data=imgbytes)

    camara.release()