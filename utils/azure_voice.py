import azure.cognitiveservices.speech as speechsdk
import uuid
import datetime
import os

def voiceToText(voice_file):
    # config
    audio_config = speechsdk.AudioConfig(filename=voice_file)

    speech_config = speechsdk.SpeechConfig(subscription="da1538d820424891b02e32a673603339", region="eastasia")
    speech_config.speech_recognition_language="en-US"
    speech_config.auto_detect=True
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # recognize
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        reply = result.text
    else:
        cancel_details = result.cancellation_details
    return reply

def textToVoice(text):
    unique_id = uuid.uuid4().hex
    file_ext = ".wav"
    timestamp_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%M%S%fZ")
    # Must have path, not only file name so that ffmpeg can find the file
    home_dir = os.path.expanduser('~')
    file_path = os.path.join(home_dir, 'wechat_data')
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = f"{timestamp_str}_{unique_id}{file_ext}"
    file_path = os.path.join(file_path, file_name)

    # config
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
    speech_config = speechsdk.SpeechConfig(subscription="da1538d820424891b02e32a673603339", region="eastasia")
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text).get()
    relpy = ""
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        reply = file_path
    else:
        cancel_details = result.cancellation_details
    return reply