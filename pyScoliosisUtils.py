# -*- coding: utf-8 -*-
# !/bin/env python
import pickle


def load_data(filename="data.pickle"):
    with open(filename, 'rb') as restore_data:
        data = pickle.load(restore_data)

    return data


def save_data(data, filename="data.pickle"):
    try:
        with open(filename, 'wb') as savedata:
            pickle.dump(data, savedata)
    except IOError as ierr:
        print("File Error: " + str(ierr))
    except pickle.PickleError as perr:
        print("Pickle Error: " + str(perr))


def dummy_data():
    data = []
    for i in range(0, 600):
        it = str(i + 1)
        p = [i + 1, "district " + it, "school " + it, "class " + it, "student number " + it, u"姓名 " + it,
             "contact information ********************* " + it, "measured angle " + it, "", "", "", False,
             "A"]
        # print p
        data.append(p)
    return data
