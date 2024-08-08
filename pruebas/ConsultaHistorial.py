import wx

class ConsultaHistorialDialog(wx.Dialog):
    def __init__(self, parent, data):
        super(ConsultaHistorialDialog, self).__init__(parent, title="Consulta de Historial Médico", size=(400, 600))

        panel = wx.Panel(self)

        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        form_sizer = wx.FlexGridSizer(10, 2, 10, 10)  # 10 filas, 2 columnas con márgenes entre elementos

        # Tamaño fijo para los labels para alineación uniforme
        label_size = (80, -1)  # 80 de ancho, altura automática

        # Campos de información (solo labels)
        form_sizer.Add(wx.StaticText(panel, label="Nombre:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(wx.StaticText(panel, label=data["nombre"]), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        form_sizer.Add(wx.StaticText(panel, label="Especie:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(wx.StaticText(panel, label=data["especie"]), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        form_sizer.Add(wx.StaticText(panel, label="Raza:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(wx.StaticText(panel, label=data["raza"]), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        form_sizer.Add(wx.StaticText(panel, label="Edad:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(wx.StaticText(panel, label=data["edad"]), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        form_sizer.Add(wx.StaticText(panel, label="Sexo:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(wx.StaticText(panel, label=data["sexo"]), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        form_sizer.Add(wx.StaticText(panel, label="Peso:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(wx.StaticText(panel, label=data["peso"]), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        form_sizer.Add(wx.StaticText(panel, label="Propietario:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(wx.StaticText(panel, label=data["propietario"]), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        form_sizer.Add(wx.StaticText(panel, label="Teléfono:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(wx.StaticText(panel, label=data["telefono"]), 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        # Layout para Dirección
        form_sizer.Add(wx.StaticText(panel, label="Dirección:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_TOP)
        self.direccion_text = wx.TextCtrl(panel, size=(300, 50), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.direccion_text.SetValue(data["direccion"])
        form_sizer.Add(self.direccion_text, 1, wx.EXPAND)

        # Layout para Descripción
        form_sizer.Add(wx.StaticText(panel, label="Descripción:", size=label_size), 0, wx.ALIGN_RIGHT | wx.ALIGN_TOP)
        self.descripcion_text = wx.TextCtrl(panel, size=(300, 150), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.descripcion_text.SetValue(data["descripcion"])
        form_sizer.Add(self.descripcion_text, 1, wx.EXPAND)

        # Añadir el formulario y campos extendidos al contenedor
        vbox.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 15)

        # Botones de acción
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        close_button = wx.Button(panel, label="Cerrar")
        hbox.Add(close_button, 0, wx.ALL, 5)

        vbox.Add(hbox, 0, wx.ALIGN_CENTER)

        panel.SetSizer(vbox)

        # Bind evento de botón
        close_button.Bind(wx.EVT_BUTTON, self.on_close)

    def on_close(self, event):
        self.EndModal(wx.ID_CLOSE)
