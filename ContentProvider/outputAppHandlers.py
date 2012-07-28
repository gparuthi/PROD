def TwitterIdJS(ids):
    print ids
    #returns the js code for the twitter app 
    ret = "gadgets/twitter_search.html?ids=\x22"+','.join(ids)+"\x22"
    return ret

def TwitterTagsJS(ids):
    print ids
    #returns the js code for the twitter app 
    ret = "gadgets/twitter_search.html?ids=\x22"+' OR '.join(ids)+"\x22"
    return ret

def FlickrTags(ids):
    print ids
    #returns the js code for the twitter app 
    ret = "gadgets/flickr_tags.html?ids=\x22"+','.join(ids)+"\x22"
    return ret

def FlickrIds(ids):
    print ids
    #returns the js code for the twitter app 
    ret = "gadgets/flickr_ids.html?ids=\x22"+','.join(ids)+"\x22"
    return ret