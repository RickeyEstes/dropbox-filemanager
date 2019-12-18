#!/usr/bin/env python
# -*- coding: utf-8 -*-


import dropbox


class DropboxClient:

    def __init__(self):
        # This access token can be used to access your account via the API.
        # self.app_key = APP_KEY
        pass

    def connect(self, APP_KEY):
        ''' Connecting to the dropbox account'''
        # pass in the access token for the account you want to link.
        try:
            self.dbx = dropbox.Dropbox(APP_KEY)
        except dropbox.exceptions.BadInputError:
            pass

    def test(self):
        # Test it out to make sure you've linked the right account.
        self.dbx.users_get_current_account()
        self.dbx.files_create_folder()
    def upload(self, files):
        '''Uploading files to your dropbox account'''
        for file in files:
            with open(file, 'rb') as f:
                self.dbx.files_upload(f.read(), '/' + file.split('/')[-1])

    def remove(self, file):
        '''Remove files from the account'''
        self.dbx.files_delete(file)

    def list_files(self):
        '''Return list of uploaded files'''
        file_list = []
        metadata = self.dbx.files_list_folder(path='', recursive=True)
        for m in metadata.entries:
            if isinstance(m, dropbox.files.FileMetadata):
                file_list.append(f'{m.path_display}, {m.name}, {m.client_modified}, {m.size}')
        return file_list