from itertools import permutations, combinations
import numpy as np

def calculate_umass_coherence(X, word_topic, clusters, k, N=5):
    k_coherence = []
    count_data = X.copy()
    # Transform to binary count
    count_data[np.where(count_data != 0)] = 1

    # For each cluster, calculate coherence
    for idx_cluster in range(k):
        cluster_data = count_data[clusters == idx_cluster]

        # If there aren't any documents assigned to the cluster, skip it
        if cluster_data.shape[0] == 0:
            continue

        # Calculate cooccurence matrix
        cooccurence = np.dot(cluster_data.T, cluster_data)

        # For each topic, get N top words
        idx = word_topic[:,idx_cluster].argsort()[::-1][:N]
        perms = permutations(idx, 2)
        k_score = []
        for i,j in perms:
            if cooccurence[i,i] == 0:
                continue
            score = np.log((cooccurence[i,j]+0.01)/cooccurence[i,i])
            k_score.append(score)
        k_topic = np.mean(np.asarray(k_score))
        k_coherence.append(k_topic)
    return k_coherence, np.median(k_coherence), np.std(k_coherence)


def calculate_uci_coherence(X, word_topic, clusters, k, N=5):
    """ UCI coherence: it calculates PMI for the top-N words using
    an external dataset.  """
    k_pmi = []
    count_data = X.copy()
    # Transform to binary count
    count_data[np.where(count_data != 0)] = 1

    # For each cluster, calculate PMI
    for idx_cluster in range(0, k):

        cluster_data = count_data[clusters == idx_cluster]

        # If there aren't any documents assigned to the cluster, skip it
        if cluster_data.shape[0] == 0:
            continue

        # Calculate cooccurence matrix
        cooccurence = np.dot(cluster_data.T, cluster_data)

        # For each topic, get N top words
        idx = word_topic[:,idx_cluster].argsort()[::-1][:N]
        combs = combinations(idx, 2)
        k_score = []
        for i,j in combs:
            if cooccurence[i,i] == 0 or cooccurence[j,j] == 0:
                raise RuntimeError("Some words do not occur in topic %d. Choose a smaller number of N." %
                                   idx_cluster)
            score = np.log((cooccurence[i,j]+0.01)/(cooccurence[i,i] * cooccurence[j,j]))
            k_score.append(score)
        k_topic = np.mean(np.asarray(k_score))
        k_pmi.append(k_topic)
    return k_pmi, np.mean(k_pmi), np.std(k_pmi)
