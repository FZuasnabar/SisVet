from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing, Line
import os
import wx
import json
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
        
        report_button = wx.Button(panel, label="Generar Informe", size=(150, 30))
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
                    # Validar los datos del formulario
                    if dialog.validate_data():
                        updated_data = dialog.get_data()
                        # Actualizar historial solo si los datos actualizados son válidos
                        if updated_data:
                            self.update_historial(updated_data)
                            self.refresh_historial_list()
                    dialog.Destroy()

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

    def on_item_double_click(self, event):
        selected_item = event.GetIndex()
        historial_id = self.historial_list.GetItemText(selected_item, 0)
        data = self.get_historial_data(historial_id)
        
        if data:
            dialog = ConsultaHistorialDialog(self, data=data)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            wx.MessageBox("No se encontró el historial seleccionado.", "Error", wx.OK | wx.ICON_ERROR)

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
        self.historial_list.SetItem(index, 10, data.get('descripcion', ''))

    def save_historial(self, historial_data):
        self.datos_historial.append(historial_data)
        self.save_all_data()


    def update_historial(self, updated_data):
        # Obtener el ID del historial actualizado
        historial_id = updated_data.get('id')

        # Comprobar si el ID está presente en los datos actualizados
        if not historial_id:
            return

        # Buscar el historial en la lista de datos
        historial = self.get_historial_data(historial_id)

        # Verificar si el historial fue encontrado
        if historial:
            # Actualizar el historial en la lista de datos
            for i, h in enumerate(self.datos_historial):
                if h['id'] == historial_id:
                    # Actualiza el historial con los datos proporcionados
                    self.datos_historial[i] = updated_data
                    self.save_all_data()
                    return

    def get_historial_data(self, historial_id):
        for historial in self.datos_historial:
            if historial['id'] == historial_id:
                return historial
        return None

    def save_all_data(self):
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(self.datos_historial, file, indent=4)

    def load_all_data(self):
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as file:
                self.datos_historial = json.load(file)
                self.update_next_id()
                self.refresh_historial_list()

    def refresh_historial_list(self):
        self.historial_list.DeleteAllItems()
        for data in self.datos_historial:
            self.add_historial_to_list(data)

    def reorder_ids(self):
        for i, historial in enumerate(self.datos_historial):
            historial['id'] = str(i + 1)

    def update_next_id(self):
        if self.datos_historial:
            self.next_id = max(int(historial['id']) for historial in self.datos_historial) + 1
        else:
            self.next_id = 1

    def on_generate_report(self, event):
        # Abrir un cuadro de diálogo para seleccionar la ubicación del archivo
        dialog = wx.FileDialog(self, "Guardar Informe como PDF", "", "", "Archivos PDF (*.pdf)|*.pdf", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_CANCEL:
            return  # El usuario canceló la acción
        
        file_path = dialog.GetPath()
        dialog.Destroy()

        # Obtener datos de la instancia seleccionada
        selected_item = self.historial_list.GetFirstSelected()
        if selected_item != -1:
            historial_id = self.historial_list.GetItemText(selected_item, 0)
            data = self.get_historial_data(historial_id)
            if data:
                self.create_pdf_report(data, file_path)
            else:
                wx.MessageBox("No se encontró el historial seleccionado.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Debe seleccionar un historial para generar el informe.", "Advertencia", wx.OK | wx.ICON_WARNING)

    def create_pdf_report(self, data, file_path):
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        width, height = letter

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            name='TitleStyle',
            fontName='Helvetica-Bold',
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.black
        )

        data_style = ParagraphStyle(
            name='DataStyle',
            fontName='Helvetica',
            fontSize=10,
            alignment=0,
            spaceAfter=10  # Espacio después de cada campo de datos
        )

        elements = []

        # Agregar título en mayúsculas con subrayado
        title_text = "Historial Médico".upper()
        title_paragraph = Paragraph(f"<u>{title_text}</u>", title_style)
        elements.append(title_paragraph)
        elements.append(Spacer(1, 12))

        data_lines = [
            ("Nombre:", data['nombre']),
            ("Especie:", data['especie']),
            ("Raza:", data['raza']),
            ("Edad:", data['edad']),
            ("Sexo:", data['sexo']),
            ("Peso:", data['peso']),
            ("Propietario:", data['propietario']),
            ("Teléfono:", data['telefono']),
            ("Dirección:", data['direccion'])
        ]

        max_label_length = max(len(label) for label, _ in data_lines)
        spacing = 10  # Espacio entre los campos de datos

        for label, value in data_lines:
            line = f"<b>{label}</b> {value.rjust(max_label_length + 2)}"
            elements.append(Paragraph(line, data_style))

        # Línea horizontal centralizada
        line_drawing = Drawing(width, 0.3 * inch)
        line_x_start = 0  # Margen desde el borde izquierdo
        line_x_end = width - 155  # Margen desde el borde derecho
        line_drawing.add(Line(line_x_start, 10, line_x_end, 10))  # Dibuja la línea horizontal
        elements.append(line_drawing)
        elements.append(Spacer(1, 6))

        # Descripción con espacio adicional
        description_label = Paragraph("<b>Descripción:</b>", data_style)
        elements.append(description_label)
        elements.append(Spacer(1, 6))  # Espacio entre la etiqueta y el texto de la descripción
        description = data.get('descripcion', 'No hay descripción')
        description_paragraph = Paragraph(description, data_style)
        elements.append(description_paragraph)

        image_path = data.get('imagen')
        if not image_path or not os.path.exists(image_path):
            image_path = 'D:/SistemaVet/FotosPerfil/imagen-no-disponible.png'
        
        image_width = 140
        image_height = 130
        x_position = width - image_width - 110
        y_position = height - image_height - 130

        elements.append(Spacer(1, 20))  # Espacio antes de la imagen

        doc.build(elements, onFirstPage=lambda c, d: self.add_image(c, image_path, image_width, image_height, x_position, y_position))

        wx.MessageBox(f"Informe PDF generado con éxito en {file_path}", "Información", wx.OK | wx.ICON_INFORMATION)

    def add_image(self, canvas, image_path, width, height, x, y):
        """Añade una imagen al canvas en la posición y tamaño especificado"""
        canvas.drawImage(image_path, x, y, width=width, height=height)



if __name__ == "__main__":
    app = wx.App()
    frame = HistorialMedicoFrame(None)
    frame.Show()
    app.MainLoop()
