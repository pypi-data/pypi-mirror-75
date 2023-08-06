from .zbprotocol_pb2 import PermissionsEntry, PermissionConstraint, FieldConstraintType, PermissionConstraintType, FieldConstraint, FieldConstraintValueType

class PermConstraint():

    def __init__(self, field, req_value='@uid'):
        """
        Initializes PermConstraint on the specified field with a given required value. 

        Parameters:
            field: string 
            req_value: string (default='@uid')

        Returns:
            PermConstraint 
        """
        self.field = field 
        self.req_value = req_value 

    
class PermEntry():

    def __init__(self, level, audience_type, audience_id=''):
        """
        Initializes PermEntry with given level, audience_type, and audience_id. 

        Parameters:
            level: PermissionLevel  
            audience_type: PermissionAudienceType 
            audience_id: string (default='')

        Returns:
            PermEntry
        """
        self.level = level 
        self.audience_type = audience_type 
        self.audience_id = audience_id 
        self.constraints = [] 

    def add_constraint(self, c):
        """
        Adds constraint to the PermEntry. 

        Parameters:
            c: PermConstraint
        """
        self.constraints.append(c)

    def to_protocol(self, uid, table_id):
        """
        Returns PermissionsEntry object. 

        Parameters:
            uid: string 
            table_id: string

        Returns: 
            PermissionsEntry
        """
        return PermissionsEntry(
            id=uid,
            tableId=table_id,
            audienceType=self.audience_type,
            audienceId=self.audience_id,
            level=self.level,
            nonce=0,
            credential=None,
            constraints=to_field_constraints(uid, table_id, self.constraints)
        )


def to_field_constraint(uid, table_id, cs):
    """
    Returns PermissionConstraint object. 

    Parameters: 
        uid: string 
        table_id: string 
        cs: PermConstraint object 

    Returns: 
        PermissionConstraint 
    """
    f_typ = FieldConstraintValueType.CONSTANT 
    f_val = cs.req_value 

    if cs.req_value.lower() == '@uid':
        f_typ = FieldConstraintValueType.UID 
        f_val = ''
    elif cs.req_value.lower() == '@time':
        f_typ = FieldConstraintValueType.TIMESTAMP
        f_val = ''
    elif cs.req_value.lower() == '@order':
        f_typ = FieldConstraintValueType.NATURAL_ORDER
        f_val = ''
    elif cs.req_value.lower() == '@random':
        f_typ = FieldConstraintValueType.RANDOM
        f_val = ''

    return PermissionConstraint(
        constraintType=PermissionConstraintType.FIELD,
        fieldConstraint=FieldConstraint(
            constraintType=FieldConstraintType.EQUALS_VALUE,
            fieldKey=cs.field,
            valueType=f_typ,
            requiredValue=f_val
        )
    )

def to_field_constraints(uid, table_id, cs):
    """
    Returns PermissionConstraint object. 

    Paramters:
        uid: string 
        table_id: string 
        cs: PermConstraint object 

    Returns: 
        PermissionConstraint 
    """
    fcs = []
    
    for i in cs:
        fcs.append(to_field_constraint(uid, table_id, i))

    return fcs 