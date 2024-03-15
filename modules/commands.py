import os
import json
from modules.utilities import save_html, send_reply, generate_document_message_payload, generate_template_message_payload, generate_text_message_payload, translate_to_spanish, generate_text_button_message_payload, generate_audio_message_payload, text_to_speech, get_tram_ArrTime

REPLIT_URL = os.environ['REPLIT_URL']
with open("static/tram_stops/stops.json", 'r') as f:
  tram_stops = json.load(f)


def handle_help_command(contact_id):
  try:
    send_reply(generate_template_message_payload(contact_id, "help_template"))
  except Exception as e:
    send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def handle_google_command(contact_id, query):
  try:
    save_html(f"https://google.com/search?q={'+'.join(query.split())}",
              'static/google.html')
    send_reply(
        generate_document_message_payload(
            contact_id, f"{REPLIT_URL}/file/google.html", query,
            f"google-{'-'.join(query.split())}.html"))
  except Exception as e:
    send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def handle_google_image_command(contact_id, query):
  try:
    save_html(
        f"https://google.com/search?tbm=isch&q={'+'.join(query.split())}",
        'static/google.html')
    send_reply(
        generate_document_message_payload(
            contact_id, f"{REPLIT_URL}/file/google.html", query,
            f"google-image-{'-'.join(query.split())}.html"))
  except Exception as e:
    send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def handle_yahoo_command(contact_id, query):
  try:
    save_html(f"https://search.yahoo.com/search?p={'+'.join(query.split())}",
              'static/yahoo.html')
    send_reply(
        generate_document_message_payload(
            contact_id, f"{REPLIT_URL}/file/yahoo.html", query,
            f"yahoo-{'-'.join(query.split())}.html"))
  except Exception as e:
    send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def handle_url_command(contact_id, words):
  if len(words) != 2:
    send_reply(generate_text_message_payload(contact_id, "Sift URL mgad hh."))
  else:
    try:
      save_html(words[1], 'static/url.html')
      send_reply(
          generate_document_message_payload(contact_id,
                                            f"{REPLIT_URL}/file/url.html",
                                            words[1], f"url-{words[1]}.html"))
    except Exception as e:
      send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def handle_urban_command(contact_id, query):
  try:
    save_html(
        f"https://www.urbandictionary.com/define.php?term={'+'.join(query.split())}",
        'static/urban.html')
    send_reply(
        generate_document_message_payload(
            contact_id, f"{REPLIT_URL}/file/urban.html", query,
            f"urban-{'-'.join(query.split())}.html"))
  except Exception as e:
    send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def handle_spanish_command(contact_id, expression):
  try:
    translation = translate_to_spanish(expression)
    text_to_speech(translation)
    send_reply(generate_text_message_payload(contact_id, translation))
    send_reply(
        generate_audio_message_payload(contact_id,
                                       f"{REPLIT_URL}/file/tts.mp3"))
  except Exception as e:
    send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def handle_tts_command(contact_id, expression):
  try:
    text_to_speech(expression)
    send_reply(
        generate_audio_message_payload(contact_id,
                                       f"{REPLIT_URL}/file/tts.mp3"))
  except Exception as e:
    send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def handle_tram_command(contact_id, stop_name):
  try:
    send_reply(
        generate_text_message_payload(contact_id,
                                      get_tram_ArrTime(tram_stops, stop_name)))
  except Exception as e:
    send_reply(generate_text_message_payload(contact_id, f"Error: {str(e)}"))


def build_response(value):
  if 'messages' in value and value['messages'][0]['type'] in [
      'text', 'button', 'interactive'
  ]:
    # Retrive the contact's id
    contact_id = value['contacts'][0]['wa_id']
    # Retrive the message's body
    # In case it's a text message
    if 'text' in value['messages'][0]:
      message_body = value['messages'][0]['text']['body']
    # In case it's a Button
    elif 'button' in value['messages'][0] and 'text' in value['messages'][0][
        'button']:
      message_body = value['messages'][0]['button']['text']
    # In case it's a Reply Button
    elif 'interactive' in value['messages'][0]:
      message_body = value['messages'][0]['interactive']['button_reply'][
          'title']
    else:
      return

    # console log
    print(f"{contact_id} sent {message_body}")

    # Help command
    if message_body.lower().startswith('/help'):
      handle_help_command(contact_id)

    # google commands
    if message_body.lower().startswith('/google'):
      query = message_body.split(maxsplit=1)[1]
      if message_body.lower().startswith('/googleimage'):
        handle_google_image_command(contact_id, query)
      else:
        handle_google_command(contact_id, query)

    # yahoo command
    elif message_body.lower().startswith('/yahoo'):
      query = message_body.split(maxsplit=1)[1]
      handle_yahoo_command(contact_id, query)

    # url command
    elif message_body.lower().startswith('/url'):
      words = message_body.split()
      handle_url_command(contact_id, words)

    # spanish command
    elif message_body.lower().startswith('/spanish'):
      expression = message_body.split(maxsplit=1)[1]
      handle_spanish_command(contact_id, expression)

    # tts command
    elif message_body.lower().startswith('/tts'):
      expression = message_body.split(maxsplit=1)[1]
      handle_tts_command(contact_id, expression)

    # urban command
    elif message_body.lower().startswith('/urban'):
      query = message_body.split(maxsplit=1)[1]
      handle_urban_command(contact_id, query)

    # tram command
    elif message_body.lower().startswith('/tram'):
      query = message_body.split(maxsplit=1)[1]
      handle_tram_command(contact_id, query)
