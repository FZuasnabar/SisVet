import wx
from HistorialMedico import HistorialMedicoFrame

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        # Configuración de la ventana principal
        self.SetTitle("Sistema de Gestión Veterinaria")
        self.SetSize((1280, 720))  # Resolución inicial

        # Crear el toolbar
        toolbar = self.CreateToolBar(style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        toolbar.SetBackgroundColour(wx.Colour(220, 220, 220))  # Color gris claro

        # Tamaño de los iconos
        icon_size = (48, 48)

        # Añadir botones al toolbar con iconos con borde visual
        historial_bitmap = wx.Bitmap("D:/SistemaVet/Iconos/historial-medico.png", wx.BITMAP_TYPE_PNG).ConvertToImage().Scale(icon_size[0], icon_size[1]).ConvertToBitmap()
        historial_tool = toolbar.AddTool(wx.ID_ANY, "Historial Médico", historial_bitmap)

        citas_bitmap = wx.Bitmap("D:/SistemaVet/Iconos/gestion-citas.png", wx.BITMAP_TYPE_PNG).ConvertToImage().Scale(icon_size[0], icon_size[1]).ConvertToBitmap()
        citas_tool = toolbar.AddTool(wx.ID_ANY, "Gestión de Citas", citas_bitmap)

        toolbar.Realize()
        self.SetToolBar(toolbar)

        # Eventos para los botones del toolbar
        self.Bind(wx.EVT_TOOL, self.on_show_historial_medico, historial_tool)

    def on_show_historial_medico(self, event):
        frame = HistorialMedicoFrame(self)
        frame.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
