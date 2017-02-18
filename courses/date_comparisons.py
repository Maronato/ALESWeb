from dateutil.relativedelta import relativedelta


class AllEvents():

    def __init__(self, begin, weeks=0, months=0):
        self.begin = begin
        self.args = {}
        if weeks != 0:
            self.args['weeks'] = +weeks
        if months != 0:
            self.args['months'] = +months

        self.end = begin + relativedelta(months=+6)

    def generate(self):
        current = self.begin
        while current < self.end:
            yield current
            current = current + relativedelta(**self.args)

    def compare(self, gen_2):
        for i in self.generate():
            for j in gen_2.generate():
                if i == j:
                    return True
        return False
