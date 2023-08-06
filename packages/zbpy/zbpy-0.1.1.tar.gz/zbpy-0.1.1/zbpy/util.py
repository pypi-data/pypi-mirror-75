from .cryptography import generate_key_pair, encode_private_key, encode_public_key
from .zbprotocol_pb2 import EcdsaSignature, NewIdentityRequest, NewIdentityConfirm
from .zbprotocol_pb2_grpc import ZetabaseProviderStub
#from .zbcert import ZBCERT
#from .indexedfieldentity import IndexedField
#import pandas as pd
#import numpy as np
#import uuid
import json
#from ast import literal_eval
from packaging.version import parse as parse_version
import os
import grpc
import re
import phonenumbers
import time
from sys import platform



class Nonce():
    # def nonce_maker(self):
    #     """Generate pseudo-random number and seconds since epoch (UTC)."""
    #     nonce = uuid.uuid1()
    #     oauth_timestamp, oauth_nonce = str(nonce.time), nonce.hex
    #     return oauth_nonce, oauth_timestamp

    def get_nonce(self):
        """
        Returns int.
        """
        nonce = time.time()
        return int(nonce)

def empty_signature():
    """
    Returns empty EcdsaSignature object.
    """
    return EcdsaSignature(r='', s='')

def unwrap_zb_error(error):
    """
    Unwraps error.

    Parameters:
        error: ZbError
    """
    if error is None:
        return None
    elif error.code == 0 and len(error.message) > 0:
        raise Exception(error.message)
    return None

def is_sem_ver_version_at_least(user_version, min_version):
    """
    Returns boolean.

    Parameters:
        user_version: string
        min_version: string
    """
    parsed_user_version = parse_version(user_version)
    parsed_min_version = parse_version(min_version)

    if parsed_user_version < parsed_min_version:
        return False
    return True

def get_stub():
    """
    Returns ZetabaseClientStub.
    """
    server_addr = 'api.zetabase.io:443'

    #ca_cert = 'zbcert.1'
    #certpath = os.path.join(os.path.dirname(__file__), 'zbcert.1')
    #trusted_certs = get_cert()
    #credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs.encode('utf-8'))
    credentials = grpc.ssl_channel_credentials()
    conn = grpc.secure_channel(server_addr, credentials)
    stub = ZetabaseProviderStub(conn)
    return stub


def clean_string_for_filename(filename):
    """
    Returns string.

    Parameters:
        filename: string
    """
    valid_file = re.sub('[^\w_.)( -]', '', filename)
    return valid_file


class IdentityDefinition():

    def __init__(self, id, parent_id, pub_key_enc, priv_key_enc):
        self.id = id
        self.parent_id = parent_id
        self.pub_key_enc = pub_key_enc
        self.priv_key_enc = priv_key_enc

    def to_dict(self):
        """
        Returns dictionary.
        """
        return {
            'id': self.id,
            'pub_key': self.pub_key_enc,
            'priv_key': self.priv_key_enc
        }


def new_account_interactive():
    agree_to_tos = input("Please visit the Zetabase Terms of Service at: https://zetabase.io/tos\nDo you agree to and accept the Terms? [y/n]: ").strip().lower()
    if agree_to_tos == 'n':
        return

    email = input('Email Address: ').strip()
    name = input('Your username: ').strip()

    valid_phone = False
    phone = input('Your mobile number with region code (e.g. +12125551212 for U.S.): ').strip()
    while(not valid_phone):
        parsed_phone = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(parsed_phone):
            phone = input('Invalid number. A phone number is required to confirm your account and set up 2FA.\nPlease provide your mobile number in international format (e.g. +12125551212 for U.S.): ').strip()
        else:
            valid_phone = True

    valid_password = False
    password = input('Your administrator website password: ').strip()
    while(not valid_password):
        if len(password) < 6:
            password = input('Invalid password (too short). Your administrator website password: ').strip()
        else:
            valid_password = True

    generate_key = input('Would you like us to generate a key for this identity (y/n): ').strip()

    if generate_key.lower() == 'y':
        priv_key, pub_key = generate_key_pair()

        encoded_priv = encode_private_key(priv_key, pub_key)

        a = '-----BEGIN PRIVATE KEY-----'
        b = '-----END PRIVATE KEY-----'
        c = '-----BEGIN EC PRIVATE KEY-----'
        d = '-----END EC PRIVATE KEY-----'
        start_b = 0
        start_e = encoded_priv.find(d)
        length = len(c)
        file_key = encoded_priv[length+1:start_e]

        encoded_priv = f'{a}\n{file_key}{b}\n'

        encoded_pub = f'{encode_public_key(pub_key)}\n'

        ts = int(time.time())
        fn_pub = f'zetabase.{ts}.pub'
        fn_priv = f'zetabase.{ts}.priv'
        key_fn = fn_pub
        pk_fn = fn_priv

        with open(fn_pub, 'w') as pub_file:
            pub_file.write(encoded_pub)

        with open(fn_priv, 'w') as priv_file:
            priv_file.write(encoded_priv)

    else:
        path_to_pub = input('Path to public key file: ')
        key_fn = path_to_pub.strip()

        path_to_priv = input('Path to private key file: ')
        pk_fn = path_to_priv.strip()

    with open(key_fn) as f:
        pub_key_enc = f.read()

    with open(pk_fn) as f:
        priv_key_enc = f.read()


    stub = get_stub()
    res = stub.RegisterNewIdentity(NewIdentityRequest(
        name=name,
        email=email,
        adminPassword=password,
        mobile=phone,
        pubKeyEncoded=str(pub_key_enc)
    ))

    if res.error is not None and res.error.code != 0:
        print(f'Failed to register new identity {res.error.message} ({res.error.code})')
    else:
        user_id = res.id
        id_defn = IdentityDefinition(
            id=user_id,
            parent_id='',
            pub_key_enc=str(pub_key_enc),
            priv_key_enc=str(priv_key_enc)
        )

        id_fn = f'zetabase.{clean_string_for_filename(name)}.identity'
        input_data = id_defn.to_dict()

        with open(id_fn, 'w') as f:
            json.dump(input_data, f, indent=1)

        verification_code = input('You will receive a text message with a verification code. Please input it now: ').strip().replace('\r', '').replace('\n', '')

        error = stub.ConfirmNewIdentity(NewIdentityConfirm(
            id=res.id,
            parentId='',
            verificationCode=str(verification_code)
        ))
        wrong_confirmation = True

        if unwrap_zb_error(error) is None:
            wrong_confirmation = False

        while(wrong_confirmation):
            verification_code = input('Wrong code. Please re-input it now: ').strip().replace('\r', '').replace('\n', '')
            error = stub.ConfirmNewIdentity(NewIdentityConfirm(
                id=res.id,
                parentId='',
                verificationCode=str(verification_code)
                ))

            if util.unwrap_zb_error(error) is None:
                wrong_confirmation = False

        print(f'Success! Result: saved identity to file: {id_fn}\n > Id {user_id}')

def test_zbpy():
    """
    Test your zbpy installation.
    """
    from . import test_zbpy
    test_zbpy.zbpy_unittests()
