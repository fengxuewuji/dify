import uuid
import hashlib
import subprocess
from io import BytesIO
from typing import Optional
from functools import reduce
from pydub import AudioSegment

from core.model_runtime.entities.model_entities import ModelPropertyKey
from core.model_runtime.errors.validate import CredentialsValidateFailedError
from core.model_runtime.errors.invoke import InvokeBadRequestError
from core.model_runtime.model_providers.__base.tts_model import TTSModel
from core.model_runtime.model_providers.openai._common import _CommonOpenAI

from typing_extensions import Literal
from flask import Response, stream_with_context
from openai import OpenAI
import concurrent.futures


class OpenAIText2SpeechModel(_CommonOpenAI, TTSModel):
    """
    Model class for OpenAI Speech to text model.
    """
    def _invoke(self, model: str, credentials: dict, content_text: str, streaming: bool, user: Optional[str] = None) -> any:
        """
        _invoke text2speech model

        :param model: model name
        :param credentials: model credentials
        :param content_text: text content to be translated
        :param streaming: output is streaming
        :param user: unique user id
        :return: text translated to audio file
        """
        self._is_ffmpeg_installed()
        audio_type = self._get_model_audio_type(model, credentials)
        if streaming:
            return Response(stream_with_context(self._tts_invoke_streaming(model=model,
                                                                           credentials=credentials,
                                                                           content_text=content_text,
                                                                           user=user)),
                            status=200, mimetype=f'audio/{audio_type}')
        else:
            return self._tts_invoke(model=model, credentials=credentials, content_text=content_text, user=user)

    def validate_credentials(self, model: str, credentials: dict, user: Optional[str] = None) -> None:
        """
        validate credentials text2speech model

        :param model: model name
        :param credentials: model credentials
        :param user: unique user id
        :return: text translated to audio file
        """
        try:
            self._tts_invoke(
                model=model,
                credentials=credentials,
                content_text='Hello world!',
                user=user
            )
        except Exception as ex:
            raise CredentialsValidateFailedError(str(ex))

    def _tts_invoke(self, model: str, credentials: dict, content_text: str, user: Optional[str] = None) -> any:
        """
        _tts_invoke text2speech model

        :param model: model name
        :param credentials: model credentials
        :param content_text: text content to be translated
        :param user: unique user id
        :return: text translated to audio file
        """
        audio_type = self._get_model_audio_type(model, credentials)
        word_limit = self._get_model_word_limit(model, credentials)
        max_workers = self._get_model_workers_limit(model, credentials)

        try:
            sentences = list(self._split_text_into_sentences(text=content_text, limit=word_limit))
            audio_bytes_list = list()

            # Create a thread pool and map the function to the list of sentences
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(self._process_sentence, sentence, model, credentials) for sentence
                           in sentences]
                for future in futures:
                    try:
                        audio_bytes_list.append(future.result())
                    except Exception as ex:
                        raise InvokeBadRequestError(str(ex))

            audio_segments = [AudioSegment.from_file(BytesIO(audio_bytes), format=audio_type) for audio_bytes in
                              audio_bytes_list if audio_bytes]
            combined_segment = reduce(lambda x, y: x + y, audio_segments)
            buffer: BytesIO = BytesIO()
            combined_segment.export(buffer, format=audio_type)
            buffer.seek(0)
            return Response(buffer.read(), status=200, mimetype=f"audio/{audio_type}")
        except Exception as ex:
            raise InvokeBadRequestError(str(ex))

    # Todo: To improve the streaming function
    def _tts_invoke_streaming(self, model: str, credentials: dict, content_text: str, user: Optional[str] = None) -> any:
        """
        _tts_invoke_streaming text2speech model

        :param model: model name
        :param credentials: model credentials
        :param content_text: text content to be translated
        :param user: unique user id
        :return: text translated to audio file
        """
        # transform credentials to kwargs for model instance
        credentials_kwargs = self._to_credential_kwargs(credentials)
        voice_name = self._get_model_voice(model, credentials)
        word_limit = self._get_model_word_limit(model, credentials)
        audio_type = self._get_model_audio_type(model, credentials)
        tts_file_id = self._get_file_name(content_text)
        file_path = f'storage/generate_files/{audio_type}/{tts_file_id}.{audio_type}'
        try:
            client = OpenAI(**credentials_kwargs)
            sentences = list(self._split_text_into_sentences(text=content_text, limit=word_limit))
            for sentence in sentences:
                response = client.audio.speech.create(model=model, voice=voice_name, input=sentence.strip())
                response.stream_to_file(file_path)
        except Exception as ex:
            raise InvokeBadRequestError(str(ex))

    def _get_model_voice(self, model: str, credentials: dict) -> Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]:
        """
        Get voice for given tts model

        :param model: model name
        :param credentials: model credentials
        :return: voice
        """
        model_schema = self.get_model_schema(model, credentials)

        if model_schema and ModelPropertyKey.DEFAULT_VOICE in model_schema.model_properties:
            return model_schema.model_properties[ModelPropertyKey.DEFAULT_VOICE]

    def _get_model_audio_type(self, model: str, credentials: dict) -> str:
        """
        Get audio type for given tts model

        :param model: model name
        :param credentials: model credentials
        :return: voice
        """
        model_schema = self.get_model_schema(model, credentials)

        if model_schema and ModelPropertyKey.AUDOI_TYPE in model_schema.model_properties:
            return model_schema.model_properties[ModelPropertyKey.AUDOI_TYPE]

    def _get_model_word_limit(self, model: str, credentials: dict) -> int:
        """
        Get audio type for given tts model
        :return: audio type
        """
        model_schema = self.get_model_schema(model, credentials)

        if model_schema and ModelPropertyKey.WORD_LIMIT in model_schema.model_properties:
            return model_schema.model_properties[ModelPropertyKey.WORD_LIMIT]

    def _get_model_workers_limit(self, model: str, credentials: dict) -> int:
        """
        Get audio max workers for given tts model
        :return: audio type
        """
        model_schema = self.get_model_schema(model, credentials)

        if model_schema and ModelPropertyKey.MAX_WORKERS in model_schema.model_properties:
            return model_schema.model_properties[ModelPropertyKey.MAX_WORKERS]

    @staticmethod
    def _split_text_into_sentences(text: str, limit: int, delimiters=None):
        if delimiters is None:
            delimiters = set('。！？；\n')

        buf = []
        word_count = 0
        for char in text:
            buf.append(char)
            if char in delimiters:
                if word_count >= limit:
                    yield ''.join(buf)
                    buf = []
                    word_count = 0
                else:
                    word_count += 1
            else:
                word_count += 1

        if buf:
            yield ''.join(buf)

    @staticmethod
    def _get_file_name(file_content: str) -> str:
        hash_object = hashlib.sha256(file_content.encode())
        hex_digest = hash_object.hexdigest()

        namespace_uuid = uuid.UUID('a5da6ef9-b303-596f-8e88-bf8fa40f4b31')
        unique_uuid = uuid.uuid5(namespace_uuid, hex_digest)
        return str(unique_uuid)

    def _process_sentence(self, sentence: str, model: str, credentials: dict):
        """
        _tts_invoke openai text2speech model api

        :param model: model name
        :param credentials: model credentials
        :param sentence: text content to be translated
        :return: text translated to audio file
        """
        # transform credentials to kwargs for model instance
        credentials_kwargs = self._to_credential_kwargs(credentials)
        voice_name = self._get_model_voice(model, credentials)

        client = OpenAI(**credentials_kwargs)
        response = client.audio.speech.create(model=model, voice=voice_name, input=sentence.strip())
        if isinstance(response.read(), bytes):
            return response.read()

    @staticmethod
    def _is_ffmpeg_installed():
        try:
            output = subprocess.check_output("ffmpeg -version", shell=True)
            if "ffmpeg version" in output.decode("utf-8"):
                return True
            else:
                raise InvokeBadRequestError("ffmpeg is not installed")
        except Exception:
            raise InvokeBadRequestError("ffmpeg is not installed")
