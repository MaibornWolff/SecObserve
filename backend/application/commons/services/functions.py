from application.commons.models import Settings


def get_classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name


def get_base_url_frontend() -> str:
    settings = Settings.load()
    base_url_frontend = settings.base_url_frontend
    if not base_url_frontend.endswith("/"):
        base_url_frontend += "/"
    return base_url_frontend
