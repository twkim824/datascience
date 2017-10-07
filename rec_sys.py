from math import sqrt
import matplotlib.pyplot as plt

# Movie Recommendation System

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


def transform_data(data):   # changes data structure from each critics' movie
                            # ratings to each movie's critic ratings
    transformed = {}
    for critic in data:
        for movie in data[critic]:
            transformed.setdefault(movie, {})
            transformed[movie][critic] = data[critic][movie]
    return transformed

print(transform_data(critics))
                
# Two methods to determine taste similarity between two people:
    
# Method 1

def euclidean(data, person1, person2):
    
    common = {}         # dict containing common movies rated
    
    for movie in data[person1]:
        if movie in data[person2]:
            common[movie] = 1
            
    if len(common) == 0:
        return 0
    
    sumofsquares = sum([pow(data[person1][movie]-data[person2][movie],2)
                        for movie in common])
    
    return (1/(1+sqrt(sumofsquares)))

# Method 2

def pearson(data, person1, person2):    
    
    common = {}
    
    for movie in data[person1]:
        if movie in data[person2]:
            common[movie] = 1
    
    n = len(common)
    
    if n == 0:
        return 0
    
    mean1 = sum([data[person1][movie] for movie in common]) / n
    mean2 = sum([data[person2][movie] for movie in common]) / n
    sum1 = sum([(data[person1][movie]-mean1)*(data[person2][movie]-mean2) 
                for movie in common])
    sum2 = sum([pow(data[person1][movie]-mean1, 2) for movie in common])
    sum3 = sum([pow(data[person2][movie]-mean2, 2) for movie in common])
    denom = sqrt(sum2*sum3)
    
    return sum1 / denom
    
print(pearson(critics, 'Lisa Rose', 'Gene Seymour'))

# Return an ordered list of critics with similar tastes (descending)
# Print a graph showing similarity scores for each of the other critics

def rankCritics(data, person):
    scores = [(pearson(data, person, critic), critic) 
    for critic in data if critic != person]
    scores.sort()
    scores.reverse()
    
    score_arr = []
    critic_arr = []
    my_xticks = []
    
    for each in scores:
        score_arr.append(each[0])
        my_xticks.append(each[1])
    
    for i in range(len(score_arr)):
        critic_arr.append(i)
        
    plt.figure(1)
    plt.xticks(critic_arr, my_xticks)
    plt.plot(critic_arr, score_arr, 'ro')

rankCritics(critics, 'Toby')

# Making recommendation: rating of each movie based on other critics' ratings
# Print a graph showing the recommended movies and predicted ratings

def recommendations(data, person):
    ratings = {}
    score_sum = {}
    lst=[]
    movie_axis = []
    rating_axis = []
    my_xticks = []
    for critic in data:
        if critic == person:
            continue
        
        score = pearson(data, person, critic)
        for movie in data[critic]:
            if movie not in data[person]:
                if movie in ratings:
                    ratings[movie] += score * data[critic][movie]
                    score_sum[movie] += score
                else:
                    ratings[movie] = score * data[critic][movie]
                    score_sum[movie] = score
    for key in ratings.keys():
        ratings[key] = ratings[key] / score_sum[key]
        lst.append((ratings[key],key))
    
    lst.sort()
    lst.reverse()
    
    for tup in lst:
        rating_axis.append(tup[0])
        my_xticks.append(tup[1])
    
    for i in range(len(ratings)):
        movie_axis.append(i)
    
    plt.figure(2)
    plt.xticks(movie_axis, my_xticks)
    plt.axis([-1,len(ratings),0,5])
    plt.plot(movie_axis, rating_axis, 'ro')

recommendations(critics, 'Toby')
    
    
    
    
    
    
    
    
    