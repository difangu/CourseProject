#!/usr/bin/env python
# coding: utf-8

# In[8]:


# read txt docs by lines, order has been matched exactly when exported from pre-processing phase 
school = [line.rstrip() for line in open('./input/dblp_school.txt')]
title  = [line.rstrip() for line in open('./input/dblp_title.txt')]
word  = [line.rstrip() for line in open('./input/dblp_word.txt')]


# In[9]:


school[0:10]


# In[10]:


def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


# In[11]:


title[0:10]


# In[12]:


# we have totally 10 schools that have been shown below
unique_school = list(unique(school))
unique_school


# In[13]:



#print(unique_school)
for i in range(0, len(unique_school)):
     print(i, unique_school[i]) 


# In[14]:


# this function will return school index that matches its input school name
def return_index(sc_name): 
    indices = [i for i, x in enumerate(school) if x == sc_name]
    return indices


# In[15]:


# create a list of list where each sublist contains all titles from that particular school
school_title_list = list()
for i in range(0, len(unique_school)):
    tmp = list()
    print(unique_school[i])
    school_ind_list = return_index(unique_school[i])
    for j in school_ind_list:
        tmp.append(title[j])
    school_title_list.append(tmp)  


# In[16]:


school_title_list[5]


# In[17]:


# For example, the first school is University of Satilde;o Paulo, Brazil
unique_school[0]


# In[18]:


# University of Satilde;o Paulo, Brazil's first item has index 1 in title list 
return_index(unique_school[0])[0]


# In[19]:


# return title with index = 1
title[return_index(unique_school[0])[0]]


# In[20]:


# This matches what we have from the school_title_list 
title[return_index(unique_school[0])[0]] == school_title_list[0][0]


# In[21]:


# write all of file in a for loop:
for i in range(0, len(unique_school)):
    school_name = unique_school[i]
    print(school_name + " has been output!")
    f = open("./school_output/school" + str(i) + ".txt", "w")
    for j in range(0, len(school_title_list[i])):
        if j == 0:
            f.write((school_title_list[i][j]))
        else: 
            f.write('\n' + (school_title_list[i][j]))
f.close()


# #### USA Colleges:
# (Note: we select colleges in the USA only because the main language used is English, which is easier for us to understand.)

# In[22]:


# We are using 3 USA schools to perform the annotation: 
# 5 MIT 
# 8 GT 
# 3 UoM

print("MIT has contributed", len(return_index(unique_school[5])), "papers in the conference.")
print("GT has contributed", len(return_index(unique_school[8])), "papers in the conference.")
print("UoM has contributed", len(return_index(unique_school[3])), "papers in the conference.")


# In[ ]:





# In[ ]:





# In[ ]:




