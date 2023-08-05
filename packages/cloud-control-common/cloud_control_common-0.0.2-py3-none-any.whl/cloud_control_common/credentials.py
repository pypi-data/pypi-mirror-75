class Credentials:

    def __init__(self, event):
        credentials = event.get('credentials')
        self.__username = credentials['username']
        self.__password = credentials['password']

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def __eq__(self, other):
        return isinstance(other,
                          Credentials) and other.__username == self.__username and other.__password == self.__password
