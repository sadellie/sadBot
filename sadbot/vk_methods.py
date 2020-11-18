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
from utils.utils import get_random
import requests

# Для авторизации
vk_session = vk_api.VkApi(token=config.token)
longpoll = VkBotLongPoll(vk_session, config.club_id)
vk = vk_session.get_api()
print("vk_methods called!!!")


def get_user_info(ids: int) -> dict:
    """
    Get main information about user

    :param ids: user id
    :return: Info about user (first name, last name etc.)
    """
    return vk.users.get(user_ids=ids)[0]


def send_message(peer_id: int,
                 message: str = None,
                 reply_to: int = None,
                 attachments: str = None,
                 keyboard: str = None,
                 sticker_id: int = None,
                 template: str = None):
    """Wrapper for message.send

    :param peer_id: Chat peer_id (where to send)
    :param message: Message text
    :param reply_to: Id of the message which we will reply to
    :param attachments: Attachment
    :param keyboard: Keyboard
    :param sticker_id: Sticker_id
    :param template: Carousel
    """

    vk.messages.send(
        peer_id=peer_id,
        random_id=get_random(),
        message=message,
        reply_to=reply_to,
        attachment=attachments,
        keyboard=keyboard,
        template=template,
        sticker_id=sticker_id
    )


def send_message_event_answer(peer_id: int,
                              user_id: int,
                              event_id: str,
                              event_data):
    """
    Wrapper for messages.sendMessageEventAnswer

    :param peer_id: Chat peer_id (where to send)
    :param user_id: id of user who will receive event answer
    :param event_id: id of the event
    :param event_data: Data of the event. Action to open link, app or show Snackbar
    """
    vk.messages.sendMessageEventAnswer(
        peer_id=peer_id,
        user_id=user_id,
        event_id=event_id,
        event_data=event_data)


def save_photo_to_vk(image_path: str):
    """
    Uploads image from device storage

    :param image_path: Path to image
    :return: Returns formatted photo_id (ready to be used in send_message())
    """
    image = open(image_path, 'rb')
    req = requests.post(
        url=vk.photos.getMessagesUploadServer(),
        files={'photo': image}
    ).json()
    c = vk.photos.saveMessagesPhoto(
        photo=req['photo'],
        server=req['server'],
        hash=req['hash'])[0]
    photo_id = "photo{}_{}".format(c["owner_id"], c["id"])
    return photo_id
