import wx
import os

class ConsultaHistorialDialog(wx.Dialog):
    def __init__(self, parent, data=None):
        super(ConsultaHistorialDialog, self).__init__(parent, title="Consulta de Historial Médico", size=(580, 600))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox_main = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = wx.Panel(panel)
        left_vbox = wx.BoxSizer(wx.VERTICAL)

        # Definir campos del formulario
        form_sizer = wx.FlexGridSizer(10, 2, 10, 10)

        form_sizer.Add(wx.StaticText(left_panel, label="Nombre:"), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(wx.StaticText(left_panel, label=data.get("nombre", "")), flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Especie:"), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(wx.StaticText(left_panel, label=data.get("especie", "")), flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Raza:"), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(wx.StaticText(left_panel, label=data.get("raza", "")), flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Edad:"), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(wx.StaticText(left_panel, label=data.get("edad", "")), flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Sexo:"), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(wx.StaticText(left_panel, label=data.get("sexo", "")), flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Peso:"), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(wx.StaticText(left_panel, label=data.get("peso", "")), flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Propietario:"), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(wx.StaticText(left_panel, label=data.get("propietario", "")), flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Teléfono:"), flag=wx.ALIGN_RIGHT)
        form_sizer.Add(wx.StaticText(left_panel, label=data.get("telefono", "")), flag=wx.EXPAND)

        # Campos de texto grandes
        form_sizer.Add(wx.StaticText(left_panel, label="Dirección:"), flag=wx.ALIGN_RIGHT)
        direccion_text = wx.TextCtrl(left_panel, value=data.get("direccion", ""), style=wx.TE_READONLY | wx.TE_MULTILINE, size=(200, 60))
        form_sizer.Add(direccion_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Descripción:"), flag=wx.ALIGN_RIGHT)
        descripcion_text = wx.TextCtrl(left_panel, value=data.get("descripcion", ""), style=wx.TE_READONLY | wx.TE_MULTILINE, size=(200, 100))
        form_sizer.Add(descripcion_text, flag=wx.EXPAND)

        left_vbox.Add(form_sizer, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # Botón Cerrar
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        close_button = wx.Button(left_panel, label="Cerrar")
        hbox_buttons.Add(close_button, 0, wx.ALL, 5)
        left_vbox.Add(hbox_buttons, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        left_panel.SetSizer(left_vbox)

        # Panel derecho para la imagen
        right_panel = wx.Panel(panel)
        right_vbox = wx.BoxSizer(wx.VERTICAL)

        # Panel para el cuadro de previsualización de la imagen
        image_panel = wx.Panel(right_panel, size=(200, 200))
        image_panel.SetBackgroundColour(wx.Colour(220, 220, 220))

        self.image_preview = wx.StaticBitmap(image_panel, size=(200, 200))
        self.image_preview.SetBackgroundColour(wx.Colour(190, 190, 190))

        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_sizer.Add(self.image_preview, 1, wx.EXPAND | wx.ALL, 0)
        image_panel.SetSizer(image_sizer)

        right_vbox.Add(image_panel, 0, wx.EXPAND | wx.ALL, 10)

        right_panel.SetSizer(right_vbox)

        hbox_main.Add(left_panel, 2, wx.EXPAND | wx.ALL, 10)
        hbox_main.Add(right_panel, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(hbox_main, 1, wx.EXPAND)

        panel.SetSizer(vbox)

        # Cargar imagen si existe
        if data and data.get("imagen"):
            self.load_image(data.get("imagen"))

        # Bind evento de botón
        close_button.Bind(wx.EVT_BUTTON, self.on_close)

    def on_close(self, event):
        self.EndModal(wx.ID_CLOSE)

    def load_image(self, path):
        try:
            # Verificar que la ruta no esté vacía y que el archivo exista
            if path and os.path.isfile(path):
                image = wx.Image(path, wx.BITMAP_TYPE_ANY)
                if image.IsOk():
                    # Escalar la imagen para ajustarla al tamaño del cuadro
                    image = image.Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
                    bitmap = wx.Bitmap(image)
                    self.image_preview.SetBitmap(bitmap)
                    self.Refresh()
                else:
                    wx.LogError("La imagen no se cargó correctamente.")
            else:
                wx.LogError(f"Archivo no encontrado: {path}")
        except Exception as e:
            wx.LogError(f"Error al cargar la imagen: {e}")
