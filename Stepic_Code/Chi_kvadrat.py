from scipy.stats import chi2_contingency

import scipy


table = [[18,7],[6,13]] #загружаем исходную табличку


chi2, prob, df, expected = scipy.stats.chi2_contingency(table) #рассчитываем параметры Хи-квадрат


#вывод:


output = "test Statistics: {}\ndegrees of freedom: {}\np-value: {}\n"


print(output.format( chi2, df, prob))


print(expected)