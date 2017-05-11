import os

import re
import requests
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

User = get_user_model()


class FacebookBackend():
    def authenticate(self, facebook_id, extra_fields=None):
        # Download profile picture
        # STEP1 : Get profile picture URL in desired format
        url_profile = 'https://graph.facebook.com/{user_id}/picture'.format(user_id=facebook_id)
        params = {
            'type': 'large',
            'width': 200,
            'height': 200
        }
        # STEP2 : Create temp file on memory
        temp_file = NamedTemporaryFile(delete=False)
        # STEP3 : Request to "get" profile image from URL
        # Note : "stream=True" lets download process in pieces rather than downloading at once
        r = requests.get(url_profile, params, stream=True)
        # STEP4 : Extract file extension from requested URL
        _, file_ext = os.path.splitext(r.url)
        print('Front : {}'.format(_))
        print('Back : {}'.format(file_ext))
        # RegExp : Call arg3(file_ext), find pattern given by arg1(r'(\.[^?]+).*'), replace it with arg2(r'\1')
        # arg1 : From period(\.) to anything but ?([^?]) as many as possible(+)
        # arg1 : Then anything(.) as many as possible(*)
        # arg2 : r'(\.[^?]+)' == r'\1', first group within arg1
        # Note : r'\0' == r('\.[^?]+).*', the whole RegExp
        file_ext = re.sub(r'(\.[^?]+).*', r'\1', file_ext)
        print('File Extension : {}'.format(file_ext))
        # STEP5 : Give a file name
        file_name = '{}{}'.format(facebook_id, file_ext)
        # STEP6 : Receive data per 1024 bytes from stream connected response and write over temp file (NOT DONE!)
        for chunk in r.iter_content(1024):
            temp_file.write(chunk)

        # Return a MyUser whose username is facebook_id
        # Or, create one with defaults
        defaults = {
            'first_name': extra_fields.get('first_name', ''),
            'last_name': extra_fields.get('last_name', ''),
            'email': extra_fields.get('email', ''),
        }

        user, user_created = User.objects.get_or_create(
            defaults=defaults,
            username=facebook_id
        )

        # STEP7 : Fill ImageField with temp_file using file_name and save
        user.img_profile.save(file_name, File(temp_file))
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
