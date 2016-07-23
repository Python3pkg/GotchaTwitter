from pushbullet import PushBullet
# # pb = PushBullet('o.cJm1iLu3sJtvm7P0YIHuBvy8lpYtPOIQ')
# pb = PushBullet('o.X7MEj0qDukl4uhj8EZ28K5tAY0P5c0c0')
# push = pb.push_note("Just a Test", "test test test test test test test test test test test test test test test ")


class PushBullet_(PushBullet):

    def notify(self, title, message):
        return self.push_note(title, message)