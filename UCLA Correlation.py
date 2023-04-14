import pandas as pd
import numpy as np
import scipy.stats as stats
import sklearn.metrics as mets
import matplotlib.pyplot as plt

ucla_df = pd.read_csv('Correlation UCLA-TruDiag.csv').set_index('Patient Id')
tesch_df = pd.read_csv('RafaelleUCLAPopulationData.csv', encoding='cp1252').set_index('PID')
full_immune = pd.read_csv('TruD_10k_Funnorm_RCP_Teschendorff12CellDeconvolution.csv').set_index('Unnamed: 0')
tp = pd.read_csv('PopulationData_100522.csv', encoding='cp1252').set_index('PID')
tm = pd.read_csv('PatientMetaData_100522.csv', encoding='cp1252').set_index('PID')



normals = {'CD4Tnv': ['Suppressor T-Cell %', 'Helper T-Cell %', 'Suppressor T-Cells', 'T-Cells %', 'Helper T-Cell %'],
           'CD4Tmem': ['Suppressor T-Cell %', 'Helper T-Cell %', 'Suppressor T-Cells', 'T-Cells %', 'Helper T-Cell %'],
           'CD8Tnv': ['Suppressor T-Cell %', 'Helper T-Cell %', 'Suppressor T-Cells', 'T-Cells %', 'Helper T-Cell %'],
           'CD8Tmem': ['Suppressor T-Cell %', 'Helper T-Cell %', 'Suppressor T-Cells', 'T-Cells %', 'Helper T-Cell %'],
           'T-Sum': 'T-Cells %',
           'Bnv': 'B-Cell %',
           'Bmem': 'B-Cell %',
           'B-Sum': 'B-Cell %',
           'NK': 'NK Cell %',
           }
normal2 = ['CD4Tnv %',
           'CD4Tmem %',
           'CD8Tnv %',
           'CD8Tmem %',
           'Bnv %',
           'Bmem %',
           'NK %']
exps = ['Suppressor T-Cell %',
        'Suppressor T-Cells',
        'Helper T-Cell %',
        'Helper T-Cells',
        'T-Cells %',
        'T-Cells',
        'Helper T-Cell %',
        'Helper T-Cells',
        'B-Cell %',
        'B-Cells',
        'NK Cell %',
        'NK Cells',
        'Naive Suppressor Cell %',
        'Naive Suppressor Cells',
        'Senescent Suppressor Cell %',
        'Senescent Suppressor Cells',
        'CMV Antibodies (IGG)']
tesch_df['Extrinsic Age'] = tesch_df['Extrinsic Age'].round(2)
print(tesch_df['Decimal Chronological Age'])

pids = []
print(len(ucla_df.index))
tesch_metrics = pd.DataFrame()
exp_metrics = pd.DataFrame()
x = 0
for patient in ucla_df.index:
    ucla_ex = round(ucla_df.loc[patient, 'Extrinsic Epigenetic Age'], 2)
    ucla_dun = round(ucla_df.loc[patient, 'Pace of Aging'], 2)
    ucla_age = round(ucla_df.loc[patient, 'Age'], 1)
    if isinstance(ucla_ex, pd.Series):
        ucla_ex = ucla_ex.iloc[0]

    # print('UCLA: ', ucla)
    tesch_patient = tesch_df[tesch_df['Extrinsic Age'] == ucla_ex]
    print(tesch_patient)
    if isinstance(ucla_dun, pd.Series):
        if len(ucla_dun.values) > 1:
            ucla_dun = ucla_dun.iloc[0]
    if len(tesch_patient.values) > 1:
        tesch_patient = tesch_patient[tesch_patient['DunedinPoAm'] == ucla_dun]
    pid = tesch_patient.index
    idat_id = tesch_patient['Patient ID']

    if len(tesch_patient) == 0:
        ucla_ex += .01
        tesch_patient = tesch_df[tesch_df['Extrinsic Age'] == ucla_ex]
        if len(tesch_patient) == 0:
            ucla_ex -= .02
            tesch_patient = tesch_df[tesch_df['Extrinsic Age'] == ucla_ex]

    if len(tesch_patient) != 0 and len(tesch_patient) != 2:
        # print('Tesch: ', len(pid))
        pass
    else:
        for p in pid:
            tesch_patient = tesch_patient[tesch_patient['Decimal Chronological Age'].round(1) == ucla_age]

    tesch_df.loc[pid, 'UCLA ID'] = patient
    full_immune.loc[idat_id, 'UCLA ID'] = patient
    full_immune.loc[idat_id, 'T-Sum'] = full_immune.loc[idat_id, 'CD4Tnv'] + full_immune.loc[idat_id, 'CD4Tmem'] + full_immune.loc[idat_id, 'CD8Tnv'] + full_immune.loc[idat_id, 'CD8Tmem']
    full_immune.loc[idat_id, 'B-Sum'] = full_immune.loc[idat_id, 'Bmem'] + full_immune.loc[idat_id, 'Bnv']
    pids.extend(pid)

    for met in full_immune.columns:
        if met != 'UCLA ID':
            met = met + ' %'
        if not isinstance(idat_id, str) and len(idat_id) > 0:
            # print(idat_id)
            # print('\nIDAT ID: ', idat_id.values[0])
            # print('\nRow: ', full_immune.loc[idat_id, met].values[0])
            # print('\nPatient: ', patient)
            tesch_metrics.loc[patient, met] = full_immune.loc[idat_id, met.replace(' %', '')].values[0] * 100
        elif len(idat_id) > 0:
            idat_id = idat_id.values[0]
            # if isinstance(idat_id, ):

            # print('\nIDAT ID: ', idat_id)
            # print('\nRow: ', full_immune.loc[idat_id, met])
            # print('\nPatient: ', patient)
            tesch_metrics.loc[patient, met] = full_immune.loc[idat_id, met] * 100
        else:
            tesch_metrics.loc[patient, met] = np.nan
    for met in exps:
        if met == 'CMV Antibodies (IGG)':
            ucmet = met + ' (U/mL)'
        elif met in ['Helper T-Cells',
                     'Naive Suppressor Cells',
                     'NK Cells',
                     'Suppressor T-Cells',
                     'T-Cells',
                     'Senescent Suppressor Cells',
                     'Naive Suppressor Cells']:
            ucmet = met + ' (/cmm)'
        else:
            ucmet = met

        if not isinstance(idat_id, str):
            if len(idat_id.values) > 1:
                idat_id = idat_id.values[0]
            val = ucla_df.loc[patient, met]
            if isinstance(val, pd.Series):
                val = val.values[0]
            exp_metrics.loc[patient, ucmet] = val
        elif len(idat_id) > 0:
            idat_id = idat_id.values[0]
            exp_metrics.loc[patient, ucmet] = ucla_df.loc[patient, met]
        else:
            exp_metrics.loc[patient, ucmet] = np.nan
print(tesch_metrics)
# for v in tesch_metrics.index:
#     tesch_metrics.loc[v, 'Sum'] = np.nansum(tesch_metrics.loc[v, normal2])
# tesch_metrics.to_csv('TeschMetrics.csv')
exp_metrics.to_csv('UCLA_ExperimentalMetrics.csv')

df_list = [tesch_metrics, exp_metrics]
df_names = ['EpiDISH Outputs', 'Experimental Values']
with pd.ExcelWriter('UCLA_Analysis_Metrics.xlsx') as writer:
    for x in range(2):
        exec('df_list[x].to_excel(writer, df_names[x])')
exit()

ucla_df = ucla_df.sort_values(by='Patient Id')
for col in ucla_df.columns:
    print(ucla_df[col])
    if '%' in str(col) and 'units' not in col.lower():
        ucla_df[col] = ucla_df[col].fillna(0).astype(int) / 100
ucla_df.replace(0, np.nan, inplace=True)

