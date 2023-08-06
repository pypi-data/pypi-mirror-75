import requests
import json
import os
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

class HttpMethod:

    """
    HttpMethod will have methods to send
    GET, POST, PATCH, PUT, DELETE request to the initalized url
    """
   
    def __init__(self, extension, session, *args, **kwargs):
        self.url = "https://api.intra.42.fr{}".format(extension)
        self.filter = kwargs["format"] if "format" in kwargs else {}
        self.page = kwargs["pages"] if "pages" in kwargs else {'size':100, 'number':1}
        self.sort = kwargs["sort"] if "sort" in kwargs else ""
        self.session = session

    def ParseParams(self):

        filter_query = "&".join([f"filter[{key}]={value}" for key, value in self.filter.items()]) if self.filter else ""
        page_query = "&".join([f"page[{key}]={value}" for key, value in self.page.items()]) if self.page else ""

        result = filter_query or page_query
        if filter_query and page_query:
            result = f"?{filter_query}&{page_query}"

        if self.sort:
            if result:
                result += f"&sort={self.sort}"
            else:
                result = f"sort={self.sort}"

        return f"?{result}" if result else ""
 
    def Get(self):
        """
        return json
        """
        response = self.session.get(self.url + self.ParseParams())
        response.raise_for_status()
        if self.page and "number" in self.page: self.page['number'] += 1
        return json.loads(response.text)

    def Post(self, data):
        """
        return response Object
        """
        response = self.session.post(self.url, json=data)
        response.raise_for_status()
        return response

    def Patch(self, data):
        """
        return response Object
        """
        response = self.session.patch(self.url, json=data)
        response.raise_for_status()
        return response

    def Put(self, data):
        """
        return response Object
        """
        response = self.session.put(self.url, json=data)
        response.raise_for_status()
        return response

    def Delete(self):
        """
        return response Object
        """
        response = self.session.delete(self.url)
        response.raise_for_status()
        return response

