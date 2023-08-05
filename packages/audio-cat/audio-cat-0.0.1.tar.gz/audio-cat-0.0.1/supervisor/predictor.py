import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from sklearn.mixture import GaussianMixture


def scale_and_pca(X, n_components=0.95):

    """

    Quick scaling and pca method

    X: 2d array of data
    n_components: fed to PCA see sklearn.decomposition.PCA for more info https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

    return 2d array of scaled and pca data

    """

    st_scaler = StandardScaler()
    X_ss = st_scaler.fit_transform(X)

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_ss)

    return X_pca



def optimal_K(X_pca, max=40, random_state=420, inertia=False):

    """

    Use k-means to find optimal number of clusters

    X_pca: 2d scaled and pca data, see scale_and_pca
    max: max search of clusters, default=40
    random_state: random state to keep uniformity between trials default=420
    inertia: return list of inertias to plot in format (x, y), default=False

    """

    inertias = []
    sils = []

    for k in range(2, max):
        kmeans = KMeans(n_clusters=k, random_state=random_state).fit(X_pca)
        inertias.append(kmeans.inertia_)
        sils.append(silhouette_score(X_pca, kmeans.labels_))

    if inertia:
        return ([*range(2, max)], inertias)


    return np.argmax(sils) + 2



def gaussian_clustering(K, X_pca, n_init=10, random_state=420):

    """

    gaussian mixture to group different sources of sound

    K: number of components
    X_pca: 2d scaled and pca data, see scale_and_pca
    n_init: gaussian clustering cycles
    random_state: random state to keep uniformity between trials default=420

    """

    gm = GaussianMixture(n_components=K, n_init=n_init, random_state=random_state)
    gm.fit(X_pca)
    y_gm = gm.predict(X_pca)

    return y_gm


def reconstruction_error(pca, X):
    X_pca = pca.transform(X)
    X_recon = pca.inverse_transform(X_pca)
    mse = np.square(X_recon-X).mean(axis=-1)
    return mse



def pca_reconstruction_error(X_pca, y_pred):

    """

    using custom pca reconstruction model to try to find mistakes in clustering and improve pipeline,
        - functions better on larger datsets with more even speakers

    X_pca: 2d scaled and pca data, see scale_and_pca
    y_pred: predicted y labels for X_pca, see kmeans and gaussian mixture

    returns a dataframe with possible different combinations of clusters

    """

    clustered_data = {x:X_pca[y_pred == x] for x in set(y_pred)}
    y_pred = pd.Series(y_pred)
    labels = pd.DataFrame(y_pred, columns=['og'])


    for key, item in clustered_data.items():
        
        cluster_pca = PCA(n_components=0.99).fit(item)
        rec = reconstruction_error(cluster_pca, item)
        threshold = np.std(rec) + rec.mean()
        
        cluster_labels = y_pred.copy()
        
        non_cluster = cluster_labels[cluster_labels != key]
        inds = non_cluster[list(reconstruction_error(cluster_pca, X_pca[cluster_labels != key]) < threshold)].index
        
        cluster_labels.iloc[inds] = key
        #print(f"{key} : {inds}")
        print(f"replaced {len(inds)} instance(s) with {key}")
        
        labels[key] = cluster_labels


    return labels