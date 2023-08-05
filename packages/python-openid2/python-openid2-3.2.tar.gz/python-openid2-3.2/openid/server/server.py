# -*- test-case-name: openid.test.test_server -*-
"""OpenID server protocol and logic.

Overview
========

    An OpenID server must perform three tasks:

        1. Examine the incoming request to determine its nature and validity.

        2. Make a decision about how to respond to this request.

        3. Format the response according to the protocol.

    The first and last of these tasks may performed by
    the L{decodeRequest<Server.decodeRequest>} and
    L{encodeResponse<Server.encodeResponse>} methods of the
    L{Server} object.  Who gets to do the intermediate task -- deciding
    how to respond to the request -- will depend on what type of request it
    is.

    If it's a request to authenticate a user (a X{C{checkid_setup}} or
    X{C{checkid_immediate}} request), you need to decide if you will assert
    that this user may claim the identity in question.  Exactly how you do
    that is a matter of application policy, but it generally involves making
    sure the user has an account with your system and is logged in, checking
    to see if that identity is hers to claim, and verifying with the user that
    she does consent to releasing that information to the party making the
    request.

    Examine the properties of the L{CheckIDRequest} object, optionally
    check L{CheckIDRequest.returnToVerified}, and and when you've come
    to a decision, form a response by calling L{CheckIDRequest.answer}.

    Other types of requests relate to establishing associations between client
    and server and verifying the authenticity of previous communications.
    L{Server} contains all the logic and data necessary to respond to
    such requests; just pass the request to L{Server.handleRequest}.


OpenID Extensions
=================

    Do you want to provide other information for your users
    in addition to authentication?  Version 2.0 of the OpenID
    protocol allows consumers to add extensions to their requests.
    For example, with sites using the U{Simple Registration
    Extension<http://openid.net/specs/openid-simple-registration-extension-1_0.html>},
    a user can agree to have their nickname and e-mail address sent to a
    site when they sign up.

    Since extensions do not change the way OpenID authentication works,
    code to handle extension requests may be completely separate from the
    L{OpenIDRequest} class here.  But you'll likely want data sent back by
    your extension to be signed.  L{OpenIDResponse} provides methods with
    which you can add data to it which can be signed with the other data in
    the OpenID signature.

    For example::

        # when request is a checkid_* request
        response = request.answer(True)
        # this will a signed 'openid.sreg.timezone' parameter to the response
        # as well as a namespace declaration for the openid.sreg namespace
        response.fields.setArg('http://openid.net/sreg/1.0', 'timezone', 'America/Los_Angeles')

    There are helper modules for a number of extensions, including
    L{Attribute Exchange<openid.extensions.ax>},
    L{PAPE<openid.extensions.pape>}, and
    L{Simple Registration<openid.extensions.sreg>} in the L{openid.extensions}
    package.

Stores
======

    The OpenID server needs to maintain state between requests in order
    to function.  Its mechanism for doing this is called a store.  The
    store interface is defined in C{L{openid.store.interface.OpenIDStore}}.
    Additionally, several concrete store implementations are provided, so that
    most sites won't need to implement a custom store.  For a store backed
    by flat files on disk, see C{L{openid.store.filestore.FileOpenIDStore}}.
    For stores based on MySQL or SQLite, see the C{L{openid.store.sqlstore}}
    module.


Upgrading
=========

From 1.0 to 1.1
---------------

    The keys by which a server looks up associations in its store have changed
    in version 1.2 of this library.  If your store has entries created from
    version 1.0 code, you should empty it.

From 1.1 to 2.0
---------------

    One of the additions to the OpenID protocol was a specified nonce
    format for one-way nonces.  As a result, the nonce table in the store
    has changed.  You'll need to run contrib/upgrade-store-1.1-to-2.0 to
    upgrade your store, or you'll encounter errors about the wrong number
    of columns in the oid_nonces table.

    If you've written your own custom store or code that interacts
    directly with it, you'll need to review the change notes in
    L{openid.store.interface}.

@group Requests: OpenIDRequest, AssociateRequest, CheckIDRequest,
    CheckAuthRequest

@group Responses: OpenIDResponse

@group HTTP Codes: HTTP_OK, HTTP_REDIRECT, HTTP_ERROR

@group Response Encodings: ENCODE_KVFORM, ENCODE_HTML_FORM, ENCODE_URL
"""
from __future__ import unicode_literals

import base64
import logging
import os
import time
import warnings
from copy import deepcopy

import six
from cryptography.hazmat.primitives import hashes

from openid import cryptutil, kvform, oidutil
from openid.association import Association, default_negotiator, getSecretSize
from openid.dh import DiffieHellman
from openid.message import (IDENTIFIER_SELECT, OPENID1_URL_LIMIT, OPENID2_NS, OPENID_NS, InvalidNamespace,
                            InvalidOpenIDNamespace, Message)
from openid.oidutil import string_to_text
from openid.server.trustroot import TrustRoot, verifyReturnTo
from openid.store.nonce import mkNonce
from openid.urinorm import urinorm

_LOGGER = logging.getLogger(__name__)

HTTP_OK = 200
HTTP_REDIRECT = 302
HTTP_ERROR = 400

BROWSER_REQUEST_MODES = ['checkid_setup', 'checkid_immediate']

ENCODE_KVFORM = ('kvform',)
ENCODE_URL = ('URL/redirect',)
ENCODE_HTML_FORM = ('HTML form',)

UNUSED = None


class OpenIDRequest(object):
    """I represent an incoming OpenID request.

    @cvar mode: the C{X{openid.mode}} of this request.
    @type mode: six.text_type

    @ivar message: Original request message.
    @type message: Message
    """
    mode = None

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        else:
            # If no message is defined, create an empty one.
            self.message = Message(OPENID2_NS)

    @property
    def namespace(self):
        """Return request namespace."""
        msg = 'The "namespace" attribute of {} objects is deprecated. Use "message.getOpenIDNamespace()" instead'
        warnings.warn(msg.format(type(self).__name__), DeprecationWarning, stacklevel=2)
        return self.message.getOpenIDNamespace()


