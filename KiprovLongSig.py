import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import datetime
import time

kips = pd.read_csv('KiprovSamples_060322_results_AllSamples.csv')
print(len(kips.index))

# kips['AltumAge']
# altumPredicts = pd.read_csv('C:/Users/jack/PycharmProjects/TruDiagnostic/AltumAge/Data/Outputs/Kiprov_GMQN_BMIQ_betavaluesAltumOutput.csv').set_index('Unnamed: 0')
# print(altumPredicts)
# for patient in altumPredicts.columns:
#     kips.loc[patient, 'AltumAge'] = altumPredicts[patient].values
# kips.to_csv('KiprovSamples_060322_results_AllSamples NEW.csv')
#
# exit()
kipsName = kips.copy()

for i in range(len(kips['Patient.ID'])):
    name = kips['Patient.ID'][i]
    new_name = name.split('_')[0]

    kipsName.loc[i, 'Patient.ID'] = new_name

noageKips = kips[kips['Decimal.Chronological.Age'] == '---']
kipsName.drop(index=kips[kips['Decimal.Chronological.Age'] == '---'].index, inplace=True)
kips.set_index('Patient.ID', inplace=True)
kipsName.set_index('Patient.ID', inplace=True)

clocks = ['Date',
          'OldPipeline.horvath',
          'OldPipeline.hannum',
          'OldPipeline.phenoage',
          'HannumAge_Updated',
          'HorvathAge_Updated',
          'PhenoAge',
          'DunedinPACE',
          'TruD.Clock',
          'TruD.PCclock',
          'PCHorvath1',
          'PCHorvath2',
          'PCHannum',
          'PCPhenoAge',
          'PCGrimAge']
residuals = pd.DataFrame(index=kips.index, columns=clocks)
drop_indices = []
for clock in clocks:
    for patient in kips.index:
        if str(kips.loc[patient, clock]) == '---' or str(kips.loc[patient, 'Decimal.Chronological.Age']) == '---':
            drop_indices.append(patient)
        elif clock == 'DunedinPACE':
            residuals.loc[patient, clock] = float(kips.loc[patient, clock])
        elif clock == 'Date':
            dateVal = kips.loc[patient, clock]
            # print('First dateval: ', dateVal)
            # day, month, year = dateVal.split('/')[0], dateVal.split('/')[1], dateVal.split('/')[2]
            # dateVal = day + '/' + month + '/' + '20' + year
            # print(dateVal)
            residuals.loc[patient, clock] = time.mktime(datetime.datetime.strptime(dateVal, '%m/%d/%Y').timetuple())  #time.mktime(
        else:
            residuals.loc[patient, clock] = float(kips.loc[patient, clock]) - float(kips.loc[patient, 'Decimal.Chronological.Age'])
residuals.drop(index=drop_indices, inplace=True)
# residuals.to_csv('Residuals.csv')
unique_patients = np.unique(kipsName.index)
print(residuals)

patient_indices = {}
for patient in np.unique(kipsName.index):
    indices = []
    print('Patient1: ', patient)
    for idx in kips.index:
        if str(int(patient)) in str(idx):
            indices.append(idx)

    patient_set = kips.loc[indices].sort_values(by=['Date'])
    # print('Patient set: ', patient_set)

    if len(patient_set.index) > 1:
        value = list(patient_set.index)
        value.sort()
        patient_indices[patient] = value
        print('Patient: ', patient)

# print(patient_indices)

count_org = {}
for k in patient_indices.keys():
    count_org[k] = len(patient_indices[k])
    print(patient_indices[k])


idols = ['IDOL_output.CD8T',
         'IDOL_output.CD4T',
         'IDOL_output.NK',
         'IDOL_output.Bcell',
         'IDOL_output.Neu',
         'IDOL_output.CD4T.CD8T',
         'DNAmTL',
         'PCDNAmTL']
print(residuals)
for patient in kips.index:
    for idol in idols:
        residuals.loc[patient, idol] = kips.loc[patient, idol]
residuals.to_csv('KiprovResiduals+IDOLS.csv')
exit()

