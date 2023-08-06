#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def test_split_remove(text):
    import re
    punctuation = '!,;:?"\''
    def removePunctuation(text):
        text = re.sub('[{}]+'.format(punctuation),'',text) #re.sub用于替换字符串中的匹配项
        return text.strip().split()


# In[17]:


"""
import re
 
punctuation = '!,;:?"\''
def removePunctuation(text):
    text = re.sub('[{}]+'.format(punctuation),'',text) #re.sub用于替换字符串中的匹配项
    return text.strip().split()
 
text = " Hello, world!  "
print(removePunctuation(text))

"""


# In[11]:


#punctuation = '!,;:?"\''
#print('[{}]+'.format(punctuation))

