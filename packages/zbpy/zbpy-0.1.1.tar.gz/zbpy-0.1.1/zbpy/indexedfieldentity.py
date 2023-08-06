from .zbprotocol_pb2 import TableIndexField, TableIndexFields

class IndexedField():

    def __init__(self, field_name, index_type, lang_code=''):
        """
        Initializes IndexedField. 

        Parameters:
            field_name: string 
            index_type: zbprotocol_pb2.QueryOrdering 
            lang_code: string 

        Returns: 
            IndexedField 
        """
        self.field_name = field_name
        self.index_type = index_type
        self.lang_code = lang_code 

    def set_language_code(self, code):
        """
        Sets the language code of the IndexedField.

        Parameters:
            code: string
        """
        self.lang_code = code 

    def to_protocol(self):
        """
        Returns:
            TableIndexField
        """
        return TableIndexField(
            field=self.field_name,
            ordering=self.index_type,
            languageCode=self.lang_code
        )


def indexed_fields_to_protocol(ifs):
    """
    Parameters:
        ifs: IndexedField

    Returns: 
        list of TableIndexFields
    """
    arr = []
    for field in ifs:
        arr.append(field.to_protocol())
    return TableIndexFields(
        fields=arr
    )
