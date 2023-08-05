# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# This file is auto-generated by substrates/meta/rewrite.py
# It will be surfaced by the build system as a symlink at:
#   `tensorflow_probability/substrates/numpy/experimental/inference_gym/targets/ground_truth/synthetic_log_gaussian_cox_process.py`
# For more info, see substrate_runfiles_symlinks in build_defs.bzl
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



# Lint as: python2, python3
# Copyright 2020 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
r"""Ground truth values for `synthetic_log_gaussian_cox_process`.

Automatically generated using the command:

```
bazel run //tools/inference_gym_ground_truth:get_ground_truth --   --target \
  synthetic_log_gaussian_cox_process \
  --stan_samples \
  50000 \
```
"""

import numpy as np

IDENTITY_AMPLITUDE_MEAN = np.array([
    0.32072022433999997,
]).reshape(())

IDENTITY_AMPLITUDE_MEAN_STANDARD_ERROR = np.array([
    3.0940358102820867e-05,
]).reshape(())

IDENTITY_AMPLITUDE_STANDARD_DEVIATION = np.array([
    0.02559753029515912,
]).reshape(())

IDENTITY_LENGTH_SCALE_MEAN = np.array([
    0.20118323845504,
]).reshape(())

IDENTITY_LENGTH_SCALE_MEAN_STANDARD_ERROR = np.array([
    0.00013817309709052925,
]).reshape(())

IDENTITY_LENGTH_SCALE_STANDARD_DEVIATION = np.array([
    0.10701400857692753,
]).reshape(())

IDENTITY_LOG_INTENSITY_MEAN = np.array([
    4.20288236326,
    4.709207094080001,
    4.62233113842,
    4.944547228639999,
    4.28999354994,
    4.39554439676,
    4.518892563640001,
    4.15161704376,
    4.74945860724,
    4.427181770020001,
    4.6141229693,
    4.6048662583599995,
    4.75778922404,
    4.4900421474600005,
    4.5865291818400005,
    4.79564131308,
    4.508236103019999,
    4.304835396380001,
    4.416794986,
    4.095037292120001,
    4.97264671832,
    4.17825554262,
    4.21719904902,
    4.37156110816,
    4.59551701196,
    4.7252760272600005,
    4.84813004802,
    4.854912794400001,
    4.406343230859999,
    5.24489042876,
    4.870945183839999,
    4.548702735040001,
    4.36177244338,
    4.17766253032,
    4.52816158328,
    4.733318624499999,
    5.052602071400001,
    4.8258750821,
    4.700472078440001,
    3.990449227399999,
    4.7337001052800005,
    4.40447427638,
    3.9581792201,
    5.0218719962,
    4.395250676120001,
    4.03439999154,
    4.3266505539399995,
    4.22946238568,
    4.034910857519999,
    4.36182705406,
    4.587829210680001,
    4.90518674516,
    4.31571661928,
    4.3955445199000005,
    4.1079588327200005,
    5.03507415382,
    4.51065169096,
    4.49872020478,
    4.78889924052,
    4.78861489722,
    4.59516177668,
    4.99802586672,
    4.8116544040800004,
    4.49050597756,
    4.339599036339999,
    3.62890155888,
    5.0161057071599995,
    4.63141923614,
    4.2147211353600005,
    4.4487148675,
    4.489757085519999,
    4.97223816018,
    4.6920652575599995,
    4.278970918920001,
    4.7486786793,
    4.78899014594,
    5.2041679068199995,
    4.70833082244,
    4.59541683122,
    4.811339776559999,
    4.4886272641,
    4.45720560652,
    4.39471775008,
    4.71724139846,
    4.42751357322,
    4.426985393039999,
    4.86267490034,
    4.16349831328,
    4.61321866986,
    5.00495364782,
    4.4160133517,
    4.79712528414,
    4.95237454752,
    4.885064734559999,
    4.519466438299999,
    4.37278476326,
    4.43848836884,
    4.42695140016,
    4.4588055957599995,
    3.8917194078999997,
]).reshape((100,))

