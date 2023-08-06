import os
import string
import random
import subprocess
from collections import namedtuple

import keyring
import questionary
import requests
from requests.models import PreparedRequest

# from httpx import Request # Possible future import to replace requests

from requests.adapters import HTTPAdapter
from urllib3 import Retry
import webbrowser

import logging
from multiprocessing import Queue
from webtest.http import StopableWSGIServer
import falcon

from wommit.utils.utils import get_repo_info
from wommit.utils import decos


# Used to store PR and issue data.
Issue = namedtuple("Issue", ["type", "number", "title"])
Commit = namedtuple("Commit", ["sha", "title"])


class ApiHandler:

    def __init__(self):
        self.keyring_name = "git:https://github.com"
        self.keyring_username = "PersonalAccessToken"

        self.token = self.get_token()

    def get_commits(self):

        variables = get_repo_info()

        api_url = "https://api.github.com/graphql"

        runargs = {'text': True, 'check': True, 'capture_output': True, 'encoding': 'utf-8'}
        branchname = subprocess.run('git branch --show-current'.split(), **runargs).stdout.strip()
        # query = """
        #         query ($owner : String!, $name : String!){
        #           repository(owner: $owner, name: $name) {
        #             commitComments(last: 20){
        #               edges {
        #                     node {
        #                       bodyText
        #                     }
        #                   }
        #             }
        #         }
        #     }"""

        query = """query($owner:String!, $name:String!) {
  repository(owner: $owner, name: $name) {
    refs(refPrefix: "refs/heads/", orderBy: {direction: DESC, field: TAG_COMMIT_DATE}, first: 100) {
      totalCount
      edges {
        node {
          name
          target {
            ...on Commit {
              history(first:10){
              edges{
              node{
              messageHeadline
              id
              abbreviatedOid
              }
              }
                totalCount
              }
              
            }
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}"""

        def r_func(token):

            return requests.post(
                api_url,
                json={"query": query, "variables": variables},
                headers={"Authorization": "token {}".format(token)},
            )

        r = r_func(self.token)


        r_data = r.json()

        commits = []

        for node in r_data['data']['repository']['refs']['edges']:
            currbranch = node['node']['name']
            if currbranch == branchname:
                for commit in node['node']['target']['history']['edges']:
                    commit_msg = commit['node']['messageHeadline']
                    id = commit['node']['abbreviatedOid']
                    # print(f"--> {commit_msg} , {id}")
                    commits.append(Commit(id, commit_msg))

        return commits


    def get_issues(self) -> dict:

        api_url = "https://api.github.com/graphql"

        variables = get_repo_info()
        if not variables:
            return {}

        #token = self.get_token()
        # token = "abc"

        query = """
        query ($owner : String!, $name : String!){
          repository(owner: $owner, name: $name) {
            issues(last:10, states:OPEN) {
              edges {
                node {
                  title
                  number
                }
              }
            }
            pullRequests(last: 10, states: OPEN){
              edges {
                node {
                  title
                  number
                }
              }
            }
          }
        }
        """

        def r_func(token):

            return requests.post(
                api_url,
                json={"query": query, "variables": variables},
                headers={"Authorization": "token {}".format(token)},
            )

        r = r_func(self.token)


        r_data = r.json()

        if str(r.status_code) == "401":
            print("Local access token is incorrect for user credentials.")
            return

        elif 'errors' in r_data:
            print("Token does not have access to Github repo, or it doesn't exist.")
            logging.info(r_data['errors'])

            # r = r_func(self.oauth_flow())
            #
            # r_data = r.json()

            # if questionary.confirm(
            #     "Do you want to try a manual access token?", default=True
            # ).ask():
            #     self.get_token_manually()
            # else:
            #     return
            return

            # r = r_func(self.get_token_manually())

            # a31166d848e219933c08a0c3d2cd69cefe6f9a5f
            # raise NoRepoAccessError



        issue_nodes = r_data["data"]["repository"]["issues"]["edges"]
        pr_nodes = r_data["data"]["repository"]["pullRequests"]["edges"]



        def make_retvals(valname, allvals) -> list:

            return [
                Issue(valname, "#" + str(inner_d["number"]), inner_d["title"])
                for node in allvals
                for inner_d in node.values()
            ]

        complist = [*make_retvals("issue", issue_nodes), *make_retvals("PR", pr_nodes)]
        retvals = sorted(complist, key=lambda x: x.number)

        return retvals

    def get_token(self):
        """ Accesses local Windows Certificates to return a Github access token.
        :return: token str
        """

        # NOTE: this code currently returns a access token with incorrect scopes, and needs manual verification from
        # bkkp to access bkkp/valuable, which CLI doesn't. Working on resolving.
        #

        token = self.get_local_token()
        if token:
            return token
        else:
            print(f'Could not find a git access token under {self.keyring_name} {self.keyring_username}.')
            # token = self.get_token_manually()
            token = self.oauth_flow()


        return token

    def get_local_token(self):
        # known_names = ['Personal Access Token', 'PersonalAccessToken']
        # for n in known_names:
        try:
            k_key = keyring.get_credential(self.keyring_name, self.keyring_username).password
            return k_key
        # token = keyring.get_password("git:https://github.com", n)
        except Exception:
            e_key = os.getenv("GITHUB_TOKEN")
            return e_key

    def get_token_manually(self):
        return input("Get token from Github and paste here:")

    def oauth_flow(self):

        # https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/
        # 1
        link = "https://github.com/login/oauth/authorize"
        client_id = "c60cc3da378a890cab46"
        # Secret added by justification of Github devs: https://github.com/cli/cli/issues/1245#issuecomment-652907737
        client_secret = "a96aac7b2cede42ab754b21414f89c22add8db91"

        port = 8080
        callback_name = "/callback"
        #
        redirect_uri = "http://localhost:{}{}".format(port, callback_name)
        token_url = "https://github.com/login/oauth/access_token"
        # Gen random state string
        letters = string.ascii_lowercase
        state = "".join(random.choice(letters) for i in range(20))
        # scopes
        scope = "read:org repo gist"

        # Authorize user
        authorize_params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
        }
        req = PreparedRequest()
        req.prepare_url(link, authorize_params)
        webbrowser.open(req.url)

        ret_params = HttpHandler(port, callback_name).run()

        code = ret_params["code"]
        print("got the code " + code)

        # 2
        post_params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "state": state,
        }
        sesh = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        sesh.mount("http://", adapter)
        sesh.mount("https://", adapter)
        r = sesh.post(token_url, params=post_params, verify=False)
        # print(r.text)
        # make this work sometime
        # print(r.json())
        # print(r.text)
        token = self.find_between(r.text, "=", "&")
        # print(token)
        # print("new token is: " + token)

        # Sets the environment variable for future use. YOLO
        keyring.set_password(self.keyring_name, self.keyring_username, token)

        # 3
        return token

    def find_between(self, s, first, last):
        """This is absolute shite, requests.json() just isnt working"""
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def _get_issues_res(self) -> dict:
        """Deprecated REST API version."""

        api_url = "https://api.github.com/repos/bkkp/valuable/issues"
        token = self.get_token()
        r = requests.get(
            api_url,
            headers={"Authorization": "token {}".format(token)},
            params={"state": "open"},
        ).json()
        issue_numbers = ["#" + str(a["number"]) for a in r]

        return issue_numbers