class CheckAuthRequest(OpenIDRequest):
    """A request to verify the validity of a previous response.

    @cvar mode: "X{C{check_authentication}}"
    @type mode: six.text_type

    @ivar assoc_handle: The X{association handle} the response was signed with.
    @type assoc_handle: six.text_type
    @ivar signed: The message with the signature which wants checking.
    @type signed: L{Message}

    @ivar invalidate_handle: An X{association handle} the client is asking
        about the validity of.  Optional, may be C{None}.
    @type invalidate_handle: six.text_type

    @see: U{OpenID Specs, Mode: check_authentication
        <http://openid.net/specs.bml#mode-check_authentication>}
    """
    mode = "check_authentication"

    required_fields = ["identity", "return_to", "response_nonce"]

    def __init__(self, assoc_handle, signed, invalidate_handle=None, message=None):
        """Construct me.

        These parameters are assigned directly as class attributes, see
        my L{class documentation<CheckAuthRequest>} for their descriptions.

        @type assoc_handle: six.text_type, six.binary_type is deprecated
        @type signed: L{Message}
        @type invalidate_handle: six.text_type, six.binary_type is deprecated
        """
        super(CheckAuthRequest, self).__init__(message=message)
        self.assoc_handle = string_to_text(assoc_handle,
                                           "Binary values for assoc_handle are deprecated. Use text input instead.")
        self.signed = signed
        if invalidate_handle is not None:
            invalidate_handle = string_to_text(
                invalidate_handle, "Binary values for invalidate_handle are deprecated. Use text input instead.")
        self.invalidate_handle = invalidate_handle

    @classmethod
    def fromMessage(klass, message, op_endpoint=UNUSED):
        """Construct me from an OpenID Message.

        @param message: An OpenID check_authentication Message
        @type message: L{openid.message.Message}

        @returntype: L{CheckAuthRequest}
        """
        assoc_handle = message.getArg(OPENID_NS, 'assoc_handle')
        sig = message.getArg(OPENID_NS, 'sig')
        invalidate_handle = message.getArg(OPENID_NS, 'invalidate_handle')
        if (assoc_handle is None or sig is None):
            fmt = "%s request missing required parameter from message %s"
            raise ProtocolError(message, text=fmt % (klass.mode, message))

        signed = message.copy()
        # openid.mode is currently check_authentication because
        # that's the mode of this request.  But the signature
        # was made on something with a different openid.mode.
        # http://article.gmane.org/gmane.comp.web.openid.general/537
        if signed.hasKey(OPENID_NS, "mode"):
            signed.setArg(OPENID_NS, "mode", "id_res")

        self = klass(assoc_handle, signed, invalidate_handle, message)
        return self

    def answer(self, signatory):
        """Respond to this request.

        Given a L{Signatory}, I can check the validity of the signature and
        the X{C{invalidate_handle}}.

        @param signatory: The L{Signatory} to use to check the signature.
        @type signatory: L{Signatory}

        @returns: A response with an X{C{is_valid}} (and, if
           appropriate X{C{invalidate_handle}}) field.
        @returntype: L{OpenIDResponse}
        """
        is_valid = signatory.verify(self.assoc_handle, self.signed)
        # Now invalidate that assoc_handle so it this checkAuth message cannot
        # be replayed.
        signatory.invalidate(self.assoc_handle, dumb=True)
        response = OpenIDResponse(self)
        valid_str = (is_valid and "true") or "false"
        response.fields.setArg(OPENID_NS, 'is_valid', valid_str)

        if self.invalidate_handle:
            assoc = signatory.getAssociation(self.invalidate_handle, dumb=False)
            if not assoc:
                response.fields.setArg(
                    OPENID_NS, 'invalidate_handle', self.invalidate_handle)
        return response

    def __str__(self):
        if self.invalidate_handle:
            ih = " invalidate? %r" % (self.invalidate_handle,)
        else:
            ih = ""
        sig = self.message.getArg(OPENID_NS, 'sig')
        s = "<%s handle: %r sig: %r: signed: %r%s>" % (self.__class__.__name__, self.assoc_handle, sig, self.signed, ih)
        return s


class PlainTextServerSession(object):
    """An object that knows how to handle association requests with no
    session type.

    @cvar session_type: The session_type for this association
        session. There is no type defined for plain-text in the OpenID
        specification, so we use 'no-encryption'.
    @type session_type: six.text_type

    @see: U{OpenID Specs, Mode: associate
        <http://openid.net/specs.bml#mode-associate>}
    @see: AssociateRequest
    """
    session_type = 'no-encryption'
    allowed_assoc_types = ['HMAC-SHA1', 'HMAC-SHA256']

    @classmethod
    def fromMessage(cls, unused_request):
        return cls()

    def answer(self, secret):
        return {'mac_key': oidutil.toBase64(secret)}


class DiffieHellmanSHA1ServerSession(object):
    """An object that knows how to handle association requests with the
    Diffie-Hellman session type.

    @cvar session_type: The session_type for this association
        session.
    @type session_type: six.text_type

    @cvar algorithm: Hash algorithm for MAC key generation.
    @type algorithm: hashes.HashAlgorithm
    @cvar hash_func: Hash function for MAC key generation. Deprecated attribute.
    @type hash_func: function

    @ivar dh: The Diffie-Hellman algorithm values for this request
    @type dh: DiffieHellman

    @ivar consumer_public_key: The public key sent by the consumer in the associate request
    @type consumer_public_key: six.text_type

    @see: U{OpenID Specs, Mode: associate
        <http://openid.net/specs.bml#mode-associate>}
    @see: AssociateRequest
    """
    session_type = 'DH-SHA1'
    algorithm = hashes.SHA1()
    hash_func = None
    allowed_assoc_types = ['HMAC-SHA1']

    def __init__(self, dh, consumer_public_key):
        self.dh = dh
        if isinstance(consumer_public_key, six.integer_types):
            warnings.warn("Public key should be base64 encoded.", DeprecationWarning)
            consumer_public_key = cryptutil.longToBase64(consumer_public_key)
        # Check if the key can be decoded
        try:
            base64.b64decode(consumer_public_key)
        except (ValueError, TypeError) as error:
            raise ValueError("{!r} is not a valid base64 string: {}".format(consumer_public_key, error))
        self.consumer_public_key = consumer_public_key

    @property
    def consumer_pubkey(self):
        """Return consumer public key as integer."""
        warnings.warn("Attribute consumer_pubkey si deprecated, use consumer_public_key instead.", DeprecationWarning)
        return cryptutil.base64ToLong(self.consumer_public_key)

    @classmethod
    def fromMessage(cls, message):
        """
        @param message: The associate request message
        @type message: openid.message.Message

        @returntype: L{DiffieHellmanSHA1ServerSession}

        @raises ProtocolError: When parameters required to establish the
            session are missing.
        """
        dh_modulus = message.getArg(OPENID_NS, 'dh_modulus')
        dh_gen = message.getArg(OPENID_NS, 'dh_gen')
        if (dh_modulus is None and dh_gen is not None or dh_gen is None and dh_modulus is not None):
            if dh_modulus is None:
                missing = 'modulus'
            else:
                missing = 'generator'

            raise ProtocolError(message,
                                'If non-default modulus or generator is '
                                'supplied, both must be supplied. Missing %s'
                                % (missing,))

        if dh_modulus or dh_gen:
            dh = DiffieHellman(dh_modulus, dh_gen)
        else:
            dh = DiffieHellman.fromDefaults()

        consumer_public_key = message.getArg(OPENID_NS, 'dh_consumer_public')
        if consumer_public_key is None:
            raise ProtocolError(message, "Public key for DH-SHA1 session "
                                "not found in message %s" % (message,))

        return cls(dh, consumer_public_key)

    def answer(self, secret):
        if self.hash_func is not None:
            warnings.warn("Attribute hash_func is deprecated, use algorithm instead.", DeprecationWarning)
            mac_key = self.dh.xorSecret(cryptutil.base64ToLong(self.consumer_public_key), secret, self.hash_func)
            mac_key = oidutil.toBase64(mac_key)
        else:
            mac_key = self.dh.xor_secret(self.consumer_public_key, base64.b64encode(secret), self.algorithm)
        return {
            'dh_server_public': self.dh.public_key,
            'enc_mac_key': mac_key,
        }


class DiffieHellmanSHA256ServerSession(DiffieHellmanSHA1ServerSession):
    session_type = 'DH-SHA256'
    algorithm = hashes.SHA256()
    allowed_assoc_types = ['HMAC-SHA256']


