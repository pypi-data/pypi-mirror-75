import os
import grpc
from . import zbprotocol_pb2_grpc
from . import zbprotocol_pb2
from . import auth
from . import pagination
from .util import *
from .datasci import *
from .indexedfieldentity import indexed_fields_to_protocol
from . import cryptography
import pandas as pd
import numpy as np
import tempfile
try:
    from IPython.core.magic import line_magic, Magics, magics_class
except:
    pass
from sys import platform

if platform != 'win32':
    from fastecdsa import curve
    from fastecdsa.keys import import_key as import_key_fastecdsa
else:
    from ellipticcurve import privateKey, publicKey


CLIENT_VERSION = '0.1-alpha'

class ZetabaseClient():
    """
    An instance of a Zetabase client.
    """
    def __init__(self, uid):
        """
        Initializes a new Zetabase client.

        Parameters:
            uid: string

        Returns:
            ZetabaseClient
        """
        self.user_id = uid #string
        self.server_addr = 'api.zetabase.io:443' #string
        self.insecure = None #bool
        self.parent_id = None #string
        self.login_id = None #string
        self.priv_key = None #ecsda.PublicKey
        self.pub_key = None #ecdsa.PrivateKey
        self.password = None #string
        self.nonce_maker = Nonce() #Nonce
        self.conn = None #grpc.ClientConn
        self.stub = None #ZetabaseProviderStub
        self.jwt_token = None #string

    def connect(self):
        """
        Establishes a connection between the Zetabase client to the server.
        """
        if self.insecure:
            self.conn = grpc.insecure_channel(self.server_addr)

        else:
            #ca_cert = 'zbcert.1'
            #certpath = os.path.join(os.path.dirname(__file__), 'zbcert.1')
            #trusted_certs = open(ca_cert).read()
            #trusted_certs = get_cert()
            #trusted_certs = ssl.get_server_certificate(('api.zetabase.io', 443))
            credentials = grpc.ssl_channel_credentials()
            self.conn = grpc.secure_channel(self.server_addr, credentials)

        self.stub = zbprotocol_pb2_grpc.ZetabaseProviderStub(self.conn)

    def check_version(self):
        """
        Checks to see if Client version is compatible.

        Returns:
            boolean, zbpprotocol_pb2.VersionDetails
        """
        if not self.check_ready():
            raise Exception('NotReady')

        info = self.stub.VersionInfo(zbprotocol_pb2.ZbEmpty())
        min_client_version = info.minClientVersion

        is_enough = is_sem_ver_version_at_least(CLIENT_VERSION, min_client_version)

        return is_enough, info

    def set_insecure(self):
        """
        Sets insecure of the ZetabaseClient to true.
        """
        self.insecure = True

    def set_parent(self, id):
        """
        Sets the parent_id of the ZetabaseClient to id.

        Parameters:
            id: string.
        """
        self.parent_id = id

    def set_id_key(self, priv, pub):
        """
        Sets the private and public keys of the ZetabaseClient to priv and pub respectively.

        Parameters:
            priv: fastecdsa.PrivateKey
            pub: fastecdsa.PublicKey
        """
        self.priv_key = priv
        self.pub_key = pub

    def set_server_addr(self, addr):
        """
        Sets the server address of the ZetabaseClient.

        Parameters:
            addr: string
        """
        self.server_addr = addr

    def set_id_password(self, login_id, pwd):
        """
        Sets the login_id and password of the ZetabaseClient.

        Parameter:
            login_id: string
            pwd: string
        """
        self.password = pwd
        self.login_id = login_id

    def check_ready(self):
        """
        Checks to see if the ZetabaseClient is ready to make a request.

        Returns:
            boolean
        """
        if self.priv_key is not None or (self.password is not None and self.login_id is not None):
            if self.conn is not None:
                if self.login_id is not None and self.jwt_token is None:
                    err = self.auth_login_jwt()
                    if err is not None:
                        return False
                return True
        return False

    def jwt_credential(self):
        """
        Uses the zetabase user's jwt_token to create proof of credential if they have one.

        Returns:
            ProofOfCredential
        """
        if self.jwt_token is not None:
            return auth.make_credential_jwt(self.jwt_token)
        return None

    def ecdsa_credential(self, nonce, extra_bytes):
        """
        Creates ecdsa proof of credential using the specified nonce and bytes.

        Parameters:
            nonce: int
            extra_bytes: list of bytes

        Returns:
            ProofOfCredential
        """
        return auth.make_credential_ecdsa(nonce, self.user_id, extra_bytes, self.priv_key)

    def login_jwt(self, login_id, password):
        """
        Connects to Zetabase and logs in using jwt.

        Parameters:
            login_id: string
            password: string
        """
        self.connect()
        self.set_id_password(login_id, password)
        self.auth_login_jwt()

    def setup_ecdsa(self, priv_filepath, pub_filepath):
        """
        Connects to Zetabase, imports the public and private key, and sets them so the user is ready to make requests.

        Parameters:
            priv_filepath: string (filepath to private key)
            pub_filepath: string (filepath to public key)
        """
        self.connect()
        priv_key = import_key(priv_filepath, False)
        pub_key = import_key(pub_filepath, True)
        self.set_id_key(priv_key, pub_key)

    def auth_login_jwt(self):
        """
        Uses jwt to login a ZetabaseClient that is already connected.

        Returns:
            None (if no error else raises exception)
        """
        if self.conn is None:
            raise Exception('NotReady')
        elif self.password is None:
            raise Exception('NoPasswordProvided')

        parId = ''
        if self.parent_id is not None:
            parId = self.parent_id

        response = self.stub.LoginUser(zbprotocol_pb2.AuthenticateUser(
            parentId=parId,
            password=self.password,
            handle=self.login_id,
            nonce=self.nonce_maker.get_nonce(),
            credential=auth.make_credential_jwt(self.jwt_token)
        ))
        if response.jwtToken is not None and response.id is not None:
            self.jwt_token = response.jwtToken
            self.user_id = response.id
        return None

    def get_credential(self, nonce, x_bytes):
        """
        Creates proof of credential based on which type of proof of credential the zetabase user is using, jwt or ecdsa.

        Parameters:
            nonce: int
            x_bytes: bytes

        Returns:
            ProofOfCredential
        """
        proof_of_credential = None
        if self.jwt_token is not None:
            proof_of_credential = self.jwt_credential()
        else:
            proof_of_credential = self.ecdsa_credential(nonce, x_bytes)
        return proof_of_credential

    def list_keys(self, table_id, table_owner_id=None):
        """
        Lists the keys for the specified table.

        Parameter:
            table_id: string
            table_owner_id: string (default=self.user_id)

        Returns:
            GetPages
        """
        if table_owner_id is None:
            table_owner_id = self.user_id

        return self.list_keys_with_pattern(table_id, '', table_owner_id)

    def list_tables(self, return_json=False):
        """
        Lists all tables owned by the specified id.

        Parameters:
            return_json: boolean

        Returns:
            zbprotocol_pb2.ListTablesResponse
        """
        nonce = self.nonce_maker.get_nonce()
        proof_of_credential = self.get_credential(nonce, None)

        result = self.stub.ListTables(zbprotocol_pb2.ListTablesRequest(
            id=self.user_id,
            nonce=nonce,
            tableOwnerId=self.user_id,
            credential=proof_of_credential
        ))

        if return_json:
            return result.tableDefinitions
        return [table.tableId for table in result.tableDefinitions]

    def get(self, table_id, keys, table_owner_id=None, max_item_size=1000):
        """
        Returns items from the specified table with the specified keys.

        Parameters:
            table_id: string
            keys: list of strings
            table_owner_id: string (default=self.user_id)
            max_item_size: integer (default=1000)

        Returns:
            GetPages
        """
        get_pages = pagination.GetPages(self, keys, max_item_size, table_id, table_owner_id)
        return get_pages


    def get_helper(self, table_id, keys, table_owner_id=None):
        """
        Returns items from the specified table with the specified keys.

        Parameters:
            table_id: string
            keys: list of strings
            table_owner_id: string (default=self.user_id)

        Returns:
            GetPages
        """
        if table_owner_id is None:
            table_owner_id = self.user_id

        def pag_requester(idx):
            tim, has_nxt = self.__get_helper(table_owner_id, table_id, keys, idx)
            return tim, has_nxt

        return pagination.standard_pagination_handler(pag_requester)

    def __get_helper(self, table_owner_id, table_id, keys, page_idx):
        """
        Returns map of bytes and boolean.

        Parameters:
            table_owner_id: string
            table_id: string
            keys: list of strings
            page_idx: integer
        """
        if not self.check_ready():
            raise Exception('NotReady')

        nonce = self.nonce_maker.get_nonce()
        proof_of_credential = self.get_credential(nonce, None)

        res = self.stub.GetData(zbprotocol_pb2.TableGet(
            id=self.user_id,
            tableOwnerId=table_owner_id,
            tableId=table_id,
            nonce=nonce,
            credential=proof_of_credential,
            pageIndex=page_idx,
            keys=keys
        ))

        m = {}
        for data_pair in res.data:
            m[data_pair.key] = data_pair.value
        return m, res.pagination.hasNextPage

    def get_all(self, table_id, table_owner_id=None):
        """
        Returns all items from the specified table. 

        Parameters: 
            table_id: string 
            table_owner_id: string (default=self.user_id)

        Returns: 
            GetPages
        """
        list_keys = self.list_keys(table_id, table_owner_id)
        keys = [key for key in list_keys]
        return self.get(table_id, keys, table_owner_id)

    def id(self):
        """
        Gives the ZetabaseClient's user id.

        Returns:
            string
        """
        return self.user_id

    def confirm_new_sub_user(self, subuser_id, verification_code):
        """
        Confirms the creation of a new subuser using the subuser's verification code (sent to phone).

        Parameters:
            subuser_id: string
            verification_code: string

        Returns:
            None (if no error else raises exception)
        """
        error = self.stub.ConfirmNewIdentity(zbprotocol_pb2.NewIdentityConfirm(
            id=subuser_id,
            parentId=self.user_id,
            verificationCode=str(verification_code)
        ))

        return unwrap_zb_error(error)

    def new_sub_user(self, handle, email, mobile, password, signup_code, group_id):
        """
        Creates a new subuser and returns the subuser's id.

        Parameters:
            handle: string
            email: string
            mobile: string
            password: string
            signup_code: string
            group_id: string

        Returns:
            string, PrivateKey, PublicKey
        """
        priv_key, pub_key = cryptography.generate_key_pair()
        priv_key_encoded = cryptography.encode_private_key(priv_key, pub_key)
        pub_key_encoded = cryptography.encode_public_key(pub_key)

        result = self.stub.CreateUser(zbprotocol_pb2.NewSubIdentityRequest(
            id=self.user_id,
            name=handle,
            email=email,
            mobile=mobile,
            loginPassword=password,
            pubKeyEncoded=pub_key_encoded,
            signupCode=signup_code,
            groupId=group_id
        ))

        id = result.id
        return id, priv_key, pub_key

    def add_permission(self, table_id, perm, table_owner_id=None):
        """
        Adds a new permission to an existing table.

        Parameters:
            table_id: string
            perm: PermEntry
            table_owner_id: string (default=self.user_id)

        Returns:
            None (if no error else raises exception)
        """
        if table_owner_id is None:
            table_owner_id = self.user_id

        if not self.check_ready():
            raise Exception('NotReady')

        nonce = self.nonce_maker.get_nonce()
        perms_ent = perm.to_protocol(table_owner_id, table_id)
        perms_ent.nonce = nonce
        proof_of_credential = self.get_credential(nonce, cryptography.permissions_entry_signing_bytes(perms_ent))

        error = self.stub.SetPermission(zbprotocol_pb2.PermissionsEntry(
            id=perms_ent.id,
            tableId=perms_ent.tableId,
            audienceType=perms_ent.audienceType,
            audienceId=perms_ent.audienceId,
            level=perms_ent.level,
            nonce=perms_ent.nonce,
            credential=proof_of_credential,
            constraints=perms_ent.constraints
        ))

        return unwrap_zb_error(error)


    def list_keys_with_pattern(self, table_id, pattern, table_owner_id=None):
        """
        Lists keys that begin with a certain prefix.

        Parameters:
            table_id: string
            pattern: string
            table_owner_id: string (default=self.user_id)

        Returns:
            GetPages
        """
        if table_owner_id is None:
            table_owner_id = self.user_id

        def pag_requester(idx):
            m = {}
            tim, has_nxt = self.__list_keys_with_pattern_helper(table_owner_id, table_id, pattern, idx)
            for k in tim:
                m[k] = None
            return m, has_nxt

        f = pag_requester
        return pagination.standard_pagination_handler(f)

    def __list_keys_with_pattern_helper(self, table_owner_id, table_id, pattern, pg_inx):
        """
        Returns string array and boolean.
        """
        if not self.check_ready:
            raise Exception('NotReady')
        nonce = self.nonce_maker.get_nonce()
        proof_of_credential = self.get_credential(nonce, None)

        res = self.stub.ListKeys(zbprotocol_pb2.ListKeysRequest(
            id=self.user_id,
            tableId=table_id,
            tableOwnerId=table_owner_id,
            pattern=pattern,
            nonce=nonce,
            pageIndex=pg_inx,
            credential=proof_of_credential
        ))

        rig = res.keys
        return rig, res.pagination.hasNextPage

    def get_sub_identities(self):
        """
        Returns all of the subusers of the ZetabaseClient.

        Returns:
            zbprotocol_pb2.SubIdentitiesList.subIdentities
        """
        if not self.check_ready():
            raise Exception('NotReady')

        nonce = self.nonce_maker.get_nonce()
        proof_of_credential = self.get_credential(nonce, None)

        result = self.stub.ListSubIdentities(zbprotocol_pb2.SimpleRequest(
            id=self.user_id,
            nonce=nonce,
            credential=proof_of_credential
        ))

        return result.subIdentities

    def query(self, table_id, qry, table_owner_id=None):
        """
        Queries keys based on the specified query and table.

        Parameters:
            table_id: string
            qry: Query type object
            table_owner_id: string (default=self.user_id)

        Returns:
            PaginationHandler
        """
        if table_owner_id is None:
            table_owner_id = self.user_id

        qry = qry.to_sub_query()

        def pag_requester(idx):
            tim, has_next = self.__query_helper(table_owner_id, table_id, idx, qry)
            return tim, has_next

        return pagination.standard_pagination_handler(pag_requester)

    def query_data(self, table_id, qry, table_owner_id=None, max_item_size=1000): 
        """
         Queries keys based on the specified query and table.

        Parameters:
            table_id: string
            qry: Query type object
            table_owner_id: string (default=self.user_id)

        Returns:
            GetPages
        """
        res = self.query(table_id, qry, table_owner_id)
        keys = [k for k in res]
        return self.get(table_id, keys, table_owner_id, max_item_size)

    def __query_helper(self, table_owner_id, table_id, pg_inx, qry):
        """
        Returns a map of strings to bytes and a boolean.
        """
        if not self.check_ready:
            raise Exception('NotReady')

        nonce = self.nonce_maker.get_nonce()
        proof_of_credential = self.get_credential(nonce, None)

        res = self.stub.QueryKeys(zbprotocol_pb2.TableQuery(
             id=self.user_id,
             tableOwnerId=table_owner_id,
             tableId=table_id,
             query=qry,
             nonce=nonce,
             pageIndex=pg_inx,
             credential=proof_of_credential
        ))

        m = {}
        for k in res.keys:
            m[k] = None

        return m, res.pagination.hasNextPage

    def put_data(self, table_id, key, value, overwrite=False, table_owner_id=None):
        """
        Put the specified data into the specified table with the given key.

        Parameters:
            table_id: string
            key: string
            value: bytes
            overwrite: boolean (default=True)
            table_owner_id: string (default=self.user_id)

        Returns:
            None (if no error else raises exception)
        """
        if not self.check_ready():
            raise Exception('NotReady')

        if table_owner_id is None:
            table_owner_id = self.user_id

        nonce = self.nonce_maker.get_nonce()
        x_bytes = cryptography.table_put_extra_signing_bytes(key, value)
        proof_of_credential = self.get_credential(nonce, x_bytes)

        error = self.stub.PutData(zbprotocol_pb2.TablePut(
            id=self.user_id,
            tableOwnerId=table_owner_id,
            tableId=table_id,
            key=key,
            value=value,
            overwrite=overwrite,
            nonce=nonce,
            credential=proof_of_credential
        ))

        return unwrap_zb_error(error)

    def put_multi(self, table_id, keys, values, overwrite=False, table_owner_id=None):
        """
        Put multiple pieces of data into a table with the specified keys.

        Parameters:
            table_id: string
            keys: list of strings
            values: list of bytes
            overwrite: boolean (default=False)
            table_owner_id: string (default=self.user_id)

        Returns:
            None (if no error else raises exception)
        """
        put_pages = pagination.PutPages(self, keys, values)
        res = put_pages.put_all(table_id, overwrite, table_owner_id)
        return res

    def put_multi_helper(self, table_id, keys, values, overwrite=False, table_owner_id=None):
        """
        Put multiple pieces of data into a table with the specified keys.

        Parameters:
            table_id: string
            keys: list of strings
            values: list of bytes
            overwrite: boolean (default=False)
            table_owner_id: string (default=self.user_id)

        Returns:
            None (if no error else raises exception)
        """
        if len(values) != len(keys):
            raise Exception('ImproperDimensions')

        if table_owner_id is None:
            table_owner_id = self.user_id

        nonce = self.nonce_maker.get_nonce()
        dps = []
        for i in range(len(keys)):
            dps.append(zbprotocol_pb2.DataPair(
                key=keys[i],
                value=values[i]
            ))

        x_bytes = cryptography.multi_put_extra_signing_bytes_md5(dps)
        proof_of_credential = self.get_credential(nonce, x_bytes)

        result = self.stub.PutDataMulti(zbprotocol_pb2.TablePutMulti(
            id=self.user_id,
            tableOwnerId=table_owner_id,
            tableId=table_id,
            overwrite=overwrite,
            nonce=nonce,
            credential=proof_of_credential,
            pairs=dps
        ))

        return unwrap_zb_error(result)

    def put_np_array(self, table_id, array, np_key, overwrite=False, table_owner_id=None):
        """
        Put numpy array into a table with the given key.

        Parameters:
            table_id: string
            array: np.array
            key: string
            overwrite: boolean (default=False)
            table_owner_id: string (default=self.user_id)

        Returns:
            None (if no error else raises exception)
        """
        assert isinstance(array, np.ndarray)

        error = None
        more_data = True
        start_entry = 0
        while(more_data):
            keys, input_bytes, done = parse_np_array(array, np_key, start_entry)
            more_data = not done

            error = self.put_multi(table_id, keys, input_bytes, overwrite, table_owner_id)

            if unwrap_zb_error(error) is not None:
                return unwrap_zb_error(error)

            start_entry += 1024 #NEED TO CHANGE THIS AND NUM IN parse_np_array IN ORDER TO CHANGE HOW MANY ENTRIES ARE SENT AT A TIME

        return None

    def put_dataframe(self, table_id, dataframe, df_key, overwrite=False, table_owner_id=None):
        """
        Put pandas DataFrame into a json table with a specified key that will designate all entries of the dataframe.

        Parameters:
            table_id: string
            dataframe: pandas.DataFrame
            df_key: string
            overwrite: boolean (default=False)
            table_owner_id: string (default=self.user_id)

        Returns:
            None (if no error else raises exception)
        """
        assert isinstance(dataframe, pd.DataFrame)

        error = None
        more_data = True
        start_entry = 0
        while(more_data):
            keys, input_bytes, done = df_to_kvp(dataframe, df_key, start_entry)
            more_data = not done

            error = self.put_multi(table_id, keys, input_bytes, overwrite, table_owner_id)

            if unwrap_zb_error(error) is not None:
                return unwrap_zb_error(error)

            start_entry += 1000 #NEED TO CHANGE THIS AND NUM IN dv_to_kvp IN ORDER TO CHANGE HOW MANY ENTRIES ARE SENT AT A TIME

        return None

    def put_dataframe_new_table(self, table_id, dataframe, df_key, perms=[], specify_fields=None, allow_jwt=True):
        """
        Creates a new table with indexed fields to match the names and types of the dataframe's columns. By default, all columns will be indexed, but
        a subset can be specified by listing the names of the columns in the 'specify_fields' parameter.

        Parameters:
            table_id: string
            dataframe: pandas.DataFrame
            df_key: string
            perms: list of PermEntry objects (default=[])
            specify_fields: list of strings (default=All columns)
            allow_jwt: boolean (default=False)

        Returns:
            None (if no error else raises exception)
        """
        assert isinstance(dataframe, pd.DataFrame)

        indexed_fields = parse_df_columns(dataframe, specify_fields)

        error = self.create_table(table_id, zbprotocol_pb2.TableDataFormat.JSON, indexed_fields, perms, allow_jwt)

        if unwrap_zb_error(error) is not None:
            return unwrap_zb_error(error)

        self.put_dataframe(table_id, dataframe, df_key)

        return None

    def delete_table(self, table_id, table_owner_id=None):
        """
        Deletes the specified table.

        Parameters:
            table_id: string
            table_owner_id: string (default=self.user_id)

        Returns:
            None (if no error else raises exception)
        """
        if table_owner_id is None:
            table_owner_id = self.user_id

        if not self.check_ready():
            raise Exception('NotReady')

        nonce = self.nonce_maker.get_nonce()
        extra_bytes = table_id.encode('utf-8')
        proof_of_credential = self.get_credential(nonce, extra_bytes)

        result = self.stub.DeleteObject(zbprotocol_pb2.DeleteSystemObjectRequest(
            id=self.user_id,
            objectType=zbprotocol_pb2.SystemObjectType.TABLE,
            tableOwnerId=table_owner_id,
            tableId=table_id,
            objectId=table_id,
            nonce=nonce,
            credential=proof_of_credential
        ))

        return unwrap_zb_error(result)

    def delete_key(self, table_id, key, table_owner_id=None):
        """
        Deletes the specified key.

        Parameters:
            table_id: string
            key: string
            table_owner_id: string (default=self.user_id)

        Returns:
            None (if no error else raises exception)
        """
        if table_owner_id is None:
            table_owner_id = self.user_id

        if not self.check_ready():
            raise Exception('NotReady')

        nonce = self.nonce_maker.get_nonce()
        extra_bytes = key.encode('utf-8')
        proof_of_credential = self.get_credential(nonce, extra_bytes)

        result = self.stub.DeleteObject(zbprotocol_pb2.DeleteSystemObjectRequest(
            id=self.user_id,
            objectType=zbprotocol_pb2.SystemObjectType.KEY,
            tableOwnerId=table_owner_id,
            tableId=table_id,
            objectId=key,
            nonce=nonce,
            credential=proof_of_credential
        ))

        return unwrap_zb_error(result)


    def grpc_stub(self):
        """
        Returns:
            ZetabaseProviderStub
        """
        return self.stub

    def create_table(self, table_id, data_type, indexed_fields=[], perms=[], allow_jwt=True):
        """
        Creates a table with given attributes.

        Parameters:
            table_id: string
            data_type: zbprotocol_pb2.TableDataFormat
            indexed_fields: list of IndexedField (default=[])
            perms: list of PermEntrys (default=[])
            allow_jwt: boolean (default=False)

        Returns:
            None (if no error else raises exception)
        """
        if not self.check_ready():
            raise Exception('NotReady')

        p_entries = []
        for perm in perms:
            p_entries.append(perm.to_protocol(self.user_id, table_id))

        nonce = self.nonce_maker.get_nonce()
        sig_bytes = cryptography.table_create_signing_bytes(table_id, p_entries)
        proof_of_credential = self.get_credential(nonce, sig_bytes)

        error = self.stub.CreateTable(zbprotocol_pb2.TableCreate(
            id=self.user_id,
            tableId=table_id,
            dataFormat=data_type,
            indices=indexed_fields_to_protocol(indexed_fields),
            nonce=nonce,
            allowTokenAuth=allow_jwt,
            credential=proof_of_credential,
            permissions=p_entries
        ))

        return unwrap_zb_error(error)

