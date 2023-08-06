from . import zbprotocol_pb2


class QueryAnd():
     
    def __init__(self, left, right):
        """
        Initializes QueryAnd object. 

        Parameters:
            left: SubQueryConvertible 
            right: SubQueryConvertible
        """
        self.left = left #SubQueryConvertible 
        self.right = right #SubQueryConvertible

    def to_sub_query(self):
        """
        Returns TableSubQuery object. 
        """
        return zbprotocol_pb2.TableSubQuery(
            isCompound=True,
            compoundOperator=zbprotocol_pb2.QueryLogicalOperator.LOGICAL_AND,
            compoundLeft=self.left.to_sub_query(),
            compoundRight=self.right.to_sub_query(),
            comparison=None      
        )

class QueryOr():

    def __init__(self, left, right):
        """
        Initializes QueryOr object. 

        Parameters:
            left: SubQueryConvertible 
            right: SubQueryConvertible 
        """
        self.right = right #SubQueryConvertible
        self.left = left #SubQueryConvertible

    def to_sub_query(self):
        """
        Returns TableSubQuery object. 
        """
        return zbprotocol_pb2.TableSubQuery(
            isCompound=True,
            compoundOperator=zbprotocol_pb2.QueryLogicalOperator.LOGICAL_OR,
            compoundLeft=self.left.to_sub_query(),
            compoundRight=self.right.to_sub_query(),
            comparison=None
        )

class QueryEquals():

    def __init__(self, field, comp_value):
        """
        Initializes QueryEquals object. 

        Parameters:
            field: string 
            comp_value: any (sorta) 
        """
        self.field = field 
        self.comp_value = comp_value 

    def to_sub_query(self):
        """
        Returns TableSubQuery object.
        """
        value = self.comp_value
        field = self.field 
        value_str, q_order = query_object_typify(value)
        return zbprotocol_pb2.TableSubQuery(
            isCompound=False,
            compoundOperator=0,
            compoundLeft=None,
            compoundRight=None,
            comparison=zbprotocol_pb2.TableSubqueryComparison(
                op=zbprotocol_pb2.QueryOperator.EQUALS,
                field=field,
                value=value_str,
                ordering=q_order
            )
        )

class QueryNotEqual():

    def __init__(self, field, comp_value):
        """
        Initializes QueryEquals object. 

        Parameters:
            field: string 
            comp_value: any (sorta) 
        """
        self.field = field 
        self.comp_value = comp_value 

    def to_sub_query(self):
        """
        Returns TableSubQuery object.
        """
        value = self.comp_value 
        field = self.field 
        value_str, q_order = query_object_typify(value)
        return zbprotocol_pb2.TableSubQuery(
            isCompound=False,
            compoundOperator=0,
            compoundLeft=None,
            compoundRight=None,
            comparison=zbprotocol_pb2.TableSubqueryComparison(
                op=zbprotocol_pb2.QueryOperator.NOT_EQUALS,
                field=field,
                value=value_str,
                ordering=q_order
            )
        )
    
class QueryGreaterThan():

    def __init__(self, field, comp_value):
        """
        Initializes QueryGreaterThan object. 

        Parameters:
            field: string 
            comp_value: any
        """
        self.field = field 
        self.comp_value = comp_value 

    def to_sub_query(self):
        """
        Return TableSubQuery object. 
        """
        value = self.comp_value
        field = self.field 
        value_str, q_order = query_object_typify(value)
        return zbprotocol_pb2.TableSubQuery(
            isCompound=False,
            compoundOperator=0,
            compoundLeft=None,
            compoundRight=None,
            comparison=zbprotocol_pb2.TableSubqueryComparison(
                op=zbprotocol_pb2.QueryOperator.GREATER_THAN,
                field=field,
                value=value_str,
                ordering=q_order
            )
        )

class QueryGreaterThanEqual():

    def __init__(self, field, comp_value):
        """
        Initializes QueryGreaterThanEqual object.

        Parameters:
            field: string 
            value: any 
        """
        self.field = field 
        self.comp_value = comp_value 

    def to_sub_query(self):
        """
        Returns a TableSubQuery object. 
        """
        value = self.comp_value 
        field = self.field 
        value_str, q_order = query_object_typify(value)
        return zbprotocol_pb2.TableSubQuery(
            isCompound=False,
            compoundOperator=0,
            compoundLeft=None,
            compoundRight=None,
            comparison=zbprotocol_pb2.TableSubqueryComparison(
                op=zbprotocol_pb2.QueryOperator.GREATER_THAN_EQ,
                field=field,
                value=value_str,
                ordering=q_order
            )
        )

class QueryLessThan():

    def __init__(self, field, comp_value):
        """
        Initializes QuerylessThan object

        Parameters:
            field: string 
            comp_value: any 
        """
        self.field = field 
        self.comp_value = comp_value 

    def to_sub_query(self):
        """
        Returns a TableSubQuery object. 
        """
        value = self.comp_value
        field = self.field 
        value_str, q_order = query_object_typify(value)
        return zbprotocol_pb2.TableSubQuery(
            isCompound=False,
            compoundOperator=0,
            compoundLeft=None,
            compoundRight=None,
            comparison=zbprotocol_pb2.TableSubqueryComparison(
                op=zbprotocol_pb2.QueryOperator.LESS_THAN,
                field=field,
                value=value_str,
                ordering=q_order
            )
        )

class QueryLessThanEqual():

    def __init__(self, field, comp_value):
        """
        Initializes QueryLessThanEqual object. 

        Parameters:
            field: string
            comp_value: any
        """
        self.field = field 
        self.comp_value = comp_value 

    def to_sub_query(self):
        """
        Returns TableSubQuery object.
        """
        value = self.comp_value
        field = self.field 
        value_str, q_order = query_object_typify(value)
        return zbprotocol_pb2.TableSubQuery(
            isCompound=False,
            compoundOperator=0,
            compoundLeft=None,
            compoundRight=None,
            comparison=zbprotocol_pb2.TableSubqueryComparison(
                op=zbprotocol_pb2.QueryOperator.LESS_THAN_EQ,
                field=field,
                value=value_str,
                ordering=q_order
            )
        )

class QueryTextSearch():

    def __init__(self, field, comp_value):
        """
        Initializes QueryTextSearch object.

        Parameters:
            field: string 
            comp_value: any
        """
        self.field = field 
        self.comp_value = comp_value 

    def to_sub_query(self):
        """
        Returns TableSubQuery object.
        """
        value = self.comp_value
        field = self.field 
        value_str, q_order = query_object_typify(value)
        q_order = zbprotocol_pb2.QueryOrdering.FULL_TEXT
        return zbprotocol_pb2.TableSubQuery(
            isCompound=False,
            compoundOperator=0,
            compoundLeft=None,
            compoundRight=None,
            comparison=zbprotocol_pb2.TableSubqueryComparison(
                op=zbprotocol_pb2.QueryOperator.TEXT_SEARCH,
                field=field,
                value=value_str,
                ordering=q_order
            )
        )

def query_object_typify(value):
    """
    Returns string, QueryOrdering.

    Parameters:
        value: any
    """
    q_order = zbprotocol_pb2.QueryOrdering.LEXICOGRAPHIC 
    
    if isinstance(value, int) or isinstance(value, float):
        q_order = zbprotocol_pb2.QueryOrdering.REAL_NUMBERS
        value_str = str(value)
    else:
        value_str = str(value)
    
    return value_str, q_order 