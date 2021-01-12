from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from numpy import concatenate
import pandas as pd
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping
from sklearn import preprocessing
import re


def rename(df, emptyColumns, dfName):
    """
    Renames header of the specified df, if it contains columns that are contained in the emptyColumns list, which
    contains lists of countries with their missing indicators (from the full list of indicators: indicatorsDFNames) of
    format: <country>, <indicator>.

    :param df: the datafrmae specified
    :param emptyColumns: the list with the countries,and their missing indicators(from the full list of indicators)
    :param dfName: the df's name/title from the list of df names (indicator or country), in order to check if is in the
    emptyColumns list
    :return: the transformed/renamed df
    """
    header = [x for x in df.columns]
    for row in emptyColumns:
        if row[0] in df.columns and dfName == row[1] :
            header.remove(row[0])
        elif row[1] in df.columns and dfName == row[0]:
            header.remove(row[1])
    df.columns = header
    return df


def scale(df):
    """
    Scales the dataframe specifyied to range (0,1), after dropping columns with only NaN values

    :param df: datafrmame to be scaled
    :return: scaled dataframe, scaler used, list with df columns with only NaN values
    """
    flag = False
    temp_col = None
    # save temporarily the date column
    if 'date' in df.columns:
        flag = True
        temp_col = df['date']
    # remove any column that contains the word 'date', as dates cannot be scaled
    if any(re.match(".*date.*", x) for x in df.columns):
        # drop columns that contain the word date(e.g. date,  date(t+1))
        df = df[[x for x in df.columns if x.lower()[:4] != 'date']]

    # drop nan columns
    df = df.dropna(how='all', axis=1)
    # save the columns and the index, to be assigned after scaling
    idx = df.index
    header = df.columns
    # drops the date index
    df = df.reset_index(drop=True)
    # returns a numpy array
    x = df.values

    # ensure all data is float
    x = x.astype('float64')

    # scale the dataframe to range (0,1)
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    x_scaled = min_max_scaler.fit_transform(x)
    # add the removed 'date' column
    df_scaled = pd.DataFrame(x_scaled, index=idx, columns=header)
    if flag:
        df_date = pd.DataFrame(temp_col)
        df_scaled = pd.concat([df_date, df_scaled], axis=1)
    return df_scaled, min_max_scaler


# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True, columns_list=None):
    """
    Transform dataframe, containing columns/time-series to a format that enables supervised learning to Machine Learnning
    algorithms. For example, if there is one column with values ranging (1,10), it will create two columns <(t-1)> <(t)>,
    with <t-1> column, containing values (1 to 10) and and <t> column values (2 to 10, with last row empty). In that way
    column <t-1> is the X column and <t> is the y column, if we use supervised learning.

    :param data: df to be transformed
    :param n_in: times, that are going to be used for X variable (e.g. with n_in=2, df will has columns <t-2> <t-1>)
    :param n_out: time, that are going to be usef for y variable (e.g. with n_out=2, df will has columns <t> <t+1>)
    :param dropnan: Boolean value, specifying if there are going to be drop columns with NaN values
    :param columns_list: list containing the desired df's columns/names, combined with each <time> (...,t-1,t,t+1,...)
    :return: dataframe transformed to format, that enables supervised learning
    """
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('%s(t-%d)' % (j, i)) for j in columns_list]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('%s(t)' % (j)) for j in columns_list]
        else:
            names += [('%s(t+%d)' % (j, i)) for j in columns_list]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


