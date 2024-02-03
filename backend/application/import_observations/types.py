class Parser_Source:
    SOURCE_API = "API"
    SOURCE_FILE = "File"
    SOURCE_MANUAL = "Manual"
    SOURCE_UNKOWN = "Unkown"

    SOURCE_CHOICES = [
        (SOURCE_API, SOURCE_API),
        (SOURCE_FILE, SOURCE_FILE),
        (SOURCE_MANUAL, SOURCE_MANUAL),
        (SOURCE_UNKOWN, SOURCE_UNKOWN),
    ]


class Parser_Type:
    TYPE_SCA = "SCA"
    TYPE_SAST = "SAST"
    TYPE_DAST = "DAST"
    TYPE_IAST = "IAST"
    TYPE_SECRETS = "Secrets"
    TYPE_INFRASTRUCTURE = "Infrastructure"
    TYPE_OTHER = "Other"
    TYPE_MANUAL = "Manual"

    TYPE_CHOICES = [
        (TYPE_SCA, TYPE_SCA),
        (TYPE_SAST, TYPE_SAST),
        (TYPE_DAST, TYPE_DAST),
        (TYPE_IAST, TYPE_IAST),
        (TYPE_SECRETS, TYPE_SECRETS),
        (TYPE_INFRASTRUCTURE, TYPE_INFRASTRUCTURE),
        (TYPE_OTHER, TYPE_OTHER),
        (TYPE_MANUAL, TYPE_MANUAL),
    ]
