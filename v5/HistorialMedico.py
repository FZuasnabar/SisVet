import wx
import json
import os
from ConsultaHistorial import ConsultaHistorialDialog
from FormularioHistorial import FormularioHistorialDialog

# Ruta del archivo JSON
JSON_FILE_PATH = 'D:/SistemaVet/Jsons/Jsons historiales/historiales.json'

class HistorialMedicoFrame(wx.Frame):
    def __init__(self, parent):
        super(HistorialMedicoFrame, self).__init__(parent, title="Historial Médico", size=(800, 600))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Botones
        new_button = wx.Button(panel, label="Nuevo Historial", size=(150, 30))
        hbox_buttons.Add(new_button, 0, wx.ALL, 5)
        new_button.Bind(wx.EVT_BUTTON, self.on_new_historial)

        modify_button = wx.Button(panel, label="Modificar Historial", size=(150, 30))
        hbox_buttons.Add(modify_button, 0, wx.ALL, 5)
        modify_button.Bind(wx.EVT_BUTTON, self.on_modify_historial)

        delete_button = wx.Button(panel, label="Eliminar Historial", size=(150, 30))
        hbox_buttons.Add(delete_button, 0, wx.ALL, 5)
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete_historial)

        vbox.Add(hbox_buttons, 0, wx.ALL | wx.LEFT, 10)

        # Campo de búsqueda y filtros
        hbox_search = wx.BoxSizer(wx.HORIZONTAL)
        lblFiltro = wx.StaticText(panel, label="Filtrado :")
        self.txtFiltro = wx.TextCtrl(panel)
        self.txtFiltro.Bind(wx.EVT_TEXT, self.OnFiltrar)
        hbox_search.Add(lblFiltro, flag=wx.RIGHT, border=8)
        hbox_search.Add(self.txtFiltro, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox_search, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox_filters = wx.BoxSizer(wx.HORIZONTAL)
        lblEspecie = wx.StaticText(panel, label="Especie:")
        self.choice_especie = wx.Choice(panel, choices=["Perro", "Gato"])
        self.choice_especie.Bind(wx.EVT_CHOICE, self.OnFiltrar)
        hbox_filters.Add(lblEspecie, flag=wx.RIGHT, border=8)
        hbox_filters.Add(self.choice_especie, proportion=1)

        lblSexo = wx.StaticText(panel, label="Sexo:")
        self.choice_sexo = wx.Choice(panel, choices=["Macho", "Hembra"])
        self.choice_sexo.Bind(wx.EVT_CHOICE, self.OnFiltrar)
        hbox_filters.Add(lblSexo, flag=wx.RIGHT, border=8)
        hbox_filters.Add(self.choice_sexo, proportion=1)

        clear_filters_button = wx.Button(panel, label="Eliminar Filtros")
        clear_filters_button.Bind(wx.EVT_BUTTON, self.OnClearFilters)
        hbox_filters.Add(clear_filters_button, 0, wx.ALL, 5)
        
        vbox.Add(hbox_filters, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Tabla para mostrar los historiales
        self.historial_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.historial_list.InsertColumn(0, "ID", width=60)
        self.historial_list.InsertColumn(1, "Nombre", width=120)
        self.historial_list.InsertColumn(2, "Especie", width=80)
        self.historial_list.InsertColumn(3, "Raza", width=80)
        self.historial_list.InsertColumn(4, "Edad", width=60)
        self.historial_list.InsertColumn(5, "Sexo", width=80)
        self.historial_list.InsertColumn(6, "Peso", width=80)
        self.historial_list.InsertColumn(7, "Propietario", width=120)
        self.historial_list.InsertColumn(8, "Teléfono", width=100)
        self.historial_list.InsertColumn(9, "Dirección", width=150)
        self.historial_list.InsertColumn(10, "Descripción", width=200)

        vbox.Add(self.historial_list, 1, wx.ALL | wx.EXPAND, 10)

        panel.SetSizer(vbox)

        self.datos_historial = []
        self.next_id = 1  # ID inicial para nuevos historiales

        self.historial_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_double_click)

        self.load_all_data()

    def on_new_historial(self, event):
        with FormularioHistorialDialog(self) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                data = dialog.get_data()
                if 'id' not in data or not data['id']:
                    data['id'] = str(self.next_id)
                    self.next_id += 1
                self.save_historial(data)
                self.add_historial_to_list(data)

    def on_modify_historial(self, event):
        selected_item = self.historial_list.GetFirstSelected()
        if selected_item != -1:
            historial_id = self.historial_list.GetItemText(selected_item, 0)
            data = self.get_historial_data(historial_id)
            if data:
                dialog = FormularioHistorialDialog(self, data=data)
                if dialog.ShowModal() == wx.ID_OK:
                    updated_data = dialog.get_data()
                    self.update_historial(updated_data)
                    self.refresh_historial_list()
                dialog.Destroy()
            else:
                wx.MessageBox("No se encontró el historial.", "Error", wx.OK | wx.ICON_ERROR)

    def on_delete_historial(self, event):
        selected_item = self.historial_list.GetFirstSelected()
        if selected_item != -1:
            historial_id = self.historial_list.GetItemText(selected_item, 0)
            confirm = wx.MessageBox(
                f"¿Estás seguro de eliminar el historial con ID '{historial_id}'?",
                "Confirmación de eliminación",
                wx.YES_NO | wx.ICON_WARNING
            )
            if confirm == wx.YES:
                # Eliminar el historial de la lista y de los datos
                self.historial_list.DeleteItem(selected_item)
                self.datos_historial = [historial for historial in self.datos_historial if historial['id'] != historial_id]
                self.reorder_ids()  # Reordenar los IDs
                self.save_all_data()
                # Actualizar la vista
                self.refresh_historial_list()
                self.update_next_id()

    def OnClearFilters(self, event):
        self.txtFiltro.SetValue("")
        self.choice_especie.SetSelection(wx.NOT_FOUND)
        self.choice_sexo.SetSelection(wx.NOT_FOUND)
        self.OnFiltrar(None)

    def OnFiltrar(self, event):
        filtro_nombre = self.txtFiltro.GetValue().lower()
        especie = self.choice_especie.GetStringSelection()
        sexo = self.choice_sexo.GetStringSelection()

        self.historial_list.DeleteAllItems()

        for data in self.datos_historial:
            if (filtro_nombre in data['nombre'].lower() or filtro_nombre == "") and \
               (especie == "" or data['especie'] == especie) and \
               (sexo == "" or data['sexo'] == sexo):
                self.add_historial_to_list(data)

    #Método para cargar los datos a la ventana de consulta
    def on_item_double_click(self, event):
        selected_item = event.GetIndex()
        historial_id = self.historial_list.GetItemText(selected_item, 0)
        data = self.get_historial_data(historial_id)
        
        if data:
            dialog = ConsultaHistorialDialog(self, data=data)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            wx.MessageBox("No se encontró el historial.", "Error", wx.OK | wx.ICON_ERROR)

    def add_historial_to_list(self, data):
        index = self.historial_list.InsertItem(self.historial_list.GetItemCount(), data['id'])
        self.historial_list.SetItem(index, 1, data['nombre'])
        self.historial_list.SetItem(index, 2, data['especie'])
        self.historial_list.SetItem(index, 3, data['raza'])
        self.historial_list.SetItem(index, 4, data['edad'])
        self.historial_list.SetItem(index, 5, data['sexo'])
        self.historial_list.SetItem(index, 6, data['peso'])
        self.historial_list.SetItem(index, 7, data['propietario'])
        self.historial_list.SetItem(index, 8, data['telefono'])
        self.historial_list.SetItem(index, 9, data['direccion'])
        self.historial_list.SetItem(index, 10, data['descripcion'])

    def get_historial_data(self, historial_id):
        for data in self.datos_historial:
            if data['id'] == historial_id:
                return data
        return None

    def update_historial(self, updated_data):
        for index, data in enumerate(self.datos_historial):
            if data['id'] == updated_data['id']:
                self.datos_historial[index] = updated_data
                self.save_all_data()
                break

    def reorder_ids(self):
        """Reordena los IDs de los historiales para llenar huecos."""
        # Primero, obtenemos todos los IDs actuales y los ordenamos
        sorted_historiales = sorted(self.datos_historial, key=lambda x: int(x['id']))
        # Luego, actualizamos los IDs
        for i, historial in enumerate(sorted_historiales):
            historial['id'] = str(i + 1)
        self.datos_historial = sorted_historiales

    def refresh_historial_list(self):
        self.historial_list.DeleteAllItems()
        for data in self.datos_historial:
            self.add_historial_to_list(data)

    def save_historial(self, historial_data):
        self.datos_historial.append(historial_data)
        self.save_all_data()

    def save_all_data(self):
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump(self.datos_historial, f, indent=4)

    def load_all_data(self):
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as f:
                try:
                    self.datos_historial = json.load(f)
                except json.JSONDecodeError:
                    self.datos_historial = []
        else:
            self.datos_historial = []

        self.refresh_historial_list()
        self.update_next_id()

    def update_next_id(self):
        if self.datos_historial:
            ids = [int(historial['id']) for historial in self.datos_historial if historial['id'].isdigit()]
            # Generamos el siguiente ID disponible
            self.next_id = 1
            while str(self.next_id) in [historial['id'] for historial in self.datos_historial]:
                self.next_id += 1
        else:
            self.next_id = 1

if __name__ == "__main__":
    app = wx.App()
    frame = HistorialMedicoFrame(None)
    frame.Show()
    app.MainLoop()

