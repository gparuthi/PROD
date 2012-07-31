'''
Created on Jul 28, 2012

@author: gparuthi
'''

def TwitterIdJS(ids):
    print ids
    #returns the js code for the twitter app 
    ret = "gadgets/twitter_search.html?ids="+str(ids)+""
    return ret

def TwitterTagsJS(ids):
    print ids
    #returns the js code for the twitter app 
    ret = "gadgets/twitter_search.html?ids="+ ids.replace(',',' OR ')+""
    return ret

def FlickrTags(ids):
    print ids
    #returns the js code for the twitter app 
    ret = "gadgets/flickr_tags.html?ids="+str(ids)+""
    return ret

def FlickrIds(ids):
    print ids
    #returns the js code for the twitter app 
    ret = "gadgets/flickr_ids.html?ids="+ str(ids)+""
    return ret