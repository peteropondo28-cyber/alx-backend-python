from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, Notification, MessageHistory, Conversation

User = get_user_model()

class MessagingSignalsTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='alice', password='pass', email='a@example.com')
        self.u2 = User.objects.create_user(username='bob', password='pass', email='b@example.com')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content="Hello Bob")
        # After creation, a notification should exist for u2
        notif = Notification.objects.filter(user=self.u2, message=msg).first()
        self.assertIsNotNone(notif)
        self.assertEqual(notif.body, "Hello Bob")

    def test_message_edit_logs_history(self):
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content="Original")
        # emulate editing: change content and save
        msg.content = "Edited content"
        # Optional: mark who edited
        msg._editing_user = self.u1
        msg.save()
        history = MessageHistory.objects.filter(message=msg).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, "Original")

    def test_unread_manager(self):
        # create 3 messages, mark one as read
        Message.objects.create(sender=self.u1, receiver=self.u2, content="m1")
        m2 = Message.objects.create(sender=self.u1, receiver=self.u2, content="m2")
        m2.read = True
        m2.save()
        unread = Message.unread.for_user(self.u2)
        self.assertEqual(unread.count(), 1)

    def test_threaded_replies(self):
        # create parent message and replies
        parent = Message.objects.create(sender=self.u1, receiver=self.u2, content="Parent")
        r1 = Message.objects.create(sender=self.u2, receiver=self.u1, content="Reply1", parent_message=parent)
        r2 = Message.objects.create(sender=self.u1, receiver=self.u2, content="Reply to Reply", parent_message=r1)
        # get thread
        thread_data = parent.get_thread()
        self.assertEqual(thread_data['id'], parent.id)
        self.assertGreaterEqual(len(thread_data['replies']), 1)
        # check nested reply
        self.assertEqual(thread_data['replies'][0]['replies'][0]['content'], "Reply to Reply")
