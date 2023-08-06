import unittest 
from . import client, queries, indexedfieldentity, permissionentity, zbprotocol_pb2, zbprotocol_pb2_grpc
import grpc 
import uuid
import json
import time  
import pandas as pd
import numpy as np 
import time

def zbpy_unittests():
    jwt_or_ecdsa = str(input('Would you like to test with jwt or ecdsa? (enter "j" or "e"): ')).strip()

    user_id = str(input('Enter your Zetabase user ID: ')).strip()

    if jwt_or_ecdsa == 'j':
        username = str(input('Enter your Zetabase username: ')).strip()
        password = str(input('Enter your Zetabase password: ')).strip()

        test_user = client.ZetabaseClient(user_id)
        test_user.connect()
        test_user.set_id_password(username, password)
        test_user.auth_login_jwt()

    elif jwt_or_ecdsa == 'e':
        test_user = client.ZetabaseClient(user_id)
        test_user.connect()

        file_pub = str(input('Enter the filepath to your public key: ')).strip()
        file_priv = str(input('Enter the filpath to your private key: ')).strip()

        pub_key = client.import_key(file_pub, public=True)
        priv_key = client.import_key(file_priv, public=False)
        test_user.set_id_key(priv_key, pub_key)





    table_json = str(uuid.uuid4().int)
    table_binary = str(uuid.uuid4().int)
    table_text = str(uuid.uuid4().int)
    table_df = str(uuid.uuid4().int)
    table_full_text = str(uuid.uuid4().int)

    def get_table(table_data, table_id):
        for table in table_data:
            if table.tableId == table_id:
                return table

        return -1

    class TestClientJwt(unittest.TestCase):

        def test_A_connect(self):
            #self.assertIsInstance(test_user.jwt_token, str)
            self.assertIsInstance(test_user.stub, zbprotocol_pb2_grpc.ZetabaseProviderStub)
            self.assertIsInstance(test_user.conn, grpc._channel.Channel)

        def test_B_check_version(self):
            b, info = test_user.check_version()

            self.assertEqual(b, True)
            self.assertIsInstance(info, zbprotocol_pb2.VersionDetails)

        def test_C_create_table(self):
            test_user.create_table(table_json, zbprotocol_pb2.TableDataFormat.JSON, [], [], allow_jwt=True)
            tables = test_user.list_tables(return_json=True)
            table = get_table(tables, table_json)

            self.assertEqual(table.tableId, table_json)
            self.assertEqual(table.dataFormat, zbprotocol_pb2.TableDataFormat.JSON)

            test_user.create_table(table_binary, zbprotocol_pb2.TableDataFormat.BINARY, [], [], allow_jwt=True)
            tables = test_user.list_tables(return_json=True)
            table = get_table(tables, table_binary)

            self.assertEqual(table.tableId, table_binary)
            self.assertEqual(table.dataFormat, zbprotocol_pb2.TableDataFormat.BINARY)

            test_user.create_table(table_text, zbprotocol_pb2.TableDataFormat.PLAIN_TEXT, [], [], True)
            tables = test_user.list_tables(return_json=True)
            table = get_table(tables, table_text)

            self.assertEqual(table.tableId, table_text)
            self.assertEqual(table.dataFormat, zbprotocol_pb2.TableDataFormat.PLAIN_TEXT)

        def test_D_put_get_delKey(self):
            test_data1 = {'1': 1, '2': 2, '3': 3}
            test_data1_bytes = json.dumps(test_data1).encode('utf-8')
            test_user.put_data(table_json, 'test_put_data', test_data1_bytes)
        
            get_data1 = test_user.get(table_json, ['test_put_data'])
            get_data1.return_pretty()
            data1 = [data for data in get_data1][0]

            self.assertEqual(data1, test_data1)

            #no overwrite 

            test_data2 = {'1': 3, '2':2, '3': 1}
            test_data2_bytes = json.dumps(test_data2).encode('utf-8')
            test_user.put_data(table_json, 'test_put_data', test_data2_bytes)

            get_data2 = test_user.get(table_json, ['test_put_data'])
            get_data2.return_pretty()
            data2 = [data for data in get_data2][0]

            self.assertNotEqual(test_data2, data2)

            #overwrite 

            test_user.put_data(table_json, 'test_put_data', test_data2_bytes, overwrite=True)
            
            time.sleep(3)
            get_data3 = test_user.get(table_json, ['test_put_data'])
            get_data3.return_pretty()
            data3 = [data for data in get_data3][0]

            self.assertEqual(test_data2, data3)

            dataframe = pd.DataFrame({'species': ['bear', 'bear', 'marsupial'],'population': [1864, 22000, 80000], 'height': [10.3, 10.2, 4.5]}, index=['panda', 'polar', 'koala'])

            test_user.put_dataframe_new_table(table_df, dataframe, 'df_key', allow_jwt=True)

            #np array 

            array = np.array([[1, 2, 3], [4, 5, 6]])
            test_user.put_np_array(table_binary, array, 'nparray')
            list_keys = test_user.list_keys_with_pattern(table_binary, 'nparray/%')
            keys = [key for key in list_keys]
            result = test_user.get(table_binary, keys)
            
            arr_get = result.to_numpy_arrays()

            comparison = arr_get == array 
            are_equal = comparison.all() 

            self.assertEqual(are_equal, True)


        def test_E_get_query_keys(self):
            species = queries.Field('species')
            population = queries.Field('population')
            height = queries.Field('height')

            query = (species == 'bear') & (population < 2000)
            result = test_user.query_data(table_df, query)
            result.return_pretty()
            data = [i for i in result][0]

            self.assertEqual({"species": "bear", "population": 1864, "height": 10.3}, data)

            query = (population >= 80000) & (species == 'marsupial')
            result = test_user.query_data(table_df, query)
            result.return_pretty()
            data = [i for i in result][0]

            self.assertEqual({"species": "marsupial", "population": 80000, "height": 4.5}, data)

            query = ((height == 10.3) & (population <=1864)) | (height > 11)
            result = test_user.query_data(table_df, query)
            result.return_pretty()
            data = [i for i in result][0]

            self.assertEqual({"species": "bear", "population": 1864, "height": 10.3}, data)

            query = (height >= 10.3)
            result = test_user.query_data(table_df, query)
            result.return_pretty()
            data = [i for i in result][0]

            self.assertEqual(data, {"species": "bear", "population": 1864, "height": 10.3}  )

            query = (height > 10.3)
            result = test_user.query_data(table_df, query)
            data = result.data_all()

            self.assertEqual({}, data)

            list_keys = test_user.list_keys(table_df)
            keys = [key for key in list_keys]
            result = test_user.get(table_df, keys)
            result.return_pretty()
            get_data = [i for i in result]
            true_data = [{"species": "bear", "population": 1864, "height": 10.3}, {"species": "bear", "population": 22000, "height": 10.2}, {"species": "marsupial", "population": 80000, "height": 4.5}]
            
            for i in get_data:
                self.assertIn(i, true_data)

        def test_F_put_multi(self):
            keys = ['key1', 'key2', 'key3']
            data1 = {'name': 'Austin', 'age': 49}
            data2 = {'name': 'Lucie', 'age': 40}
            data3 = {'name': 'Lila', 'age': 50}

            entry_data = [data1, data2, data3]
            entry_bytes = []

            for data in entry_data:
                entry_bytes.append(json.dumps(data).encode('utf-8'))

            test_user.put_multi(table_json, keys, entry_bytes)
            
            result = test_user.get(table_json, keys)
            result.return_pretty()

            for data in result:
                self.assertIn(data, entry_data)


        def test_G_full_text(self):
            i_field = indexedfieldentity.IndexedField('text', zbprotocol_pb2.QueryOrdering.FULL_TEXT)
            test_user.create_table(table_full_text, zbprotocol_pb2.TableDataFormat.JSON, [i_field], allow_jwt=True)

            message = {'text': 'Hello my name is Austin'}
            test_user.put_data(table_full_text, 'test1', json.dumps(message).encode('utf-8'))

            text = queries.Field('text')
            query = (text % 'Austin')

            result = test_user.query_data(table_full_text, query)
            result.return_pretty()
            get_data = [i for i in result][0]

            self.assertEqual(message, get_data)



        def test_H_del_tables(self):
            test_user.delete_table(table_json)
            test_user.delete_table(table_df)
            test_user.delete_table(table_binary)
            test_user.delete_table(table_text)



    def suite():
        suite = unittest.TestSuite()
        suite.addTest(TestClientJwt('test_A_connect'))
        suite.addTest(TestClientJwt('test_B_check_version'))
        suite.addTest(TestClientJwt('test_C_create_table'))
        suite.addTest(TestClientJwt('test_D_put_get_delKey'))
        suite.addTest(TestClientJwt('test_E_get_query_keys'))
        suite.addTest(TestClientJwt('test_F_put_multi'))
        suite.addTest(TestClientJwt('test_G_full_text'))
        suite.addTest(TestClientJwt('test_H_del_tables'))
        return suite





    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())