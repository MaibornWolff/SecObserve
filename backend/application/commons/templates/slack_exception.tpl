{
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Exception {{ exception_class }} has occured"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "Exception {{ exception_class }} has occured"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Exception class:*\n{{ exception_class }}"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Exception message:*\n{{ exception_message }}"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Timestamp:*\n{{ date_time|date:"Y-m-d H:i:s.u" }}"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*Trace:*\n{{ exception_trace }}"
				}
			]
		}
	]
}
