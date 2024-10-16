class License_Policy_Evaluation_Result:
    RESULT_ALLOWED = "Allowed"
    RESULT_FORBIDDEN = "Forbidden"
    RESULT_UNKOWN = "Unkown"

    RESULT_CHOICES = [
        (RESULT_ALLOWED, RESULT_ALLOWED),
        (RESULT_FORBIDDEN, RESULT_FORBIDDEN),
        (RESULT_UNKOWN, RESULT_UNKOWN),
    ]
