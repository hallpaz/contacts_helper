import httplib2
import os
import time

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow

from models import WappContact, ContactGroup
from utils import lendigits

CONNECTIONS = 'connections'
RESOURCE_NAME = "people/me"
FACEDIGIT = 5
NEXTPAGETOKEN = 'nextPageToken'
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


def get_contacts_list(service, fields, page_size=2000):
        results = service.people().connections().list(
                    resourceName=RESOURCE_NAME,
                    personFields=fields,
                    pageSize=pageSize).execute()
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
            body=wappcontact.data,
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


def get_total_items(firstdigit):
    # TODO: cache items on firebase or on sql database (SQLite)
    contacts_list = []
    page_size = 2000
    results = service.people().connections().list(
                    resourceName=RESOURCE_NAME,
                    personFields='names',
                    pageSize=page_size).execute()
    contacts_list.extend(results.get(CONNECTIONS, []))
    while len(contacts_list)%page_size == 0:
        next_page = results.get(NEXTPAGETOKEN)
        results = service.people().connections().list(
                        resourceName=RESOURCE_NAME,
                        personFields='names',
                        pageSize=page_size,
                        pageToken=next_page).execute()
        contacts_list.extend(results)

    filtered_contacts = [c for c in contacts_list if c.name[0] == str(digit)]
    # compute new index
    index = len(filtered_contacts) + 1
    # get the size in digits of the code in use
    charsize = len(filtered_contacts[0].name.split()[0])

    return 0

def update_total_items(firstdigit, amount=1):
    # TODO: increment items on cached data adding **amount** to it
    pass

def get_new_code(digit, charsize):
    index = get_total_items(digit) + 1
    code = str(digit) + (charsize-lendigits(index)-1)*'0' + str(index)
    update_total_items(digit)
    return code


def new_supporter(phone, digit=FACECODE, name=""):
    contact = WappContact()
    contact.phone_number = phone
    # TODO:


def enumerate_contacts(contacts, firstdigit, charsize):
    index = 1
    firstdigit = str(firstdigit)
    for contact in contacts:
        # firstdigit + number of 0s needed to fill charsize + index
        code = firstdigit + (charsize-lendigits(index)-1)*'0' + str(index)

        parts = contact.name.split()
        parts[0] = code
        # newname = " ".join(parts)
        # contact.name = newname
        contact.given_name = code
        if len(parts) > 1:
            contact.family_name = " ".join(parts[1:])
        else:
            contact.family_name = ""
        index = index+1

    return contacts

def work_and_enumerate(contacts, charsize=6):
    reenumerated = []
    for i in range(0,5):
        current = [c for c in contacts if c.name.startswith(str(i))]
        if current:
            reenumerated.append(enumerate_contacts(current, i, charsize))

    return reenumerated



CLIENT_ID= os.environ['CLIENT_ID']
CLIENT_SECRET= os.environ['CLIENT_SECRET']
SCOPE='https://www.googleapis.com/auth/contacts'

if __name__ == '__main__':
    http = authorize_app(CLIENT_ID, CLIENT_SECRET,SCOPE)
    people_service = build(serviceName='people', version='v1', http=http)
    contacts_list = get_contacts_list(people_service, 'names,emailAddresses,phoneNumbers', pageSize=2000)

    groups_list = get_groups_list(people_service)

    contacts = []
    testcontact = None
    for person in contacts_list:
        contact = WappContact(person)
        if contact.name[0].isdigit():
            contacts.append(contact)


    print(len(contacts), 'NUMBERS')
    sorted(contacts)
    reenumerateds = work_and_enumerate(contacts)
    #
    for contacts in reenumerateds:
        for i in range(len(contacts)):
            # if not contacts[i].phone_number:
            print(i, contacts[i], 'MOD')
            # print(repr(contacts[i]))
            time.sleep(1)
            modify_contact(people_service, contacts[i], 'names,phoneNumbers')

                # print(repr(contacts[i]))
        print("------------------------------")

    #
    #
    #
    #
    # contact_groups = []
    # for group_data in groups_list:
    #     contact_groups.append(ContactGroup(group_data))
    #
    # # pass Marden to "Pessoal" group
    # supporters_group = [g for g in contact_groups if g.name()=="Apoiadores"][0]
    # # marden = [p.resource_name() for p in contacts if p.name()=="Marden Rodrigues"][0]
    #
    # # modify_group(people_service, supporters_group, contacts_add=[marden])
    #
    # contacts = work_and_enumerate(contacts, 6)
    # current_index = 0
    # found = False
    # for i in range(len(contacts)):
    #     newindex = contacts[i].name[0]
    #     if newindex.isdigit():
    #         found = True
    #     if newindex != current_index:
    #         print("---------------------------")
    #         current_index = newindex
    #     print(i, contacts[i])

    # for i in range(len(contact_groups)):
    #     print(i, contact_groups[i])