class AssociateRequest(OpenIDRequest):
    """A request to establish an X{association}.

    @cvar mode: "X{C{check_authentication}}"
    @type mode: six.text_type

    @ivar assoc_type: The type of association.  The protocol currently only
        defines one value for this, "X{C{HMAC-SHA1}}".
    @type assoc_type: six.text_type

    @ivar session: An object that knows how to handle association
        requests of a certain type.

    @see: U{OpenID Specs, Mode: associate
        <http://openid.net/specs.bml#mode-associate>}
    """

    mode = "associate"

    session_classes = {
        'no-encryption': PlainTextServerSession,
        'DH-SHA1': DiffieHellmanSHA1ServerSession,
        'DH-SHA256': DiffieHellmanSHA256ServerSession,
    }

    def __init__(self, session, assoc_type, message=None):
        """Construct me.

        The session is assigned directly as a class attribute. See my
        L{class documentation<AssociateRequest>} for its description.
        """
        super(AssociateRequest, self).__init__(message=message)
        self.session = session
        self.assoc_type = assoc_type

    @classmethod
    def fromMessage(klass, message, op_endpoint=UNUSED):
        """Construct me from an OpenID Message.

        @param message: The OpenID associate request
        @type message: openid.message.Message

        @returntype: L{AssociateRequest}
        """
        if message.isOpenID1():
            session_type = message.getArg(OPENID_NS, 'session_type')
            if session_type == 'no-encryption':
                _LOGGER.warning('Received OpenID 1 request with a no-encryption '
                                'assocaition session type. Continuing anyway.')
            elif not session_type:
                session_type = 'no-encryption'

            # in 1.0 assoc_type has default
            assoc_type = message.getArg(OPENID_NS, 'assoc_type', 'HMAC-SHA1')
        else:
            session_type = message.getArg(OPENID2_NS, 'session_type')
            if session_type is None:
                raise ProtocolError(message,
                                    text="session_type missing from request")

            # in 2.0 assoc_type is required
            assoc_type = message.getArg(OPENID2_NS, 'assoc_type')
            if assoc_type is None:
                raise ProtocolError(message,
                                    text="assoc_type missing from request")

        try:
            session_class = klass.session_classes[session_type]
        except KeyError:
            raise ProtocolError(message,
                                "Unknown session type %r" % (session_type,))

        try:
            session = session_class.fromMessage(message)
        except ValueError as why:
            raise ProtocolError(message, 'Error parsing %s session: %s' %
                                (session_class.session_type, six.text_type(why)))

        if assoc_type not in session.allowed_assoc_types:
            fmt = 'Session type %s does not support association type %s'
            raise ProtocolError(message, fmt % (session_type, assoc_type))

        self = klass(session, assoc_type, message=message)
        return self

    def answer(self, assoc):
        """Respond to this request with an X{association}.

        @param assoc: The association to send back.
        @type assoc: L{openid.association.Association}

        @returns: A response with the association information, encrypted
            to the consumer's X{public key} if appropriate.
        @returntype: L{OpenIDResponse}
        """
        response = OpenIDResponse(self)
        response.fields.updateArgs(OPENID_NS, {
            'expires_in': '%d' % (assoc.getExpiresIn(),),
            'assoc_type': self.assoc_type,
            'assoc_handle': assoc.handle,
        })
        response.fields.updateArgs(OPENID_NS,
                                   self.session.answer(assoc.secret))

        if not (self.session.session_type == 'no-encryption' and self.message.isOpenID1()):
            # The session type "no-encryption" did not have a name
            # in OpenID v1, it was just omitted.
            response.fields.setArg(
                OPENID_NS, 'session_type', self.session.session_type)

        return response

    def answerUnsupported(self, message, preferred_association_type=None,
                          preferred_session_type=None):
        """Respond to this request indicating that the association
        type or association session type is not supported."""
        if self.message.isOpenID1():
            raise ProtocolError(self.message)

        response = OpenIDResponse(self)
        response.fields.setArg(OPENID_NS, 'error_code', 'unsupported-type')
        response.fields.setArg(OPENID_NS, 'error', message)

        if preferred_association_type:
            response.fields.setArg(
                OPENID_NS, 'assoc_type', preferred_association_type)

        if preferred_session_type:
            response.fields.setArg(
                OPENID_NS, 'session_type', preferred_session_type)

        return response


