from Experiment.SurrogateModel import *

from Settings.CustomSettings import *
from Settings.BinPackingSettings import *
from Settings.LocalSearchSettings import *
from Settings.SurrogateModelSettings import *

# INITIALIZE
customSettings, localSearchSettings, surrogateModelSettings, binPackingSettings = \
    CustomSettings(), LocalSearchSettings(), SurrogateModelSettings(), BinPackingSettings()


#### DIT WAS EERST DE HELE MAIN CLASS
customSettings, localSearchSettings, surrogateModelSettings, binPackingSettings = \
    CustomSettings(), LocalSearchSettings(), SurrogateModelSettings(), BinPackingSettings()

if surrogateModelSettings.BO:
    surrogateModel = BayesianSurrogateModel(surrogateModelSettings, localSearchSettings,
                                            customSettings, binPackingSettings).solve(surrogateModelSettings)

# if surrogateModelSettings.hyperOpt:
#     surrogateModel = HyperoptSurrogateModel(surrogateModelSettings, localSearchSettings,
#                                             customSettings, binPackingSettings)
#


# NO SURROGATE: JUST LOCAL SEARCH ON BIN PACKING
# binpackingBatch = BinPackingBatchCustom(binPackingSettings)
# solver = LocalSearch2(localSearchSettings)
# solver.setInitialWeights(localSearchSettings) # will not be updated by variable weights
# for i in range(binPackingSettings.batchSize):
#     solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)




# GROTE LOOP OM ALLE RESULTATEN SNEL TE FIXEN.
# numberInstances = 1000
#
# # Excelrow van tabblad 'resultaten_test_5runs' linksboven
# for excelRow in range(2,17):
#
#     # initialize:
#     RUNVERSIONA = False
#     RUNVERSIONB = False
#     if excelRow == 2:
#         searchSpace_dict = {
#             'w1': (4.507, 4.5071),
#             'w3': (-0.244, -0.2439)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = True
#     elif excelRow == 3:
#         searchSpace_dict = {
#             'w1': (-2.11, -2.109),
#             'w3': (-2.681, -2.6809)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = False
#     elif excelRow == 4:
#         searchSpace_dict = {
#             'w1': (4.274, 4.2741),
#             'w3': (2.232, 2.2321)
#         }
#         RUNVERSIONA = False
#         RUNVERSIONB = True
#     elif excelRow == 5:
#         searchSpace_dict = {
#             'w1': (3.877, 3.8771),
#             'w3': (0.6709, 0.67091)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = True
#     elif excelRow == 6:
#         searchSpace_dict = {
#             'w1': (-1.903, -1.9029),
#             'w3': (2.746, 2.7461)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = False
#     elif excelRow == 7:
#         searchSpace_dict = {
#             'w1': (4.015, 4.0151),
#             'w3': (2.043, 2.0431)
#         }
#         RUNVERSIONA = False
#         RUNVERSIONB = True
#
#     elif excelRow == 8:
#         searchSpace_dict = {
#             'w1': (4.692, 4.6921),
#             'w3': (0.1854, 0.18541)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = True
#     elif excelRow == 9:
#         searchSpace_dict = {
#             'w1': (-1.043, -1.0429),
#             'w3': (-1.067, -1.0669)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = False
#     elif excelRow == 10:
#         searchSpace_dict = {
#             'w1': (4.927, 4.9271),
#             'w3': (0.426, 0.4261)
#         }
#         RUNVERSIONA = False
#         RUNVERSIONB = True
#     elif excelRow == 11:
#         searchSpace_dict = {
#             'w1': (2.146, 2.1461),
#             'w3': (-1.656, -1.6559)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = True
#     elif excelRow == 12:
#         searchSpace_dict = {
#             'w1': (0.07283, 0.07284),
#             'w3': (1.3, 1.301)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = False
#     elif excelRow == 13:
#         searchSpace_dict = {
#             'w1': (4.02, 4.021),
#             'w3': (2.211, 2.2111)
#         }
#         RUNVERSIONA = False
#         RUNVERSIONB = True
#     elif excelRow == 14:
#         searchSpace_dict = {
#             'w1': (3.918, 3.9181),
#             'w3': (2.038, 2.0381)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = True
#     elif excelRow == 15:
#         searchSpace_dict = {
#             'w1': (-2.723, -2.7229),
#             'w3': (1.041, 1.0411)
#         }
#         RUNVERSIONA = True
#         RUNVERSIONB = False
#     elif excelRow == 16:
#         searchSpace_dict = {
#             'w1': (5, 5.001),
#             'w3': (0.03012, 0.03013)
#         }
#         RUNVERSIONA = False
#         RUNVERSIONB = True
#
#     setattr(localSearchSettings, 'searchSpace_dict', searchSpace_dict)
#     setattr(localSearchSettings, 'pbounds_bo', searchSpace_dict)
#
#
#     print('EXCELROW------', excelRow, localSearchSettings.searchSpace_dict)
#     print()
#     print()
#
#     # TEST OVER DINGEN MET VERSCHILLENDE GROOTTE: (VOOR VERSCHILLENDE PROBLEM VERSIONS)
#     # Eerst deze batch
#     setattr(binPackingSettings, 'batchSizeType6', 0)
#     setattr(binPackingSettings, 'batchSizeType8', 5)
#     setattr(binPackingSettings, 'stepSize6', 0)
#     setattr(binPackingSettings, 'stepSize8', 1)
#     setattr(binPackingSettings, 'LB8', 9)
#     setattr(binPackingSettings, 'batchSize', 5)
#     setattr(surrogateModelSettings, 'init_points_bo', 200)
#
#
#
#
#     if surrogateModelSettings.BO:
#         surrogateModel = BayesianSurrogateModel(surrogateModelSettings, localSearchSettings,
#                 customSettings, binPackingSettings).solve(surrogateModelSettings)
#
#
#     # Eerst deze batch
#     # if RUNVERSIONB:
#     #     setattr(binPackingSettings, 'batchSizeType6', numberInstances)
#     #     setattr(binPackingSettings, 'batchSizeType8', 0)
#     #     setattr(binPackingSettings, 'batchSize', numberInstances)
#     #
#     #
#     #
#     #     for LB in range(5, 16):
#     #         setattr(binPackingSettings, 'LB6', LB)
#     #         print('ROW', excelRow, 'INSTANCE TYPE B, SIZE', binPackingSettings.LB6)
#     #
#     #         if surrogateModelSettings.BO:
#     #             surrogateModel = BayesianSurrogateModel(surrogateModelSettings, localSearchSettings,
#     #                                                     customSettings, binPackingSettings).solve(surrogateModelSettings)
#     #
#     # if RUNVERSIONA:
#     #     setattr(binPackingSettings, 'batchSizeType8', numberInstances)
#     #     setattr(binPackingSettings, 'batchSizeType6', 0)
#     #     setattr(binPackingSettings, 'batchSize', numberInstances)
#     #
#     #     for LB in range(5, 16):
#     #         setattr(binPackingSettings, 'LB8', LB)
#     #         print('ROW', excelRow, 'INSTANCE TYPE A, SIZE', binPackingSettings.LB8)
#     #         if surrogateModelSettings.BO:
#     #             surrogateModel = BayesianSurrogateModel(surrogateModelSettings, localSearchSettings,
#     #                                                     customSettings, binPackingSettings).solve(surrogateModelSettings)