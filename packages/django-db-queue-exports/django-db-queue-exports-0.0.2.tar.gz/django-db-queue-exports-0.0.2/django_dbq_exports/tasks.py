from django.utils import timezone
from django.conf import settings
from django.utils.module_loading import import_string
import logging

from .models import Export

logger = logging.getLogger(__name__)


def export_task(job):
    workspace = job.workspace
    export = Export.objects.get(pk=workspace.get("export_id"))
    requested_export_function = settings.EXPORTS[export.export_type]

    try:
        export_function = import_string(requested_export_function)
    except ImportError as e:
        logger.exception(
            f"Export id={export.id} of type {export.export_type} import failed.\n"
        )
        export.update_status(Export.STATUS.FAILED, "Export function import failed.")
        raise

    export.started = timezone.now()
    export.save()

    output = None
    export.update_status(Export.STATUS.RUNNING)
    try:
        output = export_function(export.export_params)
    except Exception:
        logger.exception(
            f"Export id={export.id} of type {export.export_type} execution failed.\n"
        )
        export.update_status(
            Export.STATUS.FAILED,
            "Export function execution failed. See log for details.",
        )
        raise

    export.update_status(Export.STATUS.COMPLETE)
    export.completed = timezone.now()
    export.save()
    if output:
        export.result_reference = output
        export.save()
