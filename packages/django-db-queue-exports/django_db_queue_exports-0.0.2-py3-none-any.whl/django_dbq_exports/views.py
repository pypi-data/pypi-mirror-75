from rest_framework import generics

from django_dbq_exports.models import Export
from django_dbq_exports.serializers import ExportSerializer


class DBQExportListCreateView(generics.ListCreateAPIView):
    """
    List all exports.
    Creates new export and automatically triggers a dbq job.
    """

    serializer_class = ExportSerializer
    queryset = Export.objects.all()
    # TODO: Add suport for custom permissions


class DBQRetrieveView(generics.RetrieveAPIView):
    """
    Retreive a single export - filterable by id.
    """

    serializer_class = ExportSerializer
    queryset = Export.objects.all()
    # TODO: Add suport for custom permissions