def forecast(df, forecasting_column=None, n_in=1, n_out=1):
    """
    Predicts/forcasts time series data. First plots the time series containing inside the defined dataframe, then
    reformats (reframes) the dataframe to format: index: numbers(int), header: var1(t-1), var2(t-1), var1(t), var2(t),
    where var1,var2 are columns/time-series from the defined df (may be more or less), and parameter 't' is the
    method/way to transform time series dataframe to supervised learnning dataframe. One 'time' is used for prediction:
    (t or above) and evaluation (meaning: hiding the (t or above) column, predicting and compare the predicted results
    with the real) The 'time' (t-1) or below that, are used for learning the Machine Learning Algorithm, here LSTM
    (Long Short-term memory) Neural Networks.

    :param df: dataframe containing time series.Format: index: dates, header: countries/indicators or anything else
    'indicatorDFNames', returned from function mergeDFs
    :param forecasting_column: the column, that is going to be forecasted
    :param n_in: the number of times (e.g. for 3: t-1,t-2,t-3) which will be used for learning
    :param n_out: the number of times (e.g. for 2: t,t+1) which will be predicted/forecasted.
    :param evaluation: Boolean value specifying if fuction is going to predict new values, or predict hidden values in
    order to evaluate the learning method(practicaly if the data is going to be splitted in train_X,test_X,
    train_y,test_y, so that it can evaluate the model's prediction with the true values).

    :return: None if used for evaluation (pamam: evaluation =True), or else forecasting column updated with the
    insertion of the predicgted values
    """

    # drop columns wich have  NaN values
    df = df.dropna(axis=1)

    # call fuction to rename header/columns
    #df = rename(df, emptyColumns, dfName)
    # save the dataframe's last date (so that we could know what is the next, which will be predicted)
    last_date = df.index[len(df.index)-1]
    # if column selected for forecasting isn't inside the df's columns, inform and exit/return to previous state
    if forecasting_column not in [x for x in df.columns]:
        print("\n\nNo such column:"+forecasting_column+", in current dataframe: ", [x for x in df.columns])
        return np.nan, np.nan

    # frame the df to format for supervised learning
    reframed = series_to_supervised(df, n_in, n_out, columns_list=[x for x in df.columns])

    # drop columns we don't want to predict
    dropList = []
    # for columns from current 'time' (t) and above
    for col in reframed.columns[len(df.columns):len(df.columns)*(int(n_in)+int(n_out))]:
        if n_out == 1:  # if forecasting current 'time'(t)-it is used for evaluation of the learning method
            # save to list,all the current 'time' (t) columns,except the forecasting column's,
            # so that they can be dropped
            if col != forecasting_column+'(t)':
                dropList.append(col)    #
        else:   # if forecasting times (t+1) and later,-it is used for predicted unknown values
            # save to a list forecasting future times: (t+1) and above, for the forecasting column,
            # so that they aren't going to be deleted
            predict_times = [forecasting_column+'(t+'+str(x)+')' for x in range(1,n_out)]
            # add to the list  all the current 'time':(t) columns in the list,
            # so that they aren't going to be deleted either
            predict_times.extend([x+'(t)' for x in [y for y in df.columns]])
            # save to drop_list, all the df's columns except those saved in previous list:predict_list
            if col not in predict_times:
                dropList.append(col)
    # drop the columns saved on the drop list
    reframed.drop(dropList, axis=1, inplace=True)

    # temporary save the df's header and index
    header = [x for x in reframed.columns]
    idx = [x for x in reframed.index]

    # call the function to scale the df into range(0,1)
    scaledReframed, scaler = scale(reframed)

    # rename the df's header and index, with the names they had before scaling
    scaledReframed.index = idx
    scaledReframed.columns = header

    if n_out == 1 : # if last 'time' is (t)
        n_out +=1 # so that the 'start' var in next loop doesn't go to zero

    count = 1
    # for each of the times [(t) and above], of the columns that are going to be forecasted, learn lstm NN with the
    # other columns, except the current, and forecast the current
    for n in scaledReframed.iloc[:, -(n_out-1):]:
        # name X, the dataframe slice of columns different of the one that is going to be predicted and y the remaining
        y = scaledReframed[n]  # class labels
        Xcolumns = [x for x in scaledReframed if x != n]
        X = scaledReframed.loc[:, Xcolumns]  # all features

        # if function is used for evaluaing the learning method,hiding the class label,predicting it, and compute the
        # distance (here RSME), from the actual data
        # save to numpy array
        Xval = X.values
        yval = y.values
        # reshape input to be 3D [samples, timesteps, features]
        Xval = Xval.reshape((Xval.shape[0], 1, Xval.shape[1]))

        # design network
        model = Sequential()
        model.add(LSTM(40, input_shape=(Xval.shape[1], Xval.shape[2])))
        # model.add(Dropout(0, 2))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        batch_size = int(len(scaledReframed.index)*0.7)   # use 70% of rows-samples as batch-size

        # fit network
        history = model.fit(Xval, yval, epochs=50, batch_size=batch_size, validation_split=0.2,
                            callbacks=[EarlyStopping(monitor='val_loss', patience=10)], verbose=2, shuffle=False)
        # Training Phase
        # model.summary()

        # select last line of X,y data, in order to make the prediction of y, from the values of X
        ypred = y[len(y)-1]
        Xpred = pd.DataFrame(X.iloc[-1, :])
        Xpred = Xpred.transpose()

        # make a prediction
        Xpred = Xpred.values
        Xpred = Xpred.reshape((Xpred.shape[0], 1, Xpred.shape[1]))
        yhat = model.predict(Xpred)

        # reshape for inverting scaling
        Xpred = Xpred.reshape((Xpred.shape[0], Xpred.shape[2]))
        # invert scaling for forecast columns/values
        inv_yhat = concatenate((Xpred, yhat), axis=1)
        inv_yhat = scaler.inverse_transform(inv_yhat)
        predicted_value = inv_yhat[0][-1]

        # create a dataframe of zero-containing matrix, in order to save X,y,which used in prediction
        matrix = np.zeros(shape=(1, len(df.columns)), dtype=float)
        pred_df = pd.DataFrame(matrix, columns=[x for x in df.columns])

        # use as index, for the previously created df, the last date of the given df,added by one year
        new_df_idx = [str(int(str(last_date).split('-')[0])+count)+'-01-01']
        count += 1
        pred_df.index = new_df_idx
        # append the, previously created df, to the given (initial) df
        df = df.append(pred_df)
        # assign to the initial df, the predicted value
        df.at[new_df_idx, forecasting_column] = predicted_value
        del new_df_idx, predicted_value, matrix, pred_df, inv_yhat, yhat, history, model, Xval, yval

        print('\nforecast')
        print(df[forecasting_column])

        # return the forecasting column, updated with the insertion of the predicted value
        return df[forecasting_column]


