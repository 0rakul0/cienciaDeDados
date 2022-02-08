#feito pelo professor Fernando Cardoso
import plotly.express as px
import inspect
import json
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
import snscrape.modules.twitter as sntwitter

# ## Content Mining
k = "(Eleições OR Eleição OR Lula OR Bolsonaro OR Michel Temer OR Doria OR Eduardo Paes OR Presidente OR Governo OR Governador OR Sérgio Moro OR sf_moro OR SF_Moro OR Ciro OR Dilma)"

maxTweets = 20
years = [
    2019, 2020, 2021, 2022
]
tweets = []
try:
    for y in years:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
                k + ' since:<year>-01-01 until:<year>-12-31 lang:pt'.replace("<year>", str(y))
        ).get_items()):
            if i > maxTweets:
                break
            theme = k.split("OR")[0].replace("(", "")

           # print(inspect.getmembers(tweet))

            username = tweet.username
            text = tweet.content
            pubdate = tweet.date
            permalink = tweet.url
            outlinks = tweet.outlinks
            tcooutlinks = tweet.tcooutlinks
            tweets.append({
                "permalink": permalink,
                "text": text,
                "username": username,
                "outlinks": outlinks,
                "tcooutlinks": tcooutlinks,
                "date": pubdate,
                "to": tweet.inReplyToUser,
                "likes": tweet.likeCount,
                "replies": tweet.replyCount,
                "retweets": tweet.retweetCount,
                "mentions": tweet.mentionedUsers,
                "theme": k.split("OR")[0].replace("(", "")
            })
            scraper = sntwitter.TwitterSearchScraper('from:' + username + ' filter:replies')
            for i, tweet in enumerate(scraper.get_items()):
                if i > 10:
                    break
                tweets.append(
                    {
                        "permalink": tweet.url,
                        "text": tweet.content,
                        "username": tweet.username,
                        "outlinks": tweet.outlinks,
                        "tcooutlinks": tweet.tcooutlinks,
                        "date": tweet.date,
                        "to": tweet.inReplyToUser,
                        "likes": tweet.likeCount,
                        "replies": tweet.replyCount,
                        "retweets": tweet.retweetCount,
                        "mentions": tweet.mentionedUsers,
                        "theme": k.split("OR")[0].replace("(", "")
                    }
                )

        print("----------------------------")
        print("Year: ", y)
        print("Tweets Length: ", len(tweets))

except Exception as e:
    print("Private Accounts Error:", e)

### Minimal Preprocessing
final_set = pd.DataFrame(tweets)
final_set['date'] = pd.to_datetime(final_set['date'])
final_set['to'] = final_set['to'].apply(lambda x: str(x).replace("https://twitter.com/", ""))
final_set['likes'].fillna(0, inplace=True)

# Exporting Data
#final_set.to_csv("./data/elections_tweet_br.csv", index=False)

# Importing Data
#final_set = pd.read_csv("./data/elections_tweet_br.csv")

# Exploring a Sample
for k, v in final_set.sample(5).iterrows():
    print("---------------")
    print("User: ", v['username'])
    print("Date: ", v['date'])
    print("Tweet: ", v['text'])


# to explore the available features we can get

inspect.getmembers(sntwitter.TwitterProfileScraper, predicate=inspect.ismethod)
inspect.getmembers(sntwitter, lambda a:not(inspect.isroutine(a)))


### Profile Mining

users_list = []
for u in final_set['username'].fillna("-1").unique():
    if u != "-1":
        try:
            user = sntwitter.TwitterProfileScraper(u, isUserId=False)

            #             print(inspect.getmembers(user))

            user_obj = {
                "username": user.entity.username,
                "displayname": user.entity.displayname,
                "description": user.entity.description,
                "description_urls": user.entity.descriptionUrls,
                "verified": user.entity.verified,
                "followers": user.entity.followersCount,
                "followees": user.entity.friendsCount,
                "statuses": user.entity.statusesCount,
                "favorites": user.entity.favouritesCount,
                "listed_counts": user.entity.listedCount,
                "media_count": user.entity.mediaCount,
                "location": user.entity.location,
                "protected": user.entity.protected,
                "link_url": user.entity.linkUrl,
                "link_tco_url": user.entity.linkTcourl,
                "profile_image_url": user.entity.profileImageUrl,
                "profile_banner_url": user.entity.profileBannerUrl,
                "label": user.entity.label
            }
            users_list.append(user_obj)
        except Exception as e:
            print("Error: ", e)

users_df = pd.DataFrame(users_list)
users_df.info()
#users_df.to_csv('./data/twitter_users_mining.csv', index=False)
#users_df = pd.read_csv('./data/twitter_users_mining.csv')

joint_set = final_set.join(users_df.set_index('username'), on='username')
joint_set.columns
joint_set[[
    'text', 'username', 'date', 'to',
    'likes', 'replies', 'retweets', 'verified',
    'followers', 'followees', 'statuses', 'favorites',
    'media_count'
]]

### Graph

### Stablishing the Adjacences List
adjacences = []

