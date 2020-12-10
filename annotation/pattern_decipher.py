#!/usr/bin/env python
# coding: utf-8

# In[70]:


import numpy as np


# #### Load Data

# In[71]:


#5 Massachusetts Institute of Technology, Cambridge, MA, USA
#8 Georgia Institute of Technology, Atlanta, GA, USA
#3 University of Maryland, College Park, MD, USA
MIT_D = [line.rstrip() for line in open('./school_output/school2.txt')]
GT_D = [line.rstrip() for line in open('./school_output/school8.txt')]
UoM_D = [line.rstrip() for line in open('./school_output/school9.txt')]

# here we load the frequent pattern for selected U.S schools 
dictionary = [line.rstrip() for line in open('./input/dblp_word.txt')]
MIT = [line.rstrip() for line in open('./pattern_output/output2.txt')]
GT = [line.rstrip() for line in open('./pattern_output/output8.txt')]
UoM = [line.rstrip() for line in open('./pattern_output/output9.txt')]


# #### List Conversion:

# In[72]:


def listlize(alist):
    count = 0 
    for i in alist:
        alist[count] = i.split()
        count = count + 1
    return alist


# In[73]:


def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


# In[74]:


MIT_D = listlize(MIT_D)
GT_D = listlize(GT_D)
UoM_D = listlize(UoM_D)


# #### School Title Pattern Examples:

# In[75]:


MIT[0:5]


# In[76]:


GT[0:5]


# In[77]:


UoM[0:5]


# #### Sublist Conversion:

# In[78]:


def extract_sublist(school_list):
    another_list = list()
    for i in range(0, len(school_list)):
        some_list = school_list[i].split()
        tmp_list = list()
        for i in some_list:
            if i != '#SUP:':
                tmp_list.append(int(i))
            elif i == '#SUP:':
                another_list.append(tmp_list)
                break
    return another_list


# In[79]:


MIT_list = extract_sublist(MIT)
GT_list = extract_sublist(GT)
UoM_list = extract_sublist(UoM)


# In[80]:


MIT_list[0:5]


# #### Create Dictionary: 

# In[81]:


new_dict = dict()
for i in range(0, len(dictionary)):
    key1 = dictionary[i].split()[1]
    item1 = dictionary[i].split()[0]
    new_dict[key1] = item1


# In[82]:


# this is the new dictionary that can be mapped from integer to any words:
new_dict["-1"] = None # add -1 as blank
new_dict # the dictionary contains more than English because it was derived when pooling all schools across the globe


# #### Remove Redundancy: 

# In[83]:


def setize(alist):
    new_list = list([0]*len(alist))
    for i in range(0, len(alist)):
        alist[i] = list(unique(alist[i]))
    return alist


# In[84]:


def rm_du_sublst(alist):
    return list(unique(tuple((i)) for i in setize(alist)))


# In[85]:


final_MIT = rm_du_sublst(MIT_list)
final_GT = rm_du_sublst(GT_list)
final_UoM = rm_du_sublst(UoM_list)


# In[86]:


final_MIT[0:10]


# In[87]:


final_GT[0:10]


# In[88]:


final_UoM[0:10]


# #### Mutual Information: 

# In[89]:


def mu_info(Pa, Da, School):
    #beta = Y = school 
    #alpha = X = pattern
    D1 = MIT_D
    D2 = GT_D
    D3 = UoM_D
    
    if School == "MIT":
        Pd = len(D1)
    elif School == "GT":
        Pd = len(D2)
    elif School == "UoM":
        Pd = len(D3)

    # fixed
    D_all = D1 + D2 + D3
    absD = len(D_all)
    Py = Pd/absD

    count_ab = 0 
    countX = 0

    # all count of pattern in the target transaction (school)
    for i in range(0, len(Da)):
        count_ab = all(str(elem) in Da[i] for elem in Pa) + count_ab

    # all counts of pattern appearing in all transactions (all schools)
    for i in range(0, len(D_all)):
        countX = all(str(elem) in D_all[i] for elem in Pa) + countX

    Px = countX/len(D_all)
    X1Y1 = count_ab/absD
    X0Y1 = (len(D1) - count_ab)/absD
    X1Y0 = 0
    X0Y0 = (absD - count_ab)/absD

    result = X1Y1 * np.log(X1Y1/(Px*Py)) + X0Y1 * np.log(X0Y1/(Px*Py)) + X0Y0 *np.log(X0Y0/(Px*Py))
    return result


# In[90]:


# MIT Mutual Information: 
MIT_MI = list()
for i in final_MIT:  #iterate every pattern of MIT 
    MIT_MI.append(mu_info(Pa = list(i), Da = MIT_D, School = "MIT"))


# In[91]:


# GT Mutual Information: 
GT_MI = list()
for i in final_GT:  #iterate every pattern of MIT 
    GT_MI.append(mu_info(Pa = list(i), Da = GT_D, School = "GT"))


# In[92]:


# UoM Mutual Information: 
UoM_MI = list()
for i in final_UoM:  #iterate every pattern of MIT 
    UoM_MI.append(mu_info(Pa = list(i), Da = UoM_D, School = "UoM"))


# #### Feature Pattern: 

# In[93]:


MIT_top = list()
GT_top = list()
UoM_top = list()

for i in range(1,16):
    MIT_top.append(final_MIT[np.argsort(MIT_MI)[-i]])
    GT_top.append(final_GT[np.argsort(GT_MI)[-i]])
    UoM_top.append(final_UoM[np.argsort(UoM_MI)[-i]])


# #### Word Conversion:

# In[94]:


def word_convert(college_top):
    result_list = list()
    for i in college_top:
        tmp = list()
        for j in i: 
            if new_dict[str(j)] != None: 
                tmp.append(new_dict[str(j)])
            else: 
                pass
        result_list.append(tmp)    
    return result_list


# In[95]:


print(word_convert(MIT_top))
f = open("./outcome/MIT.txt", "w")
for i in range(0, len(word_convert(MIT_top))):
    if i == 0: 
        f.write(str(word_convert(MIT_top)[i]))
    else:
        f.write("\n" + str(word_convert(MIT_top)[i]))
f.close()


# In[96]:


print(word_convert(GT_top))
f = open("./outcome/GT.txt", "w")
for i in range(0, len(word_convert(GT_top))):
    if i == 0: 
        f.write(str(word_convert(GT_top)[i]))
    else:
        f.write("\n" + str(word_convert(GT_top)[i]))
f.close()


# In[97]:


print(word_convert(UoM_top))
f = open("./outcome/UoM.txt", "w")
for i in range(0, len(word_convert(UoM_top))):
    if i == 0: 
        f.write(str(word_convert(UoM_top)[i]))
    else:
        f.write("\n" + str(word_convert(UoM_top)[i]))
f.close()


# In[ ]:





# In[ ]:




