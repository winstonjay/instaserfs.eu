
def unique_words(data, k):

    unique = []

    for val in data:
        for v in val.split():
            if not v in unique:

                unique.append(v)

    return len(unique) * 1


def word_occurance_and_count(b, data):

    count, total_words = 0, 0

    for d in data:
        for word in d.split():
            total_words += 1
            if b in d:
                count += 1

    return count, total_words


class Mini_Naive_Bayes(object):
    """docstring for Naive_Bayes"""
    def __init__(self, data):
        super(Naive_Bayes, self).__init__()
        self.data = data


    def probability_dist(self, a):
        return float(1) / len(self.data)


    # def given_probability(self, b, a)
        


