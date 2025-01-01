from twilio.twiml.voice_response import VoiceResponse
from google.cloud import texttospeech
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Google Text-to-Speech client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"
tts_client = texttospeech.TextToSpeechClient()

def synthesize_speech(text):
    try:
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = tts_client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)
        return "output.mp3"
    except Exception as e:
        logging.error(f"Error synthesizing speech: {e}")
        return None

# Set up Twilio client
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_client = Client(account_sid, auth_token)

def make_call(to_number, from_number, message):
    audio_file = synthesize_speech(message)
    if audio_file is None:
        logging.error("Failed to synthesize speech. Call not initiated.")
        return None

    try:
        response = VoiceResponse()
        response.play(audio_file)
        response.gather(num_digits=1, action='/handle-key', method='POST')
        call = twilio_client.calls.create(
            twiml=response,
            to=to_number,
            from_=from_number
        )
        logging.info(f"Call initiated with SID: {call.sid}")
        return call.sid
    except Exception as e:
        logging.error(f"Error making call: {e}")
        return None

# Example usage
to_number = '+1234567890'
from_number = '+0987654321'
message = 'Hello, this is a test call from your AI bot. Press 1 to confirm.'
call_sid = make_call(to_number, from_number, message)
if call_sid:
    print(f"Call initiated with SID: {call_sid}")
else:
    print("Call failed.")