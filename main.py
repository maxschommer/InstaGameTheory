from InstagramAPI import InstagramAPI
import time
import numpy as np
from matplotlib import pyplot as plt
import random


instauser = 'XXXX'
instapass = 'XXXX'

class MediaLikes(object):
    def __init__(self, user_likes, media_id, is_liked):
        super(MediaLikes, self).__init__()
        self.user_likes = user_likes
        self.media_id = media_id
        self.is_liked = is_liked

    def __str__(self):
        return "User Likes: \n{}\nMedia ID: \n{}\nIs Liked: {}".format(self.user_likes, self.media_id, self.is_liked) 

def like_posts(media_list, api):
    for media_itm in media_list:
        api.like(media_itm.media_id)

def get_likes_list(username, api):
    media_likes_list = []
    api.searchUsername(username)
    info = api.LastJson
    username_id = info['user']['pk']
    user_posts = api.getUserFeed(username_id)
    if user_posts==False:
        return False
    info = api.LastJson
    for post in info['items']:
        post_like_list = []
        media_id = post['id']

        api.getMediaLikers(media_id)
        f = api.LastJson['users']
        for x in f:
            post_like_list.append(x['username'])
        media_likes_list.append(MediaLikes(post_like_list, media_id, post['has_liked']))
    return media_likes_list


def flatten_list(a_list):
    return [item for sublist in a_list for item in sublist]

def extract_user_likes(MediaLikesList):
    res = []
    for media in MediaLikesList:
        res = res + media.user_likes
    return res

def list_to_hist(data):
    data_hist = {}
    for elt in data:
        if elt in data_hist:
            data_hist[elt] = data_hist[elt] + 1
        else:
            data_hist[elt] = 1
    return data_hist

def plot_list(x, y):
    y = y.astype('int')
    print(y)
    fig, ax = plt.subplots()    
    width = 0.3 # the width of the bars 
    ind = np.arange(len(y))  # the x locations for the groups
    ax.barh(ind, y, width, color="blue")
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(x, minor=False)
    plt.xlabel('Number of Likes')
    plt.ylabel('User Profile')      
    plt.title("Instagram Likes Statistics")
    plt.show()

def get_unliked_idxs(usr_name, like_list):
    not_liked_idxs = []
    for i, media in enumerate(like_list):
        if media.is_liked:
            continue
        else:
            not_liked_idxs.append(i)
    return not_liked_idxs

def run_autoliker(strategy="tit_for_tat", verbose=False):
    api = InstagramAPI(instauser, instapass)
    api.login()

    # Uncomment if login issues, then while sleeping click on the link to verify your login.
    # time.sleep(15)
    # api.login()

    print('Account: {}'.format(api.username))

    media_likes_list = get_likes_list(instauser, api)

    personal_likes_list = extract_user_likes(media_likes_list)
    personal_likes_hist = list_to_hist(personal_likes_list)

    personal_likes_hist_arr = list(personal_likes_hist.items())

    for usr_likes in personal_likes_hist_arr:

        usr = usr_likes[0]
        usr_like_num = int(usr_likes[1])
        print("Checking likes for user: {}".format(usr))
        print("User Likes {} of my posts.".format(usr_like_num))
        their_media_like_list = get_likes_list(usr, api)
        if their_media_like_list==False:
            print("Skipping Private user.")
            continue
        num_posts = len(their_media_like_list)
        print("Number of User Posts: {}".format(num_posts))

        their_like_list = extract_user_likes(their_media_like_list)
        their_like_hist = list_to_hist(their_like_list)
        if verbose:
            print("{}'s Like Histogram: \n{}".format(usr, their_like_hist))
        if instauser not in their_like_hist:
            i_liked_them_cnt = 0
        else:
            i_liked_them_cnt =  their_like_hist[instauser]

        more_likes_needed = personal_likes_hist[usr] - i_liked_them_cnt

        print("More likes needed: {}".format(more_likes_needed))
        unliked_post_idxs = get_unliked_idxs(instauser, their_media_like_list)

        # If the user has fewer posts than then number of my posts they liked
        if more_likes_needed > len(unliked_post_idxs):
            more_likes_needed = len(unliked_post_idxs)

        if more_likes_needed < 1:
            continue

        if strategy=="tit_for_tat":
            posts_to_like_idxs  = random.sample(unliked_post_idxs, more_likes_needed)
        if strategy=="percentage":
            # TODO Implement
            pass

        posts_to_like = [their_media_like_list[i] for i in posts_to_like_idxs]
        like_posts(posts_to_like, api)
        if verbose:
            print("Liking the following posts of user {}: \n".format(usr))
            for post in posts_to_like:
                print(post)
        print("Done! Next user.")
        # return
    print("Finished all users!")



if __name__ == '__main__':
    run_autoliker(strategy="tit_for_tat")
