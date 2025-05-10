class RegionFields:
    CODE = "code"
    NAME = "name"
    COUNTRY = "country"
    GEOMETRY = "geometry"
    NAME_AR = "name_ar"
    NAME_EN = "name_en"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