for k, v in final_set[["username", "to", "likes", "text"]].iterrows():
    if str(v['to']) not in ('NaN', 'nan', '', ' '):
        adjacences.append({"origin": v['username'], "target": v["to"], "weight": v['likes'] + 1,
                           "text": v['text']})  # likes+1 to cover 0 likes

### Graph Strucutre Basic Building Operations
def direct_edges(relations_obj):
    edges = []

    for a in relations_obj:
        edge = {"origin": None, "target": None, "weight": None, "text": None}
        edge['target'] = a['target']
        edge['origin'] = a['origin']
        edge['weight'] = a['weight']
        edge['text'] = a['text']
        edges.append(edge)
    return [
        (
            e['origin'],
            e['target'],
            {
                'title': str(e['text']),
                'weight': str(e['weight'])
            }
        )
        for e in edges
    ]


def nodes_from_df(df):
    nodes = []
    for n in np.append(df["username"].unique(), df["to"].astype('str').unique()):
        nodes.append((
            str(n), {'title': n}
        ))
    return nodes


def build_kb_graph(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

import networkx as nx

nodes = nodes_from_df(final_set[~final_set['to'].isnull()])
edges = direct_edges(adjacences)
kbg = build_kb_graph(nodes, edges)

### Graph Visualization
def draw_graph3(networkx_graph, directed=True, notebook=True, output_filename='graph.html', show_buttons=False,
                only_physics_buttons=False):
    """
    This function accepts a networkx graph object,
    converts it to a pyvis network object preserving its node and edge attributes,
    and both returns and saves a dynamic network visualization.

    Valid node attributes include:
        "size", "value", "title", "x", "y", "label", "color".

        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_node)

    Valid edge attributes include:
        "arrowStrikethrough", "hidden", "physics", "title", "value", "width"

        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_edge)


    Args:
        networkx_graph: The graph to convert and display
        notebook: Display in Jupyter?
        output_filename: Where to save the converted network
        show_buttons: Show buttons in saved version of network?
        only_physics_buttons: Show only buttons controlling physics of network?
    """

    # import
    from pyvis import network as net

    # make a pyvis network
    pyvis_graph = net.Network(notebook=notebook, directed=directed)
    pyvis_graph.set_edge_smooth('dynamic')
    pyvis_graph.width = '1000px'
    # for each node and its attributes in the networkx graph
    for node, node_attrs in networkx_graph.nodes(data=True):
        pyvis_graph.add_node(node, **node_attrs)
    #         print(node,node_attrs)

    # for each edge and its attributes in the networkx graph
    for source, target, edge_attrs in networkx_graph.edges(data=True):
        # if value/width not specified directly, and weight is specified, set 'value' to 'weight'
        # print(edge_attrs)
        if not 'value' in edge_attrs and not 'width' in edge_attrs and 'weight' in edge_attrs:
            # place at key 'value' the weight of the edge
            edge_attrs['value'] = edge_attrs['weight']
        # add the edge
        pyvis_graph.add_edge(source, target, **edge_attrs)

    # turn buttons on
    if show_buttons:
        if only_physics_buttons:
            pyvis_graph.show_buttons(filter_=['physics'])
        else:
            pyvis_graph.show_buttons()

    # return and also save
    return pyvis_graph.show(output_filename)


print("Nodes: ", len(nodes))
print("Edges: ", len(edges))

draw_graph3(kbg)

### Analytics
px.histogram(final_set.sort_values(by=['likes'], ascending=True), x='likes', color='likes')
px.histogram(users_df.sort_values(by=['statuses'], ascending=False), x="username", y="statuses", color="verified")
px.histogram(users_df.sort_values(by=['favorites'], ascending=False), x="username", y="favorites", color="verified")
fig = px.box(joint_set, y="likes", x='username')
fig.show()

import plotly.graph_objects as go

grouped_df = joint_set.groupby(['username']).sum().reset_index().query("likes >= 150")

labels = grouped_df['username']
values = grouped_df['likes']

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.update_layout(title='Profiles with at least 150 sum likes')
fig.show()
grouped_df = joint_set.groupby(['username']).count().reset_index()

## Top Unique Tweets QTY
grouped_df.sort_values(by=['text'], ascending=False).reset_index(drop=True)[['username', 'text']]
fig = px.line(joint_set.query("username in ('vanderrmacedo','PeeWee91197678','MiguelJac1')").sort_values(
    by=['date']).reset_index(), x="date", y="likes", color='username', title='Likes evolution by Profile')
fig.show()
vocab = " ".join(joint_set['text'].values)

# lista de stopword
nltk.download()
stopwords = set(STOPWORDS)
stopwords.update(
    nltk.corpus.stopwords.words('portuguese') + ["q", "pra", "vc", "c", "p", "pq", "co", "aí", "tá", "t", "https"])

# gerar uma wordcloud
wordcloud = WordCloud(stopwords=stopwords,
                      background_color="black",
                      width=1600, height=800).generate(vocab)

# mostrar a imagem final
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.set_axis_off()

plt.imshow(wordcloud);
wordcloud.to_file("elections.png")