if platform != 'win32':

    def import_key(filepath, public, curve=curve.P256):
        """
        Returns the keys located at the specified filepath.

        Parameters:
            filepath: string
            public: boolean
            curve: fastecdsa.curve (default=P256)

        Returns:
            fastecdsa.key (public or private)
        """
        if not public:
            new_text = ''
            file_key = ''
            a = '-----BEGIN PRIVATE KEY-----'
            b = '-----END PRIVATE KEY-----'
            c = '-----BEGIN EC PRIVATE KEY-----'
            d = '-----END EC PRIVATE KEY-----'
            with open(filepath, 'r') as f:
                text = f.read()
                start_b = 0
                start_e = text.find(b)
                length = len(a)
                file_key = text[length+1:start_e]

            new_text = f'{c}\n{file_key}{d}\n'

            with tempfile.NamedTemporaryFile(mode='w+t', suffix='.priv', prefix=os.path.basename(__file__)) as tf:
                name = tf.name[tf.name.rfind('/'):]
                tf_directory = f'{os.path.dirname(tf.name)}{name}'
                tf.writelines(new_text)
                text = tf.read()

                priv_key = import_key_fastecdsa(tf_directory, public=public, curve=curve)
                return priv_key[0]


        return import_key_fastecdsa(filepath, public=public, curve=curve)

