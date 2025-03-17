import shapefile
import os
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import ShapefileData
from .serializers import ShapefileSerializer

class UploadShapefileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        archivo_shp = request.FILES.get("archivo")
        if not archivo_shp:
            return Response({"error": "Debe subir un archivo .shp"}, status=status.HTTP_400_BAD_REQUEST)

        # Guardar el archivo temporalmente
        ruta_archivo = f"shapefiles/temp_{archivo_shp.name}"
        with open(ruta_archivo, "wb+") as destino:
            for chunk in archivo_shp.chunks():
                destino.write(chunk)

        # Leer el archivo SHP
        try:
            sf = shapefile.Reader(ruta_archivo)
            for shape in sf.shapeRecords():
                # Convertir las coordenadas a un formato compatible con Django
                puntos = shape.shape.points
                if len(puntos) == 1:
                    geom = Point(puntos[0])
                else:
                    geom = MultiPolygon([Polygon(puntos)])

                shapefile_data = ShapefileData.objects.create(
                    nombre=archivo_shp.name,
                    archivo=archivo_shp,
                    geom=geom
                )
                shapefile_data.save()
            
            os.remove(ruta_archivo)  # Borrar archivo temporal
            return Response({"message": "Archivo cargado correctamente"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            os.remove(ruta_archivo)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListShapefilesView(APIView):
    def get(self, request):
        shapefiles = ShapefileData.objects.all()
        serializer = ShapefileSerializer(shapefiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

