# EDITH database documentation

## Tables
There are 5 tables (defined in `edith/app/models.py`):

|  Tables in EDITH | Purpose |
| ------------ |---|
| users |defines users|
| departments| defines BAMPFA departments, to which users are assigned|
| metadata_sources |defines databases to be queried for descriptive metadata|
| metadata_fields|defines metadata fields in the system |
| paths | defines paths such as the system shared directory (EDITH watched folder) [WIP] |

---

### Users
|  field name | purpose  | data example  |
| ------------ | ------------ | ------------ |
|  id | unique id  | 42  |
|  email | user's email address  | me@example.com  |
| username  | username  | fuzzywuzzy  |
|  first_name | user's first name  | John  |
| last_name  |  user's last name | Lennon  |
| RSusername  |  username from ResourceSpace (used in API call) | fuzzywuzzy77  |
|  RSkey | API key from ResourceSpace  | 12345  |
|  password_hash |  hash of user's password | 09jin4nkj4   |
|  department_id |  system id of user's department | 13   |
|  is_admin | yes/no is the user an administrator?  | No |

### Departments
|  field name | purpose  | data example  |
| ------------ | ------------ | ------------ |
|  id | unique id  | 42  |
|  deptname | display name of department  | accounting  |
| description  | a free text description  | accounting is boring, don't let them access any videos  |

### Data_Sources
|  field name | purpose  | data example  |
| ------------ | ------------ | ------------ |
|  id | unique id  | 42  |
|  dbName | display name of the database  | a_database  |
| fmpLayout  | FileMaker layout to be accessed by the XML API if applicable  | Some_Layout  |
|  IPaddress | the IP address or server address of the database  | 1.2.3.4 / myserver.com  |
| namespace | Namespace for XML/XPATH queries. This is used by `lxml` to parse the XML returned from FileMaker and is required (parsing will fail and nothing will be returned without it!) | {"filemaker":"http://www.filemaker.com/xml/fmresultset"} |
| username  |  user name with read access to the db | fuzzywuzzy  |
| credentials  |  password for above user | cool_password  |
|  primaryAssetID | name of field in db with the first identifier that queries should use to find an asset (should be unique to db)  | `accessionNumber`  |
|  secondaryAssetID |  name of field in db with a second identifier that queries should use to find an asset in case the first one fails or is absent (should be unique to db) | `barcode`   |
|  tertiryAssetID |  name of field in db with a third identifier that queries should use to find an asset in case the first two fail or are absent (should be unique to db) | `FileMaker record id`   |

### Metadata_Fields
|  field name | purpose  | data example  |
| ------------ | ------------ | ------------ |
|  id | unique id  | 42  |
|  fieldName | display name of the field  | cool field!  |
| fieldUniqueName  | name for the field that is internally unique  | coolField  |
|  fieldSourceName | name of the field in an external data source  | cool_field  |
| fieldCategory  |  category that a field belongs to (hard coded in select field in front end now) | Events  |
| dataSource_id  |  id of data source the field belongs to | 2  |
|  rsFieldID | integer id for field in ResourceSpace  | 34  |
|  description |  free text description of field | this field is for alternative titles only   |

### Paths [WIP/not used now]
|  field name | purpose  | data example  |
| ------------ | ------------ | ------------ |
|  id | unique id  | 42  |
|  fullPath | full path being defined  | /home/user/folder  |
| IPaddress  | ip address of system where the path is  | 1.2.3.4 / localhost  |
| description  | a free text description  | this is the path to the shared directory  |