else:

    def import_key(filepath, public):
        """
        Returns the keys located at the specified filepath.

        Parameters:
            filepath: string
            public: boolean
        Returns:
            ellipticcurve.key (public or private)
        """

        if not public:
            a = '-----BEGIN PRIVATE KEY-----'
            b = '-----END PRIVATE KEY-----'
            c = '-----BEGIN EC PRIVATE KEY-----'
            d = '-----END EC PRIVATE KEY-----'
            with open(filepath, 'r') as f:
                text = f.read()
                start_b = 0
                start_e = text.find(b)
                length = len(a)
                file_key = text[length+1:start_e]

            new_text = f'{c}\n{file_key}{d}'

            return privateKey.PrivateKey.fromPem(new_text)

        a = '-----BEGIN PUBLIC KEY-----'
        b = '-----END PUBLIC KEY-----'
        c = '-----BEGIN EC PUBLIC KEY-----'
        d = '-----END EC PUBLIC KEY-----'
        with open(filepath, 'r') as f:
            text = f.read()
            start_b = 0
            start_e = text.find(b)
            length = len(a)
            file_key = text[length+1:start_e]

        new_text = f'{c}\n{file_key}{d}'


        return publicKey.PublicKey.fromPem(new_text)

try:
    @magics_class
    class NewAccount(Magics):
        @line_magic
        def createaccount(self, line):
            new_account_interactive()

    try:
        ip = get_ipython()
        ip.register_magics(NewAccount)
    except:
        pass
except:
    pass
