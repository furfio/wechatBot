import azure.cognitiveservices.speech as speechsdk

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
        logger.info("[Azure] voiceToText voice file name={} text={}".format(voice_file, result.text))
        reply = result.text
    else:
        cancel_details = result.cancellation_details
        logger.error("[Azure] voiceToText error, result={}, errordetails={}".format(result, cancel_details.error_details))
    return reply