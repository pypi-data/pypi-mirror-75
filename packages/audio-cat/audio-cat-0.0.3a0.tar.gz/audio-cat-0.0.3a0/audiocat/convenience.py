from sklearn.manifold import TSNE
import pandas as pd
from . import scale_and_pca
from .predictor import optimal_bayes, optimal_K, gaussian_clustering
from .utils import group_samples

def quick_TSNE(X, random_state=420, dim=2):

    """

    Quick and easy method of visually validating predictions

    X: 2d array of data note, will work better after scaling applying PCA
    random_state: random state of tsne algorithm, keep the same for similar results, default=420
    dim: output dimensions if plotting on 2-d graph leave as 2 else change to 3. default=2

    returns tuple of len(d) 1dim data


    """

    X_tsne = TSNE(n_components=dim, random_state=random_state).fit_transform(X)

    return [ X_tsne[:, d] for d in range(dim) ]



def group_from_dataset_path(d_path, a_path, title, destination='audio', optimizer='bayes', K=None, max_=10, add_labels=True, keep_original=True):

    sound_data = pd.read_csv(d_path)  
    X_pca = scale_and_pca(sound_data.drop(['filename', 'label'], axis=1))

    if not K:
        
        if optimizer == 'bayes':
            K = optimal_bayes(X_pca, max_=max_)

        elif optimizer == 'kmeans':
            K = optimal_K(X_pca, max_=max_)

    y = gaussian_clustering(X_pca, K)

    des = group_samples(sound_data.filename, y, title, a_path, destination=destination, keep_original=keep_original)

    if add_labels:
        sound_data.label = np.array(y)
        sound_data.to_csv(d_path, index=False)


    return des