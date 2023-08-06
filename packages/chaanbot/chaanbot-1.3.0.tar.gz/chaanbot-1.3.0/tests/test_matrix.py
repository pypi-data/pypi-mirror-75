from unittest import TestCase, mock
from unittest.mock import Mock

from chaanbot.matrix import Matrix


class TestMatrixUtility(TestCase):
    def setUp(self):
        config = Mock()
        config.get.return_value = None
        matrix_client = Mock()
        self.matrix = Matrix(config, matrix_client)

    def test_initialize_black_and_whitelisted_rooms(self):
        config = Mock()
        config.get.side_effect = self._get_config_side_effect
        matrix_client = Mock()
        matrix = Matrix(config, matrix_client)
        self.assertEqual(["whitelisted"], matrix.whitelisted_room_ids)
        self.assertEqual(["blacklisted"], matrix.blacklisted_room_ids)

    def _get_config_side_effect(*args, **kwargs):
        if args[1] == "chaanbot":
            if args[2] == "blacklisted_room_ids":
                return "blacklisted"
            elif args[2] == "whitelisted_room_ids":
                return "whitelisted"
        return None

    def test_get_room_by_room_id(self):
        room_id = "id"
        mocked_room = Mock()
        mocked_room.room_id = room_id

        rooms = {"123123": mocked_room}

        actual_room = self.matrix.get_room(rooms, room_id)

        self.assertEquals(mocked_room, actual_room)

    def test_get_room_by_canonical_alias(self):
        canonical_alias = "alias"
        mocked_room = Mock()
        mocked_room.canonical_alias = canonical_alias

        rooms = {"123123": mocked_room}

        actual_room = self.matrix.get_room(rooms, canonical_alias)

        self.assertEquals(mocked_room, actual_room)

    def test_get_room_by_name(self):
        name = "name"
        mocked_room = Mock()
        mocked_room.name = name

        rooms = {"123123": mocked_room}

        actual_room = self.matrix.get_room(rooms, name)

        self.assertEquals(mocked_room, actual_room)

    def test_get_room_by_alias(self):
        alias = "realalias"
        mocked_room = Mock()
        mocked_room.aliases = ["fakealias", alias]

        rooms = {"123123": mocked_room}

        actual_room = self.matrix.get_room(rooms, alias)

        self.assertEquals(mocked_room, actual_room)

    def test_dont_get_room_if_no_match(self):
        mocked_room = Mock()
        mocked_room.aliases = ["no"]
        mocked_room.name = "no"
        mocked_room.canonical_alias = "no"
        mocked_room.room_id = "no"

        rooms = {"123123": mocked_room}

        actual_room = self.matrix.get_room(rooms, "yes!")

        self.assertIsNone(actual_room)

    def test_get_user_by_id(self):
        user_id = "user"
        mocked_room = mock.Mock()
        mocked_user = mock.Mock()

        mocked_room.get_joined_members.return_value = [mocked_user]
        mocked_user.user_id = user_id

        actual_user = self.matrix.get_user(mocked_room, user_id)

        self.assertEquals(mocked_user, actual_user)

    def test_get_user_by_display_name(self):
        display_name = "displayname"
        mocked_room = mock.Mock()
        mocked_user = mock.Mock()

        mocked_room.get_joined_members.return_value = [mocked_user]
        mocked_user.displayname = display_name

        actual_user = self.matrix.get_user(mocked_room, display_name)

        self.assertEquals(mocked_user, actual_user)
        mocked_room.get_joined_members.assert_called_once()

    def test_dont_get_user_if_no_match(self):
        display_name = "displayname"
        user_id = "user"
        mocked_room = mock.Mock()
        mocked_user = mock.Mock()

        mocked_room.get_joined_members.return_value = [mocked_user]
        mocked_user.displayname = display_name
        mocked_user.user_id = user_id

        actual_user = self.matrix.get_user(mocked_room, "neither")

        self.assertIsNone(actual_user)
        mocked_room.get_joined_members.assert_called_once()

    def test_make_api_call_when_get_presence(self):
        expected_presence = "presence"
        user_id = "user"
        self.matrix.matrix_client.api._send.return_value = expected_presence

        actual_presence = self.matrix.get_presence(user_id)

        self.assertEquals(expected_presence, actual_presence)
        self.matrix.matrix_client.api._send.assert_called_with("GET", "/presence/" + user_id + "/status")

    def test_user_online_if_presence_is_online(self):
        expected_presence = {"presence": "online"}
        user_id = "user"
        self.matrix.matrix_client.api._send.return_value = expected_presence

        online = self.matrix.is_online(user_id)

        self.assertTrue(online)
        self.matrix.matrix_client.api._send.assert_called_with("GET", "/presence/" + user_id + "/status")

    def test_user_not_online_if_presence_is_offline(self):
        expected_presence = {"presence": "offline"}
        user_id = "user"
        self.matrix.matrix_client.api._send.return_value = expected_presence

        online = self.matrix.is_online(user_id)

        self.assertFalse(online)
        self.matrix.matrix_client.api._send.assert_called_with("GET", "/presence/" + user_id + "/status")
