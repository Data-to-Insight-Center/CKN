from komadu_client.synthetic_gen.util import get_graphdb
import numpy as np

get_inputs_for_campaign = "match (sg:SweepGroup{id: 'grayscott-sg1'})-[r*]-(input:Input) return input"


def unique_rows(a):
    # todo: fix this
    # extracted from stackoverflow
    # https://stackoverflow.com/questions/8560440/removing-duplicate-columns-and-rows-from-a-numpy-2d-array
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def main():
    graphdb = get_graphdb()
    result = graphdb.retrieve_data(get_inputs_for_campaign)
    feature_space = []
    for i in range(len(result)):
        node = result[i]['input']
        features = []
        if node['Du'] is None:
            continue
        features.append(node['L'])
        features.append(node['Du'])
        features.append(node['Dv'])
        features.append(node['F'])
        features.append(node['k'])
        features.append(node['dt'])
        features.append(node['plotgap'])
        features.append(node['steps'])
        features.append(node['noise'])
        feature_space.append(np.array(features))
    feature_space_array = unique_rows(np.array(feature_space))
    print(feature_space_array)
    np.savetxt('output.csv', feature_space_array, delimiter=",")


if __name__ == "__main__":
    main()
