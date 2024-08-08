import wx
import os
import json

class FormularioHistorialDialog(wx.Dialog):
    def __init__(self, parent, data=None):
        super(FormularioHistorialDialog, self).__init__(parent, title="Formulario de Historial Médico", size=(580, 600))

        # Inicializar el atributo image_path
        self.image_path = None

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox_main = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = wx.Panel(panel)
        left_vbox = wx.BoxSizer(wx.VERTICAL)

        # Definir campos del formulario
        form_sizer = wx.FlexGridSizer(10, 2, 10, 10)

        # Campos de texto pequeños
        form_sizer.Add(wx.StaticText(left_panel, label="Nombre:"), flag=wx.ALIGN_RIGHT)
        self.nombre_text = wx.TextCtrl(left_panel, size=(120, -1))
        form_sizer.Add(self.nombre_text)

        form_sizer.Add(wx.StaticText(left_panel, label="Especie:"), flag=wx.ALIGN_RIGHT)
        self.especie_radio_box = wx.RadioBox(left_panel, choices=["Perro", "Gato", "Otro"], style=wx.RA_HORIZONTAL, size=(200, -1))
        form_sizer.Add(self.especie_radio_box, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Raza:"), flag=wx.ALIGN_RIGHT)
        self.raza_text = wx.TextCtrl(left_panel, size=(120, -1))
        form_sizer.Add(self.raza_text)

        form_sizer.Add(wx.StaticText(left_panel, label="Edad:"), flag=wx.ALIGN_RIGHT)
        self.edad_text = wx.TextCtrl(left_panel, size=(120, -1))
        form_sizer.Add(self.edad_text)

        form_sizer.Add(wx.StaticText(left_panel, label="Sexo:"), flag=wx.ALIGN_RIGHT)
        self.sexo_radio_box = wx.RadioBox(left_panel, choices=["Macho", "Hembra"], style=wx.RA_HORIZONTAL, size=(200, -1))
        form_sizer.Add(self.sexo_radio_box, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Peso:"), flag=wx.ALIGN_RIGHT)
        self.peso_text = wx.TextCtrl(left_panel, size=(120, -1))
        form_sizer.Add(self.peso_text)

        form_sizer.Add(wx.StaticText(left_panel, label="Propietario:"), flag=wx.ALIGN_RIGHT)
        self.propietario_text = wx.TextCtrl(left_panel, size=(120, -1))
        form_sizer.Add(self.propietario_text)

        form_sizer.Add(wx.StaticText(left_panel, label="Teléfono:"), flag=wx.ALIGN_RIGHT)
        self.telefono_text = wx.TextCtrl(left_panel, size=(120, -1))
        form_sizer.Add(self.telefono_text)

        # Campos de texto grandes
        form_sizer.Add(wx.StaticText(left_panel, label="Dirección:"), flag=wx.ALIGN_RIGHT)
        self.direccion_text = wx.TextCtrl(left_panel, style=wx.TE_MULTILINE, size=(180, 60))
        form_sizer.Add(self.direccion_text, flag=wx.EXPAND)

        form_sizer.Add(wx.StaticText(left_panel, label="Descripción:"), flag=wx.ALIGN_RIGHT)
        self.descripcion_text = wx.TextCtrl(left_panel, style=wx.TE_MULTILINE, size=(180, 100))
        form_sizer.Add(self.descripcion_text, flag=wx.EXPAND)

        left_vbox.Add(form_sizer, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # Botones OK y Cancelar
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(left_panel, id=wx.ID_OK, label="Aceptar")
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)

        cancel_button = wx.Button(left_panel, id=wx.ID_CANCEL, label="Cancelar")
        hbox_buttons.Add(ok_button, 0, wx.ALL, 5)
        hbox_buttons.Add(cancel_button, 0, wx.ALL, 5)
        left_vbox.Add(hbox_buttons, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        left_panel.SetSizer(left_vbox)

        # Panel derecho para la imagen y los botones de agregar y eliminar
        right_panel = wx.Panel(panel)
        right_vbox = wx.BoxSizer(wx.VERTICAL)

        # Panel para el cuadro de previsualización de la imagen
        image_panel = wx.Panel(right_panel, size=(200, 200))
        image_panel.SetBackgroundColour(wx.Colour(220, 220, 220))

        self.image_preview = wx.StaticBitmap(image_panel, size=(200, 200))
        self.image_preview.SetBackgroundColour(wx.Colour(190, 190, 190))

        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_sizer.Add(self.image_preview, 1, wx.EXPAND | wx.ALL, 0)
        image_panel.SetSizer(image_sizer)

        right_vbox.Add(image_panel, 0, wx.EXPAND | wx.ALL, 10)

        hbox_photo_buttons = wx.BoxSizer(wx.HORIZONTAL)

        add_photo_button = wx.Button(right_panel, label="Agregar Foto")
        add_photo_button.Bind(wx.EVT_BUTTON, self.on_add_photo)
        hbox_photo_buttons.Add(add_photo_button, 0, wx.ALL, 5)

        delete_photo_button = wx.Button(right_panel, label="Eliminar Foto")
        delete_photo_button.Bind(wx.EVT_BUTTON, self.on_delete_photo)
        hbox_photo_buttons.Add(delete_photo_button, 0, wx.ALL, 5)

        right_vbox.Add(hbox_photo_buttons, 0, wx.ALL | wx.CENTER, 10)

        right_panel.SetSizer(right_vbox)

        hbox_main.Add(left_panel, 2, wx.EXPAND | wx.ALL, 10)
        hbox_main.Add(right_panel, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(hbox_main, 1, wx.EXPAND)

        panel.SetSizer(vbox)

        # Cargar datos si se proporcionaron
        if data:
            self.load_data(data)

    def on_ok(self, event):
        if self.validate_data():
            # Aquí va el código para procesar los datos si la validación es exitosa
            self.EndModal(wx.ID_OK)
        # Si la validación falla, no hacemos nada, así el formulario permanece abierto


    def on_add_photo(self, event):
        with wx.FileDialog(self, "Seleccionar imagen", wildcard="Imagenes (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            self.image_path = file_dialog.GetPath().replace("\\", "/")  # Reemplazar las barras invertidas por barras normales
            self.load_image(self.image_path)

    def on_delete_photo(self, event):
        self.image_path = None
        self.image_preview.SetBitmap(wx.NullBitmap)
        self.Refresh()
        self.update_json_image_path()

    def load_image(self, path):
        try:
            if path and os.path.isfile(path):
                image = wx.Image(path, wx.BITMAP_TYPE_ANY)
                if image.IsOk():
                    image = image.Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
                    bitmap = wx.Bitmap(image)
                    self.image_preview.SetBitmap(bitmap)
                    self.Refresh()
                else:
                    print("La imagen no se cargó correctamente.")
            else:
                print(f"Archivo no encontrado: {path}")
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def update_json_image_path(self):
        # Asumiendo que el JSON está en un archivo llamado 'data.json'
        json_file_path = 'data.json'
        if not os.path.exists(json_file_path):
            return
        
        with open(json_file_path, 'r') as file:
            data_list = json.load(file)
        
        # Encuentra el registro correspondiente y elimina la ruta de la imagen
        for record in data_list:
            if record.get("id") == self.id:
                record["imagen"] = None
                break
        
        with open(json_file_path, 'w') as file:
            json.dump(data_list, file, indent=4)

    def get_data(self):
        if not self.validate_data():
            return None
        
        imagen_path = self.image_path.replace("\\", "/") if self.image_path else None
        return {
            "id": getattr(self, 'id', None),
            "nombre": self.nombre_text.GetValue(),
            "especie": self.especie_radio_box.GetStringSelection(),
            "raza": self.raza_text.GetValue(),
            "edad": self.edad_text.GetValue(),
            "sexo": self.sexo_radio_box.GetStringSelection(),
            "peso": self.peso_text.GetValue(),
            "propietario": self.propietario_text.GetValue(),
            "telefono": self.telefono_text.GetValue(),
            "direccion": self.direccion_text.GetValue(),
            "descripcion": self.descripcion_text.GetValue(),
            "imagen": imagen_path  # Devolver la ruta de la imagen con barras normales
        }

    def load_data(self, data):
        self.nombre_text.SetValue(data.get("nombre", ""))
        self.especie_radio_box.SetStringSelection(data.get("especie", ""))
        self.raza_text.SetValue(data.get("raza", ""))
        self.edad_text.SetValue(data.get("edad", ""))
        self.sexo_radio_box.SetStringSelection(data.get("sexo", ""))
        self.peso_text.SetValue(data.get("peso", ""))
        self.propietario_text.SetValue(data.get("propietario", ""))
        self.telefono_text.SetValue(data.get("telefono", ""))
        self.direccion_text.SetValue(data.get("direccion", ""))
        self.descripcion_text.SetValue(data.get("descripcion", ""))
        self.id = data.get("id", None)

        # Cargar la imagen si existe
        self.image_path = data.get("imagen")
        if self.image_path:
            self.load_image(self.image_path)
            
    def validate_data(self):
        """ Valida que todos los campos estén completos y que los datos de edad y peso sean válidos. """
        # Lista para almacenar mensajes de error
        error_messages = []

        # Verificar que todos los campos de texto estén completos
        for field, label in [
            (self.nombre_text, "Nombre"),
            (self.raza_text, "Raza"),
            (self.propietario_text, "Propietario"),
            (self.telefono_text, "Teléfono"),
            (self.direccion_text, "Dirección"),
            (self.descripcion_text, "Descripción")
        ]:
            if not field.GetValue().strip():
                error_messages.append(f"El campo '{label}' no puede estar vacío.")

        # Validar Edad
        edad = self.edad_text.GetValue().strip()
        if not edad:
            error_messages.append("El campo de edad no puede estar vacío.")
        else:
            try:
                edad = int(edad)
                if edad < 0:
                    error_messages.append("La edad debe ser un número entero positivo.")
            except ValueError:
                error_messages.append("La edad debe ser un número entero válido.")

        # Validar Peso
        peso = self.peso_text.GetValue().strip()
        if not peso:
            error_messages.append("El campo de peso no puede estar vacío.")
        else:
            try:
                peso = float(peso)
                if peso < 0:
                    error_messages.append("El peso debe ser un número decimal positivo.")
            except ValueError:
                error_messages.append("El peso debe ser un número decimal válido.")

        # Mostrar mensajes de error si hay alguno
        if error_messages:
            wx.MessageBox("\n".join(error_messages), "Error", wx.OK | wx.ICON_ERROR)
            return False

        return True


    

