import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from scipy.signal import savgol_filter as sgf
from sklearn.feature_selection import SelectKBest, chi2, f_classif

class KLDivergence():
    def __init__(self, k=10):
        self.k = k

    def fit(self, X, y=None):
        """Compute the mean and std to be used for later scaling.
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape [n_samples, n_features]
            The data used to compute the mean and standard deviation
            used for later scaling along the features axis.
        y
            Ignored
        """

        # Reset internal state before fitting

        return self.kl_fit(X, y)

    def kl_fit(self, X, y):

        y_unique = list(np.unique(y))
        features_list = np.linspace(0, X.shape[1] - 1, X.shape[1]).astype("int")
        X_1 = X[y == y_unique[0]]
        X_2 = X[y == y_unique[1]]
        x_1_mean = np.mean(X_1, axis=0)
        x_2_mean = np.mean(X_2, axis=0)

        p = abs(x_1_mean)
        q = abs(x_2_mean)
        sid_p = list(p[i] * np.log2(p[i] / q[i]) for i in range(len(p)))
        sid_q = list(q[i] * np.log2(q[i] / p[i]) for i in range(len(p)))

        mean_KL = list(0.5 * (sid_p[_] + sid_q[_]) for _ in range(len(sid_p)))
        results = pd.DataFrame(features_list, columns=["features_index"])
        results["mean_KL_divregence"] = mean_KL
        self.results_sorted = results.sort_values(by="mean_KL_divregence", ascending=False)

        if self.k == "all":
            self.best_feat = self.results_sorted["features_index"]

        else:
            self.best_feat = self.results_sorted["features_index"].iloc[:self.k]

        return self

    def transform(self, X):
        """Perform standardization by centering and scaling
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data used to scale along the features axis.

        """

        X = X[:, self.best_feat.index]

        return X

    def set_params(self, **params):
        """
        Set the parameters of this estimator.
        The method works on simple estimators as well as on nested objects
        (such as pipelines). The latter have parameters of the form
        ``<component>__<parameter>`` so that it's possible to update each
        component of a nested object.
        Parameters
        ----------
        **params : dict
            Estimator parameters.
        Returns
        -------
        self : object
            Estimator instance.
        """

        return self

    def fit_transform(self, X, y=None, **fit_params):
        """
        Fit to data, then transform it.
        Fits transformer to X and y with optional parameters fit_params
        and returns a transformed version of X.
        Parameters
        ----------
        X : numpy array of shape [n_samples, n_features]
            Training set.
        y : numpy array of shape [n_samples]
            Target values.
        **fit_params : dict
            Additional fit parameters.
        Returns
        -------
        X_new : numpy array of shape [n_samples, n_features_new]
            Transformed array.
        """
        # non-optimized default implementation; override when a better
        # method is possible for a given clustering algorithm
        if y is None:
            # fit method of arity 1 (unsupervised transformation)
            return self.fit(X, **fit_params).transform(X)
        else:
            # fit method of arity 2 (supervised transformation)
            return self.fit(X, y, **fit_params).transform(X)



class SpectraPrapering:

    def __init__(self, X):
        self.X = X

    def spectra_normalization(self, plot=False):
        df = pd.DataFrame(self.X.T)
        df = df.apply(lambda v: v / ((v ** 2).sum()) ** 0.5)
        df = df.apply(lambda v: v / v.max())
        self.X_norm = df.T.values

        if plot:
            fig, (ax1, ax2) = plt.subplots(2)
            ax1.plot(self.X.T)
            ax1.set_title("Original")
            ax2.plot(self.X_norm.T)
            ax2.set_title("Normalized")
            plt.show()
        return self.X_norm



def derivative(X, deriv=2, window_length=13, polyorder=3):
                X_dev = sgf(X,
                 window_length=window_length,
                 polyorder=polyorder,
                 deriv=deriv,
                 delta=1.0,
                 axis=1,
                 mode='nearest')
                return X_dev


