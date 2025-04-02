import os
import logging
import boto3
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

logger = logging.getLogger("mkdocs.plugins.tts-amazon-polly")

class AmazonPollyTTSPlugin(BasePlugin):
    config_scheme = (
        ("output_dir", config_options.Type(str, default="audio")),
        ("voice_id", config_options.Type(str, default="Matthew")),
    )

    def __init__(self):
        self.polly_client = boto3.client("polly")

    def on_page_markdown(self, markdown, page, config, files):
        logger.debug(f"[tts-amazon-polly] Processing page: {page.file.src_path}")
        logger.debug(f"[tts-amazon-polly] Page metadata: {page.meta}")
        
        generate_audio = page.meta.get("generate_audio", False)
        if not generate_audio:
            logger.info(f"[tts-amazon-polly] Skipping TTS for {page.file.src_path} (No 'generate_audio' tag)")
            return markdown

        # Output directory
        output_dir = os.path.join(config["site_dir"], self.config["output_dir"])
        os.makedirs(output_dir, exist_ok=True)

        # Clean content
        text_content = markdown.replace("<!-- more -->", "").strip()
        if not text_content:
            logger.warning(f"[tts-amazon-polly] Skipping page with no meaningful content: {page.file.src_path}")
            return markdown

        # Generate filename
        audio_filename = f"{os.path.splitext(page.file.src_path)[0]}.mp3"
        audio_path = os.path.join(output_dir, audio_filename)

        os.makedirs(os.path.dirname(audio_path), exist_ok=True)

        if not os.path.exists(audio_path):
            logger.info(f"[tts-amazon-polly] Generating audio for: {page.file.src_path}")
            try:
                response = self.polly_client.synthesize_speech(
                    Text=text_content, OutputFormat="mp3", VoiceId=self.config["voice_id"]
                )

                logger.debug(f"[tts-amazon-polly] Polly response metadata: {response['ResponseMetadata']}")

                if "AudioStream" in response:
                    with open(audio_path, "wb") as audio_file:
                        audio_file.write(response["AudioStream"].read())
                    logger.info(f"[tts-amazon-polly] Audio saved: {audio_path}")
                else:
                    logger.error(f"[tts-amazon-polly] No AudioStream in response for {page.file.src_path}")

            except Exception as e:
                logger.error(f"[tts-amazon-polly] Amazon Polly TTS failed: {e}")
                return markdown

        audio_tag = f'<audio controls><source src="/{self.config["output_dir"]}/{audio_filename}" type="audio/mpeg"></audio>\n\n'
        return markdown.replace("<!-- more -->", "<!-- more -->\n\n" + audio_tag, 1)
