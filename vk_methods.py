#    Copyright 2020 Elshan Agaev
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Wrappers for vk_api library methods
"""
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
import config
import time
import requests

# Для авторизации
vk_session = vk_api.VkApi(token=config.token)
longpoll = VkBotLongPoll(vk_session, config.club_id)
vk = vk_session.get_api()


# Random id
def get_random():
    """
    Generate random message_id. Necessary to send message

    :return: random number
    """
    return time.time() * 100000


def get_user_info(ids):
    """
    Get main information about user

    :param ids: user id
    :return: Info about user (first name, last name etc.)
    """
    return vk.users.get(user_ids=ids)[0]


def send_message(peer_id,
                 message: str = None,
                 attachments: str = None,
                 keyboard: str = None,
                 sticker_id: str = None,
                 template: str = None):
    """Send message

    :param peer_id: Chat peer_id (where to send)
    :param message: Message text
    :param attachments: Attachment
    :param keyboard: Keyboard
    :param sticker_id: Sticker_id
    :param template: Carousel
    """
    print("send message called")
    
    vk.messages.send(
        peer_id=peer_id,
        random_id=get_random(),
        message=message,
        attachment=attachments,
        keyboard=keyboard,
        template=template,
        sticker_id=sticker_id)
    
    print("sent")
    return 0

# def send_message_carousel(p: str):
#     """
#     Send carousel in chat with link to tutorial in VK articles
#
#     :param p: Chat peer_id (where to send)
#     """
#     vk.messages.send(
#         peer_id=p,
#         random_id=get_random(),
#         message=r_tutorial,
#         template=carousel)


def save_photo_to_vk(image_path: str):
    """
    Send image from device storage (used in full_mode for cool uptime pics)

    :param image_path: Path to image
    :return: Returns formatted photo_id (ready to be used in send_message())
    """
    image = open(image_path, 'rb')  # TODO rb?
    a = vk.photos.getMessagesUploadServer()
    b = requests.post(
        a['upload_url'],
        files={
            'photo': image}
    ).json()
    c = vk.photos.saveMessagesPhoto(
        photo=b['photo'],
        server=b['server'],
        hash=b['hash'])[0]
    d = "photo{}_{}".format(c["owner_id"], c["id"])

    return d
