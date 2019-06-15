import numpy as np
#import imageio
import cv2
import sklearn.neighbors
import matplotlib
import imageio
import scipy.sparse
import warnings

nn = 10


def knn_matte(img1, trimap, mylambda=80):
    #[m, n, c] = img.shape

    #img = matplotlib.colors.rgb_to_hsv(img1)
    img = img1
    [m, n, c] = img.shape

    img, trimap = img/255.0, trimap/255.0
    foreground = (trimap > 0.99).astype(int)
    background = (trimap < 0.01).astype(int)
    all_constraints = foreground + background

    print('Finding nearest neighbors')
    a, b = np.unravel_index(np.arange(m*n), (m, n))
    feature_vec = np.append(np.transpose(img.reshape(m*n,c)), [ a, b]/np.sqrt(m*m + n*n), axis=0).T
    nbrs = sklearn.neighbors.NearestNeighbors(n_neighbors=10, n_jobs=4).fit(feature_vec)
    knns = nbrs.kneighbors(feature_vec)[1]

    # Compute Sparse A
    print('Computing sparse A')
    row_inds = np.repeat(np.arange(m*n), 10)
    col_inds = knns.reshape(m*n*10)
    vals = 1 - np.linalg.norm(feature_vec[row_inds] - feature_vec[col_inds], axis=1)/(c+2)
    A = scipy.sparse.coo_matrix((vals, (row_inds, col_inds)),shape=(m*n, m*n))

    D_script = scipy.sparse.diags(np.ravel(A.sum(axis=1)))
    L = D_script-A
    D = scipy.sparse.diags(np.ravel(all_constraints[:,:, 0]))
    v = np.ravel(foreground[:,:,0])
    c = 2*mylambda*np.transpose(v)
    H = 2*(L + mylambda*D)

    print('Solving linear system for alpha')
    warnings.filterwarnings('error')
    alpha = []
    try:
        alpha = np.minimum(np.maximum(scipy.sparse.linalg.spsolve(H, c), 0), 1).reshape(m, n)
    except Warning:
        x = scipy.sparse.linalg.lsqr(H, c)
        alpha = np.minimum(np.maximum(x[0], 0), 1).reshape(m, n)
    return alpha


def main():
    #img = scipy.misc.imread('donkey.png')[:,:,:3]
    #trimap = scipy.misc.imread('donkeyTrimap.png')[:,:,:3]

    img = scipy.misc.imread('0046.jpg')[:,:,:3]
    trimap = cv2.imread('0046pok2.png')[:,:,:3]

    kernel = np.ones((3, 3), np.uint8)
    sure_fg = cv2.erode(trimap, kernel, iterations=4)
    sure_bg = cv2.dilate(sure_fg, kernel, iterations=15)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, thresh = cv2.threshold(unknown, 240, 255, cv2.THRESH_BINARY)
    unknown[thresh == 255] = 128
    finaltrimap = sure_fg + unknown


    cv2.imshow('trimap', trimap)
    cv2.waitKey(0)

    alpha = knn_matte(img, trimap)
    #imageio.imwrite('donkeyAlpha.png', alpha)
    #scipy.misc.imsave('donkeyAlpha.png', alpha)
    plt.title('Alpha Matte')
    plt.imshow(alpha, cmap='gray')

    im_over = np.full(img.shape, fill_value=[0,0,0], dtype=np.float64 )
            #cv2.imshow('grgdt', im_over)
            #cv2.waitKey(0)
            #im_white = np.full(ob.shape, fill_value=[255,255,255])
    im_over[:, :, 0] =  (1-alpha) * im_over[:,:,0] + alpha * img[:, :, 0]    # white bckgnd
    im_over[:, :, 1] =  (1-alpha) * im_over[:,:,1] + alpha * img[:, :, 1]    # white bckgnd
    im_over[:, :, 2] =  (1-alpha) * im_over[:,:,2] + alpha * img[:, :, 2]
    imageio.imwrite('00046_knn.png', im_over.astype(np.uint8))

    plt.show()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import scipy.misc
    main()
