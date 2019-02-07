import numpy as np
import statsmodels.api as sm
import itertools


#時系列データ:DATA, パラメータs(周期):sを入力すると、最も良いパラメーターとそのBICを出力
def selectparameter(DATA,s):
    p = d = q = range(0, 1)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    parameters = []
    BICs = np.array([])
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(DATA,
                                            order=param,
                seasonal_order=param_seasonal)
                results = mod.fit()
                parameters.append([param, param_seasonal, results.bic])
                BICs = np.append(y,results.bic)
            except:
                continue
    return print(parameters[np.argmin(BICs)])
