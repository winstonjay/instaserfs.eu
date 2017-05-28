from parse_input import switch_possessive

class Reminder_Unit(object):

    def __init__(self):
        super(Reminder_Unit, self).__init__()


    def response(self, sentence, subjects):
        if subjects:
            response = "Ok i would remind you about %s" % switch_possessive(subjects)
        else:
            response = "remind you about what?"
        return response

        