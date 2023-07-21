# received_list=[
# [1678, 30],  # 1678 is the ID, 30 is the view count
#     [1987, 99],
#     [1822, 50],
#     [1678, 22],  # ID already appears
#     [2299, 30],
#     [1987, 100],
# ]


# articles_and_views={}

# for each_list in received_list:
#     article_id=each_list[0]
#     article_views=each_list[1]

#     if articles_and_views.get(article_id):

#         articles_and_views[article_id]+=article_views
#     else:
#         articles_and_views[article_id]=article_views

import os
from dotenv import load_dotenv

load_dotenv()
uer=os.getenv("MAIL_USERNAME")
print(uer)