print(tesch_df)
shared = list(set(tesch_df['Patient ID']) & set(full_immune.index))
full_immune = full_immune.loc[shared]
full_immune = full_immune.sort_values(by='UCLA ID')
shared = list(set(tesch_df['UCLA ID']) & set(ucla_df.index))
ucla_df = ucla_df.loc[shared]
full_immune = full_immune.fillna('Wooga')
full_immune = full_immune[full_immune['UCLA ID'] != 'Wooga']

ucla_df = ucla_df.loc[full_immune['UCLA ID']]
ucla_df = ucla_df[~ucla_df.index.duplicated(keep='first')]
full_immune.set_index(full_immune['UCLA ID'].astype(int), inplace=True)
full_immune = full_immune[~full_immune.index.duplicated(keep='first')]

print(len(np.unique(ucla_df.index)))
print(len(np.unique(full_immune['UCLA ID'])))
print(ucla_df, full_immune)
print(ucla_df.columns)
full_immune.to_csv('FI.csv')

meta_list = {}
performances = pd.DataFrame(index=list(normals.keys())[5:], columns=['Pearson Coefficient', 'Pearson P-Val', 'Spearman Coefficient', 'Spearman P-Val', 'R-Squared', 'MAE'])
for output in normals.keys():
    raf_metrics = normals[output]
    print(output)
    multiple = False
    def analysis(metric):
        tesch, raf = full_immune.loc[:, output], ucla_df.loc[:, metric]
        bad_indices = []
        x = 0
        for val in tesch:
            if np.isnan(val):
                bad_indices.append(x)
            x += 1
        x = 0
        for val in raf:
            if np.isnan(val) and [raf==val].index not in bad_indices:
                bad_indices.append(x)
            x += 1
        tesch, raf = tesch.drop(tesch.index[bad_indices]), raf.drop(raf.index[bad_indices])
        # print(len(tesch), len(raf))

        try:
            spearman, spearP, pearson, pearsP = stats.spearmanr(tesch, raf)[0], stats.spearmanr(tesch, raf)[1], stats.pearsonr(tesch, raf)[0], stats.pearsonr(tesch, raf)[1]
        except Exception as e:
            spearman, spearP, pearson, pearsP = np.nan, np.nan, np.nan, np.nan
            print(e)
        try:
            mae, rsq = mets.mean_absolute_error(tesch, raf), pearson * pearson
        except Exception as e:
            mae, rsq = np.nan, np.nan
            print(e)

        if 'CD' in output:
            row_idx = output + '-' + metric
        else:
            row_idx = output

        performances.loc[row_idx, 'Pearson Coefficient'], performances.loc[row_idx, 'Spearman Coefficient'] = pearson, spearman
        performances.loc[row_idx, 'Pearson P-Val'], performances.loc[row_idx, 'Spearman P-Val'] = pearsP, spearP
        performances.loc[row_idx, 'MAE'], performances.loc[row_idx, 'R-Squared'] = mae, rsq

        meta_metrics = pd.DataFrame({'EpiDISH': tesch, 'Real': raf}, index=tesch.index)
        meta_metrics.loc['Average ' + row_idx, 'EpiDISH'], meta_metrics.loc['Average ' + row_idx, 'Real'] = np.average(tesch), np.average(raf)
        meta_list[row_idx] = meta_metrics

    if isinstance(raf_metrics, list):
        for m in raf_metrics:
            analysis(m)
    else:
        analysis(raf_metrics)




with pd.ExcelWriter('ImmuneDeconvolutionUCLA_Analysis.xlsx') as writer:
    for mm_name in meta_list.keys():
        mm = meta_list[mm_name]
        exec('mm.to_excel(writer, mm_name)')
performances.to_csv('ImmuneDeconvolutionUCLA_Analysis.csv')
# print(pids)
# tesch_df = tesch_df.loc[pids]
# print(len(tp))
# tp = tp.loc[pids]
# print(len(tm))
# pids = list(set(tm.index) & set(pids))
# tm = tm.loc[pids]
# tesch_df.to_csv('NewTesch.csv')
#
# tp.to_csv('TeschPop.csv')
# tm.to_csv('TeschMeta.csv')

