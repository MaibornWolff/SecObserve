from django.apps import apps
from django.db.models.fields import CharField, TextField

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


def clip_fields(application: str, model: str, my_object) -> None:
    Model = apps.get_model(application, model)
    for field in Model._meta.get_fields():
        if isinstance(field, (CharField, TextField)):
            _, _, _, key_args = field.deconstruct()
            max_length = key_args.get("max_length")
            if max_length:
                value = getattr(my_object, field.name)
                if value and len(value) > max_length:
                    setattr(my_object, field.name, value[: max_length - 4] + " ...")
                    value = getattr(my_object, field.name)
                    if value.count("```") == 1:
                        # There is an open code block, that we have to close
                        setattr(
                            my_object,
                            field.name,
                            value[: max_length - 9] + "\n```\n\n...",
                        )


def get_comma_separated_as_list(comma_separated_string: str) -> list[str]:
    return_list = comma_separated_string.split(",") if comma_separated_string else []
    return [x.strip() for x in return_list]