def sticking_imges(imgs_list, sorting="horizontal", show_out_ph=True, resize_tuple="none", save=False, out_name_end_type="out.tif", out_type="tiff",
                   dpi=600):
    """

    :param imgs_list: list contain the location of the images (list of strings)
    :param sorting: defoalt "horizontal" and can change to "vertical" (string)
    :param show_out_ph:  do you want to see the final image? True or False (boolean)
    :param resize_tuple: new size (tuple)
    :param save: do you want to save the final image? True or False (boolean)
    :param out_name_end_type: the name or location of the final image in order to save (string)
    :param out_type: type of tinal image, defoal is "tiff" (string)
    :param dpi: 300, 600, 1200 (integer)
    :return: sticking images
    """
    numpyes = []
    intinal_sizes = np.zeros((len(imgs_list), 2))
    for im in imgs_list:
        if resize_tuple == "none":
            img = Image.open(im)
        else:
            img = Image.open(im).resize(resize_tuple, Image.ANTIALIAS)

        numpyes.append(np.array(img))

    if sorting == "horizontal":
        im_out = Image.fromarray(np.hstack(tuple(numpyes)))



    elif sorting == "vertical":
        im_out = Image.fromarray(np.vstack(tuple(numpyes)))

    if show_out_ph:
        im_out.show()

    if save:
        if out_type == "tiff":
            im_out.save(out_name_end_type,
                        compression='tiff_lzw',
                        dpi=(dpi, dpi),
                        optimize=True,
                        )
        else:
            im_out.save(out_name_end_type,
                        dpi=(dpi, dpi))


def image_resizing_ratio(init_location, final_location, percent, dpi=300):
    """
    Resize image input image and percent | Keep aspect ratio
    :param init_location:
    :param final_location:
    :param percent:
    :return:
    """
    img = Image.open(init_location)
    w, h = img.size
    img_resized = img.resize((int(float(percent*w)/float(100)),int(float(percent*h)/float(100))))
    img_resized.show()
    img_resized.save(final_location, dpi=(dpi, dpi))


def references_comparing_for_papers_edit(text_file_location):
    """
    This function checking if there are duplicate references in papers.
    Copy the refernces from the paper "with the numbers" and paste it in Notepad text file
    then write in a new first row the word "title".
    :param text_file_location:  Notepad text file location
    :return: report (pandas df)
    """
    df = pd.read_fwf(text_file_location).drop("Unnamed: 1", axis=1)
    X = df["title"].values.astype(str)
    df_ = pd.DataFrame(X, columns=["ref"])
    string_list = list(df_["ref"].apply(lambda _: _[_.find("\t") + 1:]))
    vectroized = CountVectorizer().fit_transform(string_list)
    vectors = vectroized.toarray()
    csim = cosine_similarity(vectors)
    similarity = np.around(csim[(csim > .70) & (csim < .95)] * 100, 0).astype(int)
    similarity = similarity[: int(0.5 * len(similarity))]
    v = np.argwhere((csim > .70) & (csim < .95))
    v = v[: int(0.5 * len(v))]
    df_out = pd.DataFrame()
    df_out["references_1_num"] = (v[:, 0] + 1)
    df_out["references_2_num"] = (v[:, 1] + 1)
    df_out["reference_text_1"] = df_out["references_1_num"].apply(lambda _: string_list[_ - 1])
    df_out["reference_text_2"] = df_out["references_2_num"].apply(lambda _: string_list[_ - 1])
    df_out["similarity %"] = similarity

    return df_out


class SqlImportCsv:
    def __init__(self, df, file_location, table_name="table"):
        """
        This class convert CSV files into SQL tables
        :param df: data frame (pandas)
        :param file_location: file location spuse to be inside the major folder that you defined in SQL (string)
        :param table_name: name of the table that you want to create (string)
        """
        self.df = df
        self.file_location = file_location
        self.table_name = table_name

    def praper_sql_table(self):
        qu = "CREATE TABLE public." + self.table_name + "("
        headers = "("
        self.columns = self.df.columns.values.astype(str)
        for ty in (self.columns):
            if (self.df[ty].dtype == "float64") | (self.df[ty].dtype == "int64"):

                typ = "NUMERIC"
            elif self.df[ty].dtype == "object":
                typ = "TEXT"
            else:
                typ = "OBJECT"

            q = "%s %s, \n" % (ty, typ)
            headers = headers + ty + ","
            qu = qu + q

        qu = qu + ");"
        self.qu = qu[:-5] + qu[-4:]
        self.headers = headers[:-1] + ")"
        print(qu)

    def import_file(self):

        import_ = "COPY %s %s\nFROM '%s' DELIMITER ',' CSV HEADER;" % (self.table_name, self.headers, self.file_location)
        self.import_ = import_

        self.praper_import = "%s\n%s" % (self.qu, self.import_)

        print(self.praper_import)


