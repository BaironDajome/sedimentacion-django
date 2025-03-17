from django.contrib.gis.db import models

class ShapefileData(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to="shapefiles/")
    geom = models.GeometryField()  # Guarda la geometría
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