IDENTITY_LOG_INTENSITY_MEAN_STANDARD_ERROR = np.array([
    0.00011831364250478179,
    9.483775963372658e-05,
    9.652919947341661e-05,
    8.337013132959046e-05,
    0.00011561150079562063,
    0.00010717200253882,
    0.00010195651375929193,
    0.0001205320162422976,
    9.386113705433946e-05,
    0.00010746117708222189,
    9.513196647113554e-05,
    9.788679458194594e-05,
    9.103376529463737e-05,
    0.00010326510138619498,
    9.88966852466385e-05,
    8.934004537603784e-05,
    0.00010153466095540698,
    0.00011341184864361979,
    0.00010964415651397516,
    0.00012587233046143937,
    8.054612940151116e-05,
    0.0001208952340420302,
    0.0001167726254864137,
    0.00010886175264306444,
    9.966251370592176e-05,
    9.151975387587098e-05,
    9.11956813155465e-05,
    8.806158192058707e-05,
    0.0001057966044679052,
    7.386607667819403e-05,
    8.640334021239735e-05,
    9.980389268038452e-05,
    0.00010900152016520581,
    0.00012343182503907617,
    9.896409275657552e-05,
    9.129585475941647e-05,
    7.822357383232112e-05,
    8.941742746090295e-05,
    9.276422819334156e-05,
    0.0001332885026143371,
    9.263219392419513e-05,
    0.00010691121303398835,
    0.00013319378601692032,
    8.031622848606638e-05,
    0.00010740888527632254,
    0.00012556127772572596,
    0.00011235739234055746,
    0.00011724283689932499,
    0.0001300209041111566,
    0.00011035356273550638,
    9.844139421649398e-05,
    8.529565585944775e-05,
    0.00011258795208146118,
    0.0001077154245672818,
    0.00012255879993124653,
    7.963432932840548e-05,
    0.00010345149824671217,
    0.00010385286473644432,
    9.106901844911758e-05,
    8.926194698822457e-05,
    9.844120678172515e-05,
    8.239412733449509e-05,
    8.939632403832393e-05,
    0.00010380326937392531,
    0.00011017393772468167,
    0.00015799222533737308,
    8.272167433462777e-05,
    9.599838779390758e-05,
    0.00011808183708636825,
    0.00010519763126357752,
    0.00010133537536627358,
    8.332110715962807e-05,
    9.404357584089731e-05,
    0.00011398511817799267,
    9.07019907244635e-05,
    9.053044756076378e-05,
    7.431092146436388e-05,
    9.272301371240938e-05,
    9.824480996540542e-05,
    9.036681535652437e-05,
    0.00010342078115627951,
    0.00010477490079315446,
    0.00010682360235771559,
    9.329299448876983e-05,
    0.00010669140211541223,
    0.00010695049618959563,
    8.676052428007136e-05,
    0.00011979704035683832,
    9.957144628501618e-05,
    8.420341544476581e-05,
    0.00010810136390363441,
    8.969483132833031e-05,
    8.463437664544033e-05,
    8.8071991099268e-05,
    0.00010166929387824244,
    0.00010817066970815699,
    0.00010797349137559893,
    0.00010705462630278869,
    0.00010644985890669317,
    0.0001362107992741312,
]).reshape((100,))

IDENTITY_LOG_INTENSITY_STANDARD_DEVIATION = np.array([
    0.11424020705270559,
    0.09085377890926327,
    0.0947706123941995,
    0.08171440426832924,
    0.11048535317460287,
    0.10488557130753746,
    0.09910884038099467,
    0.1166271845518286,
    0.08954562428893467,
    0.1033020945375956,
    0.09513698036249041,
    0.09545651031461784,
    0.0889270832918099,
    0.100728391015481,
    0.09617227100946373,
    0.08775279822730153,
    0.09997957787232623,
    0.10942354192370314,
    0.10425421432893842,
    0.12045558357279951,
    0.0805327613228001,
    0.11612425419280477,
    0.11346143626108722,
    0.10605810277632668,
    0.09598254820482044,
    0.09007783983873462,
    0.08565835411958048,
    0.08525677970349559,
    0.10440050505275222,
    0.07104242874714885,
    0.08437716225945378,
    0.09796366895178162,
    0.10668161094802979,
    0.11550337261218158,
    0.09869983807191436,
    0.09009157169921114,
    0.0774758040246272,
    0.08640887715868421,
    0.09128935905028154,
    0.12576266606540681,
    0.09000810503263651,
    0.10460385742479912,
    0.12751640666016478,
    0.0787373617100347,
    0.10478715461791699,
    0.12328303235109847,
    0.10824888714818304,
    0.11278854995824572,
    0.123028417098343,
    0.10625643957760271,
    0.09617433994566642,
    0.08301524961248957,
    0.10868153064048662,
    0.10480672163920438,
    0.11927463999899772,
    0.07817361179600364,
    0.09948059241956109,
    0.09983189096232159,
    0.08771703093072358,
    0.08801831245676447,
    0.09550957350676731,
    0.079605667256235,
    0.0870772291434278,
    0.10040190863606638,
    0.10751864015761466,
    0.1483202197391365,
    0.07894990560715888,
    0.09412742169667297,
    0.11385550450939112,
    0.10243752435117108,
    0.10043828859229889,
    0.0805492885380644,
    0.09163621755849682,
    0.11044100338114146,
    0.08949303963019738,
    0.08742857162093777,
    0.07224612516024854,
    0.09105574660435421,
    0.09578126932155098,
    0.08692790820696102,
    0.10047043025126168,
    0.10207485577579226,
    0.10468509923494321,
    0.0905762209706072,
    0.10331366001794706,
    0.10290507393831791,
    0.0848145019712843,
    0.116371337143016,
    0.095036183094068,
    0.07945625086263128,
    0.10388664326396169,
    0.08727670168391258,
    0.0813069994143018,
    0.08392577614306619,
    0.09922177289150036,
    0.10603680577138772,
    0.10277141438928934,
    0.10364978592149432,
    0.10202619870199639,
    0.13152269243637876,
]).reshape((100,))

