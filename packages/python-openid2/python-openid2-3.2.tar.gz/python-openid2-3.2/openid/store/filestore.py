"""This module contains an C{L{OpenIDStore}} implementation backed by flat files."""
from __future__ import unicode_literals

import logging
import os
import os.path
import string
import time
from errno import EEXIST, ENOENT
from hashlib import sha1
from tempfile import mkstemp

from openid import oidutil
from openid.association import Association
from openid.oidutil import string_to_text
from openid.store import nonce
from openid.store.interface import OpenIDStore

_LOGGER = logging.getLogger(__name__)

_filename_allowed = string.ascii_letters + string.digits + '.'
_isFilenameSafe = set(_filename_allowed).__contains__


def _safe64(s):
    h64 = oidutil.toBase64(sha1(s.encode('utf-8')).digest())
    h64 = h64.replace('+', '_')
    h64 = h64.replace('/', '.')
    h64 = h64.replace('=', '')
    return h64


def _filenameEscape(s):
    filename_chunks = []
    for c in s:
        if _isFilenameSafe(c):
            filename_chunks.append(c)
        else:
            filename_chunks.append('_%02X' % ord(c))
    return ''.join(filename_chunks)


def _removeIfPresent(filename):
    """Attempt to remove a file, returning whether the file existed at
    the time of the call.

    six.text_type -> bool
    """
    try:
        os.unlink(filename)
    except OSError as why:
        if why.errno == ENOENT:
            # Someone beat us to it, but it's gone, so that's OK
            return 0
        else:
            raise
    else:
        # File was present
        return 1


def _ensureDir(dir_name):
    """Create dir_name as a directory if it does not exist. If it
    exists, make sure that it is, in fact, a directory.

    Can raise OSError

    six.text_type -> NoneType
    """
    try:
        os.makedirs(dir_name)
    except OSError as why:
        if why.errno != EEXIST or not os.path.isdir(dir_name):
            raise


