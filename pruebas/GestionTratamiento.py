import wx
import wx.grid as gridlib

class ModuloTratamientoDialog(wx.Dialog):
    def __init__(self, parent):
        super(ModuloTratamientoDialog, self).__init__(parent, title="Módulo de Tratamiento", size=(1000, 600))
        
        panel = wx.Panel(self)
        main_vbox = wx.BoxSizer(wx.VERTICAL)
        
        title = wx.StaticText(panel, label="Gestión de Tratamientos")
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        title.SetFont(font)
        main_vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        
        # Panel superior con filtros y botones
        top_panel = wx.Panel(panel)
        top_hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        search_label = wx.StaticText(top_panel, label="Buscar:")
        self.search_ctrl = wx.TextCtrl(top_panel)
        
        filter_label = wx.StaticText(top_panel, label="Filtrar por estado:")
        self.filter_ctrl = wx.ComboBox(top_panel, choices=["Todos", "En Proceso", "Completado"], style=wx.CB_READONLY)
        
        top_hbox.Add(search_label, flag=wx.RIGHT, border=8)
        top_hbox.Add(self.search_ctrl, proportion=1, flag=wx.RIGHT, border=8)
        top_hbox.Add(filter_label, flag=wx.RIGHT, border=8)
        top_hbox.Add(self.filter_ctrl, flag=wx.RIGHT, border=8)
        
        top_panel.SetSizer(top_hbox)
        main_vbox.Add(top_panel, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Tabla principal
        self.tratamiento_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.tratamiento_list.InsertColumn(0, 'ID', width=50)
        self.tratamiento_list.InsertColumn(1, 'Paciente', width=100)
        self.tratamiento_list.InsertColumn(2, 'Propietario', width=100)
        self.tratamiento_list.InsertColumn(3, 'Tipo de Tratamiento', width=130)
        self.tratamiento_list.InsertColumn(4, 'Fecha de Inicio', width=100)
        self.tratamiento_list.InsertColumn(5, 'Fecha de Fin', width=100)
        self.tratamiento_list.InsertColumn(6, 'Veterinario Responsable', width=150)
        self.tratamiento_list.InsertColumn(7, 'Estado del Tratamiento', width=130)
        self.tratamiento_list.InsertColumn(8, 'Observaciones', width=200)
        
        main_vbox.Add(self.tratamiento_list, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        # Botones de acción
        buttons_hbox = wx.BoxSizer(wx.HORIZONTAL)
        add_button = wx.Button(panel, label="Añadir Tratamiento")
        delete_button = wx.Button(panel, label="Eliminar Tratamiento")
        edit_button = wx.Button(panel, label="Editar Tratamiento")
        
        buttons_hbox.Add(add_button, flag=wx.RIGHT, border=10)
        buttons_hbox.Add(delete_button, flag=wx.RIGHT, border=10)
        buttons_hbox.Add(edit_button, flag=wx.RIGHT, border=10)
        
        main_vbox.Add(buttons_hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        
        panel.SetSizer(main_vbox)
        
        # Bind buttons
        add_button.Bind(wx.EVT_BUTTON, self.on_add_tratamiento)
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete_tratamiento)
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit_tratamiento)

    def on_add_tratamiento(self, event):
        dialog = DetallesTratamientoDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.get_data()
            index = self.tratamiento_list.InsertItem(self.tratamiento_list.GetItemCount(), str(data['id']))
            self.tratamiento_list.SetItem(index, 1, data['paciente'])
            self.tratamiento_list.SetItem(index, 2, data['propietario'])
            self.tratamiento_list.SetItem(index, 3, data['tipo_tratamiento'])
            self.tratamiento_list.SetItem(index, 4, data['fecha_inicio'])
            self.tratamiento_list.SetItem(index, 5, data['fecha_fin'])
            self.tratamiento_list.SetItem(index, 6, data['veterinario_responsable'])
            self.tratamiento_list.SetItem(index, 7, data['estado_tratamiento'])
            self.tratamiento_list.SetItem(index, 8, data['observaciones'])
        dialog.Destroy()

    def on_delete_tratamiento(self, event):
        selected_item = self.tratamiento_list.GetFirstSelected()
        if selected_item != -1:
            self.tratamiento_list.DeleteItem(selected_item)

    def on_edit_tratamiento(self, event):
        selected_item = self.tratamiento_list.GetFirstSelected()
        if selected_item != -1:
            data = {
                'id': self.tratamiento_list.GetItemText(selected_item, 0),
                'paciente': self.tratamiento_list.GetItemText(selected_item, 1),
                'propietario': self.tratamiento_list.GetItemText(selected_item, 2),
                'tipo_tratamiento': self.tratamiento_list.GetItemText(selected_item, 3),
                'fecha_inicio': self.tratamiento_list.GetItemText(selected_item, 4),
                'fecha_fin': self.tratamiento_list.GetItemText(selected_item, 5),
                'veterinario_responsable': self.tratamiento_list.GetItemText(selected_item, 6),
                'estado_tratamiento': self.tratamiento_list.GetItemText(selected_item, 7),
                'observaciones': self.tratamiento_list.GetItemText(selected_item, 8)
            }
            dialog = DetallesTratamientoDialog(self, data)
            if dialog.ShowModal() == wx.ID_OK:
                updated_data = dialog.get_data()
                self.tratamiento_list.SetItem(selected_item, 1, updated_data['paciente'])
                self.tratamiento_list.SetItem(selected_item, 2, updated_data['propietario'])
                self.tratamiento_list.SetItem(selected_item, 3, updated_data['tipo_tratamiento'])
                self.tratamiento_list.SetItem(selected_item, 4, updated_data['fecha_inicio'])
                self.tratamiento_list.SetItem(selected_item, 5, updated_data['fecha_fin'])
                self.tratamiento_list.SetItem(selected_item, 6, updated_data['veterinario_responsable'])
                self.tratamiento_list.SetItem(selected_item, 7, updated_data['estado_tratamiento'])
                self.tratamiento_list.SetItem(selected_item, 8, updated_data['observaciones'])
            dialog.Destroy()

class DetallesTratamientoDialog(wx.Dialog):
    def __init__(self, parent, data=None):
        super(DetallesTratamientoDialog, self).__init__(parent, title="Detalles del Tratamiento", size=(400, 400))
        
        self.data = data if data else {}
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Formulario de detalles del tratamiento
        fields = [
            ('Paciente', 'paciente'),
            ('Propietario', 'propietario'),
            ('Tipo de Tratamiento', 'tipo_tratamiento'),
            ('Fecha de Inicio', 'fecha_inicio'),
            ('Fecha de Fin', 'fecha_fin'),
            ('Veterinario Responsable', 'veterinario_responsable'),
            ('Estado del Tratamiento', 'estado_tratamiento'),
            ('Observaciones', 'observaciones')
        ]
        self.controls = {}
        
        for label_text, field_name in fields:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(panel, label=label_text, size=(130, -1))
            hbox.Add(label, flag=wx.RIGHT, border=8)
            text_ctrl = wx.TextCtrl(panel)
            hbox.Add(text_ctrl, proportion=1)
            vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=5)
            self.controls[field_name] = text_ctrl

        # Botones de acción
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(panel, label="Guardar")
        cancel_button = wx.Button(panel, label="Cancelar")
        
        hbox.Add(save_button, flag=wx.RIGHT, border=10)
        hbox.Add(cancel_button)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

        # Bind buttons
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.load_data()

    def load_data(self):
        if self.data:
            for key, control in self.controls.items():
                control.SetValue(self.data.get(key, ''))

    def get_data(self):
        return {key: control.GetValue() for key, control in self.controls.items()}

    def on_save(self, event):
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

class MyApp(wx.App):
    def OnInit(self):
        dialog = ModuloTratamientoDialog(None)
        dialog.ShowModal()
        dialog.Destroy()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
