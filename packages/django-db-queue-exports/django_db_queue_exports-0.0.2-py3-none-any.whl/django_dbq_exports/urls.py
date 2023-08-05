from django.conf.urls import url
from django_dbq_exports.views import DBQExportListCreateView, DBQRetrieveView

app_name = "dbq_export"

urlpatterns = [
    url(r"^$", DBQExportListCreateView.as_view(), name="dbq-export-list-create"),
    url(
        r"^(?P<pk>[a-f0-9-]+)/$", DBQRetrieveView.as_view(), name="dbq-export-retreive"
    ),
]
