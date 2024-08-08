from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import os
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

        report_button = wx.Button(panel, label="Generar Informe PDF", size=(150, 30))
        hbox_buttons.Add(report_button, 0, wx.ALL, 5)
        report_button.Bind(wx.EVT_BUTTON, self.on_generate_report)

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

    def on_generate_report(self, event):
        selected_item = self.historial_list.GetFirstSelected()
        if selected_item != -1:
            historial_id = self.historial_list.GetItemText(selected_item, 0)
            data = self.get_historial_data(historial_id)
            if data:
                # Abrir un cuadro de diálogo para seleccionar la ruta y el nombre del archivo PDF
                with wx.FileDialog(self, "Guardar Informe como PDF", wildcard="PDF files (*.pdf)|*.pdf",
                                   style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
                    if file_dialog.ShowModal() == wx.ID_CANCEL:
                        return  # El usuario canceló la operación

                    # Obtener el path del archivo seleccionado
                    file_path = file_dialog.GetPath()
                    self.create_pdf_report(data, file_path)
            else:
                wx.MessageBox("No se encontró el historial.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Seleccione un historial para generar el informe.", "Error", wx.OK | wx.ICON_ERROR)

    def create_pdf_report(self, data, file_path):
        # Configura el documento PDF
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        width, height = letter
        
        # Define el estilo de los párrafos
        styles = getSampleStyleSheet()
        
        # Prepara la lista de elementos para el documento
        elements = []
        
        # Añade el título
        elements.append(Paragraph("Informe del Historial Médico", styles['Title']))
        elements.append(Spacer(1, 12))
        
        # Espaciado ajustable entre los campos de datos
        spacing = 10  # Espacio entre los campos de datos (ajustable)
        
        # Añade los datos
        data_lines = [
            f"Nombre: {data['nombre']}",
            f"Especie: {data['especie']}",
            f"Raza: {data['raza']}",
            f"Edad: {data['edad']}",
            f"Sexo: {data['sexo']}",
            f"Peso: {data['peso']}",
            f"Propietario: {data['propietario']}",
            f"Teléfono: {data['telefono']}",
            f"Dirección: {data['direccion']}"
        ]
        
        for line in data_lines:
            elements.append(Paragraph(line, styles['Normal']))
            elements.append(Spacer(1, spacing))
        
        # Añade la descripción con ajuste de línea
        description = data.get('descripcion', 'No hay descripción')
        elements.append(Spacer(1, spacing))
        elements.append(Paragraph(f"Descripción: {description}", styles['Normal']))

        # Añade la imagen en la parte superior derecha
        image_path = data.get('imagen', 'default_image.png')  # Usa una imagen por defecto si no hay ruta
        image_width = 140  # Ancho deseado de la imagen en el PDF
        image_height = 130  # Alto deseado de la imagen en el PDF
        x_position = width - image_width - 110  # Posición X de la imagen en el PDF (80 unidades desde el borde derecho)
        y_position = height - image_height - 130  # Posición Y de la imagen en el PDF (120 unidades desde el borde superior)

        if os.path.exists(image_path):
            # Usar el método `drawImage` para añadir la imagen
            elements.append(Spacer(1, height - y_position - 60))  # Añade espacio antes de la imagen
            elements.append(Paragraph(" ", styles['Normal']))  # Añade un párrafo vacío para el espacio
            elements.append(Spacer(1, 10))
        else:
            elements.append(Paragraph("Imagen no disponible", styles['Normal']))
        
        # Construye el documento PDF
        doc.build(elements, onFirstPage=lambda c, d: self.add_image(c, image_path, image_width, image_height, x_position, y_position))
        
        wx.MessageBox(f"Informe PDF generado con éxito en {file_path}", "Información", wx.OK | wx.ICON_INFORMATION)

    def add_image(self, canvas, image_path, width, height, x, y):
        """Añade una imagen al canvas en la posición y tamaño especificado"""
        if os.path.exists(image_path):
            canvas.drawImage(image_path, x, y, width=width, height=height)


if __name__ == "__main__":
    app = wx.App()
    frame = HistorialMedicoFrame(None)
    frame.Show()
    app.MainLoop()
