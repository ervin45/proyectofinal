from datetime import datetime
from turbogears.database import PackageHub
from sqlobject import *
from turbogears import identity

hub = PackageHub('bielerDW')
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass
 
# identity models.
class Visit(SQLObject):
    """
    A visit to your site
    """
    class sqlmeta:
        table = 'visit'

    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(SQLObject):
    """
    A Visit that is link to a User object
    """
    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_group'

    group_name = UnicodeCol(length=16, alternateID=True,
                            alternateMethodName='by_group_name')
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)

    # collection of all users belonging to this group
    users = RelatedJoin('User', intermediateTable='user_group',
                        joinColumn='group_id', otherColumn='user_id')

    # collection of all permissions for this group
    permissions = RelatedJoin('Permission', joinColumn='group_id',
                              intermediateTable='group_permission',
                              otherColumn='permission_id')


class User(SQLObject):
    """
    Reasonably basic User definition.
    Probably would want additional attributes.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_user'

    user_name = UnicodeCol(length=16, alternateID=True,
                           alternateMethodName='by_user_name')
    email_address = UnicodeCol(length=255, alternateID=True,
                               alternateMethodName='by_email_address')
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)

    # groups this user belongs to
    groups = RelatedJoin('Group', intermediateTable='user_group',
                         joinColumn='user_id', otherColumn='group_id')

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    def _set_password(self, cleartext_password):
        "Runs cleartext_password through the hash algorithm before saving."
        password_hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(password_hash)

    def set_password_raw(self, password):
        "Saves the password as-is to the database."
        self._SO_set_password(password)


class Permission(SQLObject):
    """
    A relationship that determines what each Group can do
    """
    permission_name = UnicodeCol(length=16, alternateID=True,
                                 alternateMethodName='by_permission_name')
    description = UnicodeCol(length=255)

    groups = RelatedJoin('Group',
                         intermediateTable='group_permission',
                         joinColumn='permission_id',
                         otherColumn='group_id')
from turbogears import widgets                         
                         
                         
class xmlaResponse:
    def getMemberCaption(self,m):
        caption = ""
        for item in m:
            caption = caption + item[1].text + " "
        return caption
                                     
    def response1(self, mdx):                                     
        import cElementTree as ET
        tree = ET.parse("/home/chinomng/utn/proyecto/proyectofinal/lab/mdx/mdxA-1-salida.xml")

        envelope= tree.getroot()
        body = envelope[1]
        ExecuteResponse = body[0]
        ereturn = ExecuteResponse[0]
        root = ereturn[0]
        CellData = root[3]
        Axes = root[2]
        TuplesAxes0 = Axes[0][0]
        TuplesAxes1 = Axes[1][0]
        
        filas = []
        filas.append([1,2,3,4])
        filas.append([5,6,7,8])
        filas.append([9,10,11,12])
                
        columns = []
        for item in TuplesAxes0:
                columns.append(self.getMemberCaption(item))
                
        print columns        
                
        rows = []
        for item in TuplesAxes1:
                rows.append(self.getMemberCaption(item))
                
        print rows        
                
        cells = []
        for item in CellData:
            cells.append(item[0].text)
            
        print cells    
                            
        mod = len(columns)
        print mod
        table = []
        r = [""] + columns 
        print r
        table.append(r)
        for i,item in enumerate(rows):
            r = [item] + cells[i*mod:(i+1)*mod]
            table.append(r)      

        return table
        
    def response2(self, mdx):                                     
        import cElementTree as ET
        tree = ET.parse("/home/chinomng/utn/proyecto/proyectofinal/lab/mdx/mdxA-2-salida.xml")

        envelope= tree.getroot()
        body = envelope[1]
        ExecuteResponse = body[0]
        ereturn = ExecuteResponse[0]
        root = ereturn[0]
        CellData = root[3]
        Axes = root[2]
        TuplesAxes0 = Axes[0][0]
        TuplesAxes1 = Axes[1][0]
        
        filas = []
        filas.append([1,2,3,4])
        filas.append([5,6,7,8])
        filas.append([9,10,11,12])
                
        columns = []
        for item in TuplesAxes0:
                columns.append(self.getMemberCaption(item))
                
        print columns        
                
        rows = []
        for item in TuplesAxes1:
                rows.append(self.getMemberCaption(item))
                
        print rows        
                
        cells = []
        for item in CellData:
            cells.append(item[0].text)
            
        print cells    
                            
        mod = len(columns)
        print mod
        table = []
        r = [""] + columns 
        print r
        table.append(r)
        for i,item in enumerate(rows):
            r = [item] + cells[i*mod:(i+1)*mod]
            table.append(r)      

        return table        
        
    def response3(self, mdx):                                     
        import cElementTree as ET
        tree = ET.parse("/home/chinomng/utn/proyecto/proyectofinal/lab/mdx/mdxA-3-salida.xml")

        envelope= tree.getroot()
        body = envelope[1]
        ExecuteResponse = body[0]
        ereturn = ExecuteResponse[0]
        root = ereturn[0]
        CellData = root[3]
        Axes = root[2]
        TuplesAxes0 = Axes[0][0]
        TuplesAxes1 = Axes[1][0]
        
        filas = []
        filas.append([1,2,3,4])
        filas.append([5,6,7,8])
        filas.append([9,10,11,12])
                
        columns = []
        for item in TuplesAxes0:
                columns.append(self.getMemberCaption(item))
                
        print columns        
                
        rows = []
        for item in TuplesAxes1:
                rows.append(self.getMemberCaption(item))
                
        print rows        
                
        cells = []
        for item in CellData:
            cells.append(item[0].text)
            
        print cells    
                            
        mod = len(columns)
        print mod
        table = []
        r = [""] + columns 
        print r
        table.append(r)
        for i,item in enumerate(rows):
            r = [item] + cells[i*mod:(i+1)*mod]
            table.append(r)      

        return table        