class CheckIDRequest(OpenIDRequest):
    """A request to confirm the identity of a user.

    This class handles requests for openid modes X{C{checkid_immediate}}
    and X{C{checkid_setup}}.

    @cvar mode: "X{C{checkid_immediate}}" or "X{C{checkid_setup}}"
    @type mode: six.text_type

    @ivar immediate: Is this an immediate-mode request?
    @type immediate: bool

    @ivar identity: The OP-local identifier being checked.
    @type identity: six.text_type

    @ivar claimed_id: The claimed identifier.  Not present in OpenID 1.x
        messages.
    @type claimed_id: Optional[six.text_type]

    @ivar trust_root: "Are you Frank?" asks the checkid request.  "Who wants
        to know?"  C{trust_root}, that's who.  This URL identifies the party
        making the request, and the user will use that to make her decision
        about what answer she trusts them to have.  Referred to as "realm" in
        OpenID 2.0.
    @type trust_root: six.text_type

    @ivar return_to: The URL to send the user agent back to to reply to this
        request.
    @type return_to: six.text_type

    @ivar assoc_handle: Provided in smart mode requests, a handle for a
        previously established association.  C{None} for dumb mode requests.
    @type assoc_handle: six.text_type
    """

    def __init__(self, identity, return_to, trust_root=None, immediate=False,
                 assoc_handle=None, op_endpoint=None, claimed_id=None, message=None):
        """Construct me.

        These parameters are assigned directly as class attributes, see
        my L{class documentation<CheckIDRequest>} for their descriptions.

        @raises MalformedReturnURL: When the C{return_to} URL is not a URL.
        """
        super(CheckIDRequest, self).__init__(message=message)
        self.assoc_handle = assoc_handle

        # Check the identifier validity. In case of error, create protocol error from the message in the argument.
        if self.message.isOpenID1():
            if identity is None:
                s = "OpenID 1 message did not contain openid.identity"
                raise ProtocolError(message, text=s)
        else:
            if identity is not None and claimed_id is None:
                s = ("OpenID 2.0 message contained openid.identity but not "
                     "claimed_id")
                raise ProtocolError(message, text=s)
            elif identity is None and claimed_id is not None:
                s = ("OpenID 2.0 message contained openid.claimed_id but not "
                     "identity")
                raise ProtocolError(message, text=s)

        self.identity = identity
        self.claimed_id = claimed_id
        self.return_to = return_to
        self.trust_root = trust_root or return_to

        if self.message.isOpenID2() and op_endpoint is None:
            raise ValueError("CheckIDRequest requires op_endpoint argument for OpenID 2.0 requests.")
        self.op_endpoint = op_endpoint

        if immediate:
            self.immediate = True
            self.mode = "checkid_immediate"
        else:
            self.immediate = False
            self.mode = "checkid_setup"

        # Using TrustRoot.parse here is a bit misleading, as we're not
        # parsing return_to as a trust root at all.  However, valid URLs
        # are valid trust roots, so we can use this to get an idea if it
        # is a valid URL.  Not all trust roots are valid return_to URLs,
        # however (particularly ones with wildcards), so this is still a
        # little sketchy.
        if self.return_to is not None and not TrustRoot.parse(self.return_to):
            raise MalformedReturnURL(message, self.return_to)

        # I first thought that checking to see if the return_to is within
        # the trust_root is premature here, a logic-not-decoding thing.  But
        # it was argued that this is really part of data validation.  A
        # request with an invalid trust_root/return_to is broken regardless of
        # application, right?
        if not self.trustRootValid():
            raise UntrustedReturnURL(message, self.return_to, self.trust_root)

    @classmethod
    def fromMessage(klass, message, op_endpoint):
        """Construct me from an OpenID message.

        @raises ProtocolError: When not all required parameters are present
            in the message.

        @raises MalformedReturnURL: When the C{return_to} URL is not a URL.

        @raises UntrustedReturnURL: When the C{return_to} URL is outside
            the C{trust_root}.

        @param message: An OpenID checkid_* request Message
        @type message: openid.message.Message

        @param op_endpoint: The endpoint URL of the server that this
            message was sent to.
        @type op_endpoint: Optional[six.text_type], six.binary_type is deprecated

        @returntype: L{CheckIDRequest}
        """
        mode = message.getArg(OPENID_NS, 'mode')
        assert mode in ('checkid_immediate', 'checkid_setup')
        immediate = bool(mode == 'checkid_immediate')

        return_to = message.getArg(OPENID_NS, 'return_to')
        if message.isOpenID1() and not return_to:
            fmt = "Missing required field 'return_to' from %r"
            raise ProtocolError(message, text=fmt % (message,))

        identity = message.getArg(OPENID_NS, 'identity')
        claimed_id = message.getArg(OPENID_NS, 'claimed_id')
        # There's a case for making self.trust_root be a TrustRoot
        # here.  But if TrustRoot isn't currently part of the "public" API,
        # I'm not sure it's worth doing.

        if message.isOpenID1():
            trust_root_param = 'trust_root'
        else:
            trust_root_param = 'realm'

        # Using 'or' here is slightly different than sending a default
        # argument to getArg, as it will treat no value and an empty
        # string as equivalent.
        trust_root = (message.getArg(OPENID_NS, trust_root_param) or return_to)

        if not message.isOpenID1() and (return_to is trust_root is None):
            raise ProtocolError(message, "openid.realm required when openid.return_to absent")

        assoc_handle = message.getArg(OPENID_NS, 'assoc_handle')

        if op_endpoint is not None:
            op_endpoint = string_to_text(op_endpoint,
                                         "Binary values for op_endpoint are deprecated. Use text input instead.")
        self = klass(identity, return_to, trust_root=trust_root, immediate=immediate, assoc_handle=assoc_handle,
                     op_endpoint=op_endpoint, claimed_id=claimed_id, message=message)
        return self

    def idSelect(self):
        """Is the identifier to be selected by the IDP?

        @returntype: bool
        """
        # So IDPs don't have to import the constant
        return self.identity == IDENTIFIER_SELECT

    def trustRootValid(self):
        """Is my return_to under my trust_root?

        @returntype: bool
        """
        if not self.trust_root:
            return True
        tr = TrustRoot.parse(self.trust_root)
        if tr is None:
            raise MalformedTrustRoot(self.message, self.trust_root)

        if self.return_to is not None:
            return tr.validateURL(self.return_to)
        else:
            return True

    def returnToVerified(self):
        """Does the relying party publish the return_to URL for this
        response under the realm? It is up to the provider to set a
        policy for what kinds of realms should be allowed. This
        return_to URL verification reduces vulnerability to data-theft
        attacks based on open proxies, cross-site-scripting, or open
        redirectors.

        This check should only be performed after making sure that the
        return_to URL matches the realm.

        @see: L{trustRootValid}

        @raises openid.yadis.discover.DiscoveryFailure: if the realm
            URL does not support Yadis discovery (and so does not
            support the verification process).

        @raises openid.fetchers.HTTPFetchingError: if the realm URL
            is not reachable.  When this is the case, the RP may be hosted
            on the user's intranet.

        @returntype: bool

        @returns: True if the realm publishes a document with the
            return_to URL listed

        @since: 2.1.0
        """
        return verifyReturnTo(self.trust_root, self.return_to)

    def answer(self, allow, server_url=None, identity=None, claimed_id=None):
        """Respond to this request.

        @param allow: Allow this user to claim this identity, and allow the
            consumer to have this information?
        @type allow: bool

        @param server_url: DEPRECATED.  Passing C{op_endpoint} to the
            L{Server} constructor makes this optional.

            When an OpenID 1.x immediate mode request does not succeed,
            it gets back a URL where the request may be carried out
            in a not-so-immediate fashion.  Pass my URL in here (the
            fully qualified address of this server's endpoint, i.e.
            C{http://example.com/server}), and I will use it as a base for the
            URL for a new request.

            Optional for requests where C{CheckIDRequest.immediate} is C{False}
            or C{allow} is C{True}.
        @type server_url: Optional[six.text_type], six.binary_type is deprecated

        @param identity: The OP-local identifier to answer with.  Only for use
            when the relying party requested identifier selection.
        @type identity: Optional[six.text_type], six.binary_type is deprecated

        @param claimed_id: The claimed identifier to answer with, for use
            with identifier selection in the case where the claimed identifier
            and the OP-local identifier differ, i.e. when the claimed_id uses
            delegation.

            If C{identity} is provided but this is not, C{claimed_id} will
            default to the value of C{identity}.  When answering requests
            that did not ask for identifier selection, the response
            C{claimed_id} will default to that of the request.

            This parameter is new in OpenID 2.0.
        @type claimed_id: Optional[six.text_type], six.binary_type is deprecated

        @returntype: L{OpenIDResponse}

        @change: Version 2.0 deprecates C{server_url} and adds C{claimed_id}.

        @raises NoReturnError: when I do not have a return_to.
        """
        if identity is not None:
            identity = string_to_text(identity, "Binary values for identity are deprecated. Use text input instead.")
        if claimed_id is not None:
            claimed_id = string_to_text(claimed_id,
                                        "Binary values for claimed_id are deprecated. Use text input instead.")

        if not self.return_to:
            raise NoReturnToError

        if not server_url:
            if not self.message.isOpenID1() and not self.op_endpoint:
                # In other words, that warning I raised in Server.__init__?
                # You should pay attention to it now.
                raise RuntimeError("%s should be constructed with op_endpoint "
                                   "to respond to OpenID 2.0 messages." %
                                   (self,))
            server_url = self.op_endpoint
        else:
            server_url = string_to_text(server_url,
                                        "Binary values for server_url are deprecated. Use text input instead.")

        if allow:
            mode = 'id_res'
        elif self.message.isOpenID1():
            if self.immediate:
                mode = 'id_res'
            else:
                mode = 'cancel'
        else:
            if self.immediate:
                mode = 'setup_needed'
            else:
                mode = 'cancel'

        response = OpenIDResponse(self)

        if claimed_id and self.message.isOpenID1():
            namespace = self.message.getOpenIDNamespace()
            raise VersionError("claimed_id is new in OpenID 2.0 and not "
                               "available for %s" % (namespace,))

        if allow:
            if self.identity == IDENTIFIER_SELECT:
                if not identity:
                    raise ValueError(
                        "This request uses IdP-driven identifier selection."
                        "You must supply an identifier in the response.")
                response_identity = identity
                response_claimed_id = claimed_id or identity

            elif self.identity:
                if identity and (self.identity != identity):
                    normalized_request_identity = urinorm(self.identity)
                    normalized_answer_identity = urinorm(identity)

                    if normalized_request_identity != normalized_answer_identity:
                        raise ValueError(
                            "Request was for identity %r, cannot reply "
                            "with identity %r" % (self.identity, identity))

                # The "identity" value in the response shall always be
                # the same as that in the request, otherwise the RP is
                # likely to not validate the response.
                response_identity = self.identity
                response_claimed_id = self.claimed_id
            else:
                if identity:
                    raise ValueError(
                        "This request specified no identity and you "
                        "supplied %r" % (identity,))
                response_identity = None

            if self.message.isOpenID1() and response_identity is None:
                raise ValueError(
                    "Request was an OpenID 1 request, so response must "
                    "include an identifier."
                )

            response.fields.updateArgs(OPENID_NS, {
                'mode': mode,
                'return_to': self.return_to,
                'response_nonce': mkNonce(),
            })

            if server_url:
                response.fields.setArg(OPENID_NS, 'op_endpoint', server_url)

            if response_identity is not None:
                response.fields.setArg(
                    OPENID_NS, 'identity', response_identity)
                if self.message.isOpenID2():
                    response.fields.setArg(
                        OPENID_NS, 'claimed_id', response_claimed_id)
        else:
            response.fields.setArg(OPENID_NS, 'mode', mode)
            if self.immediate:
                if self.message.isOpenID1() and not server_url:
                    raise ValueError("setup_url is required for allow=False "
                                     "in OpenID 1.x immediate mode.")
                # Make a new request just like me, but with immediate=False.
                setup_request = self.__class__(
                    self.identity, self.return_to, self.trust_root,
                    immediate=False, assoc_handle=self.assoc_handle,
                    op_endpoint=self.op_endpoint, claimed_id=self.claimed_id)

                # XXX: This API is weird.
                setup_request.message = self.message

                setup_url = setup_request.encodeToURL(server_url)
                response.fields.setArg(OPENID_NS, 'user_setup_url', setup_url)

        return response

    def encodeToURL(self, server_url):
        """Encode this request as a URL to GET.

        @param server_url: The URL of the OpenID server to make this request of.
        @type server_url: six.text_type, six.binary_type is deprecated

        @returntype: six.text_type

        @raises NoReturnError: when I do not have a return_to.
        """
        if not self.return_to:
            raise NoReturnToError

        # Imported from the alternate reality where these classes are used
        # in both the client and server code, so Requests are Encodable too.
        # That's right, code imported from alternate realities all for the
        # love of you, id_res/user_setup_url.
        q = {'mode': self.mode,
             'identity': self.identity,
             'claimed_id': self.claimed_id,
             'return_to': self.return_to}
        if self.trust_root:
            if self.message.isOpenID1():
                q['trust_root'] = self.trust_root
            else:
                q['realm'] = self.trust_root
        if self.assoc_handle:
            q['assoc_handle'] = self.assoc_handle

        response = Message(self.message.getOpenIDNamespace())
        response.updateArgs(OPENID_NS, q)
        server_url = string_to_text(server_url, "Binary values for server_url are deprecated. Use text input instead.")
        return response.toURL(server_url)

    def getCancelURL(self):
        """Get the URL to cancel this request.

        Useful for creating a "Cancel" button on a web form so that operation
        can be carried out directly without another trip through the server.

        (Except you probably want to make another trip through the server so
        that it knows that the user did make a decision.  Or you could simulate
        this method by doing C{.answer(False).encodeToURL()})

        @returntype: six.text_type
        @returns: The return_to URL with openid.mode = cancel.

        @raises NoReturnError: when I do not have a return_to.
        """
        if not self.return_to:
            raise NoReturnToError

        if self.immediate:
            raise ValueError("Cancel is not an appropriate response to "
                             "immediate mode requests.")

        response = Message(self.message.getOpenIDNamespace())
        response.setArg(OPENID_NS, 'mode', 'cancel')
        return response.toURL(self.return_to)

    def __repr__(self):
        return '<%s id:%r im:%s tr:%r ah:%r>' % (self.__class__.__name__,
                                                 self.identity,
                                                 self.immediate,
                                                 self.trust_root,
                                                 self.assoc_handle)


