import wx

class FormularioHistorialDialog(wx.Dialog):
    def __init__(self, parent, data=None):
        super(FormularioHistorialDialog, self).__init__(parent, title="Formulario de Historial Médico", size=(400, 500))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campos del formulario
        form_sizer = wx.FlexGridSizer(10, 2, 10, 10)
        form_sizer.Add(wx.StaticText(panel, label="Nombre:"), flag=wx.ALIGN_RIGHT)
        self.nombre_text = wx.TextCtrl(panel)
        form_sizer.Add(self.nombre_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Especie:"), flag=wx.ALIGN_RIGHT)
        self.especie_choice = wx.Choice(panel, choices=["Perro", "Gato"])
        form_sizer.Add(self.especie_choice, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Raza:"), flag=wx.ALIGN_RIGHT)
        self.raza_text = wx.TextCtrl(panel)
        form_sizer.Add(self.raza_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Edad:"), flag=wx.ALIGN_RIGHT)
        self.edad_text = wx.TextCtrl(panel)
        form_sizer.Add(self.edad_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Sexo:"), flag=wx.ALIGN_RIGHT)
        self.sexo_choice = wx.Choice(panel, choices=["Macho", "Hembra"])
        form_sizer.Add(self.sexo_choice, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Peso:"), flag=wx.ALIGN_RIGHT)
        self.peso_text = wx.TextCtrl(panel)
        form_sizer.Add(self.peso_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Propietario:"), flag=wx.ALIGN_RIGHT)
        self.propietario_text = wx.TextCtrl(panel)
        form_sizer.Add(self.propietario_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Teléfono:"), flag=wx.ALIGN_RIGHT)
        self.telefono_text = wx.TextCtrl(panel)
        form_sizer.Add(self.telefono_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Dirección:"), flag=wx.ALIGN_RIGHT)
        self.direccion_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        form_sizer.Add(self.direccion_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(panel, label="Descripción:"), flag=wx.ALIGN_RIGHT)
        self.descripcion_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        form_sizer.Add(self.descripcion_text, flag=wx.EXPAND)

        vbox.Add(form_sizer, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # Botones OK y Cancelar
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, id=wx.ID_OK, label="Aceptar")
        cancel_button = wx.Button(panel, id=wx.ID_CANCEL, label="Cancelar")
        hbox_buttons.Add(ok_button, 0, wx.ALL, 5)
        hbox_buttons.Add(cancel_button, 0, wx.ALL, 5)
        vbox.Add(hbox_buttons, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

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