class HttpHandler:
    def __init__(self, port, callback_name):
        self.que = Queue()
        self.port = port
        self.callback_name = callback_name

    def run(self):
        self.start_serve()
        return self.que.get()

    class Resource(object):
        def __init__(self, classman):
            self.classman = classman

        def on_get(self, req, resp):
            resp.body = "You can now close this window."
            resp.status = falcon.HTTP_200
            # print("getting me")
            # logging.info("we got a get")
            self.classman.close(req.params)

    def start_serve(self):
        api = application = falcon.API()
        self.spa = self.Resource(self)
        api.add_route(self.callback_name, self.spa)

        self.s = StopableWSGIServer(api, host="localhost", port=self.port)
        self.s.run()

        # Possible future threading/process solution.
        #
        # x = threading.Thread(target=self.s.run, daemon=True)
        # x.run()
        # s.create(api, host='localhost', port='8080')
        # serve(api, host='localhost', port='8080')

    def close(self, params):
        print("trying to close")
        self.que.put(params)
        self.s.shutdown()


if __name__ == "__main__":
    # print(IssueHandler().get_local_token())

    # print(ApiHandler().get_issues())
    print(ApiHandler().get_commits())

    # decos.trace(IssueHandler().get_issues())

    # print(IssueHandler().get_issues())
    # import os
    # print(os.environ['GITHUB_TOKEN'])
    # print(os.environ['GITHUB'])
    # print(IssueHandler().get_token())
    # print(IssueHandler().oauth_flow())
