Hello{{ first_name }},

Exception {{ exception_class }} has occured
    
Message: {{ exception_message }}

Timestamp: {{ date_time|date:"Y-m-d H:i:s.u" }}

Trace: {% autoescape off %} {{ exception_trace }} {% endautoescape %}

Regards,

SecObserve