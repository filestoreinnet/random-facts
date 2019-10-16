# -*- coding: iso-8859-15 -*-

from __future__ import print_function
import json
from botocore.vendored import requests
import random

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return build_response({}, build_short_speechlet_response("Hello. What kind of fact would you like?", False))
    elif event['request']['type'] == "IntentRequest":
        session = event['session']
        intent = event['request']['intent']
        intent_name = event['request']['intent']['name']
        sessionAttributes = session.get('attributes')
        # Dispatch to your skill's intent handlers
        if intent_name == "HistoryFactIntent":
            return get_fact(intent, session, 'history')
        elif intent_name == "ScienceFactIntent":
            return get_fact(intent, session, 'science')
        elif intent_name == "AMAZON.HelpIntent":
            return get_help(intent, session)
        elif intent_name == "AMAZON.StopIntent":
            return do_nothing()
        elif intent_name == "AMAZON.CancelIntent":
            return do_nothing()
        else:
            return build_response({}, build_short_speechlet_response("Hello. What kind of fact would you like?", False))

def get_help(intent, session):
    output = "Say, for example, 'Tell me a history fact'"
    return build_response({}, build_short_speechlet_response(output, False))
    
def get_fact(intent, session, fact_type):
    r = requests.get('http://randomstatus.in/others/en_facts.php?subject='+fact_type)
    fact_list = r.json()
    output = fact_list[random.randrange(len(fact_list))]
    return build_response({}, build_short_speechlet_response(output, True))

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_ssml_speechlet_response(title, output, plain_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>'+output.replace('&','and')+'</speak>'

        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': plain_output
        },
        'directives': [],
        'shouldEndSession': should_end_session
    }

def build_short_speechlet_response(output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': should_end_session
    }
    
def build_short_ssml_speechlet_response(output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output.replace('&','and')
        },
        'shouldEndSession': should_end_session
    }

def build_response(sessionAttributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': sessionAttributes,
        'response': speechlet_response
    }

def do_nothing():
    return build_response({}, {})

