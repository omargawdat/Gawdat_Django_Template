# from unfold.decorators import display
#
# from apps.users.models.customer import Customer
#
#
# class ModelDisplayMixin:
#     @display(description="Provider", header=True, ordering="phone_number")
#     def display_header(self, provider: Customer):
#         return [
#             provider,
#             provider.full_name,
#             "CU",
#             {
#                 "path": provider.image.url if provider.image else None,
#             },
#         ]
#
#     @display(description="Is Active?", label={"True": "success", "False": "danger"}, ordering="-is_active")
#     def display_is_active(self, provider: Provider):
#         return "True" if provider.is_active else "False"
