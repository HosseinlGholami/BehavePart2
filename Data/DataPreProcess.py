import pandas as pd
import  random
import  pickle

random.seed(2020)

acc_df=pd.read_csv('accelerations.csv').drop('acceleration_id',1)
acc_df.rename(columns={'x_value':'a-x',
                       'y_value':'a-y',
                       'z_value':'a-z'}, 
                 inplace=True)

gyr_df=pd.read_csv('gyroscopes.csv').drop('gyroscope_id',1)
gyr_df.rename(columns={'x_value':'g-x',
                       'y_value':'g-y',
                       'z_value':'g-z'}, 
                 inplace=True)
acc_df['timestamp'] = pd.to_datetime(acc_df['timestamp'])
gyr_df['timestamp'] = pd.to_datetime(gyr_df['timestamp'])

print("started")
gyr_df['g-x']=gyr_df.apply(lambda x:x[0]/max(gyr_df['g-x']),axis=1)
print("1")
gyr_df['g-y']=gyr_df.apply(lambda x:x[1]/max(gyr_df['g-y']),axis=1)
print("2")
gyr_df['g-z']=gyr_df.apply(lambda x:x[2]/max(gyr_df['g-z']),axis=1)
print("3")
acc_df['a-x']=acc_df.apply(lambda x:x[0]/max(acc_df['a-x']),axis=1)
print("4")
acc_df['a-y']=acc_df.apply(lambda x:x[1]/max(acc_df['a-y']),axis=1)
print("5")
acc_df['a-z']=acc_df.apply(lambda x:x[2]/max(acc_df['a-z']),axis=1)
print("6")

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
print("end")