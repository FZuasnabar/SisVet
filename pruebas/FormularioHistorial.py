import wx

class FormularioHistorialDialog(wx.Dialog):
    def __init__(self, parent, data=None):
        super(FormularioHistorialDialog, self).__init__(parent, title="Formulario de Historial Médico", size=(500, 550))

        # Panel principal del diálogo
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Crear una caja horizontal para los formularios y la imagen
        hbox_main = wx.BoxSizer(wx.HORIZONTAL)

        # Panel izquierdo para las etiquetas y cajas de texto
        left_panel = wx.Panel(panel)
        left_vbox = wx.BoxSizer(wx.VERTICAL)

        # Campos del formulario
        form_sizer = wx.FlexGridSizer(10, 2, 10, 10)
        form_sizer.Add(wx.StaticText(left_panel, label="Nombre:"), flag=wx.ALIGN_RIGHT)
        self.nombre_text = wx.TextCtrl(left_panel)
        form_sizer.Add(self.nombre_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Especie:"), flag=wx.ALIGN_RIGHT)
        self.especie_choice = wx.Choice(left_panel, choices=["Perro", "Gato"])
        form_sizer.Add(self.especie_choice, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Raza:"), flag=wx.ALIGN_RIGHT)
        self.raza_text = wx.TextCtrl(left_panel)
        form_sizer.Add(self.raza_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Edad:"), flag=wx.ALIGN_RIGHT)
        self.edad_text = wx.TextCtrl(left_panel)
        form_sizer.Add(self.edad_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Sexo:"), flag=wx.ALIGN_RIGHT)
        self.sexo_choice = wx.Choice(left_panel, choices=["Macho", "Hembra"])
        form_sizer.Add(self.sexo_choice, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Peso:"), flag=wx.ALIGN_RIGHT)
        self.peso_text = wx.TextCtrl(left_panel)
        form_sizer.Add(self.peso_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Propietario:"), flag=wx.ALIGN_RIGHT)
        self.propietario_text = wx.TextCtrl(left_panel)
        form_sizer.Add(self.propietario_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Teléfono:"), flag=wx.ALIGN_RIGHT)
        self.telefono_text = wx.TextCtrl(left_panel)
        form_sizer.Add(self.telefono_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Dirección:"), flag=wx.ALIGN_RIGHT)
        self.direccion_text = wx.TextCtrl(left_panel, style=wx.TE_MULTILINE, size=(-1, 60))
        form_sizer.Add(self.direccion_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Descripción:"), flag=wx.ALIGN_RIGHT)
        self.descripcion_text = wx.TextCtrl(left_panel, style=wx.TE_MULTILINE, size=(-1, 100))
        form_sizer.Add(self.descripcion_text, flag=wx.EXPAND)

        left_vbox.Add(form_sizer, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # Botones OK y Cancelar
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(left_panel, id=wx.ID_OK, label="Aceptar")
        cancel_button = wx.Button(left_panel, id=wx.ID_CANCEL, label="Cancelar")
        hbox_buttons.Add(ok_button, 0, wx.ALL, 5)
        hbox_buttons.Add(cancel_button, 0, wx.ALL, 5)
        left_vbox.Add(hbox_buttons, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        left_panel.SetSizer(left_vbox)

        # Panel derecho para la imagen y el botón de agregar
        right_panel = wx.Panel(panel)
        right_vbox = wx.BoxSizer(wx.VERTICAL)

        # Panel para el cuadro de previsualización de la imagen
        image_panel = wx.Panel(right_panel, size=(200, 200))
        image_panel.SetBackgroundColour(wx.Colour(220, 220, 220))  # Gris oscuro para el fondo del panel de imagen

        # Cuadro de previsualización de la imagen
        self.image_preview = wx.StaticBitmap(image_panel, size=(200, 200))
        self.image_preview.SetBackgroundColour(wx.Colour(190, 190, 190))  # Gris oscuro para la imagen

        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_sizer.Add(self.image_preview, 1, wx.EXPAND | wx.ALL, 0)
        image_panel.SetSizer(image_sizer)

        # Añadir el panel de imagen al panel derecho
        right_vbox.Add(image_panel, 0, wx.EXPAND | wx.ALL, 10)

        # Botón para agregar foto
        add_photo_button = wx.Button(right_panel, label="Agregar Foto")
        add_photo_button.Bind(wx.EVT_BUTTON, self.on_add_photo)
        right_vbox.Add(add_photo_button, 0, wx.ALL | wx.CENTER, 10)

        right_panel.SetSizer(right_vbox)

        # Añadir paneles a la ventana del diálogo
        hbox_main.Add(left_panel, 2, wx.EXPAND | wx.ALL, 10)
        hbox_main.Add(right_panel, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(hbox_main, 1, wx.EXPAND)

        panel.SetSizer(vbox)

        if data:
            self.nombre_text.SetValue(data.get("nombre", ""))
            self.especie_choice.SetStringSelection(data.get("especie", ""))
            self.raza_text.SetValue(data.get("raza", ""))
            self.edad_text.SetValue(data.get("edad", ""))
            self.sexo_choice.SetStringSelection(data.get("sexo", ""))
            self.peso_text.SetValue(data.get("peso", ""))
            self.propietario_text.SetValue(data.get("propietario", ""))
            self.telefono_text.SetValue(data.get("telefono", ""))
            self.direccion_text.SetValue(data.get("direccion", ""))
            self.descripcion_text.SetValue(data.get("descripcion", ""))
            self.id = data.get("id", None)  # Guarda el ID en un atributo

    def get_data(self):
        return {
            "id": getattr(self, 'id', None),  # Incluye el ID en el diccionario devuelto
            "nombre": self.nombre_text.GetValue(),
            "especie": self.especie_choice.GetStringSelection(),
            "raza": self.raza_text.GetValue(),
            "edad": self.edad_text.GetValue(),
            "sexo": self.sexo_choice.GetStringSelection(),
            "peso": self.peso_text.GetValue(),
            "propietario": self.propietario_text.GetValue(),
            "telefono": self.telefono_text.GetValue(),
            "direccion": self.direccion_text.GetValue(),
            "descripcion": self.descripcion_text.GetValue()
        }

    def on_add_photo(self, event):
        # Abrir un cuadro de diálogo para seleccionar una imagen
        with wx.FileDialog(self, "Seleccionar imagen", wildcard="Imagenes (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # El usuario canceló el diálogo

            # Obtener la ruta del archivo
            path = file_dialog.GetPath()

            # Cargar y mostrar la imagen
            self.load_image(path)

    def load_image(self, path):
        # Cargar la imagen
        image = wx.Image(path, wx.BITMAP_TYPE_ANY)

        # Redimensionar la imagen para ajustar el tamaño del cuadro de previsualización
        image = image.Scale(200, 200, wx.IMAGE_QUALITY_HIGH)

        # Convertir la imagen a un bitmap y mostrarla en el cuadro de previsualización
        bitmap = wx.Bitmap(image)
        self.image_preview.SetBitmap(bitmap)
        self.Layout()  # Reajustar el diseño para mostrar la imagen correctamente

if __name__ == "__main__":
    app = wx.App(False)
    dialog = FormularioHistorialDialog(None)
    dialog.ShowModal()
    dialog.Destroy()
    app.MainLoop()
