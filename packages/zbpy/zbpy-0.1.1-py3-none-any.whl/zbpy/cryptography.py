from sys import platform 

if platform != 'win32':
    from fastecdsa import curve, ecdsa, keys, encoding 
else:
    from ellipticcurve.ecdsa import Ecdsa
    from ellipticcurve.privateKey import PrivateKey
    from ellipticcurve.curve import p256
    from . import winsign

from hashlib import sha256, md5

def make_zetabase_signature(uid, nonce, rel_data, pk):
    """
    Returns tuple of strings.
    
    Parameters:
        uid: string 
        nonce: int 
        rel_data: bytes 
        pk: fastecdsa.PrivateKey
    """
    sbs = signing_bytes(uid, nonce)
    return sign_message_bytes(sbs, rel_data, pk)

def signing_bytes(uid, nonce):
    """
    Returns list of bytes.

    Parameters:
        uid: string 
        nonce: int
    """
    sbs = f'{uid}{nonce}'
    return sbs.encode('utf-8')
    #return bytearray(sbs.encode())

def multi_put_extra_signing_bytes(pairs):
    """
    Creates extra bytes when inserting multiple pieces of data. 

    Parameters:
        pairs: list of DataPair objects
    """
    h = md5()
    for v in pairs:
        h.update(v.value)
    bs = h.digest()
    return bs

def multi_put_extra_signing_bytes_md5(pairs):
    """
    Creates extra signing bytes for multiput. 

    Parameters:
        pair: list of DataPair objects
    """
    h = md5()
    for v in pairs:
        h.update(v.key.encode('utf-8'))
        h.update(v.value)

    bs = h.digest()
    return bs

def table_put_extra_signing_bytes(key, value):
    """
    Creates extra bytes when inserting a piece of data.

    Parameters:
        key: string 
        value: list of bytes
    """
    h = md5()
    h.update(key.encode('utf-8'))
    h.update(value)
    bs = h.digest()
    return bs

def table_create_signing_bytes(table_id, perms):
    """
    Returns list of bytes.

    Parameters:
        table_id: string 
        perms: list of PermissionsEntry objects
    """
    bs = table_id.encode('utf-8')
    bs2 = permission_set_signing_bytes(perms)
    bs += bs2
    return bs 

def permission_set_signing_bytes(perms):
    """
    Returns list of bytes. 

    Parameters:
        perms: list of PermissionsEntry objects
    """
    bs = bytes(0)
    for p in perms:
        if p is not None:
            b = permission_signing_bytes(p)
            bs += b
    return bs   

def permission_signing_bytes(entry):
    """
    Returns a list of bytes. 

    Parameters:
        entry: PermEntry object
    """
    b1 = bytes([entry.audienceType]) + bytes([entry.level])
    b2 = (entry.id + entry.tableId + entry.audienceId).encode('utf-8')
    b3 = bytes(0)
    
    for p in entry.constraints:
        b3 += bytes([p.fieldConstraint.constraintType])
        b3 += bytes([p.fieldConstraint.valueType])
        s = (p.fieldConstraint.fieldKey + p.fieldConstraint.requiredValue).encode('utf-8')
        b3 += s

    bs = b1 
    bs += b2
    bs += b3
    return bs

def permissions_entry_signing_bytes(perm):
    """
    Returns bytes.

    Parameters:
        perm: PermissionsEntry object 
    """
    return permission_set_signing_bytes([perm])

def validate_signature_bytes(pub_key, std_signing_bytes, special_data_bytes, r, s):
    """
    Returns boolean.

    Parameters:
        pub_key: fastecdsa.PublicKey
        std_sigining_bytes: list of bytes
        special_data_bytes: list of bytes 
        r: string 
        s: string
    """
    ri, si = int(r), int(s)
    bytes_to_verify = std_signing_bytes + special_data_bytes
    res = ecdsa.verify((ri, si), bytes_to_verify, pub_key, curve=curve.P256, hashfunc=sha3_256)
    return res 

if platform != 'win32':

    def generate_key_pair():
        """
        Returns fastecdsa public and private keys (fastecdsa.privKey, fastecdsa.pubKey).
        """
        private_key, public_key = keys.gen_keypair(curve.P256)
        return private_key, public_key

    def encode_public_key(pub_key):
        """
        Returns string. 

        Parameters:
            pub_key: fastecdsa.point
        """
        return encoding.pem.PEMEncoder.encode_public_key(pub_key)

    def encode_private_key(priv_key, point, curve=curve.P256):
        """
        Returns string. 

        Parameters:
            priv_key: int
            point: fastecdsa.point 
            curve: fastecdsa.curve 
        """
        return encoding.pem.PEMEncoder.encode_private_key(priv_key, point, curve)

    def sign_message_bytes(byts, rel_data_bytes, pk):
        """
        Return tuple of strings.
        """
        bytes_to_sign = None 
        if rel_data_bytes is not None:
            bytes_to_sign = byts + rel_data_bytes
        else:
            bytes_to_sign = byts
        r, s = ecdsa.sign(bytes_to_sign, pk, hashfunc=sha256, curve=curve.P256)
        return str(r), str(s)

else:

    def sign_message_bytes(byts, rel_data_bytes, pk):
        """
        Return tuple of strings.

        Parameters:
            byts: bytes 
            rel_data_bytes: bytes
            pk: ellipticcurve.PrivateKey
        """
        bytes_to_sign = None 
        if rel_data_bytes is not None:
            bytes_to_sign = byts + rel_data_bytes 
        else:
            bytes_to_sign = byts 
        r, s = winsign.sign(bytes_to_sign, pk, sha256)
        return str(r), str(s)

    def generate_key_pair():
        """
        Returns starbank-ecdsa public and private keys (ellipticcurve.privKey, ellipticcurve.pubKey).
        """
        private_key = PrivateKey(curve=p256)
        public_key = private_key.publicKey()
        return private_key, public_key

    def encode_public_key(pub_key):
        """
        Returns string. 

        Parameters:
            pub_key: ellipticcurve.PublicKey
        """
        return pub_key.toPem()

    def encode_private_key(priv_key, point, curve=p256):
        """
        Returns string. 

        Parameters:
            priv_key: ellipticcurve.PrivateKey
        """
        return priv_key.toPem()