#!/usr/bin/env python
# coding: utf-8

# In[92]:


from stackapi import StackAPI
#passing website and key
SITE = StackAPI('stackoverflow',key='1m2D1EmsS*nKHGMwKBEAgQ((')
SITE.max_pages=5
SITE.page_size=100
#calling questions API to get questions wtagged with python and sorted by activity
questions = SITE.fetch('questions', sort='activity',tagged='python')
print("Number of questions fetched: ",len(questions['items']))

#passing all question ids into a array
question_id = []
for i in (questions['items']):
    question_id.append(i['question_id'])
print("All question id's are appended to an array 'question_id'")


# In[93]:


answers = []
#calling API to get all answers of the questions by passing question ids
for i in question_id:
    answers.append(SITE.fetch('questions/{0}/answers/'.format(i)))
print("Answers for all the questions are loaded")


# In[111]:


def header(file):
    result = []
    if (file == 'allposts'):
        result.append('Tags'); result.append('Asker Reputation'); result.append('Asker Id');result.append('User type')
        result.append('Profile Image');result.append('Asker Name');result.append('Link to Asker')
        result.append('Is Answered'); result.append('View Count'); result.append('Answer Count')
        result.append('Score'); result.append('last_activity_date'); result.append('creation_date');
        result.append('last_edit_date');result.append('Question Id'); result.append('link'); result.append('Title')

        result.append('Answerer reputation'); result.append('Answerer Id'); result.append('Answerer user_type')
        result.append('Answerer accept rate'); result.append('Answerer profile_image'); result.append('Answerer Name')
        result.append('Answerer link'); result.append('Is Accepted'); result.append('Answerer score')
        result.append('last_activity_date'); result.append('last_edit_date'); result.append('creation_date')
        result.append('Answer_id'); result.append('Question_id')
    elif (file == 'meta_data'):
        result.append('Asker Id');result.append('Answerer Id');result.append('Post_link');
    #header for ask_ans file
    elif (file == 'ask_ans'):
            result.append('Asker Id');result.append('Answerer Id')
    return(result)


# In[112]:


def extract(file,tsvout):
    for i in range(len(questions['items'])):
        for j in range(len(answer[i]['items'])):
            qown = questions['items'][i]['owner']
            aown = answer[i]['items'][j]['owner']
            if qown['user_type'] == 'does_not_exist' or aown['user_type'] == 'does_not_exist':
                continue
            else:    
                out = []
                if (file == 'allposts'):
                    out.append(questions['items'][i]['tags']);out.append(qown['reputation'])
                    out.append(qown['user_id']); out.append(qown['user_type'])
                    if 'profile_image' not in qown:
                        out.append('N/A')
                    else:
                        out.append(qown['profile_image']); 
                    out.append(qown['display_name'])
                    out.append(qown['link']); out.append(questions['items'][i]['is_answered'])
                    out.append(questions['items'][i]['view_count']);
                    out.append(questions['items'][i]['answer_count']);out.append(questions['items'][i]['score'])
                    out.append(questions['items'][i]['last_activity_date']); 
                    out.append(questions['items'][i]['creation_date'])
                    if 'last_edit_date' not in questions['items'][i]:
                        out.append('N/A')
                    else:
                        out.append(questions['items'][i]['last_edit_date'])
                    out.append(questions['items'][i]['question_id']); out.append(questions['items'][i]['link'])
                    out.append(questions['items'][i]['title'])

                    out.append(aown['reputation']); out.append(aown['user_id'])
                    out.append(aown['user_type']); 
                    if 'accept_rate' not in aown:
                        out.append('N/A')
                    else:
                        out.append(aown['accept_rate'])
                    out.append(aown['profile_image']); out.append(aown['display_name'])
                    out.append(aown['link']); out.append(answer[i]['items'][j]['is_accepted'])
                    out.append(answer[i]['items'][j]['score'])
                    out.append(answer[i]['items'][j]['last_activity_date']);
                    if 'last_edit_date' not in answer[i]['items'][j]:
                        out.append('N/A')
                    else:
                        out.append(answer[i]['items'][j]['last_edit_date'])
                    out.append(answer[i]['items'][j]['creation_date']);out.append(answer[i]['items'][j]['answer_id'])
                    out.append(answer[i]['items'][j]['question_id'])
                elif (file == 'ask_ans'):
                    out.append(qown['user_id']); out.append(aown['user_id'])
                elif (file == 'meta_data'):
                    out.append(qown['user_id']); out.append(aown['user_id']); out.append(questions['items'][i]['link'])
                
                tsvout.writerow(out)


# In[118]:


def fetch(file,tsvout):
    result = header(file);
    tsvout = csv.writer(tsvout, delimiter = '\t')
    #writing header
    tsvout.writerow(result)
    extract(file,tsvout)


# In[119]:


def main(file):
    import csv
    #opening and writing the fetched data into out.tsv file
    if file == 'allposts':
        with open('C:/Users/Ravali/Desktop/allposts.tsv', 'w',encoding='utf-8') as tsvout:
            fetch(file,tsvout)
    elif (file == 'meta_data'):
        with open('C:/Users/Ravali/Desktop/allposts_metadata.tsv', 'w',encoding='utf-8') as tsvout:
            fetch(file,tsvout)
    elif (file == 'ask_ans'):
        with open('C:/Users/Ravali/Desktop/asker_answerer.tsv', 'w',encoding='utf-8') as tsvout:
            fetch(file,tsvout)
    
    print('{0}.tsv file generated'.format(file))


# In[120]:


main('allposts')
main('meta_data')
main('ask_ans')

