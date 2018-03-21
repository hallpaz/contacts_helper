from utils import phone_canonicalform

NAMES = 'names'
DISPLAYNAME = 'displayName'
GIVENNAME = 'givenName'
MIDDLENAME = 'middleName'
FAMILYNAME = 'familyName'
EMAILS = 'emailAddresses'
PHONENUMBERS = 'phoneNumbers'
CANONICALFORM = 'canonicalForm'
RESOURCENAME = 'resourceName'
VALUE = "value"

class WappContact:

    def extractdata(self, datadict):
        # print("extractdata")
        if datadict:
            # try:
            #     self._name = datadict[NAMES][0][DISPLAYNAME]
            # except(KeyError, IndexError):
            #     self._name = ""
            if datadict.get(NAMES, ""):
                # self._name = datadict[NAMES][0].get(DISPLAYNAME, "")
                self._given_name = datadict[NAMES][0].get(GIVENNAME, "")
                middlename = datadict[NAMES][0].get(MIDDLENAME, "")
                if middlename:
                    middlename = middlename + " "
                self._family_name = middlename + datadict[NAMES][0].get(FAMILYNAME, "")
            else:
                self._name = self._given_name = self._family_name = ""
            if datadict.get(EMAILS, ""):
                self._email = datadict[EMAILS][0].get(DISPLAYNAME, "")
            else:
                self._email = ""
            if datadict.get(PHONENUMBERS, ""):
                self._phone_number = ""
                index = 0
                while not self._phone_number and index < len(datadict[PHONENUMBERS]):
                    self._phone_number = phone_canonicalform(
                            datadict[PHONENUMBERS][0].get(VALUE, ""))
                    self._phone_index = index
                    index = index + 1
            else:
                self._phone_number = ""

        else:
            self._name = self._email = self._phone_number = ""
            self._phone_index = 0

    def builddata(wappcontact):
        # print("builddata")
        datadict = {}
        if type(wappcontact.name) is str and wappcontact.name:
            datadict[NAMES] = [{DISPLAYNAME: wappcontact.name}]
        if type(wappcontact.email) is str and wappcontact.email:
            datadict[EMAILS]= [{DISPLAYNAME: wappcontact.email}]
        if type(wappcontact.phone_number) is str and  wappcontact.phone_number:
            datadict[PHONENUMBERS] = [{CANONICALFORM: wappcontact.phone_number}]
        if wappcontact.resource_name():
            datadict[RESOURCENAME] = wappcontact.resource_name()
        return datadict


    def __init__(self, datadict={}):
        # print("init")
        self.data = datadict


    @property
    def data(self):
        # print("data getter")
        if not self._data:
            self._data = WappContact.builddata(self)
        return self._data

    @data.setter
    def data(self, value):
        # print("data setter")
        self._data = value
        self.extractdata(value)

    @property
    def name(self):
        # print("name getter")
        return "{} {}".format(self.given_name, self.family_name)

    # @name.setter
    # def name(self, value):
    #     # print("name setter")
    #     self._name = value
    #     #update representation
    #     if self.data.get(NAMES, []):
    #         self.data[NAMES][0][DISPLAYNAME] = value
    #     else:
    #         self.data[NAMES] = [{DISPLAYNAME: value}]

    @property
    def given_name(self):
        # print("name getter")
        return self._given_name

    @given_name.setter
    def given_name(self, value):
        # print("name setter")
        self._given_name = value
        #update representation
        if self.data.get(NAMES, []):
            self.data[NAMES][0][GIVENNAME] = value
        else:
            self.data[NAMES] = [{GIVENNAME: value}]

    @property
    def family_name(self):
        # print("name getter")
        return self._family_name

    @family_name.setter
    def family_name(self, value):
        # print("name setter")
        self._family_name = value
        #update representation
        if self.data.get(NAMES, []):
            self.data[NAMES][0][FAMILYNAME] = value
        else:
            self.data[NAMES] = [{FAMILYNAME: value}]

    @property
    def email(self):
        # print("email getter")
        return self._email

    @email.setter
    def email(self, value):
        # print("email setter")
        self._email = value

        if self.data.get(EMAILS, []):
            self.data[EMAILS][0][DISPLAYNAME] = value
        else:
            self.data[EMAILS] = [{DISPLAYNAME: value}]

    @property
    def phone_number(self):
        # print("phone getter")
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        # print("phone setter")
        self._phone_number = value

        if self.data.get(PHONENUMBERS, []):
            self.data[PHONENUMBERS][self._phone_index][VALUE] = value
        else:
            self.data[PHONENUMBERS] = [{VALUE: value}]

    def resource_name(self):
        """Returns object resource name"""

        return self._data.get(RESOURCENAME, "")

    def __str__(self):
        representation = "{} | {} | {}".format(
            self.name, self.phone_number, self.email)
        return representation

    def __repr__(self):
        return str(self.data)

    def __lt__(self, rhs):
        return self.name < rhs.name

    def __le__(self, rhs):
        return self.name <= rhs.name


class ContactGroup:

    def __init__(self, datadict):
        self.data = datadict

    def name(self):
        return self.data.get('name')

    def member_count(self):
        return self.data.get('memberCount')

    def group_type(self):
        return self.data.get('groupType')

    def resource_name(self):
        """Returns object resource name"""

        return self.data.get(RESOURCENAME)

    def __str__(self):
        representation = "Grupo: {} | {} membros".format(self.name(), self.member_count())
        return representation



#
# {
#     'etag': '%EgcBAxxxxxxxxxxxxxxxxxxxxxxxxxxxmdqQWczbz0=', 'resourceName': 'people/c2205099584422993858',
#     'phoneNumbers': [{
#         'canonicalForm': '+5521973095570',
#         'formattedType': 'Mobile',
#         'metadata': {
#             'source': {
#                 'type': 'CONTACT',
#                 'id': '1e9a187658fe4dfc2'},
#             'primary': True},
#         'value': '0552199999999',
#         'type': 'mobile'}],
#     'names': [{
#         'familyName': 'Deschamps',
#         'givenName': 'Eduardo',
#         'metadata': {
#             'source': {
#                 'type': 'CONTACT',
#                 'id': '1e9a000000fe4dfc2'},
#             'primary': True},
#         'displayName': 'Eduardo Deschamps',
#         'displayNameLastFirst': 'Deschamps, Eduardo'}]
# }
