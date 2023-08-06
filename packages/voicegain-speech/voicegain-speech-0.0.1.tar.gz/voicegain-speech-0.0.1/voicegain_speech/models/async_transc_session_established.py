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


class AsyncTranscSessionEstablished(object):
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
        'async_mode': 'AsyncMode',
        'callback': 'CallbackResp',
        'poll': 'PollResp',
        'session_id': 'str',
        'websocket': 'WebsocketResp',
        'content': 'RequestedContent'
    }

    attribute_map = {
        'async_mode': 'asyncMode',
        'callback': 'callback',
        'poll': 'poll',
        'session_id': 'sessionId',
        'websocket': 'websocket',
        'content': 'content'
    }

    def __init__(self, async_mode=None, callback=None, poll=None, session_id=None, websocket=None, content=None, local_vars_configuration=None):  # noqa: E501
        """AsyncTranscSessionEstablished - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._async_mode = None
        self._callback = None
        self._poll = None
        self._session_id = None
        self._websocket = None
        self._content = None
        self.discriminator = None

        self.async_mode = async_mode
        if callback is not None:
            self.callback = callback
        if poll is not None:
            self.poll = poll
        self.session_id = session_id
        if websocket is not None:
            self.websocket = websocket
        self.content = content

    @property
    def async_mode(self):
        """Gets the async_mode of this AsyncTranscSessionEstablished.  # noqa: E501


        :return: The async_mode of this AsyncTranscSessionEstablished.  # noqa: E501
        :rtype: AsyncMode
        """
        return self._async_mode

    @async_mode.setter
    def async_mode(self, async_mode):
        """Sets the async_mode of this AsyncTranscSessionEstablished.


        :param async_mode: The async_mode of this AsyncTranscSessionEstablished.  # noqa: E501
        :type: AsyncMode
        """
        if self.local_vars_configuration.client_side_validation and async_mode is None:  # noqa: E501
            raise ValueError("Invalid value for `async_mode`, must not be `None`")  # noqa: E501

        self._async_mode = async_mode

    @property
    def callback(self):
        """Gets the callback of this AsyncTranscSessionEstablished.  # noqa: E501


        :return: The callback of this AsyncTranscSessionEstablished.  # noqa: E501
        :rtype: CallbackResp
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """Sets the callback of this AsyncTranscSessionEstablished.


        :param callback: The callback of this AsyncTranscSessionEstablished.  # noqa: E501
        :type: CallbackResp
        """

        self._callback = callback

    @property
    def poll(self):
        """Gets the poll of this AsyncTranscSessionEstablished.  # noqa: E501


        :return: The poll of this AsyncTranscSessionEstablished.  # noqa: E501
        :rtype: PollResp
        """
        return self._poll

    @poll.setter
    def poll(self, poll):
        """Sets the poll of this AsyncTranscSessionEstablished.


        :param poll: The poll of this AsyncTranscSessionEstablished.  # noqa: E501
        :type: PollResp
        """

        self._poll = poll

    @property
    def session_id(self):
        """Gets the session_id of this AsyncTranscSessionEstablished.  # noqa: E501


        :return: The session_id of this AsyncTranscSessionEstablished.  # noqa: E501
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """Sets the session_id of this AsyncTranscSessionEstablished.


        :param session_id: The session_id of this AsyncTranscSessionEstablished.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and session_id is None:  # noqa: E501
            raise ValueError("Invalid value for `session_id`, must not be `None`")  # noqa: E501

        self._session_id = session_id

    @property
    def websocket(self):
        """Gets the websocket of this AsyncTranscSessionEstablished.  # noqa: E501


        :return: The websocket of this AsyncTranscSessionEstablished.  # noqa: E501
        :rtype: WebsocketResp
        """
        return self._websocket

    @websocket.setter
    def websocket(self, websocket):
        """Sets the websocket of this AsyncTranscSessionEstablished.


        :param websocket: The websocket of this AsyncTranscSessionEstablished.  # noqa: E501
        :type: WebsocketResp
        """

        self._websocket = websocket

    @property
    def content(self):
        """Gets the content of this AsyncTranscSessionEstablished.  # noqa: E501


        :return: The content of this AsyncTranscSessionEstablished.  # noqa: E501
        :rtype: RequestedContent
        """
        return self._content

    @content.setter
    def content(self, content):
        """Sets the content of this AsyncTranscSessionEstablished.


        :param content: The content of this AsyncTranscSessionEstablished.  # noqa: E501
        :type: RequestedContent
        """
        if self.local_vars_configuration.client_side_validation and content is None:  # noqa: E501
            raise ValueError("Invalid value for `content`, must not be `None`")  # noqa: E501

        self._content = content

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
        if not isinstance(other, AsyncTranscSessionEstablished):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AsyncTranscSessionEstablished):
            return True

        return self.to_dict() != other.to_dict()
