# InstaGameTheory
An eye for an eye, a like for a like. After all, the goal of social media is to win, right? And winning clearly means asserting dominance over your friends making sure they're properly rewarded and punished for their actions. You should like your friend's posts in direct proportion to them liking your posts, that way they're rewarded for good behavior, and punished for not liking you enough! 

InstaGameTheory is an Instagram like bot which uses the unofficial [Instagram Python API](https://github.com/LevPasha/Instagram-API-python). Its only power is to like posts (never unlike), but allows you to like others' posts using some basic strategies from game theory. 


## Usage

First, you need to install the [Instagram Python API](https://github.com/LevPasha/Instagram-API-python), numpy, and matplotlib. This can be done with the following command:

`pip install InstagramApi numpy matplotlib`

Now, open `main.py` and edit the value of `instauser` to be your username, and `instapass` to be your password. Then run `python main.py` to run the autoliker. 

## Potential Issues

If it does not login successfully because of an error similar to this: 

`{'message': 'challenge_required', 'challenge': {'url': 'https://i.instagram.com/challenge/7486640407/ltZRGanAP6/', 'api_path': '/challenge/7486640407/ltZRGanAP6/', 'hide_webview_header': True, 'lock': True, 'logout': False, 'native_flow': True}, 'status': 'fail', 'error_type': 'checkpoint_challenge_required'}`

Then uncomment the lines with `time.sleep(15)`. Then, while sleeping click on the challenge url and verify that the login attempt was you, after which it should login successfully. 
