import pandas as pd
import  random
import  pickle

random.seed(2020)

acc_df=pd.read_csv('accelerations.csv').drop('acceleration_id',1)
acc_df.rename(columns={'x_value':'a_y',
                       'y_value':'a_x',
                       'z_value':'a_z'}, 
                 inplace=True)
gyr_df=pd.read_csv('gyroscopes.csv').drop('gyroscope_id',1)
gyr_df.rename(columns={'x_value':'g_y',
                       'y_value':'g_x',
                       'z_value':'g_z'}, 
                 inplace=True)
acc_df['timestamp'] = pd.to_datetime(acc_df['timestamp'])
gyr_df['timestamp'] = pd.to_datetime(gyr_df['timestamp'])


# pos_df=pd.read_csv('positions.csv').drop('pos_id',1)
# pos_df['timestamp'] = pd.to_datetime(pos_df['timestamp'])

def clear(a,g):
    a=a.set_index("timestamp").drop("trip_id",axis=1)
    g["ts"]=a.index
    g=g.set_index(['ts']).drop("timestamp",axis=1).drop("trip_id",axis=1)
    return pd.concat([a,g], axis=1, join='outer')

sensory_data=list()
for i in range(3,36):
    g=gyr_df[gyr_df.trip_id==i]
    a=acc_df[acc_df.trip_id==i]
    if(len(a)==len(g)):
        sensory_data.append(clear(a,g))
    elif len(a)>len(g):
        while len(a)!=len(g):
            a=a.drop(random.choice(a.index))
        sensory_data.append(clear(a,g))
    elif len(a)<len(g):
        while len(a)!=len(g):
            g=g.drop(random.choice(g.index))
        sensory_data.append(clear(a,g))

with open("data_list_per_driver", "wb") as fp:
    pickle.dump(sensory_data, fp)
