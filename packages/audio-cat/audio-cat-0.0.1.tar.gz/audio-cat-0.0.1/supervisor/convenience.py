from sklearn.manifold import TSNE

def quick_TSNE(X, random_state=420, dim=2):

    """

    Quick and easy method of visually validating predictions

    X: 2d array of data note, will work better after scaling applying PCA
    random_state: random state of tsne algorithm, keep the same for similar results, default=420
    dim: output dimensions if plotting on 2-d graph leave as 2 else change to 3. default=2

    returns tuple of len(d) 1dim data


    """

    X_tsne = TSNE(n_components=dim, random_state=random_state).fit_transform(X)

    return ( X_tsne[:, d] for d in range(dim) )