class OpenIDResponse(object):
    """I am a response to an OpenID request.

    @ivar request: The request I respond to.
    @type request: L{OpenIDRequest}

    @ivar fields: My parameters as a dictionary with each key mapping to
        one value.  Keys are parameter names with no leading "C{openid.}".
        e.g.  "C{identity}" and "C{mac_key}", never "C{openid.identity}".
    @type fields: L{openid.message.Message}

    @ivar signed: The names of the fields which should be signed.
    @type signed: List[six.text_type]
    """

    # Implementer's note: In a more symmetric client/server
    # implementation, there would be more types of OpenIDResponse
    # object and they would have validated attributes according to the
    # type of response.  But as it is, Response objects in a server are
    # basically write-only, their only job is to go out over the wire,
    # so this is just a loose wrapper around OpenIDResponse.fields.

    def __init__(self, request):
        """Make a response to an L{OpenIDRequest}.

        @type request: L{OpenIDRequest}
        """
        self.request = request
        self.fields = Message(request.message.getOpenIDNamespace())

    def __str__(self):
        return "%s for %s: %s" % (
            self.__class__.__name__,
            self.request.__class__.__name__,
            self.fields)

    def toFormMarkup(self, form_tag_attrs=None):
        """Returns the form markup for this response.

        @param form_tag_attrs: Dictionary of attributes to be added to
            the form tag. 'accept-charset' and 'enctype' have defaults
            that can be overridden. If a value is supplied for
            'action' or 'method', it will be replaced.

        @returntype: six.text_type

        @since: 2.1.0
        """
        return self.fields.toFormMarkup(self.request.return_to,
                                        form_tag_attrs=form_tag_attrs)

    def toHTML(self, form_tag_attrs=None):
        """Returns an HTML document that auto-submits the form markup
        for this response.

        @returntype: six.text_type

        @see: toFormMarkup

        @since: 2.1.?
        """
        return oidutil.autoSubmitHTML(self.toFormMarkup(form_tag_attrs))

    def renderAsForm(self):
        """Returns True if this response's encoding is
        ENCODE_HTML_FORM.  Convenience method for server authors.

        @returntype: bool

        @since: 2.1.0
        """
        return self.whichEncoding() == ENCODE_HTML_FORM

    def needsSigning(self):
        """Does this response require signing?

        @returntype: bool
        """
        return self.fields.getArg(OPENID_NS, 'mode') == 'id_res'

    # implements IEncodable

    def whichEncoding(self):
        """How should I be encoded?

        @returns: one of ENCODE_URL, ENCODE_HTML_FORM, or ENCODE_KVFORM.

        @change: 2.1.0 added the ENCODE_HTML_FORM response.
        """
        if self.request.mode in BROWSER_REQUEST_MODES:
            if self.fields.isOpenID2() and \
               len(self.encodeToURL()) > OPENID1_URL_LIMIT:
                # Message can be encoded as HTML form only if it's OpenID 2.0.
                return ENCODE_HTML_FORM
            else:
                return ENCODE_URL
        else:
            return ENCODE_KVFORM

    def encodeToURL(self):
        """Encode a response as a URL for the user agent to GET.

        You will generally use this URL with a HTTP redirect.

        @returns: A URL to direct the user agent back to.
        @returntype: six.text_type
        """
        return self.fields.toURL(self.request.return_to)

    def addExtension(self, extension_response):
        """
        Add an extension response to this response message.

        @param extension_response: An object that implements the
            extension interface for adding arguments to an OpenID
            message.
        @type extension_response: L{openid.extension}

        @returntype: None
        """
        extension_response.toMessage(self.fields)

    def encodeToKVForm(self):
        """Encode a response in key-value colon/newline format.

        This is a machine-readable format used to respond to messages which
        came directly from the consumer and not through the user agent.

        @see: OpenID Specs,
           U{Key-Value Colon/Newline format<http://openid.net/specs.bml#keyvalue>}

        @returntype: six.text_type
        """
        return self.fields.toKVForm()


class WebResponse(object):
    """I am a response to an OpenID request in terms a web server understands.

    I generally come from an L{Encoder}, either directly or from
    L{Server.encodeResponse}.

    @ivar code: The HTTP code of this response.
    @type code: int

    @ivar headers: Headers to include in this response.
    @type headers: dict

    @ivar body: The body of this response.
    @type body: six.text_type
    """

    def __init__(self, code=HTTP_OK, headers=None, body=""):
        """Construct me.

        These parameters are assigned directly as class attributes, see
        my L{class documentation<WebResponse>} for their descriptions.
        """
        self.code = code
        if headers is not None:
            self.headers = headers
        else:
            self.headers = {}
        self.body = body


