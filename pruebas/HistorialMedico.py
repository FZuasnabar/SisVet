import wx
from FormularioHistorial import FormularioHistorialDialog
from ConsultaHistorial import ConsultaHistorialDialog

class HistorialMedicoFrame(wx.Frame):
    def __init__(self, parent):
        super(HistorialMedicoFrame, self).__init__(parent, title="Historial Médico", size=(800, 600))

        panel = wx.Panel(self)

        # Layout vertical principal
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Layout horizontal para botones
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Botón para crear nuevo historial
        new_button = wx.Button(panel, label="Nuevo Historial", size=(150, 30))
        hbox_buttons.Add(new_button, 0, wx.ALL, 5)
        new_button.Bind(wx.EVT_BUTTON, self.on_new_historial)

        # Botón para modificar historial
        modify_button = wx.Button(panel, label="Modificar Historial", size=(150, 30))
        hbox_buttons.Add(modify_button, 0, wx.ALL, 5)
        modify_button.Bind(wx.EVT_BUTTON, self.on_modify_historial)

        # Botón para eliminar historial
        delete_button = wx.Button(panel, label="Eliminar Historial", size=(150, 30))
        hbox_buttons.Add(delete_button, 0, wx.ALL, 5)
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete_historial)

        vbox.Add(hbox_buttons, 0, wx.ALL | wx.LEFT, 10)

        # Campo de búsqueda
        hbox_search = wx.BoxSizer(wx.HORIZONTAL)
        lblFiltro = wx.StaticText(panel, label="Filtrado :")
        self.txtFiltro = wx.TextCtrl(panel)
        self.txtFiltro.Bind(wx.EVT_TEXT, self.OnFiltrar)
        hbox_search.Add(lblFiltro, flag=wx.RIGHT, border=8)
        hbox_search.Add(self.txtFiltro, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox_search, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Filtros de especie y sexo
        hbox_filters = wx.BoxSizer(wx.HORIZONTAL)
        
        # Filtro de especie
        lblEspecie = wx.StaticText(panel, label="Especie:")
        self.choice_especie = wx.Choice(panel, choices=["Perro", "Gato"])
        self.choice_especie.Bind(wx.EVT_CHOICE, self.OnFiltrar)
        hbox_filters.Add(lblEspecie, flag=wx.RIGHT, border=8)
        hbox_filters.Add(self.choice_especie, proportion=1)

        # Filtro de sexo
        lblSexo = wx.StaticText(panel, label="Sexo:")
        self.choice_sexo = wx.Choice(panel, choices=["Macho", "Hembra"])
        self.choice_sexo.Bind(wx.EVT_CHOICE, self.OnFiltrar)
        hbox_filters.Add(lblSexo, flag=wx.RIGHT, border=8)
        hbox_filters.Add(self.choice_sexo, proportion=1)
        
        # Botón para eliminar filtros
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

        # Bind double click event to show consultation dialog
        self.historial_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_double_click)

        # Cargar datos iniciales
        self.load_all_data()

    def on_new_historial(self, event):
        with FormularioHistorialDialog(self) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                data = dialog.get_data()
                if 'id' not in data or not data['id']:
                    data['id'] = str(self.next_id)  # Asignar ID único si no está presente
                    self.next_id += 1  # Incrementar el ID para el próximo historial
                self.add_historial_to_list(data)

    def on_modify_historial(self, event):
        selected_item = self.historial_list.GetFirstSelected()
        if selected_item != -1:
            data = {
                "id": self.historial_list.GetItemText(selected_item, 0),
                "nombre": self.historial_list.GetItemText(selected_item, 1),
                "especie": self.historial_list.GetItemText(selected_item, 2),
                "raza": self.historial_list.GetItemText(selected_item, 3),
                "edad": self.historial_list.GetItemText(selected_item, 4),
                "sexo": self.historial_list.GetItemText(selected_item, 5),
                "peso": self.historial_list.GetItemText(selected_item, 6),
                "propietario": self.historial_list.GetItemText(selected_item, 7),
                "telefono": self.historial_list.GetItemText(selected_item, 8),
                "direccion": self.historial_list.GetItemText(selected_item, 9),
                "descripcion": self.historial_list.GetItemText(selected_item, 10)
            }
            with FormularioHistorialDialog(self, data) as dialog:
                if dialog.ShowModal() == wx.ID_OK:
                    updated_data = dialog.get_data()
                    self.update_historial_in_list(selected_item, updated_data)

    def on_delete_historial(self, event):
        selected_item = self.historial_list.GetFirstSelected()
        if selected_item != -1:
            confirm = wx.MessageBox(
                f"¿Estás seguro de eliminar el historial con ID '{self.historial_list.GetItemText(selected_item, 0)}'?",
                "Confirmación de eliminación",
                wx.YES_NO | wx.ICON_WARNING
            )
            if confirm == wx.YES:
                # Eliminar el historial de la lista
                self.historial_list.DeleteItem(selected_item)
                
                # Eliminar el historial de los datos
                del self.datos_historial[selected_item]

                # Reordenar los IDs
                for i in range(selected_item, len(self.datos_historial)):
                    self.datos_historial[i]['id'] = i + 1
                
                # Volver a llenar la tabla con los IDs reordenados
                self.historial_list.DeleteAllItems()
                for data in self.datos_historial:
                    index = self.historial_list.InsertItem(self.historial_list.GetItemCount(), str(data['id']))
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

                # Ajustar el ID siguiente si es necesario
                self.next_id = len(self.datos_historial) + 1


    def OnClearFilters(self, event):
        # Restablecer los valores de los filtros
        self.txtFiltro.SetValue("")
        self.choice_especie.SetSelection(wx.NOT_FOUND)
        self.choice_sexo.SetSelection(wx.NOT_FOUND)
        
        # Aplicar el filtro con los valores vacíos para mostrar todos los historiales
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

    def on_item_double_click(self, event):
        selected_item = event.GetIndex()
        data = {
            "id": self.historial_list.GetItemText(selected_item, 0),
            "nombre": self.historial_list.GetItemText(selected_item, 1),
            "especie": self.historial_list.GetItemText(selected_item, 2),
            "raza": self.historial_list.GetItemText(selected_item, 3),
            "edad": self.historial_list.GetItemText(selected_item, 4),
            "sexo": self.historial_list.GetItemText(selected_item, 5),
            "peso": self.historial_list.GetItemText(selected_item, 6),
            "propietario": self.historial_list.GetItemText(selected_item, 7),
            "telefono": self.historial_list.GetItemText(selected_item, 8),
            "direccion": self.historial_list.GetItemText(selected_item, 9),
            "descripcion": self.historial_list.GetItemText(selected_item, 10)
        }
        with ConsultaHistorialDialog(self, data) as dialog:
            dialog.ShowModal()

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
        self.datos_historial.append(data)
        self.update_next_id()  # Ajustar el siguiente ID después de añadir

    def update_historial_in_list(self, index, data):
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
        self.datos_historial[index] = data

    def load_all_data(self):
        # Inicializa la lista como vacía
        self.datos_historial = []
        self.update_next_id()  # Ajustar el siguiente ID después de cargar los datos
        self.OnFiltrar(None)  # Aplicar filtros para actualizar la vista inicial

    def update_next_id(self):
        """Actualiza next_id basado en el máximo ID en datos_historial"""
        if self.datos_historial:
            max_id = max(int(historial['id']) for historial in self.datos_historial)
            self.next_id = max_id + 1
        else:
            self.next_id = 1

if __name__ == "__main__":
    app = wx.App(False)
    frame = HistorialMedicoFrame(None)
    frame.Show()
    app.MainLoop()
