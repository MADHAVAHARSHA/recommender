import numpy as np
import pandas 
class item_similarity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.userId = None
        self.item_id = None
        self.cooccurence_matrix = None
        self.rec_dict = None
        self.rev_rec_dict = None
        self.item_similarity_recommendations = None
        self.popularity_recommendations = None
        
    
    def get_user_items(self, user):
        user_data = self.train_data[self.train_data[self.userId] == user]
        user_items = list(user_data[self.item_id].unique())
        return user_items
        
    
    def get_item_users(self, item):
        item_data = self.train_data[self.train_data[self.item_id] == item]
        item_users = set(item_data[self.userId].unique())
            
        return item_users
        
    #Get unique items (rec) in the training data
    def get_all_items_train_data(self):
        all_items = list(self.train_data[self.item_id].unique())
            
        return all_items
        
    
    def construct_cooccurence_matrix(self, user_rec, all_rec):
            
      
        user_rec_users = []        
        for i in range(0, len(user_rec)):
            user_rec_users.append(self.get_item_users(user_rec[i]))
            
        
        cooccurence_matrix = np.matrix(np.zeros(shape=(len(user_rec), len(all_rec))),float)
           
        
        for i in range(0,len(all_rec)):
            
            rec_i_data = self.train_data[self.train_data[self.item_id] == all_rec[i]]
            users_i = set(rec_i_data[self.userId].unique())
            
            for j in range(0,len(user_rec)):       
                    
                
                users_j = user_rec_users[j]
                    
                
                users_intersection = users_i.intersection(users_j)
                
                
                if len(users_intersection) != 0:
                    
                    users_union = users_i.union(users_j)
                    
                    cooccurence_matrix[j,i] = float(len(users_intersection))/float(len(users_union))
                else:
                    cooccurence_matrix[j,i] = 0
                    
        
        return cooccurence_matrix

    
    
    def generate_top_recommendations(self, user, cooccurence_matrix, all_rec, user_rec):
        print("Non zero values in cooccurence_matrix :%d" % np.count_nonzero(cooccurence_matrix))
        
        
        user_sim_scores = cooccurence_matrix.sum(axis=0)/float(cooccurence_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()
 
        sort_index = sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)
    
        
        columns = ['userId', 'App', 'score', 'rank']
        
        df = pandas.DataFrame(columns=columns)
         
        #Fill the dataframe with top n item based recommendations
        rank = 1 
        for i in range(0,len(sort_index)):
            if ~np.isnan(sort_index[i][0]) and all_rec[sort_index[i][1]] not in user_rec and rank <= 10:
                df.loc[len(df)]=[user,all_rec[sort_index[i][1]],sort_index[i][0],rank]
                
                rank = rank+1
        
        #Handle the case where there are no recommendations
        if df.shape[0] == 0:
            print("The current user has no rec for training the item similarity based recommendation model.")
            return -1
        else:
            return df
 
    
    def create(self, train_data, userId, item_id):
        self.train_data = train_data
        self.userId = userId
        self.item_id = item_id

   
    def recommend(self, user):
        
        
        user_rec = self.get_user_items(user)    
            
        print("No. of unique rec for the user: %d" % len(user_rec))
        
     
        all_rec = self.get_all_items_train_data()
        
        print("no. of unique rec in the training set: %d" % len(all_rec))
         
       
        cooccurence_matrix = self.construct_cooccurence_matrix(user_rec, all_rec)
        
        
        df_recommendations = self.generate_top_recommendations(user,
                                                               cooccurence_matrix, all_rec, user_rec)
                
        return df_recommendations
    
    #Get similar items to given items
    def get_similar_items(self, item_list):
        
        user_rec = item_list
     
        all_rec = self.get_all_items_train_data()
        
        print("no. of unique rec in the training set: %d" % len(all_rec))
         
        
        cooccurence_matrix = self.construct_cooccurence_matrix(user_rec, all_rec)
        
      
        user = ""
        df_recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_rec, user_rec)
         
        return df_recommendations