class Signatory(object):
    """I sign things.

    I also check signatures.

    All my state is encapsulated in an
    L{OpenIDStore<openid.store.interface.OpenIDStore>}, which means
    I'm not generally pickleable but I am easy to reconstruct.

    @cvar SECRET_LIFETIME: The number of seconds a secret remains valid.
    @type SECRET_LIFETIME: int
    """

    SECRET_LIFETIME = 14 * 24 * 60 * 60  # 14 days, in seconds

    # keys have a bogus server URL in them because the filestore
    # really does expect that key to be a URL.  This seems a little
    # silly for the server store, since I expect there to be only one
    # server URL.
    _normal_key = 'http://localhost/|normal'
    _dumb_key = 'http://localhost/|dumb'

    def __init__(self, store):
        """Create a new Signatory.

        @param store: The back-end where my associations are stored.
        @type store: L{openid.store.interface.OpenIDStore}
        """
        assert store is not None
        self.store = store

    def verify(self, assoc_handle, message):
        """Verify that the signature for some data is valid.

        @param assoc_handle: The handle of the association used to sign the
            data.
        @type assoc_handle: six.text_type, six.binary_type is deprecated

        @param message: The signed message to verify
        @type message: openid.message.Message

        @returns: C{True} if the signature is valid, C{False} if not.
        @returntype: bool
        """
        assoc_handle = string_to_text(assoc_handle,
                                      "Binary values for assoc_handle are deprecated. Use text input instead.")
        assoc = self.getAssociation(assoc_handle, dumb=True)
        if not assoc:
            _LOGGER.info("failed to get assoc with handle %r to verify message %r", assoc_handle, message)
            return False

        try:
            valid = assoc.checkMessageSignature(message)
        except ValueError as ex:
            _LOGGER.info("Error in verifying %s with %s: %s", message, assoc, ex)
            return False
        return valid

    def sign(self, response):
        """Sign a response.

        I take a L{OpenIDResponse}, create a signature for everything
        in its L{signed<OpenIDResponse.signed>} list, and return a new
        copy of the response object with that signature included.

        @param response: A response to sign.
        @type response: L{OpenIDResponse}

        @returns: A signed copy of the response.
        @returntype: L{OpenIDResponse}
        """
        signed_response = deepcopy(response)
        assoc_handle = response.request.assoc_handle
        if assoc_handle:
            # normal mode
            # disabling expiration check because even if the association
            # is expired, we still need to know some properties of the
            # association so that we may preserve those properties when
            # creating the fallback association.
            assoc = self.getAssociation(assoc_handle, dumb=False,
                                        checkExpiration=False)

            if not assoc or assoc.expiresIn <= 0:
                # fall back to dumb mode
                signed_response.fields.setArg(
                    OPENID_NS, 'invalidate_handle', assoc_handle)
                assoc_type = assoc and assoc.assoc_type or 'HMAC-SHA1'
                if assoc and assoc.expiresIn <= 0:
                    # now do the clean-up that the disabled checkExpiration
                    # code didn't get to do.
                    self.invalidate(assoc_handle, dumb=False)
                assoc = self.createAssociation(dumb=True, assoc_type=assoc_type)
        else:
            # dumb mode.
            assoc = self.createAssociation(dumb=True)

        try:
            signed_response.fields = assoc.signMessage(signed_response.fields)
        except kvform.KVFormError as err:
            raise EncodingError(response, explanation=six.text_type(err))
        return signed_response

    def createAssociation(self, dumb=True, assoc_type='HMAC-SHA1'):
        """Make a new association.

        @param dumb: Is this association for a dumb-mode transaction?
        @type dumb: bool

        @param assoc_type: The type of association to create.  Currently
            there is only one type defined, C{HMAC-SHA1}.
        @type assoc_type: six.text_type, six.binary_type is deprecated

        @returns: the new association.
        @returntype: L{openid.association.Association}
        """
        assoc_type = string_to_text(assoc_type, "Binary values for assoc_type are deprecated. Use text input instead.")

        secret = os.urandom(getSecretSize(assoc_type))
        uniq = oidutil.toBase64(os.urandom(4))
        handle = '{%s}{%x}{%s}' % (assoc_type, int(time.time()), uniq)

        assoc = Association.fromExpiresIn(
            self.SECRET_LIFETIME, handle, secret, assoc_type)

        if dumb:
            key = self._dumb_key
        else:
            key = self._normal_key
        self.store.storeAssociation(key, assoc)
        return assoc

    def getAssociation(self, assoc_handle, dumb, checkExpiration=True):
        """Get the association with the specified handle.

        @type assoc_handle: six.text_type, six.binary_type is deprecated

        @param dumb: Is this association used with dumb mode?
        @type dumb: bool

        @returns: the association, or None if no valid association with that
            handle was found.
        @returntype: L{openid.association.Association}
        """
        # Hmm.  We've created an interface that deals almost entirely with
        # assoc_handles.  The only place outside the Signatory that uses this
        # (and thus the only place that ever sees Association objects) is
        # when creating a response to an association request, as it must have
        # the association's secret.

        if assoc_handle is None:
            raise ValueError("assoc_handle must not be None")
        assoc_handle = string_to_text(assoc_handle,
                                      "Binary values for assoc_handle are deprecated. Use text input instead.")

        if dumb:
            key = self._dumb_key
        else:
            key = self._normal_key
        assoc = self.store.getAssociation(key, assoc_handle)
        if assoc is not None and assoc.expiresIn <= 0:
            _LOGGER.info("requested %sdumb key %r is expired (by %s seconds)",
                         (not dumb) and 'not-' or '', assoc_handle, assoc.expiresIn)
            if checkExpiration:
                self.store.removeAssociation(key, assoc_handle)
                assoc = None
        return assoc

    def invalidate(self, assoc_handle, dumb):
        """Invalidates the association with the given handle.

        @type assoc_handle: six.text_type, six.binary_type is deprecated

        @param dumb: Is this association used with dumb mode?
        @type dumb: bool
        """
        if dumb:
            key = self._dumb_key
        else:
            key = self._normal_key
        assoc_handle = string_to_text(assoc_handle,
                                      "Binary values for assoc_handle are deprecated. Use text input instead.")
        self.store.removeAssociation(key, assoc_handle)


class Encoder(object):
    """I encode responses in to L{WebResponses<WebResponse>}.

    If you don't like L{WebResponses<WebResponse>}, you can do
    your own handling of L{OpenIDResponses<OpenIDResponse>} with
    L{OpenIDResponse.whichEncoding}, L{OpenIDResponse.encodeToURL}, and
    L{OpenIDResponse.encodeToKVForm}.
    """

    responseFactory = WebResponse

    def encode(self, response):
        """Encode a response to a L{WebResponse}.

        @raises EncodingError: When I can't figure out how to encode this
            message.
        """
        encode_as = response.whichEncoding()
        if encode_as == ENCODE_KVFORM:
            wr = self.responseFactory(body=response.encodeToKVForm())
            if isinstance(response, Exception):
                wr.code = HTTP_ERROR
        elif encode_as == ENCODE_URL:
            location = response.encodeToURL()
            wr = self.responseFactory(code=HTTP_REDIRECT,
                                      headers={'location': location})
        elif encode_as == ENCODE_HTML_FORM:
            wr = self.responseFactory(code=HTTP_OK,
                                      body=response.toHTML())
        else:
            # Can't encode this to a protocol message.  You should probably
            # render it to HTML and show it to the user.
            raise EncodingError(response)
        return wr


