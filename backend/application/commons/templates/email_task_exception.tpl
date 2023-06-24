Hello{{ first_name }},

Exception {{ exception_class }} has occured while processing background task.

Function: {{ function }}

Arguments: {{ arguments }}

User: {{ user.full_name }}

Message: {{ exception_message }}

Timestamp: {{ date_time|date:"Y-m-d H:i:s.u" }}

Trace: {% autoescape off %} {{ exception_trace }} {% endautoescape %}

Regards,

SecObserve