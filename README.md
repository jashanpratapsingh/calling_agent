# Calling Bot

This project is a calling bot that uses AI voice to make phone calls. It is built using Python, Twilio, and Google Text-to-Speech.

## Project Structure

- `calling_bot.py`: Contains the main code for the calling bot.
- `README.md`: Provides an overview of the project.

## Getting Started

### Prerequisites

- Python 3.x
- Twilio account
- Google Cloud account with Text-to-Speech API enabled

### Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required libraries:
    ```sh
    pip install twilio google-cloud-texttospeech
    ```

3. Set up Google Cloud Text-to-Speech:
    - Create a project on Google Cloud Platform.
    - Enable the Text-to-Speech API.
    - Set up authentication and download the service account key JSON file.
    - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the service account key file.

### Usage

1. Open [calling_bot.py](http://_vscodecontentref_/2) and replace the placeholders with your actual credentials and phone numbers.
2. Run the bot:
    ```sh
    python calling_bot.py
    ```

## Example Code

```python
from twilio.rest import Client
from google.cloud import texttospeech
import os

# Set up Google Text-to-Speech client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"
tts_client = texttospeech.TextToSpeechClient()

def synthesize_speech(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = tts_client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    return "output.mp3"

# Set up Twilio client
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_client = Client(account_sid, auth_token)

def make_call(to_number, from_number, message):
    audio_file = synthesize_speech(message)
    call = twilio_client.calls.create(
        twiml=f'<Response><Play>{audio_file}</Play></Response>',
        to=to_number,
        from_=from_number
    )
    return call.sid

# Example usage
to_number = '+1234567890'
from_number = '+0987654321'
message = 'Hello, this is a test call from your AI bot.'
call_sid = make_call(to_number, from_number, message)
print(f"Call initiated with SID: {call_sid}")