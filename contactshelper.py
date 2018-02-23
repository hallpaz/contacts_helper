import httplib2

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow

from models import WappContact, ContactGroup
from utils import lendigits

CONNECTIONS = 'connections'
RESOURCE_NAME = "people/me"
# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for
# installed applications.
#
# Go to the Google API Console, open your application's
# credentials page, and copy the client ID and client secret.
# Then paste them into the following code.
def authorize_app(client_id, client_secret, scope, user_agent='managing-contacts/1'):
    FLOW = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        user_agent=user_agent)

    # If the Credentials don't exist or are invalid, run through the
    # installed application flow. The Storage object will ensure that,
    # if successful, the good Credentials will get written back to a
    # file.
    storage = Storage('info.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
      credentials = run_flow(FLOW, storage)

    # Create an httplib2.Http object to handle our HTTP requests and
    # authorize it with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)
    return http


def get_contacts_list(service, fields):
    results = service.people().connections().list(resourceName=RESOURCE_NAME,
        personFields=fields).execute()
    connections = results.get(CONNECTIONS, [])
    return connections

def get_groups_list(service):
    results = service.contactGroups().list().execute()
    return results.get('contactGroups', [])


def create_contact(service, wappcontact):
    results = service.people().createContact(body=repr(wappcontact)).execute()
    return results

def modify_contact(service, wappcontact, update_person_fields):
    results = service.people().updateContact(
            resourceName=wappcontact.resource_name(),
            body=repr(wappcontact),
            updatePersonFields=update_person_fields).execute()
    return results

def delete_contact(service, wappcontact):
    results = service.people().deleteContact(resource_name()).execute()
    return results

def modify_group(service, group, contacts_add, contacts_remove=[]):
    body = { "resourceNamesToAdd": contacts_add,
           "resourceNamesToRemove": contacts_remove}

    results = service.contactGroups().members().modify(
        resourceName=group.resource_name(), body=body).execute()

    return results


def enumerate_contacts(contacts, firstdigit, charsize):
    index = 1
    firstdigit = str(firstdigit)
    for contact in contacts:
        # firstdigit + number of 0s needed to fill charsize + index
        newname = firstdigit + (charsize-lendigits(index)-1)*'0' + str(index)
        contact.name = newname

    return contacts


CLIENT_ID=''
CLIENT_SECRET=''
SCOPE='https://www.googleapis.com/auth/contacts'

if __name__ == '__main__':
    http = authorize_app(CLIENT_ID, CLIENT_SECRET,SCOPE)
    people_service = build(serviceName='people', version='v1', http=http)
    contacts_list = get_contacts_list(people_service, 'names,emailAddresses,phoneNumbers')

    groups_list = get_groups_list(people_service)

    contacts = []
    for person in contacts_list:
        contact = WappContact(person)
        contacts.append(contact)

    contact_groups = []
    for group_data in groups_list:
        contact_groups.append(ContactGroup(group_data))

    # pass Marden to "Pessoal" group
    personal_group = [g for g in contact_groups if g.name()=="Pessoal"][0]
    marden = [p.resource_name() for p in contacts if p.name()=="Marden Rodrigues"][0]

    modify_group(people_service, personal_group, contacts_add=[marden])

    for i in range(len(contacts)):
        print(i, contacts[i])
    print("---------------------------")
    for i in range(len(contact_groups)):
        print(i, contact_groups[i])
