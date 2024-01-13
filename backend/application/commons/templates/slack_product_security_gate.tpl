{
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Security gate for product {{ product.name }} has changed to {{ security_gate_status }}"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "View Product <{{ product_url }}|{{ product.name }}>"
				}
			]
		}
	]
}
