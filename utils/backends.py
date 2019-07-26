from errbot.backends.base import Person, Room, RoomOccupant


class GitterPerson(Person):
    def __init__(self,
                 idd=None,
                 username=None,
                 displayName=None,
                 url=None,
                 avatarSmall=None,
                 avatarMedium=None):
        self._idd = idd
        self._username = username
        self._displayName = displayName
        self._url = url
        self._avatarSmall = avatarSmall
        self._avatarMedium = avatarMedium

    @property
    def idd(self):
        return self._idd

    @property
    def username(self):
        return self._username

    @property
    def displayName(self):
        return self._displayName

    @property
    def url(self):
        return self._url

    @property
    def avatarSmall(self):
        return self._avatarSmall

    @property
    def avatarMedium(self):
        return self._avatarMedium

    # Generic API
    @property
    def person(self):
        return self._idd

    @property
    def nick(self):
        return self._username

    @property
    def fullname(self):
        return self._displayName

    @property
    def client(self):
        return ''

    @staticmethod
    def build_from_json(from_user):
        return GitterPerson(idd=from_user['id'],
                            username=from_user['username'],
                            displayName=from_user['displayName'],
                            url=from_user['url'],
                            avatarSmall=from_user['avatarUrlSmall'],
                            avatarMedium=from_user['avatarUrlMedium'])

    def __eq__(self, other):
        return str(self) == str(other)

    def __unicode__(self):
        return self.username

    __str__ = __unicode__
    aclattr = nick


class GitterRoomOccupant(GitterPerson, RoomOccupant):
    def __init__(self,
                 room,
                 idd=None,
                 username=None,
                 displayName=None,
                 url=None,
                 avatarSmall=None,
                 avatarMedium=None):
        self._room = room
        super().__init__(idd,
                         username,
                         displayName,
                         url,
                         avatarSmall,
                         avatarMedium)

    @property
    def room(self):
        return self._room

    @staticmethod
    def build_from_json(room, json_user):
        return GitterRoomOccupant(room,
                                  idd=json_user['id'],
                                  username=json_user['username'],
                                  displayName=json_user['displayName'],
                                  url=json_user['url'],
                                  avatarSmall=json_user['avatarUrlSmall'],
                                  avatarMedium=json_user['avatarUrlMedium'])

    def __unicode__(self):
        if self.url == self._room._uri:
            return self.username  # this is a 1 to 1 MUC
        return self.username + '@' + self._room.name

    def __eq__(self, other):
        if hasattr(other, 'person'):
            return self.person == other.person
        return str(self) == str(other)

    __str__ = __unicode__