def pre_predict(df, nans_values, col):
    """
    Iterates through the rows of the df containing nan values and implements forecasting, to the columns
    containing the nan values.

    :param df: the df to be predicted
    :param nans_values: the number of nans existing in the specific column
    :param col: the specific column to be forecasted
    :return: the forecasted df
    """
    for i in range(nans_values):
        df[col] = forecast(df=df.iloc[:-nans_values + i, :], forecasting_column=col)

    return df


def predict(df):
    """
    Iterates through the dataframe columns and conducts a one-step forecasting, adding one row to the df

    :param df: the dataframe to be forecasted
    :return: the df having an extra row of the forecasted values
    """
    temp_col = None

    # temporarily save the date column, before deleting it
    if 'date' in df.columns:
        df.index = df['date']
        temp_col = df['date']
        temp_year = df['date'][len(df['date'])-1].split('-')[0]
        add_year = str(int(temp_year)+1)+'-01-01'
        add_row = pd.Series(add_year, index=[add_year])
        add_row.name = 'date'
        temp_col = pd.concat([temp_col, add_row], axis=0)
        df = df[[x for x in df.columns if x != 'date']]

    new_df = pd.DataFrame(temp_col)
    # implement the one-step forecasting
    for col in df:
        new_df[col] = forecast(df=df, forecasting_column=col)

    return new_df
