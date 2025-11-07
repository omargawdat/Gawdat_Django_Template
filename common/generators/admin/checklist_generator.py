# checklist_generator.py
from ..base import BaseGenerator


class ChecklistGenerator(BaseGenerator):
    def generate(self, fields: list) -> None:
        model_name = self.model.__name__

        content = f"""# {model_name} Admin Configuration Checklist

## Configuration Review Checklist

### ✅ 1. List View Configuration
▪ Verify the default sort makes business sense
▪ Consider if users expect newest/oldest first

### ✅ 2. Field Editability
▪ Check that sensitive fields are protected
▪ Check no fields are read-only that should be editable
▪ Verify important fields can be quick-edited from list view

### ✅ 3. Export Functionality
▪ is this field exportable? e.g. Order, Payment, Customer.
▪ Verify resource.py includes all necessary fields
▪ Test export with sample data

### ✅ 4. List View Display
▪ Include key identifying information
▪ Show status/state fields when relevant
▪ Look for calculated properties on the model
▪ Consider showing computed values (totals, counts, statuses)

### ✅ 5. Inline Admin Configuration
▪ Check if related models should be edited inline
▪ Consider TabularInline vs StackedInline based on data
"""
        self.write_file("CHECKLIST.md", content)
