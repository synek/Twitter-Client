import twitter
from Tkinter import *
from PIL import Image, ImageTk

class twit:


    def __init__(self):
        self.api = twitter.Api(consumer_key='r0S3lRPTio3EZ4Cr78uQ',
                               consumer_secret='',
                               access_token_key='813019711-9jrsfT6yIJGnJjEhYiCsh0rnpm4el5MRqOKnpKys',
                               access_token_secret='')

    def status_update(self, message):
        self.api.PostUpdate(message)

    def get_friend_statuses(self):
        self.statuses = self.api.GetFriendsTimeline(count=3)
        self.public_tweets = '\n\n'.join([x.text for x in self.statuses])

        
class client:


    def __init__(self, master):
        self.master = master
        self.clicked = False
        self.foo = StringVar()
        self.foo.set("140 characters left")

        self.image = Image.open("twitter-bird-light-bgs.png")
        self.photo = ImageTk.PhotoImage(self.image)

        self.frame = Frame(self.master)
        self.frame.grid()

        
        # Events are not bound to the object, but a bindtag associated with the object.
        # (('instance name', 'widget class', '.', 'all')) ---> Default. '.' is the path of the root window.
        # 'instance name' is the number Tkinter assigns to the widget (eg .1566456), NOT the variable it is stored in.
        # The 'instance name' binding gets the value, and the 'widget class' binding puts the user input into the widget.
        # Thus the contents of the widget are retrieved BEFORE the new text is entered, so the counter was always 1 behind.
        self.post_tweet = Text(self.master, width=60, height=5, fg = "gray", font="Arial")
        self.post_tweet.bindtags((str(self.post_tweet), 'Text', 'post', '.', 'all'))
        self.post_tweet.bind("<Button-1>", self.callback)
        self.post_tweet.bind_class("post", "<Key>", self.count)
        self.post_tweet.insert(1.0, "Compose new Tweet...")
        self.post_tweet.grid(column=0, row=1, sticky=W, padx=15)

        self.title_logo = Label(self.master, image=self.photo)
        self.title_logo.image = self.photo
        self.title_logo.grid(column=0, row=0)

        self.post_tweet_button = Button(self.master, text="Post!",
                                         command=self.tweet, width=25)
        self.post_tweet_button.grid(column=0, row=2, pady=10, sticky=W, padx=10)

        self.char_count = Label(self.master, textvariable=self.foo, fg="black")
        self.char_count.grid(column=0, row=2)

        self.friend_tweets = Text(self.master, width=60, height=20, font="Arial", state=DISABLED)
        self.friend_tweets.grid(column=0, row=3, sticky=W, padx=15)

        self.get_friend_tweets_button = Button(self.master,
                                          text="Get Recent Tweets!!",
                                          command=self.show_tweets)
        self.get_friend_tweets_button.grid(column=0, row=4, sticky=N+S+W+E, padx=10, pady=10)

        

    def tweet(self):
        self.tweet_message = self.post_tweet.get(1.0, END)
        twitter_object.status_update(self.tweet_message)
        self.post_tweet.delete(1.0, END) # 1.0 meaning line 1, char 0

    def show_tweets(self):
        twitter_object.get_friend_statuses()
        self.friend_tweets.config(state=NORMAL)
        self.friend_tweets.delete(1.0, END)
        self.friend_tweets.insert(END, twitter_object.public_tweets)
        self.friend_tweets.config(state=DISABLED)

    def callback(self, event):
        if self.clicked == False:
            self.post_tweet.delete(1.0, END)
            self.post_tweet.config(fg = "black")
            self.clicked = True

    def count(self, event):
        self.tweet_length = len(self.post_tweet.get(1.0, "end-1c")) # -1c deals with the implicit newline at the end of Text.get()
        if self.tweet_length > 140:
            self.char_count.config(fg="red")
        elif self.tweet_length < 141:
            self.char_count.config(fg="black")
        self.foo.set("%s characters left" % (str(140 - self.tweet_length)))
        
        
if __name__ == '__main__':
    twitter_object = twit()
    root = Tk()
    root.title("The Terrible Twitter Client")
    app = client(root)
    root.mainloop()
