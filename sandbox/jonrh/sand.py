import operator

count_bag = {
    '': 0.056179775280898875,
    u'all': 0.056179775280898875,
    u'help': 0.056179775280898875,
    u'just': 0.11235955056179775,
    u'businesses': 0.056179775280898875,
    u'hack': 0.16853932584269662,
    u'silk': 0.056179775280898875,
    u'shanselman': 0.056179775280898875,
    u'httpstcockhewwddxv': 0.056179775280898875,
    u'should': 0.056179775280898875,
    u'signalr': 0.056179775280898875,
    u'4': 0.11235955056179775,
    u'manicodes': 0.056179775280898875,
    u'httpstcoxk8q1m14re': 0.056179775280898875,
    u'risk': 0.056179775280898875,
    u'moms': 0.056179775280898875,
    u'intercom': 0.056179775280898875,
    u'showing': 0.056179775280898875,
    u'geek': 0.056179775280898875,
    u'framework': 0.056179775280898875,
    u'putting': 0.056179775280898875,
    u'now': 0.056179775280898875,
    u'cognitive': 0.056179775280898875,
    u'gender': 0.056179775280898875,
    u'page': 0.11235955056179775,
    u'view': 0.056179775280898875,
    u'webinar': 0.056179775280898875,
    u'httpstcoxrrbjwbchj': 0.056179775280898875,
    u'rt': 0.2808988764044944,
    u'new': 0.056179775280898193
}

# List of (term, weight) tuples sorted descending by weight. Example: [("lol", 9.89), ("kek", 3.37)]
sorted_by_weight = sorted(count_bag.items(), key=operator.itemgetter(1), reverse=True)

pretty_printable_string = ""
for term, weight in sorted_by_weight:
    pretty_printable_string += "{0:.3f}: {1}\n".format(weight, term)

print pretty_printable_string
