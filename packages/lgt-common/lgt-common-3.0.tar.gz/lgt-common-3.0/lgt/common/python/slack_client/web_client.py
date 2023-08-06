import pytz
import requests
import env
from google.cloud import storage
from lgt.common.python.slack_client.slack_client import SlackClient
from dataclasses import dataclass
from datetime import datetime, timedelta
from lgt_data.model import UserModel, LeadModel, SlackHistoryMessageModel
from lgt_data.mongo_repository import UserBotCredentialsMongoRepository

slack_login_url = os.environ.get('SLACK_LOGIN_URL')


@dataclass
class LoginResponse:
    token: str

    """
     [{
            "name": "d-s",
            "value": "1589438217",
            "domain": ".slack.com",
            "path": "/",
            "expires": -1,
            "size": 13,
            "httpOnly": true,
            "secure": true,
            "session": true,
            "sameSite": "Lax"
        }]
    """
    cookies: []


def get_slack_credentials(user: UserModel, route: LeadModel):
    """

    :rtype: UserBotCredentialsModel
    """
    repository = UserBotCredentialsMongoRepository()
    credentials = list(repository.get_bot_credentials(user.id))
    cred = next(filter(lambda x: x.bot_name == route.message.name, credentials), None)

    if not cred:
        return None

    uctnow = datetime.utcnow().replace(tzinfo=pytz.UTC)
    cred_date_time = cred.updated_at.replace(tzinfo=pytz.UTC)
    # we have to update token since it might become outdated
    if (uctnow - cred_date_time).days > 5:
        login_response = SlackWebClient.get_access_token(cred.slack_url, cred.user_name, cred.password)
        if not login_response:
            return None

        cred = repository.update_bot_creadentials(user.id, cred.bot_name,
                                                       cred.user_name, cred.password, cred.slack_url, login_response.token, login_response.cookies)
    return cred


class SlackMessageConvertService:
    @staticmethod
    def from_slack_response(user_email, bot_name, bot_token, dic):

        """
        :rtype: SlackHistoryMessageModel
        """
        result = SlackHistoryMessageModel()
        result.text = dic.get('text', '')
        result.type = dic.get('type', '')
        result.user = dic.get('user', '')
        result.ts = dic.get('ts', '')
        result.files = []

        if 'files' in dic:
            for file in dic.get('files'):
                new_file = SlackHistoryMessageModel.SlackFileModel()
                new_file.id = file.get('id')
                new_file.name = file.get('name')
                new_file.title = file.get('title')
                new_file.filetype = file.get('filetype')
                new_file.size = file.get('size')
                new_file.mimetype = file.get('mimetype')

                url_private_download = file.get('url_private_download')
                new_file.download_url = SlackFilesClient.get_file_url(user_email, bot_name, bot_token,
                                                                      new_file.id, url_private_download,
                                                                      new_file.mimetype)
                result.files.append(new_file)

        js_ticks = int(result.ts.split('.')[0] + result.ts.split('.')[1][3:])
        result.created_at = datetime.fromtimestamp(js_ticks / 1000.0)
        return result


class SlackFilesClient:
    bucket_name = 'lgt_service_file'

    # Consider to cache these file somewhere in the super-fast cache solution
    @staticmethod
    def get_file_url(user_email, bot_name, bot_token, file_id, url_private_download, mimetype):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(SlackFilesClient.bucket_name)
        blob_path = f'slack_files/{user_email}/{bot_name}/{file_id}'
        blob = bucket.get_blob(blob_path)

        if not blob:
            res = requests.get(url_private_download, headers={'Authorization': f'Bearer {bot_token}'})
            if res.status_code != 200:
                raise Exception(f'Failed to download file: {url_private_download} from slack due to response: Code: {res.status_code} Error: {res.content}')
            blob = bucket.blob(blob_path)
            blob.upload_from_string(res.content, content_type=mimetype)

        blob = bucket.get_blob(blob_path)
        # valid for 3 days
        return blob.generate_signed_url(timedelta(3))


class SlackWebClient:
    def __init__(self, token, cookies=None):

        if isinstance(cookies, list):
            cookies = {c['name']: c['value'] for c in cookies}

        self.client = SlackClient(token, cookies)

    def delete_message(self, channel: str, ts: str):
        return self.client.delete_message(channel, ts)

    def update_message(self, channel: str, ts: str, text: str):
        return self.client.update_message(channel, ts, text)

    def get_profile(self, user_id):
        return self.client.user_info(user_id)

    def get_im_list(self):
        return self.client.get_im_list()

    def chat_history(self, channel):
        return self.client.conversations_history(channel)

    def post_message(self, to, text):
        return self.client.post_message(to, text)

    def user_list(self):
        return self.client.users_list()

    def channels_list(self):
        return self.client.get_conversations_list()

    def im_open(self, sender_id):
        return self.client.im_open(sender_id)

    def update_profile(self, profile):
        return self.client.update_profile(profile)

    def channel_join(self, channels):
        return self.client.join_channels(channels)

    def channel_leave(self, channels):
        return self.client.leave_channels(channels)

    @staticmethod
    def download_file(file_url, token, cookies):
        return requests.get(file_url, allow_redirects=True, headers={f'Authorization: Bearer {token}'}, cookies=cookies)

    @staticmethod
    def get_access_token(workspace_url, user_name, password, retry=False) -> LoginResponse:
        try:
            session = requests.Session()
            resp = session.post(f'{slack_login_url}api/login',
                                json={"slack_workspace": workspace_url, "user_name": user_name, "password": password})

            if resp.status_code == 400:
                # this means invalid credentials
                return None;

            if resp.status_code != 200:
                if not retry:
                    print(f'[{workspace_url}] received {resp.status_code} from the slack login component. trying one more time')
                    return SlackWebClient.get_access_token(workspace_url, user_name, password, True)

                return None

            resp_json = resp.json()
            if 'token' not in resp_json:
                return None

            return LoginResponse(resp_json['token'], resp_json['cookies'])
        except requests.exceptions.ConnectionError:
            print('Connection error')
            raise
