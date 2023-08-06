"""
Created by DoubleA LLC 
"""
from subprocess import call

dev_null = open('/dev/null', 'w')

_connection_establishing_problem_message = """
Cannot establish connection with {api_url}:{api_port}
At this library version only next urls are available:
  * {url_1}
  * {url_2}
Please check your internet connection and API url and try again.
"""


def check_connection(api_url, api_port):
    call_answer_code = call(['curl', '{}:{}'.format(api_url, api_port)], stdout=dev_null, stderr=dev_null)
    if int(call_answer_code) != 52:
        print(_connection_establishing_problem_message.format(
            api_url=api_url, api_port=api_port,
            url_1='ru1.recognition.api.neurodatalab.dev',
            url_2='usa1.recognition.api.neurodatalab.dev'
        ))
        exit(1)