# for idol in idols:
    # idol_vals = pd.DataFrame(index=patient_indices.keys(), columns=[1, 2, 3, 4, 5, 6, 7])
    # print(idol)

    # for x in range(5):
    #     x += 1
    #
    #     valid = []
    #     for patient in count_org.keys():
    #         if count_org[patient] >= x:
    #             to_append = list(patient_indices[patient])
    #             to_append.sort()
    #             # print('Indices: ', to_append)
    #             valid.append(to_append)
    #
    #     valid = [val for sublist in valid for val in sublist]
    #     first_set = pd.Series(index=valid)
    #     for patient in patient_indices:
    #         # print('Patient: ', patient)
    #         try:
    #             pi = patient_indices[patient]
    #             first_set[patient] = np.array(kips.loc[pi, idol])
    #             for r in range(len(first_set[patient])-1):
    #                 r += 1
    #                 val = first_set[patient][r-1]
    #                 idol_vals.loc[patient, r] = val
    #             # second_set.append(kips.loc[patient, idol].values[x+1])
    #             # print(first_set, len(first_set))
    #             # print(second_set, len(second_set))
    #         except Exception as e:
    #             print('Screwup here', e)
    #     print(valid)
    #
    # print('idol_vals: \n', idol_vals)
    #
    # p_vals = []
    # p_lengths = []
    # total_lengths = []
    # for x in range(len(idol_vals.columns)-2):
    #     x+=1
    #     first_set = idol_vals[x].dropna()
    #     total_lengths.append(len(first_set))
    #     second_set = idol_vals[x+1].dropna()
    #     shared_patients = list((set(first_set.index) & set(second_set.index)))
    #     first_set, second_set = first_set.loc[shared_patients].sort_index(), second_set.loc[shared_patients].sort_index()
    #     print('First set: \n', first_set)
    #     print('Second set: \n', second_set)
    #     p_lengths.append(len(shared_patients))
    #
    #     t_test, p_val = scipy.stats.ttest_rel(first_set, second_set)
    #     p_vals.append(p_val)
    # print('P_vals: ', p_vals)

    # fig = plt.figure()
    # box = fig.add_subplot()
    #
    # exec_string = 'box.boxplot(['
    # for x in range(len(idol_vals.keys())-1)[:-2]:
    #     if x == len(idol_vals.keys()):
    #         exec_string += 'idol_vals[' + str(x+1) + '].dropna()'
    #     else:
    #         exec_string += 'idol_vals[' + str(x+1) + '].dropna(), '
    # exec_string += '])'
    # eval(exec_string)
    #
    # for v in range(len(p_vals[:-2])):
    #     p_vals[v] = round(p_vals[v], 4)
    #
    # box.set_title(idol.replace('IDOL_output.','') + ' || p-vals: ' + str(p_vals[:-2]).replace('[', '').replace(']', '') +
    #               '\n' + 'p-Val n-sizes: ' + str(p_lengths[:-2]).replace('[', '').replace(']', '')
    #               + '|| total n-sizes: ' + str(total_lengths[:-1]).replace('[', '').replace(']', ''))
    # box.set_xlabel('Test #')
    # box.set_ylabel('%')
    # plt.savefig('IDOL Figs/' + idol + 'IDOL Figure.png')
    # plt.show()

