# coding: utf-8

"""
    Voicegain Speech Recognition API v1

    # New  [RTC Callback API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain API This API is provided by [Voicegain](https://www.voicegain.ai) to its registered customers.  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # Speech-to-Text: Recognition vs Transcription Voicegain web api provides two types of methods for speech recognition.   + **/asr/recognize** - where the purpose is to identify what was said in a context of a more constrained set of choices.   This web api uses grammars as both a language model and a way to attach semantic meaning to spoken utterances. + **/asr/transcribe** - where the purpose is to **transcribe** speech audio word for word, no meaning is attached to transcribed text.   This web api uses large vocabulary language model.      The result of transcription can be returned in three formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second.  For the transcription API, real-time incremental results will be sent back with about 2 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30 seconds (or earlier for shorter audio). Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes.  Other combinations of session types, including more than 2 sessions, are currently not supported.  Please, let us know if you think you have a valid use case for other combinations.   # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.   # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Portal](https://portal.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).   # noqa: E501

    The version of the OpenAPI document: 1.11.0 - updated July 31, 2020
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ascalon_web_api_client.configuration import Configuration


class AIVRQuestion(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'audio_properties': 'AIVRPromptPropertiesAudio',
        'html_properties': 'AIVRPromptPropertiesHtml',
        'text': 'str',
        'wait_msec': 'int',
        'audio_response': 'AIVRResponsePropertiesAudio',
        'html_response': 'AIVRResponsePropertiesHtml',
        'name': 'str'
    }

    attribute_map = {
        'audio_properties': 'audioProperties',
        'html_properties': 'htmlProperties',
        'text': 'text',
        'wait_msec': 'waitMsec',
        'audio_response': 'audioResponse',
        'html_response': 'htmlResponse',
        'name': 'name'
    }

    def __init__(self, audio_properties=None, html_properties=None, text=None, wait_msec=None, audio_response=None, html_response=None, name=None, local_vars_configuration=None):  # noqa: E501
        """AIVRQuestion - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._audio_properties = None
        self._html_properties = None
        self._text = None
        self._wait_msec = None
        self._audio_response = None
        self._html_response = None
        self._name = None
        self.discriminator = None

        if audio_properties is not None:
            self.audio_properties = audio_properties
        if html_properties is not None:
            self.html_properties = html_properties
        self.text = text
        if wait_msec is not None:
            self.wait_msec = wait_msec
        if audio_response is not None:
            self.audio_response = audio_response
        if html_response is not None:
            self.html_response = html_response
        if name is not None:
            self.name = name

    @property
    def audio_properties(self):
        """Gets the audio_properties of this AIVRQuestion.  # noqa: E501


        :return: The audio_properties of this AIVRQuestion.  # noqa: E501
        :rtype: AIVRPromptPropertiesAudio
        """
        return self._audio_properties

    @audio_properties.setter
    def audio_properties(self, audio_properties):
        """Sets the audio_properties of this AIVRQuestion.


        :param audio_properties: The audio_properties of this AIVRQuestion.  # noqa: E501
        :type: AIVRPromptPropertiesAudio
        """

        self._audio_properties = audio_properties

    @property
    def html_properties(self):
        """Gets the html_properties of this AIVRQuestion.  # noqa: E501


        :return: The html_properties of this AIVRQuestion.  # noqa: E501
        :rtype: AIVRPromptPropertiesHtml
        """
        return self._html_properties

    @html_properties.setter
    def html_properties(self, html_properties):
        """Sets the html_properties of this AIVRQuestion.


        :param html_properties: The html_properties of this AIVRQuestion.  # noqa: E501
        :type: AIVRPromptPropertiesHtml
        """

        self._html_properties = html_properties

    @property
    def text(self):
        """Gets the text of this AIVRQuestion.  # noqa: E501

        text to be said or displayed  # noqa: E501

        :return: The text of this AIVRQuestion.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this AIVRQuestion.

        text to be said or displayed  # noqa: E501

        :param text: The text of this AIVRQuestion.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and text is None:  # noqa: E501
            raise ValueError("Invalid value for `text`, must not be `None`")  # noqa: E501

        self._text = text

    @property
    def wait_msec(self):
        """Gets the wait_msec of this AIVRQuestion.  # noqa: E501

        Wait time in milliseconds after playing or displaying the prompt before a callback will be made.</br> Meant mainly for GUI and has different meanings for prompt and a question:</br> **for prompt**  It is recommended to use so that interactions are paced in such a way so that the caller has sufficient time to read the prompt.</br> **for question** It is fully optional and can be used as a sort of timeout, that will allow to proceed if caller does not provide requested input.   # noqa: E501

        :return: The wait_msec of this AIVRQuestion.  # noqa: E501
        :rtype: int
        """
        return self._wait_msec

    @wait_msec.setter
    def wait_msec(self, wait_msec):
        """Sets the wait_msec of this AIVRQuestion.

        Wait time in milliseconds after playing or displaying the prompt before a callback will be made.</br> Meant mainly for GUI and has different meanings for prompt and a question:</br> **for prompt**  It is recommended to use so that interactions are paced in such a way so that the caller has sufficient time to read the prompt.</br> **for question** It is fully optional and can be used as a sort of timeout, that will allow to proceed if caller does not provide requested input.   # noqa: E501

        :param wait_msec: The wait_msec of this AIVRQuestion.  # noqa: E501
        :type: int
        """

        self._wait_msec = wait_msec

    @property
    def audio_response(self):
        """Gets the audio_response of this AIVRQuestion.  # noqa: E501


        :return: The audio_response of this AIVRQuestion.  # noqa: E501
        :rtype: AIVRResponsePropertiesAudio
        """
        return self._audio_response

    @audio_response.setter
    def audio_response(self, audio_response):
        """Sets the audio_response of this AIVRQuestion.


        :param audio_response: The audio_response of this AIVRQuestion.  # noqa: E501
        :type: AIVRResponsePropertiesAudio
        """

        self._audio_response = audio_response

    @property
    def html_response(self):
        """Gets the html_response of this AIVRQuestion.  # noqa: E501


        :return: The html_response of this AIVRQuestion.  # noqa: E501
        :rtype: AIVRResponsePropertiesHtml
        """
        return self._html_response

    @html_response.setter
    def html_response(self, html_response):
        """Sets the html_response of this AIVRQuestion.


        :param html_response: The html_response of this AIVRQuestion.  # noqa: E501
        :type: AIVRResponsePropertiesHtml
        """

        self._html_response = html_response

    @property
    def name(self):
        """Gets the name of this AIVRQuestion.  # noqa: E501

        (optional) Name to be associated with the question. Will be used to persist the values of responses to the question.  Persisted values can be referenced in prompts. If not provided the values will be returned of the subsequent callback but not persisted in AIVR session.   # noqa: E501

        :return: The name of this AIVRQuestion.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AIVRQuestion.

        (optional) Name to be associated with the question. Will be used to persist the values of responses to the question.  Persisted values can be referenced in prompts. If not provided the values will be returned of the subsequent callback but not persisted in AIVR session.   # noqa: E501

        :param name: The name of this AIVRQuestion.  # noqa: E501
        :type: str
        """

        self._name = name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AIVRQuestion):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AIVRQuestion):
            return True

        return self.to_dict() != other.to_dict()
