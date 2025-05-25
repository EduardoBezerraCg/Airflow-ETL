from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

target_path = '/opt/airflow/clickboard/processed.csv'
target = 'LeaveOrNot'

def make_test_train(df):
    x = df.drop(columns=target)
    y = df[target]
    return train_test_split(x, y, test_size=0.28, random_state=42)

def train_model(X_train, y_train):
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model