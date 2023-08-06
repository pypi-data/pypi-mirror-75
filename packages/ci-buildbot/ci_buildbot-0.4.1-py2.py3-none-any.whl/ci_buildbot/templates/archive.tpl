[
  {
    "type": "divider"
  },
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*{{ last_version_url }}*: code archived to code-drop *SUCCESS*\n*Pipeline*: {{ pipeline_url }}\n*Committer*: {{ committer }}\n*Authors*: {{ authors|join('\\n') }}"
    },
    "accessory": {
      "type": "image",
      "image_url":  "https://ads-utils-icons.s3-us-west-2.amazonaws.com/ci-buildbot/cloud-check.png",
      "alt_text": "File folder"
    }
  }
  {% if diff_url %}
  ,{
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*Changes since {{ previous_version }}*: <{{ diff_url }}|Click here>"
    }
  },
  {% endif %}
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*Changelog*\n{{ changelog|join('\\n') }}"
    }
  },
  {
    "type": "context",
    "elements": [
      {
        "type": "mrkdwn",
        "text": "{{ completed_date }} {{buildbot}}"
      }
    ]
  }
]
