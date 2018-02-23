

NAMES = 'names'
DISPLAYNAME = 'displayName'
EMAILS = 'emailAddresses'
PHONENUMBERS = 'phoneNumbers'
CANONICALFORM = 'canonicalForm'
RESOURCENAME = 'resourceName'

class WappContact:

    def extractdata(datadict):
        pass

    def builddata(wappcontact):
        data = {}
        if wappcontact.name:
            data[NAMES] = [{DISPLAYNAME: wappcontact.name}]
        if wappcontact.email:
            data[EMAILS]= [{DISPLAYNAME: wappcontact.email}]
        if wappcontact.phone_number:
            data[PHONENUMBERS] = [CANONICALFORM: wappcontact.phone_number]
        if wappcontact.resource_name:
            data[RESOURCENAME] = wappcontact.resource_name
        return data


    def __init__(self, datadict={}):
        self.data = datadict

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        #update representation
        if self.data.get(NAMES, []):
            self.data[NAMES][0][DISPLAYNAME] = self.value
        else:
            self.data[NAMES] = [{DISPLAYNAME: self.value}]

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value
        #TODO update data representation
        if self.data.get(EMAILS, []):
            self.data[EMAILS][0][DISPLAYNAME] = self.value
        else:
            self.data[EMAILS] = [{DISPLAYNAME: self.value}]

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value
        #TODO: update data representation

        if self.data.get(NAMES, []):
            self.data[PHONENUMBERS][0][CANONICALFORM] = self.value
        else:
            self.data[NAMES] = [{CANONICALFORM: self.value}]

    #TODO: make property
    def name(self):
        """Returns the displayName of the name field"""

        return self.data.get(NAMES)[0].get(DISPLAYNAME)

    def email(self):
        """ Returns the displayName of the email field"""
        if not self.data.get(EMAILS, []):
            return ""
        return self.data.get(EMAILS)[0].get(DISPLAYNAME, "")

    def phone_number(self):
        """Returns phone number canonical form"""
        if not self.data.get(PHONENUMBERS, []):
            return ""
        return self.data.get(PHONENUMBERS)[0].get(CANONICALFORM, "")

    def resource_name(self):
        """Returns object resource name"""

        return self.data.get(RESOURCENAME)

    def __str__(self):
        representation = "{} | {} | {}".format(
            self.name(), self.phone_number(), self.email())
        return representation

    def __repr__(self):
        if self.data:
            return self.data



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