def feature_selection(X, y, k=10, type_of_tech="f_classif", offset=True):
    """

    :param X:numpy array of shape [n_samples, n_features]
            Training set.
    :param y:numpy array of shape [n_samples]
            Target values.
    :param k: number of features after selection (integer)
    :param type_of_tech:
    :param offset: shifted the the data, where the minimum value will be zero (boolean)
    :return: X with the selected values
    """
    if offset:
        X = X + abs(np.min(X))

    if (type_of_tech == "chi2") | (type_of_tech == "f_classif"):
        X_select = SelectKBest(score_func=eval(type_of_tech), k=k).fit_transform(X, y)
    elif (type_of_tech == "KL"):
        X_select = KLDivergence(k=k).fit_transform(X, y)

    return X_select


def expand_data(X, y, weights=None, n_new_samples=100, random_state=None):
    """

    :param X:  {array-like, sparse matrix} of shape (n_samples, n_features)
               Training data
    :param y:array-like of shape (n_samples,)
    :param weights: list of whigtes for each class. If None, the function takes weights based on input data
    :param n_new_samples: number of the new samples (integer)
    :param random_state: seed
    :return: X, y of expanded data
    """

    if random_state == None:
        pass
    else:
        np.random.seed(random_state)
    unq = np.unique(y)

    X_new = np.zeros((1, X.shape[1]))
    y_new = np.zeros(1)

    for ix, u in enumerate(unq):
        cov = np.cov(X[y == u].T)
        mean = np.mean(X[y == u], axis=0)
        if weights == None:
            n_rate = len(y[y == u]) / len(y)
        else:
            n_rate = weights[ix]
        y_ = np.array([u for _ in range(int(n_rate * n_new_samples))])
        y_new = np.concatenate((y_new, y_))

        X_ = np.random.multivariate_normal(mean, cov, int(n_rate * n_new_samples))
        X_new = np.concatenate((X_new, X_))

    return X_new, y_new


def blanced_data(X, y, random_state=10):
    """
    This function balances the data (binary) according to the small class
    :param X: numpy array of shape [n_samples, n_features].
    :param y: numpy array of shape [n_samples]
              Target values.
    :return: blanced data (X,y)

    """
    np.random.seed(random_state)
    X_0 = X[y == 0]
    X_1 = X[y == 1]

    y_0 = y[y == 0]
    y_1 = y[y == 1]
    if X_0.shape[0] > X_1.shape[0]:
        np.random.shuffle(X_0)
        X_0 = X_0[:len(X_1)]
        y_0 = y[y == 0][:len(X_1)]
    else:
        np.random.shuffle(X_1)
        X_1 = X_1[:len(X_0)]
        y_1 = y[y == 1][:len(X_0)]

    da_0 = pd.concat([pd.DataFrame(X_0), pd.DataFrame(y_0)], axis=1)
    da_1 = pd.concat([pd.DataFrame(X_1), pd.DataFrame(y_1)], axis=1)

    data = np.concatenate((da_0.values, da_1.values), axis=0)
    np.random.shuffle(data)

    X = data[:, :-1]
    y = data[:, -1]

    return X, y.astype("int")


def mean_stb_data(X, beta=0.5):
    """
    This function calculate the confidence interval
    :param X: data (type: numpy array)
    :param beta: the width of the interval (type: float)
    :return: new data with mean, up_interval and low_interval
    """
    X_mean = X.mean()
    X_std = X.std()
    X_up = X_mean + beta * X_std
    X_low = X_mean - beta * X_std

    df = pd.DataFrame(X_mean, columns=["mean"])
    df["std"] = X_std
    df["X_up"] = X_up
    df["X_low"] = X_low

    return df, X_mean.values, X_up.values, X_low.values