class SigningEncoder(Encoder):
    """I encode responses in to L{WebResponses<WebResponse>}, signing them when required.
    """

    def __init__(self, signatory):
        """Create a L{SigningEncoder}.

        @param signatory: The L{Signatory} I will make signatures with.
        @type signatory: L{Signatory}
        """
        self.signatory = signatory

    def encode(self, response):
        """Encode a response to a L{WebResponse}, signing it first if appropriate.

        @raises EncodingError: When I can't figure out how to encode this
            message.

        @raises AlreadySigned: When this response is already signed.

        @returntype: L{WebResponse}
        """
        # the isinstance is a bit of a kludge... it means there isn't really
        # an adapter to make the interfaces quite match.
        if (not isinstance(response, Exception)) and response.needsSigning():
            if not self.signatory:
                raise ValueError(
                    "Must have a store to sign this request: %s" %
                    (response,), response)
            if response.fields.hasKey(OPENID_NS, 'sig'):
                raise AlreadySigned(response)
            response = self.signatory.sign(response)
        return super(SigningEncoder, self).encode(response)


class Decoder(object):
    """I decode an incoming web request in to a L{OpenIDRequest}.
    """

    _handlers = {
        'checkid_setup': CheckIDRequest.fromMessage,
        'checkid_immediate': CheckIDRequest.fromMessage,
        'check_authentication': CheckAuthRequest.fromMessage,
        'associate': AssociateRequest.fromMessage,
    }

    def __init__(self, server):
        """Construct a Decoder.

        @param server: The server which I am decoding requests for.
            (Necessary because some replies reference their server.)
        @type server: L{Server}
        """
        self.server = server

    def decode(self, query):
        """I transform query parameters into an L{OpenIDRequest}.

        If the query does not seem to be an OpenID request at all, I return
        C{None}.

        @param query: The query parameters as a dictionary with each
            key mapping to one value.
        @type query: dict

        @raises ProtocolError: When the query does not seem to be a valid
            OpenID request.

        @returntype: L{OpenIDRequest}
        """
        if not query:
            return None

        try:
            message = Message.fromPostArgs(query)
        except InvalidOpenIDNamespace as err:
            # It's useful to have a Message attached to a ProtocolError, so we
            # override the bad ns value to build a Message out of it.  Kinda
            # kludgy, since it's made of lies, but the parts that aren't lies
            # are more useful than a 'None'.
            query = query.copy()
            query['openid.ns'] = OPENID2_NS
            message = Message.fromPostArgs(query)
            raise ProtocolError(message, six.text_type(err))
        except InvalidNamespace as err:
            # If openid.ns is OK, but there is problem with other namespaces
            # We keep only bare parts of query and we try to make a ProtocolError from it
            query = [(key, value) for key, value in query.items() if key.count('.') < 2]
            message = Message.fromPostArgs(dict(query))
            raise ProtocolError(message, six.text_type(err))

        mode = message.getArg(OPENID_NS, 'mode')
        if not mode:
            fmt = "No mode value in message %s"
            raise ProtocolError(message, text=fmt % (message,))

        handler = self._handlers.get(mode, self.defaultDecoder)
        return handler(message, self.server.op_endpoint)

    def defaultDecoder(self, message, server):
        """Called to decode queries when no handler for that mode is found.

        @raises ProtocolError: This implementation always raises
            L{ProtocolError}.
        """
        mode = message.getArg(OPENID_NS, 'mode')
        fmt = "Unrecognized OpenID mode %r"
        raise ProtocolError(message, text=fmt % (mode,))


class Server(object):
    """I handle requests for an OpenID server.

    Some types of requests (those which are not C{checkid} requests) may be
    handed to my L{handleRequest} method, and I will take care of it and
    return a response.

    For your convenience, I also provide an interface to L{Decoder.decode}
    and L{SigningEncoder.encode} through my methods L{decodeRequest} and
    L{encodeResponse}.

    All my state is encapsulated in an
    L{OpenIDStore<openid.store.interface.OpenIDStore>}, which means
    I'm not generally pickleable but I am easy to reconstruct.

    Example::

        oserver = Server(FileOpenIDStore(data_path), "http://example.com/op")
        request = oserver.decodeRequest(query)
        if request.mode in ['checkid_immediate', 'checkid_setup']:
            if self.isAuthorized(request.identity, request.trust_root):
                response = request.answer(True)
            elif request.immediate:
                response = request.answer(False)
            else:
                self.showDecidePage(request)
                return
        else:
            response = oserver.handleRequest(request)

        webresponse = oserver.encode(response)

    @ivar signatory: I'm using this for associate requests and to sign things.
    @type signatory: L{Signatory}

    @ivar decoder: I'm using this to decode things.
    @type decoder: L{Decoder}

    @ivar encoder: I'm using this to encode things.
    @type encoder: L{Encoder}

    @ivar op_endpoint: My URL.
    @type op_endpoint: six.text_type

    @ivar negotiator: I use this to determine which kinds of
        associations I can make and how.
    @type negotiator: L{openid.association.SessionNegotiator}
    """

    signatoryClass = Signatory
    encoderClass = SigningEncoder
    decoderClass = Decoder

    def __init__(self, store, op_endpoint=None, signatoryClass=None, encoderClass=None, decoderClass=None):
        """A new L{Server}.

        @param store: The back-end where my associations are stored.
        @type store: L{openid.store.interface.OpenIDStore}

        @param op_endpoint: My URL, the fully qualified address of this
            server's endpoint, i.e. C{http://example.com/server}
        @type op_endpoint: six.text_type, six.binary_type is deprecated

        @change: C{op_endpoint} is new in library version 2.0.  It
            currently defaults to C{None} for compatibility with
            earlier versions of the library, but you must provide it
            if you want to respond to any version 2 OpenID requests.
        """
        self.store = store
        if signatoryClass is None:
            signatoryClass = self.signatoryClass
            if signatoryClass != Server.signatoryClass:
                warnings.warn("Attribute signatoryClass on Server class is deprecated."
                              "Use signatoryClass argument of __init__ instead.", DeprecationWarning)
        self.signatory = signatoryClass(self.store)
        if encoderClass is None:
            encoderClass = self.encoderClass
            if encoderClass != Server.encoderClass:
                warnings.warn("Attribute encoderClass on Server class is deprecated."
                              "Use encoderClass argument of __init__ instead.", DeprecationWarning)
        self.encoder = encoderClass(self.signatory)
        if decoderClass is None:
            decoderClass = self.decoderClass
            if decoderClass != Server.decoderClass:
                warnings.warn("Attribute decoderClass on Server class is deprecated."
                              "Use decoderClass argument of __init__ instead.", DeprecationWarning)
        self.decoder = decoderClass(self)
        self.negotiator = default_negotiator.copy()

        if not op_endpoint:
            warnings.warn("%s.%s constructor requires op_endpoint parameter "
                          "for OpenID 2.0 servers" %
                          (self.__class__.__module__, self.__class__.__name__),
                          stacklevel=2)
        self.op_endpoint = string_to_text(op_endpoint,
                                          "Binary values for op_endpoint are deprecated. Use text input instead.")

    def handleRequest(self, request):
        """Handle a request.

        Give me a request, I will give you a response.  Unless it's a type
        of request I cannot handle myself, in which case I will raise
        C{NotImplementedError}.  In that case, you can handle it yourself,
        or add a method to me for handling that request type.

        @raises NotImplementedError: When I do not have a handler defined
            for that type of request.

        @returntype: L{OpenIDResponse}
        """
        handler = getattr(self, 'openid_' + request.mode, None)
        if handler is not None:
            return handler(request)
        else:
            raise NotImplementedError(
                "%s has no handler for a request of mode %r." %
                (self, request.mode))

    def openid_check_authentication(self, request):
        """Handle and respond to C{check_authentication} requests.

        @returntype: L{OpenIDResponse}
        """
        return request.answer(self.signatory)

    def openid_associate(self, request):
        """Handle and respond to C{associate} requests.

        @returntype: L{OpenIDResponse}
        """
        # XXX: TESTME
        assoc_type = request.assoc_type
        session_type = request.session.session_type
        if self.negotiator.isAllowed(assoc_type, session_type):
            assoc = self.signatory.createAssociation(dumb=False,
                                                     assoc_type=assoc_type)
            return request.answer(assoc)
        else:
            message = ('Association type %r is not supported with '
                       'session type %r' % (assoc_type, session_type))
            (preferred_assoc_type, preferred_session_type) = self.negotiator.getAllowedType()
            return request.answerUnsupported(
                message,
                preferred_assoc_type,
                preferred_session_type)

    def decodeRequest(self, query):
        """Transform query parameters into an L{OpenIDRequest}.

        If the query does not seem to be an OpenID request at all, I return
        C{None}.

        @param query: The query parameters as a dictionary with each
            key mapping to one value.
        @type query: dict

        @raises ProtocolError: When the query does not seem to be a valid
            OpenID request.

        @returntype: L{OpenIDRequest}

        @see: L{Decoder.decode}
        """
        return self.decoder.decode(query)

    def encodeResponse(self, response):
        """Encode a response to a L{WebResponse}, signing it first if appropriate.

        @raises EncodingError: When I can't figure out how to encode this
            message.

        @raises AlreadySigned: When this response is already signed.

        @returntype: L{WebResponse}

        @see: L{SigningEncoder.encode}
        """
        return self.encoder.encode(response)


