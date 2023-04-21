from constance import config


def get_classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name


def get_base_url_frontend() -> str:
    base_url_frontend = config.BASE_URL_FRONTEND
    if not base_url_frontend.endswith("/"):
        base_url_frontend += "/"
    return base_url_frontend