class FtApi:

    def __init__(self, uid, secret):
        self.uid = uid
        self.secret = secret
        try:
            self.bearer = self.GetBearer()
        except Exception as e:
            raise Exception(e)
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer {}'.format(self.bearer)})

    def GetBearer(self):
        """
        Makes a call to get Bearer with your crendentials
        return: string
        """
        payload = {'grant_type':'client_credentials', 'client_id': self.uid,
                'client_secret': self.secret}
        try:
            test = requests.post("https://api.intra.42.fr/oauth/token", data=payload)
            if test.status_code != 200:
                raise Exception("wrong status_code:{}".format(test.status_code))
            parsed_response = json.loads(test.content.decode('utf-8'))
        except Exception as e:
            raise Exception(e)
        
        return parsed_response['access_token']

    def ReloadBearer(self):
        """
        Use this method in case 'The access token expired'
        """
        self.bearer = self.GetBearer()
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer {}'.format(self.bearer)})

    def RawEndpoint(self, endpoint):
        """
        parameter : string
        return : HttpMethod
        
        Create a HttpMethod with passed parameter as the endpoint for "https://api.intra.42.fr/"

        example :"/v2/users?filter[pool_year]=2019&page[size]=100&page[number]=3"
        """
        return HttpMethod(endpoint, self.session)

    def ColorizeJsonOutput(self, jsonObject):
        jsonStr = json.dumps(jsonObject, indent=4, sort_keys=True)
        print(highlight(jsonStr, JsonLexer(), TerminalFormatter()))

    def Accreditations(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/accreditations.html"
        """
        extension = "/v2/accreditations/{}".format(id) if id is not None else "/v2/accreditations"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Achievements(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/achievements.html"
        """
        extension = "/v2/achievements/{}".format(id) if id is not None else "/v2/achievements"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Achievements_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/achievements_users.html"
        """
        extension = "/v2/achievements_users/{}".format(id) if id is not None else "/v2/achievements_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Announcements(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/announcements.html"
        """
        extension = "/v2/announcements/{}".format(id) if id is not None else "/v2/announcements"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Apps(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/apps.html"
        """
        extension = "/v2/apps/{}".format(id) if id is not None else "/v2/apps"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Attachments(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/attachments.html"
        """
        extension = "/v2/attachments/{}".format(id) if id is not None else "/v2/attachments"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Balances(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/balances.html"
        """
        extension = "/v2/balances/{}".format(id) if id is not None else "/v2/balances"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Bloc_deadlines(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/bloc_deadlines.html"
        """
        extension = "/v2/bloc_deadlines/{}".format(id) if id is not None else "/v2/bloc_deadlines"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Blocs(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/blocs.html"
        """
        extension = "/v2/blocs/{}".format(id) if id is not None else "/v2/blocs"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Campus(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/campus.html"
        """
        extension = "/v2/campus/{}".format(id) if id is not None else "/v2/campus"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Campus_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/campus_users.html"
        """
        extension = "/v2/campus_users/{}".format(id) if id is not None else "/v2/campus_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Certificates(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/certificates.html"
        """
        extension = "/v2/certificates/{}".format(id) if id is not None else "/v2/certificates"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Certificates_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/certificates_users.html"
        """
        extension = "/v2/certificates_users/{}".format(id) if id is not None else "/v2/certificates_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Closes(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/closes.html"
        """
        extension = "/v2/closes/{}".format(id) if id is not None else "/v2/closes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Coalitions(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/coalitions.html"
        """
        extension = "/v2/coalitions/{}".format(id) if id is not None else "/v2/coalitions"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Coalitions_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/coalitions_users.html"
        """
        extension = "/v2/coalitions_users/{}".format(id) if id is not None else "/v2/coalitions_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Community_services(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/community_services.html"
        """
        extension = "/v2/community_services/{}".format(id) if id is not None else "/v2/community_services"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Cursus(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/cursus.html"
        """
        extension = "/v2/cursus/{}".format(id) if id is not None else "/v2/cursus"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Cursus_topics(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/cursus_topics.html"
        """
        extension = "/v2/cursus_topics/{}".format(id) if id is not None else "/v2/cursus_topics"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Cursus_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/cursus_users.html"
        """
        extension = "/v2/cursus_users/{}".format(id) if id is not None else "/v2/cursus_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Dashes(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/dashes.html"
        """
        extension = "/v2/dashes/{}".format(id) if id is not None else "/v2/dashes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Dashes_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/dashes_users.html"
        """
        extension = "/v2/dashes_users/{}".format(id) if id is not None else "/v2/dashes_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Endpoints(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/endpoints.html"
        """
        extension = "/v2/endpoints/{}".format(id) if id is not None else "/v2/endpoints"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Evaluations(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/evaluations.html"
        """
        extension = "/v2/evaluations/{}".format(id) if id is not None else "/v2/evaluations"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Events(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/events.html"
        """
        extension = "/v2/events/{}".format(id) if id is not None else "/v2/events"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Events_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/events_users.html"
        """
        extension = "/v2/events_users/{}".format(id) if id is not None else "/v2/events_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Exams(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/exams.html"
        """
        extension = "/v2/exams/{}".format(id) if id is not None else "/v2/exams"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Experiences(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/experiences.html"
        """
        extension = "/v2/experiences/{}".format(id) if id is not None else "/v2/experiences"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Expertises(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/expertises.html"
        """
        extension = "/v2/expertises/{}".format(id) if id is not None else "/v2/expertises"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Expertises_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/expertises_users.html"
        """
        extension = "/v2/expertises_users/{}".format(id) if id is not None else "/v2/expertises_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Feedbacks(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/feedbacks.html"
        """
        extension = "/v2/feedbacks/{}".format(id) if id is not None else "/v2/feedbacks"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Flash_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/flash_users.html"
        """
        extension = "/v2/flash_users/{}".format(id) if id is not None else "/v2/flash_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Flashes(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/flashes.html"
        """
        extension = "/v2/flashes/{}".format(id) if id is not None else "/v2/flashes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Groups(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/groups.html"
        """
        extension = "/v2/groups/{}".format(id) if id is not None else "/v2/groups"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Groups_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/groups_users.html"
        """
        extension = "/v2/groups_users/{}".format(id) if id is not None else "/v2/groups_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Internships(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/internships.html"
        """
        extension = "/v2/internships/{}".format(id) if id is not None else "/v2/internships"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Languages(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/languages.html"
        """
        extension = "/v2/languages/{}".format(id) if id is not None else "/v2/languages"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Languages_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/languages_users.html"
        """
        extension = "/v2/languages_users/{}".format(id) if id is not None else "/v2/languages_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Locations(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/locations.html"
        """
        extension = "/v2/locations/{}".format(id) if id is not None else "/v2/locations"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Mailings(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mailings.html"
        """
        extension = "/v2/mailings/{}".format(id) if id is not None else "/v2/mailings"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Messages(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/messages.html"
        """
        extension = "/v2/messages/{}".format(id) if id is not None else "/v2/messages"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Notes(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/notes.html"
        """
        extension = "/v2/notes/{}".format(id) if id is not None else "/v2/notes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Notions(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/notions.html"
        """
        extension = "/v2/notions/{}".format(id) if id is not None else "/v2/notions"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Params_project_sessions_rules(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/params_project_sessions_rules.html"
        """
        extension = "/v2/params_project_sessions_rules/{}".format(id) if id is not None else "/v2/params_project_sessions_rules"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Partnerships(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/partnerships.html"
        """
        extension = "/v2/partnerships/{}".format(id) if id is not None else "/v2/partnerships"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Partnerships_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/partnerships_users.html"
        """
        extension = "/v2/partnerships_users/{}".format(id) if id is not None else "/v2/partnerships_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Patronages(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/patronages.html"
        """
        extension = "/v2/patronages/{}".format(id) if id is not None else "/v2/patronages"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Patronages_reports(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/patronages_reports.html"
        """
        extension = "/v2/patronages_reports/{}".format(id) if id is not None else "/v2/patronages_reports"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Pools(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/pools.html"
        """
        extension = "/v2/pools/{}".format(id) if id is not None else "/v2/pools"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Products(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/products.html"
        """
        extension = "/v2/products/{}".format(id) if id is not None else "/v2/products"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_data(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/project_data.html"
        """
        extension = "/v2/project_data/{}".format(id) if id is not None else "/v2/project_data"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessions(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/project_sessions.html"
        """
        extension = "/v2/project_sessions/{}".format(id) if id is not None else "/v2/project_sessions"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessions_rules(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/project_sessions_rules.html"
        """
        extension = "/v2/project_sessions_rules/{}".format(id) if id is not None else "/v2/project_sessions_rules"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessions_skills(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/project_sessions_skills.html"
        """
        extension = "/v2/project_sessions_skills/{}".format(id) if id is not None else "/v2/project_sessions_skills"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Projects(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/projects.html"
        """
        extension = "/v2/projects/{}".format(id) if id is not None else "/v2/projects"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Projects_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/projects_users.html"
        """
        extension = "/v2/projects_users/{}".format(id) if id is not None else "/v2/projects_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Quests(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/quests.html"
        """
        extension = "/v2/quests/{}".format(id) if id is not None else "/v2/quests"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Quests_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/quests_users.html"
        """
        extension = "/v2/quests_users/{}".format(id) if id is not None else "/v2/quests_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Roles(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/roles.html"
        """
        extension = "/v2/roles/{}".format(id) if id is not None else "/v2/roles"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Roles_entities(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/roles_entities.html"
        """
        extension = "/v2/roles_entities/{}".format(id) if id is not None else "/v2/roles_entities"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Rules(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/rules.html"
        """
        extension = "/v2/rules/{}".format(id) if id is not None else "/v2/rules"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Scale_teams(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/scale_teams.html"
        """
        extension = "/v2/scale_teams/{}".format(id) if id is not None else "/v2/scale_teams"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Scales(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/scales.html"
        """
        extension = "/v2/scales/{}".format(id) if id is not None else "/v2/scales"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Scores(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/scores.html"
        """
        extension = "/v2/scores/{}".format(id) if id is not None else "/v2/scores"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Skills(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/skills.html"
        """
        extension = "/v2/skills/{}".format(id) if id is not None else "/v2/skills"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Slots(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/slots.html"
        """
        extension = "/v2/slots/{}".format(id) if id is not None else "/v2/slots"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Subnotions(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/subnotions.html"
        """
        extension = "/v2/subnotions/{}".format(id) if id is not None else "/v2/subnotions"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Tags(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/tags.html"
        """
        extension = "/v2/tags/{}".format(id) if id is not None else "/v2/tags"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Teams(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/teams.html"
        """
        extension = "/v2/teams/{}".format(id) if id is not None else "/v2/teams"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Teams_uploads(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/teams_uploads.html"
        """
        extension = "/v2/teams_uploads/{}".format(id) if id is not None else "/v2/teams_uploads"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Teams_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/teams_users.html"
        """
        extension = "/v2/teams_users/{}".format(id) if id is not None else "/v2/teams_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Titles(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/titles.html"
        """
        extension = "/v2/titles/{}".format(id) if id is not None else "/v2/titles"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Titles_users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/titles_users.html"
        """
        extension = "/v2/titles_users/{}".format(id) if id is not None else "/v2/titles_users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Topics(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/topics.html"
        """
        extension = "/v2/topics/{}".format(id) if id is not None else "/v2/topics"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Transactions(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/transactions.html"
        """
        extension = "/v2/transactions/{}".format(id) if id is not None else "/v2/transactions"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Translations(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/translations.html"
        """
        extension = "/v2/translations/{}".format(id) if id is not None else "/v2/translations"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def User_candidatures(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/user_candidatures.html"
        """
        extension = "/v2/user_candidatures/{}".format(id) if id is not None else "/v2/user_candidatures"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Users(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/users.html"
        """
        extension = "/v2/users/{}".format(id) if id is not None else "/v2/users"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Votes(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/votes.html"
        """
        extension = "/v2/votes/{}".format(id) if id is not None else "/v2/votes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Waitlists(self, *args, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/waitlists.html"
        """
        extension = "/v2/waitlists/{}".format(id) if id is not None else "/v2/waitlists"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def AccreditationsUsers(self, accreditation_id, *args, **kwargs):
        extension = "/v2/accreditations/{}/users".format(accreditation_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def AchievementsUsers(self, achievement_id, *args, **kwargs):
        extension = "/v2/achievements/{}/users".format(achievement_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def AchievementsAchievements_users(self, achievement_id, *args, **kwargs):
        extension = "/v2/achievements/{}/achievements_users".format(achievement_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def BlocsScores(self, bloc_id, *args, **kwargs):
        extension = "/v2/blocs/{}/scores".format(bloc_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def BlocsScores(self, bloc_id, id, *args, **kwargs):
        extension = "/v2/blocs/{}/scores/{}".format(bloc_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def BlocsCoalitions(self, bloc_id, *args, **kwargs):
        extension = "/v2/blocs/{}/coalitions".format(bloc_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def BlocsBloc_deadlines(self, bloc_id, *args, **kwargs):
        extension = "/v2/blocs/{}/bloc_deadlines".format(bloc_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusUsers(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/users".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusNotes(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/notes".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusExams(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/exams".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusEvents(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/events".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusQuests(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/quests".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusProducts(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/products".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusLocations(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/locations".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusAchievements(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/achievements".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusProducts(self, campus_id, id, *args, **kwargs):
        extension = "/v2/campus/{}/products/{}".format(campus_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusLocationsEnd_all(self, campus_id, *args, **kwargs):
        extension = "/v2/campus/{}/locations/end_all".format(campus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusCursusExams(self, campus_id, cursus_id, *args, **kwargs):
        extension = "/v2/campus/{}/cursus/{}/exams".format(campus_id, cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CampusCursusEvents(self, campus_id, cursus_id, *args, **kwargs):
        extension = "/v2/campus/{}/cursus/{}/events".format(campus_id, cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CertificatesCertificates_users(self, certificate_id, *args, **kwargs):
        extension = "/v2/certificates/{}/certificates_users".format(certificate_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ClosesUnclose(self, id, *args, **kwargs):
        extension = "/v2/closes/{}/unclose".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ClosesCommunity_services(self, close_id, *args, **kwargs):
        extension = "/v2/closes/{}/community_services".format(close_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CoalitionsUsers(self, coalition_id, *args, **kwargs):
        extension = "/v2/coalitions/{}/users".format(coalition_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CoalitionsScores(self, coalition_id, *args, **kwargs):
        extension = "/v2/coalitions/{}/scores".format(coalition_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CoalitionsScores(self, coalition_id, id, *args, **kwargs):
        extension = "/v2/coalitions/{}/scores/{}".format(coalition_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CoalitionsCoalitions_users(self, coalition_id, *args, **kwargs):
        extension = "/v2/coalitions/{}/coalitions_users".format(coalition_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Coalitions_usersScores(self, coalitions_user_id, *args, **kwargs):
        extension = "/v2/coalitions_users/{}/scores".format(coalitions_user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Coalitions_usersScores(self, coalitions_user_id, id, *args, **kwargs):
        extension = "/v2/coalitions_users/{}/scores/{}".format(coalitions_user_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Community_servicesValidate(self, id, *args, **kwargs):
        extension = "/v2/community_services/{}/validate".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Community_servicesInvalidate(self, id, *args, **kwargs):
        extension = "/v2/community_services/{}/invalidate".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusTags(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/tags".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusTeams(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/teams".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusExams(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/exams".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusUsers(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/users".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusQuests(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/quests".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusTopics(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/topics".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusEvents(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/events".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusLevels(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/levels".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusSkills(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/skills".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusNotions(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/notions".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusProjects(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/projects".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusCursus_users(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/cursus_users".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusAchievements(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/achievements".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusCursus_topics(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/cursus_topics".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def CursusAnnouncements(self, cursus_id, *args, **kwargs):
        extension = "/v2/cursus/{}/announcements".format(cursus_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def DashesUsers(self, dash_id, *args, **kwargs):
        extension = "/v2/dashes/{}/users".format(dash_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def DashesDashes_users(self, dash_id, *args, **kwargs):
        extension = "/v2/dashes/{}/dashes_users".format(dash_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def EventsUsers(self, event_id, *args, **kwargs):
        extension = "/v2/events/{}/users".format(event_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def EventsWaitlist(self, event_id, *args, **kwargs):
        extension = "/v2/events/{}/waitlist".format(event_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def EventsFeedbacks(self, event_id, *args, **kwargs):
        extension = "/v2/events/{}/feedbacks".format(event_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def EventsEvents_users(self, event_id, *args, **kwargs):
        extension = "/v2/events/{}/events_users".format(event_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def EventsFeedbacks(self, event_id, id, *args, **kwargs):
        extension = "/v2/events/{}/feedbacks/{}".format(event_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ExamsWaitlist(self, exam_id, *args, **kwargs):
        extension = "/v2/exams/{}/waitlist".format(exam_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ExamsExams_users(self, exam_id, *args, **kwargs):
        extension = "/v2/exams/{}/exams_users".format(exam_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ExamsExams_users(self, exam_id, id, *args, **kwargs):
        extension = "/v2/exams/{}/exams_users/{}".format(exam_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ExpertisesUsers(self, expertise_id, *args, **kwargs):
        extension = "/v2/expertises/{}/users".format(expertise_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ExpertisesExpertises_users(self, expertise_id, *args, **kwargs):
        extension = "/v2/expertises/{}/expertises_users".format(expertise_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def FlashesFlash_users(self, flash_id, *args, **kwargs):
        extension = "/v2/flashes/{}/flash_users".format(flash_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def FlashesFlash_users(self, flash_id, id, *args, **kwargs):
        extension = "/v2/flashes/{}/flash_users/{}".format(flash_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def GroupsUsers(self, group_id, *args, **kwargs):
        extension = "/v2/groups/{}/users".format(group_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def GroupsGroups_users(self, group_id, *args, **kwargs):
        extension = "/v2/groups/{}/groups_users".format(group_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def IssuesTags(self, issue_id, *args, **kwargs):
        extension = "/v2/issues/{}/tags".format(issue_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Levels(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/levels.html"
        """
        extension = "/v2/levels"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Me(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/me.html"
        """
        extension = "/v2/me"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeVotes(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mevotes.html"
        """
        extension = "/v2/me/votes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeSlots(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/meslots.html"
        """
        extension = "/v2/me/slots"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeTeams(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/meteams.html"
        """
        extension = "/v2/me/teams"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeTopics(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/metopics.html"
        """
        extension = "/v2/me/topics"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeMessages(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/memessages.html"
        """
        extension = "/v2/me/messages"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeProjects(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/meprojects.html"
        """
        extension = "/v2/me/projects"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeScale_teams(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mescale_teams.html"
        """
        extension = "/v2/me/scale_teams"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeVotesUpvotes(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mevotesupvotes.html"
        """
        extension = "/v2/me/votes/upvotes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeVotesProblems(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mevotesproblems.html"
        """
        extension = "/v2/me/votes/problems"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeVotesDownvotes(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mevotesdownvotes.html"
        """
        extension = "/v2/me/votes/downvotes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeVotesTrollvotes(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mevotestrollvotes.html"
        """
        extension = "/v2/me/votes/trollvotes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeTopicsVotes(self, topic_id, *args, **kwargs):
        extension = "/v2/me/topics/{}/votes".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeScale_teamsAs_corrected(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mescale_teamsas_corrected.html"
        """
        extension = "/v2/me/scale_teams/as_corrected"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeScale_teamsAs_corrector(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mescale_teamsas_corrector.html"
        """
        extension = "/v2/me/scale_teams/as_corrector"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeMessagesVotes(self, message_id, *args, **kwargs):
        extension = "/v2/me/messages/{}/votes".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeTopicsVotesUpvotes(self, topic_id, *args, **kwargs):
        extension = "/v2/me/topics/{}/votes/upvotes".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeTopicsVotesProblems(self, topic_id, *args, **kwargs):
        extension = "/v2/me/topics/{}/votes/problems".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeTopicsVotesDownvotes(self, topic_id, *args, **kwargs):
        extension = "/v2/me/topics/{}/votes/downvotes".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeTopicsVotesTrollvotes(self, topic_id, *args, **kwargs):
        extension = "/v2/me/topics/{}/votes/trollvotes".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeMessagesVotesUpvotes(self, message_id, *args, **kwargs):
        extension = "/v2/me/messages/{}/votes/upvotes".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeMessagesVotesProblems(self, message_id, *args, **kwargs):
        extension = "/v2/me/messages/{}/votes/problems".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeMessagesVotesDownvotes(self, message_id, *args, **kwargs):
        extension = "/v2/me/messages/{}/votes/downvotes".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MeMessagesVotesTrollvotes(self, message_id, *args, **kwargs):
        extension = "/v2/me/messages/{}/votes/trollvotes".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MessagesVotes(self, message_id, *args, **kwargs):
        extension = "/v2/messages/{}/votes".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MessagesMessages(self, message_id, *args, **kwargs):
        extension = "/v2/messages/{}/messages".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MessagesVotesUpvotes(self, message_id, *args, **kwargs):
        extension = "/v2/messages/{}/votes/upvotes".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MessagesVotesProblems(self, message_id, *args, **kwargs):
        extension = "/v2/messages/{}/votes/problems".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MessagesVotesDownvotes(self, message_id, *args, **kwargs):
        extension = "/v2/messages/{}/votes/downvotes".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def MessagesVotesTrollvotes(self, message_id, *args, **kwargs):
        extension = "/v2/messages/{}/votes/trollvotes".format(message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def NotionsTags(self, notion_id, *args, **kwargs):
        extension = "/v2/notions/{}/tags".format(notion_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def NotionsSubnotions(self, notion_id, *args, **kwargs):
        extension = "/v2/notions/{}/subnotions".format(notion_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def PartnershipsUsers(self, partnership_id, *args, **kwargs):
        extension = "/v2/partnerships/{}/users".format(partnership_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def PartnershipsPartnerships_users(self, partnership_id, *args, **kwargs):
        extension = "/v2/partnerships/{}/partnerships_users".format(partnership_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Partnerships_usersExperiences(self, partnerships_user_id, *args, **kwargs):
        extension = "/v2/partnerships_users/{}/experiences".format(partnerships_user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def PatronagesPatronages_reports(self, patronage_id, *args, **kwargs):
        extension = "/v2/patronages/{}/patronages_reports".format(patronage_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def PoolsBalances(self, pool_id, *args, **kwargs):
        extension = "/v2/pools/{}/balances".format(pool_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def PoolsBalances(self, pool_id, id, *args, **kwargs):
        extension = "/v2/pools/{}/balances/{}".format(pool_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsTeams(self, project_session_id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/teams".format(project_session_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsRules(self, project_session_id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/rules".format(project_session_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsScales(self, project_session_id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/scales".format(project_session_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsAttachments(self, project_session_id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/attachments".format(project_session_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsEvaluations(self, project_session_id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/evaluations".format(project_session_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsProject_data(self, project_session_id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/project_data".format(project_session_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsAttachments(self, project_session_id, id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/attachments/{}".format(project_session_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsProject_sessions_rules(self, project_session_id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/project_sessions_rules".format(project_session_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsProject_sessions_skills(self, project_session_id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/project_sessions_skills".format(project_session_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessionsProject_sessions_skills(self, project_session_id, id, *args, **kwargs):
        extension = "/v2/project_sessions/{}/project_sessions_skills/{}".format(project_session_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Project_sessions_rulesParams_project_sessions_rules(self, project_sessions_rule_id, *args, **kwargs):
        extension = "/v2/project_sessions_rules/{}/params_project_sessions_rules".format(project_sessions_rule_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsRetry(self, id, *args, **kwargs):
        extension = "/v2/projects/{}/retry".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsTags(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/tags".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsTeams(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/teams".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsUsers(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/users".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsExams(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/exams".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsSlots(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/slots".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsSkills(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/skills".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsScales(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/scales".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsRegister(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/register".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsProjects(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/projects".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsEvaluations(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/evaluations".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsAttachments(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/attachments".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsScale_teams(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/scale_teams".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsProjects_users(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/projects_users".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ProjectsProject_sessions(self, project_id, *args, **kwargs):
        extension = "/v2/projects/{}/project_sessions".format(project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Projects_usersRetry(self, id, *args, **kwargs):
        extension = "/v2/projects_users/{}/retry".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Projects_usersExperiences(self, projects_user_id, *args, **kwargs):
        extension = "/v2/projects_users/{}/experiences".format(projects_user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def QuestsUsers(self, quest_id, *args, **kwargs):
        extension = "/v2/quests/{}/users".format(quest_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def QuestsQuests_users(self, quest_id, *args, **kwargs):
        extension = "/v2/quests/{}/quests_users".format(quest_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def ReportsPatronages_reports(self, report_id, *args, **kwargs):
        extension = "/v2/reports/{}/patronages_reports".format(report_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def RolesRoles_entities(self, role_id, *args, **kwargs):
        extension = "/v2/roles/{}/roles_entities".format(role_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Scale_teamsMultiple_create(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/scale_teamsmultiple_create.html"
        """
        extension = "/v2/scale_teams/multiple_create"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Scale_teamsFeedbacks(self, scale_team_id, *args, **kwargs):
        extension = "/v2/scale_teams/{}/feedbacks".format(scale_team_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Scale_teamsFeedbacks(self, scale_team_id, id, *args, **kwargs):
        extension = "/v2/scale_teams/{}/feedbacks/{}".format(scale_team_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def SkillsExperiences(self, skill_id, *args, **kwargs):
        extension = "/v2/skills/{}/experiences".format(skill_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def SkillsProject_sessions_skills(self, skill_id, *args, **kwargs):
        extension = "/v2/skills/{}/project_sessions_skills".format(skill_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TagsTopics(self, tag_id, *args, **kwargs):
        extension = "/v2/tags/{}/topics".format(tag_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TagsNotions(self, tag_id, *args, **kwargs):
        extension = "/v2/tags/{}/notions".format(tag_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TeamsUsers(self, team_id, *args, **kwargs):
        extension = "/v2/teams/{}/users".format(team_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TeamsTeams_users(self, team_id, *args, **kwargs):
        extension = "/v2/teams/{}/teams_users".format(team_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TeamsReset_team_uploads(self, id, *args, **kwargs):
        extension = "/v2/teams/{}/reset_team_uploads".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TeamsTeams_uploads(self, team_id, *args, **kwargs):
        extension = "/v2/teams/{}/teams_uploads".format(team_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def Teams_uploadsMultiple_create(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/teams_uploadsmultiple_create.html"
        """
        extension = "/v2/teams_uploads/multiple_create"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TitlesUsers(self, title_id, *args, **kwargs):
        extension = "/v2/titles/{}/users".format(title_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TitlesAchievements(self, title_id, *args, **kwargs):
        extension = "/v2/titles/{}/achievements".format(title_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TitlesTitles_users(self, title_id, *args, **kwargs):
        extension = "/v2/titles/{}/titles_users".format(title_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsUnread(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/topicsunread.html"
        """
        extension = "/v2/topics/unread"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsTags(self, topic_id, *args, **kwargs):
        extension = "/v2/topics/{}/tags".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsVotes(self, topic_id, *args, **kwargs):
        extension = "/v2/topics/{}/votes".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsMessages(self, topic_id, *args, **kwargs):
        extension = "/v2/topics/{}/messages".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsVotesUpvotes(self, topic_id, *args, **kwargs):
        extension = "/v2/topics/{}/votes/upvotes".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsCursus_topics(self, topic_id, *args, **kwargs):
        extension = "/v2/topics/{}/cursus_topics".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsVotesProblems(self, topic_id, *args, **kwargs):
        extension = "/v2/topics/{}/votes/problems".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsVotesDownvotes(self, topic_id, *args, **kwargs):
        extension = "/v2/topics/{}/votes/downvotes".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsVotesTrollvotes(self, topic_id, *args, **kwargs):
        extension = "/v2/topics/{}/votes/trollvotes".format(topic_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TopicsMessagesMessages(self, topic_id, message_id, *args, **kwargs):
        extension = "/v2/topics/{}/messages/{}/messages".format(topic_id, message_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def TranslationsUpload(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/translationsupload.html"
        """
        extension = "/v2/translations/upload"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersExam(self, id, *args, **kwargs):
        extension = "/v2/users/{}/exam".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersApps(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/apps".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersTags(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/tags".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersExams(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/exams".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersSlots(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/slots".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersTeams(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/teams".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersNotes(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/notes".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersRoles(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/roles".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersTopics(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/topics".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersTitles(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/titles".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersScales(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/scales".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersEvents(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/events".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersCloses(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/closes".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersQuests(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/quests".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersGroups(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/groups".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersMailings(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/mailings".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersMessages(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/messages".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersLocations(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/locations".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersPatronages(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/patronages".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersCoalitions(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/coalitions".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersScale_teams(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/scale_teams".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersTeams_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/teams_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersInternships(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/internships".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersExperiences(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/experiences".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersEvents_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/events_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersCursus_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/cursus_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersCampus_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/campus_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersTitles_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/titles_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersGroups_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/groups_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersQuests_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/quests_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersTransactions(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/transactions".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersLocations(self, user_id, id, *args, **kwargs):
        extension = "/v2/users/{}/locations/{}".format(user_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersProjects_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/projects_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersInternships(self, user_id, id, *args, **kwargs):
        extension = "/v2/users/{}/internships/{}".format(user_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersLanguages_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/languages_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersExpertises_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/expertises_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersCorrection_pointsAdd(self, id, *args, **kwargs):
        extension = "/v2/users/{}/correction_points/add".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersUser_candidature(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/user_candidature".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersCoalitions_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/coalitions_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersPatronages_reports(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/patronages_reports".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersCertificates_users(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/certificates_users".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersCorrection_pointsRemove(self, id, *args, **kwargs):
        extension = "/v2/users/{}/correction_points/remove".format(id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersLanguages_users(self, user_id, id, *args, **kwargs):
        extension = "/v2/users/{}/languages_users/{}".format(user_id, id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersScale_teamsAs_corrected(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/scale_teams/as_corrected".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersScale_teamsAs_corrector(self, user_id, *args, **kwargs):
        extension = "/v2/users/{}/scale_teams/as_corrector".format(user_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def UsersProjectsTeams(self, user_id, project_id, *args, **kwargs):
        extension = "/v2/users/{}/projects/{}/teams".format(user_id, project_id)
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def VotesUpvotes(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/votesupvotes.html"
        """
        extension = "/v2/votes/upvotes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def VotesProblems(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/votesproblems.html"
        """
        extension = "/v2/votes/problems"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def VotesDownvotes(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/votesdownvotes.html"
        """
        extension = "/v2/votes/downvotes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
    def VotesTrollvotes(self, *args, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/votestrollvotes.html"
        """
        extension = "/v2/votes/trollvotes"
        return HttpMethod(extension, self.session, *args, **kwargs)
        