class ProtocolError(Exception):
    """A message did not conform to the OpenID protocol.

    @ivar message: The query that is failing to be a valid OpenID request.
    @type message: openid.message.Message
    """

    def __init__(self, message, text=None, reference=None, contact=None):
        """When an error occurs.

        @param message: The message that is failing to be a valid
            OpenID request.
        @type message: openid.message.Message

        @param text: A message about the encountered error.  Set as C{args[0]}.
        @type text: six.text_type, six.binary_type is deprecated
        """
        self.openid_message = message
        self.reference = reference
        self.contact = contact
        assert not isinstance(message, six.string_types)
        if text is not None:
            text = string_to_text(text, "Binary values for text are deprecated. Use text input instead.")
        Exception.__init__(self, text)

    def getReturnTo(self):
        """Get the return_to argument from the request, if any.

        @returntype: six.text_type
        """
        if self.openid_message is None:
            return None
        else:
            return self.openid_message.getArg(OPENID_NS, 'return_to')

    def hasReturnTo(self):
        """Did this request have a return_to parameter?

        @returntype: bool
        """
        return self.getReturnTo() is not None

    def toMessage(self):
        """Generate a Message object for sending to the relying party,
        after encoding.
        """
        namespace = self.openid_message.getOpenIDNamespace()
        reply = Message(namespace)
        reply.setArg(OPENID_NS, 'mode', 'error')
        reply.setArg(OPENID_NS, 'error', six.text_type(self))

        if self.contact is not None:
            reply.setArg(OPENID_NS, 'contact', six.text_type(self.contact))

        if self.reference is not None:
            reply.setArg(OPENID_NS, 'reference', six.text_type(self.reference))

        return reply

    # implements IEncodable

    def encodeToURL(self):
        return self.toMessage().toURL(self.getReturnTo())

    def encodeToKVForm(self):
        return self.toMessage().toKVForm()

    def toFormMarkup(self):
        """Encode to HTML form markup for POST.

        @since: 2.1.0
        """
        return self.toMessage().toFormMarkup(self.getReturnTo())

    def toHTML(self):
        """Encode to a full HTML page, wrapping the form markup in a page
        that will autosubmit the form.

        @since: 2.1.?
        """
        return oidutil.autoSubmitHTML(self.toFormMarkup())

    def whichEncoding(self):
        """How should I be encoded?

        @returns: one of ENCODE_URL, ENCODE_KVFORM, or None.  If None,
            I cannot be encoded as a protocol message and should be
            displayed to the user.
        """
        if self.hasReturnTo():
            if self.openid_message.isOpenID2() and \
               len(self.encodeToURL()) > OPENID1_URL_LIMIT:
                # Message can be encoded as HTML form only if it's OpenID 2.0.
                return ENCODE_HTML_FORM
            else:
                return ENCODE_URL

        if self.openid_message is None:
            return None

        mode = self.openid_message.getArg(OPENID_NS, 'mode')
        if mode:
            if mode not in BROWSER_REQUEST_MODES:
                return ENCODE_KVFORM

        # According to the OpenID spec as of this writing, we are probably
        # supposed to switch on request type here (GET versus POST) to figure
        # out if we're supposed to print machine-readable or human-readable
        # content at this point.  GET/POST seems like a pretty lousy way of
        # making the distinction though, as it's just as possible that the
        # user agent could have mistakenly been directed to post to the
        # server URL.

        # Basically, if your request was so broken that you didn't manage to
        # include an openid.mode, I'm not going to worry too much about
        # returning you something you can't parse.
        return None


class VersionError(Exception):
    """Raised when an operation was attempted that is not compatible with
    the protocol version being used."""


class NoReturnToError(Exception):
    """Raised when a response to a request cannot be generated because
    the request contains no return_to URL.
    """
    pass


class EncodingError(Exception):
    """Could not encode this as a protocol message.

    You should probably render it and show it to the user.

    @ivar response: The response that failed to encode.
    @type response: L{OpenIDResponse}
    """

    def __init__(self, response, explanation=None):
        Exception.__init__(self, response)
        self.response = response
        self.explanation = explanation

    def __str__(self):
        if self.explanation:
            s = '%s: %s' % (self.__class__.__name__,
                            self.explanation)
        else:
            s = '%s for Response %s' % (
                self.__class__.__name__, self.response)
        return s


class AlreadySigned(EncodingError):
    """This response is already signed."""


class UntrustedReturnURL(ProtocolError):
    """A return_to is outside the trust_root."""

    def __init__(self, message, return_to, trust_root):
        ProtocolError.__init__(self, message)
        self.return_to = return_to
        self.trust_root = trust_root

    def __str__(self):
        return "return_to %r not under trust_root %r" % (self.return_to,
                                                         self.trust_root)


class MalformedReturnURL(ProtocolError):
    """The return_to URL doesn't look like a valid URL."""

    def __init__(self, openid_message, return_to):
        self.return_to = return_to
        ProtocolError.__init__(self, openid_message)


class MalformedTrustRoot(ProtocolError):
    """The trust root is not well-formed.

    @see: OpenID Specs, U{openid.trust_root<http://openid.net/specs.bml#mode-checkid_immediate>}
    """
    pass


# class IEncodable: # Interface
#     def encodeToURL(return_to):
#         """Encode a response as a URL for redirection.
#
#         @returns: A URL to direct the user agent back to.
#         @returntype: str
#         """
#         pass
#
#     def encodeToKvform():
#         """Encode a response in key-value colon/newline format.
#
#         This is a machine-readable format used to respond to messages which
#         came directly from the consumer and not through the user agent.
#
#         @see: OpenID Specs,
#            U{Key-Value Colon/Newline format<http://openid.net/specs.bml#keyvalue>}
#
#         @returntype: str
#         """
#         pass
#
#     def whichEncoding():
#         """How should I be encoded?
#
#         @returns: one of ENCODE_URL, ENCODE_KVFORM, or None.  If None,
#             I cannot be encoded as a protocol message and should be
#             displayed to the user.
#         """
#         pass
