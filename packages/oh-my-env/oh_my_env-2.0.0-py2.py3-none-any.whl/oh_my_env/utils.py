# coding=utf8

import six
from cryptography.fernet import Fernet


_KEY = b'BSD4Uvd3rlKxSRLRxeq6fBUBtewwk5tJD8VtJOnQiK8='
_F = Fernet(_KEY)


def decrypt(v):
    return six.ensure_str(
            _F.decrypt(
                six.ensure_binary(v)
                )
            )

def encrypt(v):
    return six.ensure_str(
            _F.encrypt(
                six.ensure_binary(v)
                )
            )


if __name__ == "__main__":
    print(decrypt(encrypt('hello')))
