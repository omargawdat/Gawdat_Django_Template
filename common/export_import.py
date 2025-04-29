from import_export.admin import ExportActionModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX
from unfold.contrib.import_export.forms import ExportForm
from unfold.contrib.import_export.forms import ImportForm
from unfold.contrib.import_export.forms import SelectableFieldsExportForm


class CustomImportExportMixin(ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

    def get_export_formats(self):
        return [XLSX]


class ExportSelectMixin(ExportActionModelAdmin):
    export_form_class = SelectableFieldsExportForm

    def get_export_formats(self):
        return [XLSX]


class ExportNormalMixin(ExportActionModelAdmin):
    export_form_class = ExportForm

    def get_export_formats(self):
        return [XLSX]