class FileOpenIDStore(OpenIDStore):
    """
    This is a filesystem-based store for OpenID associations and
    nonces.  This store should be safe for use in concurrent systems
    on both windows and unix (excluding NFS filesystems).  There are a
    couple race conditions in the system, but those failure cases have
    been set up in such a way that the worst-case behavior is someone
    having to try to log in a second time.

    Most of the methods of this class are implementation details.
    People wishing to just use this store need only pay attention to
    the C{L{__init__}} method.

    Methods of this object can raise OSError if unexpected filesystem
    conditions, such as bad permissions or missing directories, occur.
    """

    def __init__(self, directory):
        """
        Initializes a new FileOpenIDStore.  This initializes the
        nonce and association directories, which are subdirectories of
        the directory passed in.

        @param directory: This is the directory to put the store
            directories in.
        @type directory: six.text_type, six.binary_type is deprecated
        """
        # Make absolute
        directory = os.path.normpath(os.path.abspath(directory))

        self.nonce_dir = os.path.join(directory, 'nonces')

        self.association_dir = os.path.join(directory, 'associations')

        # Temp dir must be on the same filesystem as the assciations
        # directory
        self.temp_dir = os.path.join(directory, 'temp')

        self.max_nonce_age = 6 * 60 * 60  # Six hours, in seconds

        self._setup()

    def _setup(self):
        """Make sure that the directories in which we store our data
        exist.

        () -> NoneType
        """
        _ensureDir(self.nonce_dir)
        _ensureDir(self.association_dir)
        _ensureDir(self.temp_dir)

    def _mktemp(self):
        """Create a temporary file on the same filesystem as
        self.association_dir.

        The temporary directory should not be cleaned if there are any
        processes using the store. If there is no active process using
        the store, it is safe to remove all of the files in the
        temporary directory.

        () -> (file, six.text_type)
        """
        fd, name = mkstemp(dir=self.temp_dir)
        try:
            file_obj = os.fdopen(fd, 'wb')
            return file_obj, name
        except Exception:
            # If there was an error, don't leave the temporary file
            # around.
            _removeIfPresent(name)
            raise

    def getAssociationFilename(self, server_url, handle):
        """Create a unique filename for a given server url and
        handle. This implementation does not assume anything about the
        format of the handle. The filename that is returned will
        contain the domain name from the server URL for ease of human
        inspection of the data directory.

        (six.text_type, six.text_type) -> six.text_type, six.binary_type is deprecated
        """
        server_url = string_to_text(server_url, "Binary values for server_url are deprecated. Use text input instead.")
        handle = string_to_text(handle, "Binary values for handle are deprecated. Use text input instead.")

        if server_url.find('://') == -1:
            raise ValueError('Bad server URL: %r' % server_url)

        proto, rest = server_url.split('://', 1)
        domain = _filenameEscape(rest.split('/', 1)[0])
        url_hash = _safe64(server_url)
        if handle:
            handle_hash = _safe64(handle)
        else:
            handle_hash = ''

        filename = '%s-%s-%s-%s' % (proto, domain, url_hash, handle_hash)

        return os.path.join(self.association_dir, filename)

    def storeAssociation(self, server_url, association):
        """Store an association in the association directory.

        (six.text_type, Association) -> NoneType, six.binary_type is deprecated
        """
        server_url = string_to_text(server_url, "Binary values for server_url are deprecated. Use text input instead.")

        association_s = association.serialize()
        filename = self.getAssociationFilename(server_url, association.handle)
        tmp_file, tmp = self._mktemp()

        try:
            try:
                tmp_file.write(association_s.encode('utf-8'))
                os.fsync(tmp_file.fileno())
            finally:
                tmp_file.close()

            try:
                os.rename(tmp, filename)
            except OSError as why:
                if why.errno != EEXIST:
                    raise

                # We only expect EEXIST to happen only on Windows. It's
                # possible that we will succeed in unlinking the existing
                # file, but not in putting the temporary file in place.
                try:
                    os.unlink(filename)
                except OSError as why:
                    if why.errno == ENOENT:
                        pass
                    else:
                        raise

                # Now the target should not exist. Try renaming again,
                # giving up if it fails.
                os.rename(tmp, filename)
        except Exception:
            # If there was an error, don't leave the temporary file
            # around.
            _removeIfPresent(tmp)
            raise

    def getAssociation(self, server_url, handle=None):
        """Retrieve an association. If no handle is specified, return
        the association with the latest expiration.

        (six.text_type, Optional[six.text_type]) -> Association or NoneType, six.binary_type is deprecated
        """
        server_url = string_to_text(server_url, "Binary values for server_url are deprecated. Use text input instead.")
        if handle is not None:
            handle = string_to_text(handle, "Binary values for handle are deprecated. Use text input instead.")

        if handle is None:
            handle = ''

        # The filename with the empty handle is a prefix of all other
        # associations for the given server URL.
        filename = self.getAssociationFilename(server_url, handle)

        if handle:
            return self._getAssociation(filename)
        else:
            association_files = os.listdir(self.association_dir)
            matching_files = []
            # strip off the path to do the comparison
            name = os.path.basename(filename)
            for association_file in association_files:
                if association_file.startswith(name):
                    matching_files.append(association_file)

            matching_associations = []
            # read the matching files and sort by time issued
            for name in matching_files:
                full_name = os.path.join(self.association_dir, name)
                association = self._getAssociation(full_name)
                if association is not None:
                    matching_associations.append(
                        (association.issued, association))

            matching_associations.sort()

            # return the most recently issued one.
            if matching_associations:
                (_, assoc) = matching_associations[-1]
                return assoc
            else:
                return None

    def _getAssociation(self, filename):
        try:
            assoc_file = open(filename, 'rb')
        except IOError as why:
            if why.errno == ENOENT:
                # No association exists for that URL and handle
                return None
            else:
                raise
        else:
            try:
                assoc_s = assoc_file.read()
            finally:
                assoc_file.close()

            try:
                association = Association.deserialize(assoc_s.decode('utf-8'))
            except ValueError:
                _removeIfPresent(filename)
                return None

        # Clean up expired associations
        if association.getExpiresIn() == 0:
            _removeIfPresent(filename)
            return None
        else:
            return association

    def removeAssociation(self, server_url, handle):
        """Remove an association if it exists. Do nothing if it does not.

        (six.text_type, six.text_type) -> bool, six.binary_type is deprecated
        """
        server_url = string_to_text(server_url, "Binary values for server_url are deprecated. Use text input instead.")
        handle = string_to_text(handle, "Binary values for handle are deprecated. Use text input instead.")

        assoc = self.getAssociation(server_url, handle)
        if assoc is None:
            return 0
        else:
            filename = self.getAssociationFilename(server_url, handle)
            return _removeIfPresent(filename)

    def useNonce(self, server_url, timestamp, salt):
        """Return whether this nonce is valid.

        @type server_url: six.text_type, six.binary_type is deprecated
        @rtype: bool
        """
        server_url = string_to_text(server_url, "Binary values for server_url are deprecated. Use text input instead.")

        if abs(timestamp - time.time()) > nonce.SKEW:
            return False

        if server_url:
            proto, rest = server_url.split('://', 1)
        else:
            # Create empty proto / rest values for empty server_url,
            # which is part of a consumer-generated nonce.
            proto, rest = '', ''

        domain = _filenameEscape(rest.split('/', 1)[0])
        url_hash = _safe64(server_url)
        salt_hash = _safe64(salt)

        filename = '%08x-%s-%s-%s-%s' % (timestamp, proto, domain,
                                         url_hash, salt_hash)

        filename = os.path.join(self.nonce_dir, filename)
        try:
            fd = os.open(filename, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o200)
        except OSError as why:
            if why.errno == EEXIST:
                return False
            else:
                raise
        else:
            os.close(fd)
            return True

    def _allAssocs(self):
        all_associations = []

        association_filenames = [os.path.join(self.association_dir, f) for f in os.listdir(self.association_dir)]
        for association_filename in association_filenames:
            try:
                association_file = open(association_filename, 'rb')
            except IOError as why:
                if why.errno == ENOENT:
                    _LOGGER.exception("%s disappeared during %s._allAssocs",
                                      association_filename, self.__class__.__name__)
                else:
                    raise
            else:
                try:
                    assoc_s = association_file.read()
                finally:
                    association_file.close()

                # Remove expired or corrupted associations
                try:
                    association = Association.deserialize(assoc_s.decode('utf-8'))
                except ValueError:
                    _removeIfPresent(association_filename)
                else:
                    all_associations.append(
                        (association_filename, association))

        return all_associations

    def cleanup(self):
        """Remove expired entries from the database. This is
        potentially expensive, so only run when it is acceptable to
        take time.

        () -> NoneType
        """
        self.cleanupAssociations()
        self.cleanupNonces()

    def cleanupAssociations(self):
        removed = 0
        for assoc_filename, assoc in self._allAssocs():
            if assoc.getExpiresIn() == 0:
                _removeIfPresent(assoc_filename)
                removed += 1
        return removed

    def cleanupNonces(self):
        nonces = os.listdir(self.nonce_dir)
        now = time.time()

        removed = 0
        # Check all nonces for expiry
        for nonce_fname in nonces:
            timestamp = nonce_fname.split('-', 1)[0]
            timestamp = int(timestamp, 16)
            if abs(timestamp - now) > nonce.SKEW:
                filename = os.path.join(self.nonce_dir, nonce_fname)
                _removeIfPresent(filename)
                removed += 1
        return removed