# for clock in clocks:
    # clock_vals = pd.DataFrame(index=patient_indices.keys(), columns=[1, 2, 3, 4, 5, 6, 7])

    # for x in range(5):
    #     x += 1
    #     print('Testing point', x)
    #     valid = []
    #     for p in count_org.keys():
    #         indices = list(patient_indices[p])
    #         indices.sort()
    #         valid.append(indices)
    #
    #     valid = [val for sublist in valid for val in sublist]
    #     first_set = pd.Series(index=valid)
    #     for patient in patient_indices:
    #         # print('Patient: ', patient)
    #         try:
    #             pi = patient_indices[patient]
    #             first_set[patient] = np.array(kips.loc[pi, clock])
    #             for r in range(len(first_set[patient])-1):
    #                 r += 1
    #                 val = first_set[patient][r-1]
    #                 clock_vals.loc[patient, r] = val
    #             # second_set.append(kips.loc[patient, idol].values[x+1])
    #             # print(first_set, len(first_set))
    #             # print(second_set, len(second_set))
    #         except Exception as e:
    #             print('Screwup here', e)
    #     print(valid)
    #
    # print('clock_vals: \n', clock_vals)

    # p_vals = []
    # p_lengths = []
    # total_lengths = []
    # for x in range(len(clock_vals.columns)-2):
    #     x += 1
    #     first_set = clock_vals[x].dropna()
    #     total_lengths.append(len(first_set))
    #     second_set = clock_vals[x+1].dropna()
    #     shared_patients = list((set(first_set.index) & set(second_set.index)))
    #     first_set, second_set = first_set.loc[shared_patients].sort_index(), second_set.loc[shared_patients].sort_index()
    #     print('First set: \n', first_set)
    #     print('Second set: \n', second_set)
    #     p_lengths.append(len(shared_patients))
    #
    #     t_test, p_val = scipy.stats.ttest_rel(first_set, second_set)
    #     p_vals.append(p_val)
    # print('P_vals: ', p_vals)
    #
    # fig = plt.figure()
    # box = fig.add_subplot()
    #
    # exec_string = 'box.boxplot(['
    # for x in range(len(clock_vals.keys())-1)[:-2]:
    #     if x == len(clock_vals.keys()):
    #         exec_string += 'clock_vals[' + str(x+1) + '].dropna()'
    #     else:
    #         exec_string += 'clock_vals[' + str(x+1) + '].dropna(), '
    # exec_string += '])'
    # eval(exec_string)
    #
    # for v in range(len(p_vals[:-2])):
    #     p_vals[v] = round(p_vals[v], 4)
    #
    # box.set_title(clock + ' || p-vals: ' + str(p_vals[:-2]).replace('[', '').replace(']', '') +
    #               '\n' + 'p-val n-sizes: ' + str(p_lengths[:-2]).replace('[', '').replace(']', '') +
    #               '|| total n-sizes: ' + str(total_lengths[:-1]).replace('[', '').replace(']', ''))
    # box.set_xlabel('Test #')
    # box.set_ylabel('%')
    # plt.savefig('Clock Figs/' + clock + 'Clock Figure.png')
    # plt.show()


for idol in idols:
    print(idol)

    for patient in patient_indices.keys():
        indices = []
        print('Patient1: ', patient)
        for idx in kips.index:
            if str(int(patient)) in str(idx):
                indices.append(idx)

        patient_set = residuals.loc[indices].sort_values(by=['Date']).dropna()

        if len(patient_set.index) > 1:
            idol_vals = patient_set[idol]
            age = patient_set['Date']
            minAge = np.min(age)
            for x in age.index:
                age.loc[x] = age.loc[x] - minAge
            # tests = range(patient_set)

            fig = plt.figure()
            print(age, idol_vals)
            plt.plot(age, idol_vals)

            plt.title('Analysis of ' + idol + ' values for Patient ID: ' + indices[0].split('_')[0])
            plt.xlabel('Chronological Age')
            plt.ylabel('Idol Values')
            plt.savefig('Longitudinal Analysis/' + idol + patient + 'Idol Figure.png')
            # plt.show()
            plt.close()


for clock in clocks[1:]:
    for patient in patient_indices.keys():
        indices = []
        print('Patient1: ', patient)
        for idx in kips.index:
            if str(int(patient)) in str(idx):
                indices.append(idx)

        patient_set = residuals.loc[indices].sort_values(by=['Date']).dropna()

        if len(patient_set.index) > 1:
            clock_vals = patient_set[clock]

            age = patient_set['Date']
            minAge = np.min(age)
            try:
                for x in age.index:
                    age.loc[x, 'Date'] = age.loc[x, 'Date'] - minAge

                fig = plt.figure()
                print(age, clock_vals)
                plt.plot(age, clock_vals)

                plt.title('Analysis of ' + clock + ' values for Patient ID: ' + indices[0].split('_')[0])
                plt.xlabel('Chronological Age')
                plt.ylabel('Residuals in Years')
                plt.savefig('Longitudinal Analysis/' + clock + patient + 'Clock Figure.png')
                # plt.show()
                plt.close()
            except Exception as e:
                print(e, 'Error in plotting')


