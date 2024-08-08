import wx

class HistorialMedico:
    def __init__(self):
        # Simula una base de datos con un diccionario
        self.historiales = {}

    def actualizar_historial(self, id, datos):
        # Actualiza el historial con el ID dado
        self.historiales[id] = datos

    def obtener_historial(self, id):
        # Obtiene el historial con el ID dado
        return self.historiales.get(id, {})

class ModificarHistorialFrame(wx.Frame):
    def __init__(self, parent, historial_id, historial_medico):
        super(ModificarHistorialFrame, self).__init__(parent, title="Modificar Historial Médico", size=(400, 300))
        
        self.historial_id = historial_id
        self.historial_medico = historial_medico
        
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.init_ui()
        
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def init_ui(self):
        # Obtiene los datos del historial actual
        self.historial_data = self.historial_medico.obtener_historial(self.historial_id)
        
        # Crea los campos de entrada
        self.txtNombre = wx.TextCtrl(self.panel, value=self.historial_data.get('nombre', ''))
        self.txtEspecie = wx.TextCtrl(self.panel, value=self.historial_data.get('especie', ''))
        self.txtRaza = wx.TextCtrl(self.panel, value=self.historial_data.get('raza', ''))
        self.txtEdad = wx.TextCtrl(self.panel, value=self.historial_data.get('edad', ''))
        self.txtSexo = wx.TextCtrl(self.panel, value=self.historial_data.get('sexo', ''))
        self.txtPeso = wx.TextCtrl(self.panel, value=self.historial_data.get('peso', ''))
        self.txtPropietario = wx.TextCtrl(self.panel, value=self.historial_data.get('propietario', ''))
        self.txtTelefono = wx.TextCtrl(self.panel, value=self.historial_data.get('telefono', ''))
        self.txtDireccion = wx.TextCtrl(self.panel, value=self.historial_data.get('direccion', ''))
        self.txtDescripcion = wx.TextCtrl(self.panel, value=self.historial_data.get('descripcion', ''), style=wx.TE_MULTILINE)

        # Configura el sizer para los campos de entrada
        grid_sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        grid_sizer.AddMany([
            (wx.StaticText(self.panel, label="Nombre:"), 0, wx.ALIGN_RIGHT),
            (self.txtNombre, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Especie:"), 0, wx.ALIGN_RIGHT),
            (self.txtEspecie, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Raza:"), 0, wx.ALIGN_RIGHT),
            (self.txtRaza, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Edad:"), 0, wx.ALIGN_RIGHT),
            (self.txtEdad, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Sexo:"), 0, wx.ALIGN_RIGHT),
            (self.txtSexo, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Peso:"), 0, wx.ALIGN_RIGHT),
            (self.txtPeso, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Propietario:"), 0, wx.ALIGN_RIGHT),
            (self.txtPropietario, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Teléfono:"), 0, wx.ALIGN_RIGHT),
            (self.txtTelefono, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Dirección:"), 0, wx.ALIGN_RIGHT),
            (self.txtDireccion, 1, wx.EXPAND),
            (wx.StaticText(self.panel, label="Descripción:"), 0, wx.ALIGN_RIGHT),
            (self.txtDescripcion, 1, wx.EXPAND),
        ])
        grid_sizer.AddGrowableCol(1, 1)

        self.vbox.Add(grid_sizer, 1, wx.ALL | wx.EXPAND, 10)
        
        # Botones de guardar y cancelar
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btnSave = wx.Button(self.panel, label="Guardar")
        btnCancel = wx.Button(self.panel, label="Cancelar")
        
        hbox_buttons.Add(btnSave, 0, wx.ALL, 5)
        hbox_buttons.Add(btnCancel, 0, wx.ALL, 5)
        
        self.vbox.Add(hbox_buttons, 0, wx.ALIGN_CENTER)
        
        self.panel.SetSizer(self.vbox)
        
        btnSave.Bind(wx.EVT_BUTTON, self.on_save)
        btnCancel.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_save(self, event):
        # Recoge los datos del formulario
        updated_data = {
            "nombre": self.txtNombre.GetValue(),
            "especie": self.txtEspecie.GetValue(),
            "raza": self.txtRaza.GetValue(),
            "edad": self.txtEdad.GetValue(),
            "sexo": self.txtSexo.GetValue(),
            "peso": self.txtPeso.GetValue(),
            "propietario": self.txtPropietario.GetValue(),
            "telefono": self.txtTelefono.GetValue(),
            "direccion": self.txtDireccion.GetValue(),
            "descripcion": self.txtDescripcion.GetValue(),
        }
        
        # Guarda los datos actualizados
        self.historial_medico.actualizar_historial(self.historial_id, updated_data)
        
        wx.MessageBox('Historial médico actualizado con éxito.', 'Información', wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def on_cancel(self, event):
        self.Close()

    def on_close(self, event):
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    historial_medico = HistorialMedico()
    frame = ModificarHistorialFrame(None, '1', historial_medico)
    frame.Show()
    app.MainLoop()
