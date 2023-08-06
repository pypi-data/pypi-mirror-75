from unittest import TestCase
from unittest.mock import Mock

from chaanbot.modules.highlight import Highlight


class TestHighlight(TestCase):
    event = {"sender": "sender_user_id"}

    def setUp(self) -> None:
        database = Mock()
        matrix = Mock()
        self.room = Mock()
        self.highlight = Highlight(None, matrix, database, None)

    def test_not_ran_if_wrong_command(self):
        ran = self.highlight.run(self.room, None, "highlight")
        self.assertFalse(ran)

    def test_config_has_properties(self):
        self.assertLess(0, len(self.highlight.operations))
        self.assertFalse(self.highlight.always_run)

    def test_highlight_all_without_text(self):
        user = Mock()
        user.user_id = "user1"
        members = [user]
        self.room.get_joined_members.return_value = members

        expected_send_message = "user1"

        self.highlight.run(self.room, self.event, "!hlall")

        self.room.send_text.assert_called_with(expected_send_message)

    def test_highlight_all_with_text(self):
        user = Mock()
        user.user_id = "user1"
        members = [user]
        self.room.get_joined_members.return_value = members

        argument = "helloes"
        expected_send_message = "user1: helloes"

        self.highlight.run(self.room, self.event, "!hlall " + argument)

        self.room.send_text.assert_called_with(expected_send_message)

    def test_dont_highlight_all_if_none_to_highlight(self):
        self.room.get_joined_members.return_value = []

        argument = "helloes"
        expected_send_message = "No users to highlight"

        self.highlight.run(self.room, self.event, "!hlall " + argument)

        self.room.send_text.assert_called_with(expected_send_message)

    def test_dont_highlight_sender_in_highlight_all(self):
        user = Mock()
        user.user_id = self.event["sender"]
        self.room.get_joined_members.return_value = [user]

        argument = "helloes"
        expected_send_message = "No users to highlight"

        self.highlight.run(self.room, self.event, "!hlall " + argument)

        self.room.send_text.assert_called_with(expected_send_message)

    def test_highlight_without_text(self):
        conn = Mock()
        self._mock_get_member(conn, [["user1"]])
        self._mock_get_user("user1")

        expected_send_message = "user1"

        self.highlight.run(self.room, self.event, "!hl group")

        self.room.send_text.assert_called_with(expected_send_message)
        conn.execute.assert_called_once()

    def test_should_not_run_highlight_operation_if_missing_group_argument(self):
        conn = Mock()
        self._mock_get_member(conn, [["user1"]])
        self._mock_get_user("user1")

        self.highlight.run(self.room, self.event, "!hl")

        self.room.send_text.assert_not_called()
        conn.execute.assert_not_called()

    def test_highlight_with_text(self):
        conn = Mock()
        self._mock_get_member(conn, [["user1"]])
        self._mock_get_user("user1")

        expected_send_message = "user1: helloes"

        self.highlight.run(self.room, self.event, "!hl group helloes")

        self.room.send_text.assert_called_with(expected_send_message)
        conn.execute.assert_called_once()

    def _get_user_side_effect(*args, **kwargs):
        online_user = Mock()
        online_user.user_id = "online_user"
        offline_user = Mock()
        offline_user.user_id = "offline_user"
        if args[2] == "online_user":
            return online_user
        elif args[2] == "offline_user":
            return offline_user

    def test_no_members_for_highlight(self):
        conn = Mock()
        self._mock_get_member(conn, [])

        expected_send_message = "Group \"group\" does not have any members to highlight"

        self.highlight.run(self.room, self.event, "!hl group")

        self.room.send_text.assert_called_with(expected_send_message)
        conn.execute.assert_called_once()

    def test_dont_highlight_sender_in_highlight(self):
        conn = Mock()
        self._mock_get_member(conn, [self.event["sender"]])
        self._mock_get_user(self.event["sender"])

        expected_send_message = "Group \"group\" does not have any members to highlight"

        self.highlight.run(self.room, self.event, "!hl group")

        self.room.send_text.assert_called_with(expected_send_message)
        conn.execute.assert_called_once()

    def test_successfully_adding_members_to_case_insensitive_group(self):
        conn = Mock()
        self._mock_is_in_group(conn, None)
        self._mock_get_user("user1")

        expected_send_message = "Added \"user1\" to group \"group\""

        self.highlight.run(self.room, self.event, "!hla GRouP user1")

        self.room.send_text.assert_called_with(expected_send_message)

    def test_dont_add_to_group_if_already_member(self):
        conn = Mock()
        self._mock_is_in_group(conn, "user1")
        self._mock_get_user("user1")

        expected_send_message = "Could not add \"user1\" to group \"group\""

        self.highlight.run(self.room, self.event, "!hla group user1")

        self.room.send_text.assert_called_with(expected_send_message)

    def test_dont_add_to_group_if_not_in_room(self):
        self.highlight.matrix.get_user.return_value = None

        expected_send_message = "User: \"user1\" is not in room"

        self.highlight.run(self.room, self.event, "!hla group user1")

        self.room.send_text.assert_called_with(expected_send_message)

    def test_successfully_deleting_members_from_case_insensitive_group(self):
        conn = Mock()
        self._mock_is_in_group(conn, "user1")
        self._mock_get_user("user1")

        expected_send_message = "Removed \"user1\" from group \"group\""

        self.highlight.run(self.room, self.event, "!hld gROUp user1")

        self.room.send_text.assert_called_with(expected_send_message)

    def test_dont_delete_from_group_if_not_member(self):
        conn = Mock()
        self._mock_is_in_group(conn, None)
        self._mock_get_user("user1")

        expected_send_message = "Could not remove \"user1\" from group \"group\""

        self.highlight.run(self.room, self.event, "!hld group user1")

        self.room.send_text.assert_called_with(expected_send_message)

    def _mock_get_user(self, user_id):
        user = Mock()
        user.user_id = user_id
        self.highlight.matrix.get_user.return_value = user

    def _mock_is_in_group(self, conn, return_value):
        self.highlight.database.connect.return_value = conn
        conn.__enter__ = Mock(return_value=conn)
        conn.__exit__ = Mock(return_value=None)
        result = Mock()
        conn.execute.return_value = result
        result.fetchone.return_value = return_value

    def _mock_get_member(self, conn, members):
        self.highlight.database.connect.return_value = conn

        rows = Mock()
        conn.execute.return_value = rows
        rows.fetchall.return_value = members