def spectra_plot(df,
                 label,
                 initial_feature="1801.264",
                 final_feature="898.703",
                 out_window_size_tuple_x=(900, 1800),
                 out_window_size_tuple_y=(-0.003, 0.255),
                 inset_axis=True,
                 inset_window_position=[0.02, 0.43, 0.75, 0.54],
                 labels_dict=[{"label": "S", "label_legend": "label_1", "color": "blue"}, {"label": "R", "label_legend": "label_2", "color": "red"}],
                 confidence_iterval_width=0.5,
                 texts_on_graph_dict=[{"which_axis": "ax2", "text_sentence": "ER", "position_x": 1000, "position_y": 0.025}],
                 functional_groups=True,
                 functional_groups_dict=[{"group_name": 'Amid III', "arrow_position": (1241, 0.028), "xytext": (1241, 0.05)},
                                         {"group_name": 'as CH' + r"$_3$", "arrow_position": (1456, 0.018), "xytext": (1456 - 8, 0.045)},
                                         {"group_name": 'Amid II', "arrow_position": (1548, 0.12), "xytext": (1548 - 27, 0.16)},
                                         {"group_name": 'Amid I', "arrow_position": (1659, 0.232), "xytext": (1659 - 25, 0.245)},
                                         {"group_name": "sym CCO" + r"$^-$", "arrow_position": (1400, 0.02), "xytext": (1400, 0.058)}],
                 inset_control_x=(958, 1180),
                 inset_control_y=(0, 0.1),
                 legend_location=2,
                 graph_item="none",
                 save_fig=False,
                 y_title="Absorbance (A.U)",
                 x_title="Wavenumber (cm" + r"$^{-1})$",
                 file_name="spectra"):
    """

    :param df: data frame (type: pandas df)
    :param label: name of column of the labels (type: string)
    :param initial_feature: first column name (type: string)
    :param final_feature: last column name(type: string)
    :param inset_axis: insert inset_axis as small window, True or Falst (type: boolean)
    :param inset_window_position: the limits of the inset window on respect to the major window (type: list of floats)
    :param labels_dict: list of dictionaries include the details about the classes (type: list of dictionaries)
    :param confidence_iterval_width: the width of the confidence interval (type: float)
    :param texts_on_graph_dict: list of dictionaries include the details about texts on the graph (type: list of dictionaries)
    :param functional_groups: insert functional groups as text-arrows, True or Falst (type: boolean)
    :param functional_groups_dict: list of dictionaries include the details about vibration functional groups (type: list of dictionaries)
    :param inset_control_x: tuning the x-axis limtis inside the inset-window (type: tuple)
    :param inset_control_y: tuning the y-axis limtis inside the inset-window (type: tuple)
    :param legend_location: legend location on the window (type: integer)
    :param graph_item: item for the figure, default "none" dont add any thing (type: string)
    :param save_fig: do you want to save the figure?, True or Falst (type: boolean)
    :param y_title: title of the y-axis (type: string)
    :param x_title: title of the x-axis (type: string)
    :param file_name: name of the file in case of saving the figure in file (type: strring)

    :return: show the spectra figure
    """
    wavenumbers = df.loc[:, initial_feature: final_feature].columns.values.astype("float")
    X = df.loc[:, initial_feature: final_feature]
    y = df[label]

    df_sub = pd.concat([X, y], axis=1)
    df_sub = df_sub.dropna()

    plt.rc("font", size=16, family="Times New Roman")
    plt.rc('axes', linewidth=2)
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_axes([0, 0, 1, 1])

    if inset_axis:
        ax2 = fig.add_axes(inset_window_position)
        ax2.set_yticks([])
        for lab_indx in range(len(labels_dict)):
            spectra = df_sub[df_sub[label] == labels_dict[lab_indx]["label"]]
            spectra = pd.DataFrame(spectra.drop(label, axis=1).values.astype("float"))
            _, spec_mean, spec_up, spec_low = mean_stb_data(spectra, beta=confidence_iterval_width)
            ax1.plot(wavenumbers, spec_mean, color=labels_dict[lab_indx]["color"])
            ax1.fill_between(wavenumbers, spec_up, spec_low, color=labels_dict[lab_indx]["color"], alpha=0.1)

            ax2.plot(wavenumbers, spec_mean, color=labels_dict[lab_indx]["color"], label=labels_dict[lab_indx]["label_legend"])
            ax2.fill_between(wavenumbers, spec_up, spec_low, color=labels_dict[lab_indx]["color"], alpha=0.1)

            ax2.set_xlim(inset_control_x)
            ax2.tick_params(axis='x', which='major', labelsize=12)
            ax2.set_ylim(inset_control_y)



    else:
        for lab_indx in range(len(labels_dict)):
            spectra = df_sub[df_sub[label] == labels_dict[lab_indx]["label"]]
            spectra = pd.DataFrame(spectra.drop(label, axis=1).values.astype("float"))
            _, spec_mean, spec_up, spec_low = mean_stb_data(spectra, beta=confidence_iterval_width)
            ax1.plot(wavenumbers, spec_mean, color=labels_dict[lab_indx]["color"], label=labels_dict[lab_indx]["label_legend"])
            ax1.fill_between(wavenumbers, spec_up, spec_low, color=labels_dict[lab_indx]["color"], alpha=0.1)

    if functional_groups:
        for gr in functional_groups_dict:
            ax1.annotate(gr["group_name"], xy=gr["arrow_position"], xytext=gr["xytext"],
                         arrowprops=dict(facecolor='black', shrink=0.05, width=2))

    ax1.set_xlabel(x_title, fontdict=dict(size=23, fontname="Times New Roman", fontweight='bold'))
    ax1.set_ylabel(y_title, fontdict=dict(size=23, fontname="Times New Roman", fontweight='bold'))
    ax1.set_xlim(out_window_size_tuple_x)
    ax1.set_ylim(out_window_size_tuple_y)
    ax1.tick_params(axis='both', which='major', labelsize=16)

    for tex in texts_on_graph_dict:
        if tex["which_axis"] == "ax2":
            ax2.text(tex["position_x"], tex["position_y"], s=tex["text_sentence"], fontdict=dict(size=22, fontname="Times New Roman"))
            ax2.legend(loc=legend_location, ncol=1)
        elif tex["which_axis"] == "ax1":
            ax1.text(tex["position_x"], tex["position_y"], s=tex["text_sentence"], fontdict=dict(size=22, fontname="Times New Roman"))
            ax1.legend(loc=legend_location, ncol=1)

    if graph_item != "none":
        ax1.text(1755, 0.23, s="(" + graph_item + ")", fontdict=dict(size=25, fontname="Times New Roman", fontweight="bold"))

    if save_fig:
        fig.savefig(file_name + texts_on_graph_dict[0]["text_sentence"] + ".tif", dpi=600, bbox_inches='tight',
                    pil_kwargs={"compression": "tiff_lzw"})


def plot_pie_chart(y, classes_present_symbol=["class_A", "class_B"], classes=[0, 1], chatr_title="Pie_Chart", legend_loc=1):
    """

    :param y: labels array (type: numpy array)
    :param classes_present_symbol: list of  labels present names (type: list of strings)
    :param classes: list of the labels symbol as in the array (type: list of integers)
    :param chatr_title: title of the chart (type: string)
    :param legend_loc: legend location (type: integer)
    :return: plot pie-chart
    """
    labels = []
    class_quantity = []
    for c in range(len(classes)):
        class_quantity.append(np.sum(y == classes[c]))
        labels.append(classes_present_symbol[c] + "  %d" % (class_quantity[c]))

    plt.rc("font", size=16, family="Times New Roman")
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.pie(class_quantity, autopct='%1.0f%%', shadow=True, textprops={"color": "w", "weight": "bold", "size": 21})
    ax1.axis('equal')
    plt.legend(labels, bbox_to_anchor=(0.6, 1.2), loc=legend_loc)
    plt.tight_layout()
    plt.xlabel(chatr_title, fontdict={"size": 24, "weight": "bold"})
    plt.show()


