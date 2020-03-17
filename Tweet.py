class Tweet(object):
    """ Tweet class representing the input parser as a tweet object """

    def __init__(self, id, user, language, message):
        self.id = id
        self.user = user
        self.language = language
        self.message = message

    def get_id(self):
        return self.id

    def get_user(self):
        return self.user

    def get_language(self):
        return self.language

    def get_message(self):
        return self.message
