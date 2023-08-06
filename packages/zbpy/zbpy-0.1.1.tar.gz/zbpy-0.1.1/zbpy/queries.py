from .basicqueries import *

class Field():
    """
    An instance of this class allows you to query your Zetabase table by field. 
    """
    
    def __init__(self, field):
        """
        Initializes an instance of class Field whose field (self.field) value corrosponds to the indexed field of a table. 

        Parameters:
            field: string

        Returns: 
            Field 
        """
        self.field = field
    
    def __eq__(self, other):
        assert type(other) in BASIC_TYPES, f'Cannot compare Field with: {type(other)}'
      
        query = QueryEquals(self.field, other)
        return Expression(query)

    def __ne__(self, other):
        assert type(other) in BASIC_TYPES, f'Cannot compare Field with: {type(other)}'

        query = QueryNotEqual(self.field, other)
        return Expression(query)

    def __lt__(self, other):
        assert type(other) in BASIC_TYPES, f'Cannot compaire Field with {type(other)}'
       
        query = QueryLessThan(self.field, other)
        return Expression(query)

    def __gt__(self, other):
        assert type(other) in BASIC_TYPES, f'Cannot compare Field with: {type(other)}'
       
        query = QueryGreaterThan(self.field, other)
        return Expression(query)

    def __le__(self, other):
        assert type(other) in BASIC_TYPES, f'Cannot compare Field with: {type(other)}'
       
        query = QueryLessThanEqual(self.field, other)
        return Expression(query)
    
    def __ge__(self, other):
        assert type(other) in BASIC_TYPES, f'Cannot compare Field with: {type(other)}'
       
        query = QueryGreaterThanEqual(self.field, other)
        return Expression(query)

    def __mod__(self, other):
        assert type(other) in BASIC_TYPES, f'Cannot compare Field with: {type(other)}'

        query = QueryTextSearch(self.field, other)
        return Expression(query)

class Expression():

    def __init__(self, expression):
        """
        Initializes an instance of class Expression.

        Parameters:
            expression: QueryEquals, QueryGreaterThan, QueryGreaterThanEqual, QueryLessThan, or QueryLessThanEqual
        """
        assert type(expression) in BASIC_EXPRESSIONS, f'Cannot initialize expression with: {type(expression)}'
       
        self.expression = expression 

    def __and__(self, other):
        assert type(other) in ALL_EXPRESSIONS, f'Cannot compare Expression with: {type(other)}'
        
        if isinstance(other, AndExpression) or isinstance(other, OrExpression):
            return AndExpression(self.expression, other)
        return AndExpression(self.expression, other.expression)
    
    def __or__(self, other):
        assert type(other) in ALL_EXPRESSIONS, f'Cannot compare Expression with: {type(other)}'
        
        if isinstance(other, AndExpression) or isinstance(other, OrExpression):
            return OrExpression(self.expression, other)
        return OrExpression(self.expression, other.expression)

    def to_sub_query(self):
        """
        Return TableSubQuery object. 
        """        
        return self.expression.to_sub_query()

class AndExpression():

    def __init__(self, expression1, expression2):
        """
        Initializes instance of class AndExpression. 
        """
        assert type(expression1) in ALL_EXPRESSIONS, f'Type {type(expression1)} not acceptable'
        assert type(expression2) in ALL_EXPRESSIONS, f'Type {type(expression2)} not acceptable'
       
        self.expression1 = expression1
        self.expression2 = expression2

    def to_sub_query(self):
        """
        Return TableSubQuery object. 
        """        
        and_query = QueryAnd(self.expression1, self.expression2)
        return and_query.to_sub_query()

    def __and__(self, other):
        assert type(other) in ALL_EXPRESSIONS, f'Cannot compare AndExpression with: {type(other)}'
       
        return AndExpression(self, other)

    def __or__(self, other):
        return OrExpression(self, other)

class OrExpression():

    def __init__(self, expression1, expression2):
        assert type(expression1) in ALL_EXPRESSIONS, f'Type {type(expression)} not acceptable'
        assert type(expression2) in ALL_EXPRESSIONS, f'Type {type(expression)} not acceptable'

        self.expression1 = expression1 
        self.expression2 = expression2 

    def to_sub_query(self):
        """
        Return TableSubQuery object. 

        Parameters:
            table_owner_id: string 
            table_id: string 
        """        
        or_query = QueryOr(self.expression1, self.expression2)
        return or_query.to_sub_query()

    def __and__(self, other):
        assert type(other) in ALL_EXPRESSIONS, f'Cannot compare OrExpression with {type(other)}'

        return AndExpression(self, other)

    def __or__(self, other):
        assert type(other) in ALL_EXPRESSIONS, f'Cannot compare OrExpression with {type(other)}'

        return OrExpression(self, other)

BASIC_TYPES = [str, bool, int, float]
BASIC_EXPRESSIONS = [QueryEquals, QueryNotEqual, QueryGreaterThan, QueryGreaterThanEqual, QueryLessThan, QueryLessThanEqual, QueryTextSearch]
ALL_EXPRESSIONS = [QueryEquals, QueryNotEqual, QueryGreaterThan, QueryGreaterThanEqual, QueryLessThan, QueryLessThanEqual, QueryTextSearch, AndExpression, OrExpression, Expression]