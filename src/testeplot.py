import numpy as np
import matplotlib.pyplot as plt

second_Si = [
[np.nan,-4.24267685e-15,-4.18744586e-15,-4.11649881e-15,-4.18282091e-15,-4.24236446e-15,-4.18977055e-15,-4.09654949e-15,1.66533454e-15,-3.78863607e-15,-4.24566117e-15,-2.77555756e-15,-3.35842465e-15,1.11022302e-16,-4.23799237e-15]
[np.nan,np.nan,1.49027439e-09,1.48962540e-09
,1.49027421e-09,1.49027415e-09,1.49027661e-09,1.48948508e-09
,1.37272660e-09,1.48348757e-09,1.49027415e-09,1.46058846e-09
,1.47177212e-09,1.40268774e-09,1.49027416e-09]
[np.nan,np.nan,np.nan,8.91204766e-07
,8.88612788e-07,8.88612788e-07,8.88603042e-07,8.91765669e-07
,1.35826477e-06,9.15728091e-07,8.88612989e-07,1.00721957e-06
,9.62536268e-07,1.23855768e-06,8.88612788e-07]
[np.nan,np.nan,np.nan,np.nan
,-2.64612327e-03,-2.64612327e-03,-2.64607798e-03,-2.66077347e-03
,-4.82841137e-03,-2.77211742e-03,-2.64612420e-03,-3.19724233e-03
,-2.98961661e-03,-4.27217959e-03,-2.64612327e-03]
[np.nan,np.nan,np.nan,np.nan
,np.nan,8.91429272e-15,8.96688729e-15,9.06046072e-15
,1.69864123e-14,9.36750677e-15,8.91099598e-15,1.09356968e-14
,1.01585407e-14,1.48769885e-14,8.91866480e-15]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,7.01269111e-10,7.03830754e-10
,1.08169684e-09,7.23240447e-10,7.01277180e-10,7.97348937e-10
,7.61155194e-10,9.84733628e-10,7.01277003e-10]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,1.00236676e-06
,1.73657430e-05,1.84289598e-06,8.91780276e-07,5.05213995e-06
,3.48478511e-06,1.31667807e-05,8.91773237e-07]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,-5.38427590e-03,1.93442585e-03,2.38285725e-03,4.21333603e-04
,1.16030904e-03,-3.40455189e-03,2.38286057e-03]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,-6.99619135e-02,-2.30839993e-02,-2.28136849e-01
,-1.50886178e-01,-6.28085491e-01,-2.30836524e-02]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,-1.20620566e-03,-1.30740765e-02
,-8.60302923e-03,-3.62219570e-02,-1.20618558e-03]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,-2.93598446e-07
,-2.82727385e-07,-3.49881013e-07,-2.64742440e-07]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,-3.55067259e-02,-1.57647119e-01,-2.79534057e-03]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,-9.04784753e-02,2.25676626e-02]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,-2.54843459e-02]
[np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan,np.nan
,np.nan,np.nan,np.nan]]



plt.imshow(second_Si, cmap='viridis')
plt.colorbar()
plt.show()

filename = 'sobol_analysis_IL6_second.png'
plt.savefig(filename)