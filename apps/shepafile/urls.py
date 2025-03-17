from django.urls import path
from .views import UploadShapefileView, ListShapefilesView

urlpatterns = [
    path("upload/", UploadShapefileView.as_view(), name="upload_shapefile"),
    path("list/", ListShapefilesView.as_view(), name="list_shapefiles"),
]
