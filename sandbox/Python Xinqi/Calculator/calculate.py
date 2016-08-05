import rethinkdb as r

def overall_summary():

    r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
              password="marcgoestothegym").repl()

    originalDislike = r.db('evaluation').table('results').get_field('counts').sum('originalDislike').run()
    originalLike = r.db('evaluation').table('results').get_field('counts').sum('originalLike').run()
    originalNeither = r.db('evaluation').table('results').get_field('counts').sum('originalNeither').run()
    recomendNeither = r.db('evaluation').table('results').get_field('counts').sum('recomendNeither').run()
    recommendLike = r.db('evaluation').table('results').get_field('counts').sum('recommendLike').run()
    recommendDislike = r.db('evaluation').table('results').get_field('counts').sum('recomendDislike').run()

    print("Overall Summary:\n\n"
          "Original Like: %d\n"
          "Original Neutral: %d\n"
          "Original DisLike: %d\n\n"
          "Recommend Like: %d\n"
          "Recommend Netual: %d\n"
          "Recommend Dislike: %d\n\n"
          % (originalLike, originalNeither, originalDislike,
             recommendLike, recomendNeither, recommendDislike))

def summary_for_single_user(screen_name):

    r.connect(host='ec2-52-51-162-183.eu-west-1.compute.amazonaws.com', port=28015, db='lovelace',
              password="marcgoestothegym").repl()

    originalDislike = r.db('evaluation').table('results').filter({'user_info':{'screen_name':screen_name}}).get_field('counts').sum('originalDislike').run()
    originalLike = r.db('evaluation').table('results').filter({'user_info':{'screen_name':screen_name}}).get_field('counts').sum('originalLike').run()
    originalNeither = r.db('evaluation').table('results').filter({'user_info':{'screen_name':screen_name}}).get_field('counts').sum('originalNeither').run()
    recomendNeither = r.db('evaluation').table('results').filter({'user_info':{'screen_name':screen_name}}).get_field('counts').sum('recomendNeither').run()
    recommendLike = r.db('evaluation').table('results').filter({'user_info':{'screen_name':screen_name}}).get_field('counts').sum('recommendLike').run()
    recommendDislike = r.db('evaluation').table('results').filter({'user_info':{'screen_name':screen_name}}).get_field('counts').sum('recomendDislike').run()

    print("Summary for %s:\n\n"
          "Original Like: %d\n"
          "Original Neutral: %d\n"
          "Original DisLike: %d\n\n"
          "Recommend Like: %d\n"
          "Recommend Netual: %d\n"
          "Recommend Dislike: %d\n\n"
          % (screen_name, originalLike, originalNeither, originalDislike,
             recommendLike, recomendNeither, recommendDislike))

overall_summary()
summary_for_single_user('sowasser')