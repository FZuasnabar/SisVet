import wx
import wx.grid as gridlib

class SesionTratamientoDialog(wx.Dialog):
    def __init__(self, parent):
        super(SesionTratamientoDialog, self).__init__(parent, title="Sesión de Tratamiento", size=(400, 400))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Lista de Medicamentos
        self.medicamento_list = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.medicamento_list.InsertColumn(0, 'Medicamento', width=140)
        self.medicamento_list.InsertColumn(1, 'Precio', width=100)

        vbox.Add(self.medicamento_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Campos para añadir medicamentos
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(panel, label="Medicamento:"), flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        self.medicamento_text = wx.TextCtrl(panel)
        hbox.Add(self.medicamento_text, proportion=1, flag=wx.RIGHT, border=5)
        
        hbox.Add(wx.StaticText(panel, label="Precio:"), flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        self.precio_text = wx.TextCtrl(panel)
        hbox.Add(self.precio_text, proportion=1)
        
        vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # Botón para añadir medicamentos
        add_button = wx.Button(panel, label="Añadir Medicamento")
        add_button.Bind(wx.EVT_BUTTON, self.on_add_medicamento)
        vbox.Add(add_button, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        # Botones de acción
        botonera = wx.BoxSizer(wx.HORIZONTAL)
        guardar_btn = wx.Button(panel, label="Guardar")
        cancelar_btn = wx.Button(panel, label="Cancelar")
        botonera.Add(guardar_btn, flag=wx.RIGHT, border=10)
        botonera.Add(cancelar_btn)
        vbox.Add(botonera, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Bind buttons
        guardar_btn.Bind(wx.EVT_BUTTON, self.on_save)
        cancelar_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_add_medicamento(self, event):
        medicamento = self.medicamento_text.GetValue().strip()
        precio = self.precio_text.GetValue().strip()
        if medicamento and precio:
            try:
                precio = float(precio)
                index = self.medicamento_list.InsertItem(self.medicamento_list.GetItemCount(), medicamento)
                self.medicamento_list.SetItem(index, 1, f"{precio:.2f}")
                self.medicamento_text.SetValue("")
                self.precio_text.SetValue("")
            except ValueError:
                wx.MessageBox("El precio debe ser un número válido.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Debe ingresar tanto el medicamento como el precio.", "Error", wx.OK | wx.ICON_ERROR)

    def on_save(self, event):
        # Calcular el costo total
        total_cost = 0
        for i in range(self.medicamento_list.GetItemCount()):
            total_cost += float(self.medicamento_list.GetItemText(i, 1))
        
        wx.MessageBox(f"Total del costo de los medicamentos: {total_cost:.2f}", "Información", wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

class ModuloTratamientoDialog(wx.Dialog):
    def __init__(self, parent):
        super(ModuloTratamientoDialog, self).__init__(parent, title="Módulo de Tratamiento", size=(800, 600))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Información General
        info_box = wx.BoxSizer(wx.HORIZONTAL)
        info_box.Add(wx.StaticText(panel, label="Tratamiento de: [Nombre de la Mascota]"), flag=wx.ALL, border=10)
        vbox.Add(info_box, flag=wx.EXPAND)

        # Detalles del Tratamiento
        detalles_box = wx.BoxSizer(wx.VERTICAL)
        detalles_box.Add(wx.StaticText(panel, label="Tipo de Tratamiento:"), flag=wx.LEFT | wx.TOP, border=10)
        self.tipo_tratamiento = wx.TextCtrl(panel)
        detalles_box.Add(self.tipo_tratamiento, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        detalles_box.Add(wx.StaticText(panel, label="Fechas Clave:"), flag=wx.LEFT | wx.TOP, border=10)
        fecha_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fecha_sizer.Add(wx.StaticText(panel, label="Inicio:"), flag=wx.RIGHT, border=10)
        self.fecha_inicio = wx.TextCtrl(panel)
        fecha_sizer.Add(self.fecha_inicio, flag=wx.RIGHT, border=10)
        fecha_sizer.Add(wx.StaticText(panel, label="Finalización:"), flag=wx.RIGHT, border=10)
        self.fecha_final = wx.TextCtrl(panel)
        fecha_sizer.Add(self.fecha_final)
        detalles_box.Add(fecha_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        vbox.Add(detalles_box, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # Sesiones de Tratamiento
        self.sesiones_list = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.sesiones_list.InsertColumn(0, 'Fecha', width=140)
        self.sesiones_list.InsertColumn(1, 'Tipo de Tratamiento', width=200)
        self.sesiones_list.InsertColumn(2, 'Costo Total', width=100)
        
        vbox.Add(self.sesiones_list, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)

        # Botones para añadir y eliminar sesiones
        sesion_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_sesion_btn = wx.Button(panel, label="Añadir Sesión")
        add_sesion_btn.Bind(wx.EVT_BUTTON, self.on_add_sesion)
        sesion_btn_sizer.Add(add_sesion_btn, flag=wx.RIGHT, border=10)
        
        del_sesion_btn = wx.Button(panel, label="Eliminar Sesión")
        del_sesion_btn.Bind(wx.EVT_BUTTON, self.on_del_sesion)
        sesion_btn_sizer.Add(del_sesion_btn)
        
        vbox.Add(sesion_btn_sizer, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        # Botones de Acción
        botonera = wx.BoxSizer(wx.HORIZONTAL)
        guardar_btn = wx.Button(panel, label="Guardar")
        cancelar_btn = wx.Button(panel, label="Cancelar")
        botonera.Add(guardar_btn, flag=wx.RIGHT, border=10)
        botonera.Add(cancelar_btn)
        vbox.Add(botonera, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Bind buttons
        guardar_btn.Bind(wx.EVT_BUTTON, self.on_save)
        cancelar_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_add_sesion(self, event):
        dialog = SesionTratamientoDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            fecha = "Fecha Actual"  # Aquí podrías poner un campo de fecha en el diálogo para ingresar la fecha
            tipo_tratamiento = self.tipo_tratamiento.GetValue()
            costo_total = dialog.get_total_cost()
            index = self.sesiones_list.InsertItem(self.sesiones_list.GetItemCount(), fecha)
            self.sesiones_list.SetItem(index, 1, tipo_tratamiento)
            self.sesiones_list.SetItem(index, 2, f"{costo_total:.2f}")
        dialog.Destroy()

    def on_del_sesion(self, event):
        selected_item = self.sesiones_list.GetFirstSelected()
        if selected_item != -1:
            self.sesiones_list.DeleteItem(selected_item)

    def on_save(self, event):
        wx.MessageBox("Datos del tratamiento guardados.", "Información", wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

# Ejecutar la aplicación wxPython para ver la ventana
app = wx.App(False)
dlg = ModuloTratamientoDialog(None)
dlg.ShowModal()
dlg.Destroy()
app.MainLoop()

