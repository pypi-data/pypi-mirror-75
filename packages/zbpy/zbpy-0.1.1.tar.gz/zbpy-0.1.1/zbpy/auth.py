from .zbprotocol_pb2 import ProofOfCredential, CredentialProofType, EcdsaSignature
from .util import empty_signature
from .cryptography import make_zetabase_signature


def make_credential_jwt(jwt_token):
    """
    Returns a ProofOfCredential object with an empty Ecdsa signature, credType set to JWT_TOKEN, and the zetabase user's
    jwt token. 

    Parameters: 
        jwt_token: string 
    """
    return ProofOfCredential(
        credType=CredentialProofType.JWT_TOKEN,
        signature=empty_signature(),
        jwtToken=jwt_token
    )

def make_credential_ecdsa(nonce, uid, rel_bytes, pk):
    """
    Returns a ProofOfCredential object.

    Parameters:
        uid: string 
        rel_bytes: list of bytes 
        pk: ecdsa.PrivateKey
    """
    r, s = make_zetabase_signature(uid, nonce, rel_bytes, pk)
    if r == '' or s == '':
        return None 
    return ProofOfCredential(
        credType=CredentialProofType.SIGNATURE,
        signature=EcdsaSignature(
            r=r,
            s=s
        ),
        jwtToken=''
    )
