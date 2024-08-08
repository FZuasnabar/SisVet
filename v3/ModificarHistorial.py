import wx
from FormularioHistorial import FormularioHistorialDialog
from ConsultaHistorial import ConsultaHistorialDialog

class HistorialMedicoFrame(wx.Frame):
    def __init__(self, parent):
        super(HistorialMedicoFrame, self).__init__(parent, title="Historial Médico", size=(800, 600))

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Botón para crear nuevo historial
        new_button = wx.Button(panel, label="Nuevo Historial")
        vbox.Add(new_button, 0, wx.ALL | wx.CENTER, 10)
        new_button.Bind(wx.EVT_BUTTON, self.on_new_historial)

        # Botón para modificar historial
        modify_button = wx.Button(panel, label="Modificar Historial")
        vbox.Add(modify_button, 0, wx.ALL | wx.CENTER, 10)
        modify_button.Bind(wx.EVT_BUTTON, self.on_modify_historial)

        # Botón para eliminar historial
        delete_button = wx.Button(panel, label="Eliminar Historial")
        vbox.Add(delete_button, 0, wx.ALL | wx.CENTER, 10)
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete_historial)

        # Tabla para mostrar los historiales
        self.historial_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.historial_list.InsertColumn(0, "Nombre")
        self.historial_list.InsertColumn(1, "Especie")
        self.historial_list.InsertColumn(2, "Raza")
        self.historial_list.InsertColumn(3, "Edad")
        self.historial_list.InsertColumn(4, "Sexo")
        self.historial_list.InsertColumn(5, "Peso")
        self.historial_list.InsertColumn(6, "Propietario")
        self.historial_list.InsertColumn(7, "Teléfono")
        self.historial_list.InsertColumn(8, "Dirección")
        self.historial_list.InsertColumn(9, "Descripción")

        vbox.Add(self.historial_list, 1, wx.ALL | wx.EXPAND, 10)

        panel.SetSizer(vbox)

    def on_new_historial(self, event):
        with FormularioHistorialDialog(self) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                data = dialog.get_data()
                self.add_historial_to_list(data)

    def on_modify_historial(self, event):
        selected_item = self.historial_list.GetFirstSelected()
        if selected_item != -1:
            historial_id = self.historial_list.GetItemText(selected_item, 0)
            # Aquí debes obtener los datos del historial desde la base de datos usando historial_id
            # Por ejemplo, podrías tener una función get_historial_data(id) que obtenga estos datos
            data = {
                "id": "historial_id",
                "nombre": "Nombre del historial",
                "especie": "Especie",
                "raza": "Raza",
                "edad": "Edad",
                "sexo": "Sexo",
                "peso": "Peso",
                "propietario": "Propietario",
                "telefono": "Teléfono",
                "direccion": "Dirección",
                "descripcion": "Descripción"
            }

            dialog = FormularioHistorialDialog(self, data=data)
            if dialog.ShowModal() == wx.ID_OK:
                updated_data = dialog.get_data()
                # Asegúrate de que el ID esté en updated_data
                if 'id' in updated_data:
                    self.update_historial_in_list(selected_item, updated_data)
                else:
                    wx.MessageBox("El ID del historial no se ha encontrado.", "Error", wx.OK | wx.ICON_ERROR)
            dialog.Destroy()

    def on_delete_historial(self, event):
        selected_item = self.historial_list.GetFirstSelected()
        if selected_item != -1:
            self.historial_list.DeleteItem(selected_item)

    def add_historial_to_list(self, data):
        index = self.historial_list.InsertItem(self.historial_list.GetItemCount(), data["nombre"])
        self.historial_list.SetItem(index, 1, data["especie"])
        self.historial_list.SetItem(index, 2, data["raza"])
        self.historial_list.SetItem(index, 3, data["edad"])
        self.historial_list.SetItem(index, 4, data["sexo"])
        self.historial_list.SetItem(index, 5, data["peso"])
        self.historial_list.SetItem(index, 6, data["propietario"])
        self.historial_list.SetItem(index, 7, data["telefono"])
        self.historial_list.SetItem(index, 8, data["direccion"])
        self.historial_list.SetItem(index, 9, data["descripcion"])

    def update_historial_in_list(self, index, data):
        self.historial_list.SetItem(index, 0, data["nombre"])
        self.historial_list.SetItem(index, 1, data["especie"])
        self.historial_list.SetItem(index, 2, data["raza"])
        self.historial_list.SetItem(index, 3, data["edad"])
        self.historial_list.SetItem(index, 4, data["sexo"])
        self.historial_list.SetItem(index, 5, data["peso"])
        self.historial_list.SetItem(index, 6, data["propietario"])
        self.historial_list.SetItem(index, 7, data["telefono"])
        self.historial_list.SetItem(index, 8, data["direccion"])
        self.historial_list.SetItem(index, 9, data["descripcion"])
