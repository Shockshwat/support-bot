import pickle


def get_data():
    with open("Data/Data.pickle", "rb") as f:
        Data = pickle.load(f)
        return Data


def add_data(key, value):
    Data = get_data()
    Data["name"].append(key)
    Data["values"].append(value)
    with open("Data/Data.pickle", "wb") as f:
        pickle.dump(Data, f)


def remove_data(key):
    Data = get_data()
    Data["values"].remove(Data["values"][Data["name"].index(key)])
    Data["name"].remove(key)
    with open("Data/Data.pickle", "wb") as f:
        pickle.dump(Data, f)
