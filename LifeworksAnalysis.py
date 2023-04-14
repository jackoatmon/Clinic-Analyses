import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import datetime
import time

# kips = pd.read_csv('KiprovSamples_060322_results_AllSamples.csv')
kips = pd.read_csv('C:/Users/jack/Downloads/PopulationData_120122.csv').set_index('Patient ID')
kips = kips[kips['Clinic ID'] == 70496]
print(len(kips.index))

# kips['AltumAge']
# altumPredicts = pd.read_csv('C:/Users/jack/PycharmProjects/TruDiagnostic/AltumAge/Data/Outputs/Kiprov_GMQN_BMIQ_betavaluesAltumOutput.csv').set_index('Unnamed: 0')
# print(altumPredicts)
# for patient in altumPredicts.columns:
#     kips.loc[patient, 'AltumAge'] = altumPredicts[patient].values
# kips.to_csv('KiprovSamples_060322_results_AllSamples NEW.csv')
#
# exit()
# kipsName = kips.copy()

# print(kips)
# for i in range(len(kips.index)):
#     name = kips.index[i]
#     new_name = name.split('_')[0]
#
#     kipsName.loc[name, 'Patient ID'] = new_name

# noageKips = kips[kips['Decimal Chronological Age'] == '---']
# kipsName.drop(index=kips[kips['Decimal Chronological Age'] == '---'].index, inplace=True)
# kips.set_index('Patient ID', inplace=True)
# print(kipsName)
# kipsName.dropna(axis='Patient ID', inplace=True)
# kipsName.set_index('Patient ID', inplace=True)

clocks = ['Collection Date',
          'Telomere Values',
          'Extrinsic Age',
          'Intrinsic Age',
          'Hannum PC',
          'Horvath PC',
          'Telomere Values PC',
          'GrimAge PC ',
          'PhenoAge PC']
          # 'OldPipeline.horvath',
          # 'OldPipeline.hannum',
          # 'OldPipeline.phenoage',
          # 'HannumAge_Updated',
          # 'HorvathAge_Updated',
          # 'PhenoAge',
          # 'DunedinPACE',
          # 'TruD.Clock',
          # 'TruD.PCclock',
          # 'PCHorvath1',
          # 'PCHorvath2',
          # 'PCHannum',
          # 'PCPhenoAge',
          # 'PCGrimAge']
residuals = pd.DataFrame(index=kips.index, columns=clocks)
drop_indices = []
for clock in clocks:
    for patient in kips.index:
        dateVal = kips.loc[patient, clock]

        try:
            if len(dateVal) > 1 and isinstance(dateVal, pd.Series):
                dateVal = dateVal[0]
        except:
            pass

        if isinstance(dateVal, pd.Series):
            dateVal = dateVal[0]

        if str(kips.loc[patient, clock]) == '---' or str(kips.loc[patient, 'Decimal Chronological Age']) == '---':
            drop_indices.append(patient)
        elif clock == 'DunedinPACE':
            residuals.loc[patient, clock] = float(kips.loc[patient, clock])
        elif clock == 'Collection Date':
            try:
                date = time.mktime(datetime.datetime.strptime(dateVal, '%m/%d/%Y').timetuple())
                residuals.loc[patient, clock] = date  #time.mktime(
            except Exception as e:
                print(e)
                residuals.loc[patient, clock] = np.nan
        else:
            age = kips.loc[patient, 'Decimal Chronological Age']
            try:
                if len(age) > 1 and isinstance(age, pd.Series):
                    age = age[0]
            except:
                pass
            residuals.loc[patient, clock] = float(dateVal) - float(age)
residuals.drop(index=drop_indices, inplace=True)
# residuals.to_csv('Residuals.csv')
# print('Kips: ', kipsName.index)
# unique_patients = np.unique(kipsName.index)
print(residuals)

patient_indices = {}
# print(len(np.unique(kipsName.index)))
# exit()
print(len(np.unique(kips['PID'])))
print(np.unique(kips['PID']))
print(len(kips.index))

for patient in np.unique(kips['PID']):
    indices = kips[kips['PID'] == patient].index
    print('IDX: ', patient)
    patient_set = kips.loc[indices].sort_values(by=['Collection Date'])
    # print('Patient set: ', patient_set)

    if len(patient_set.index) > 1:
        value = list(patient_set.index)
        value.sort()
        patient_indices[str(patient)] = value
        print('Patient: ', patient)

# print(patient_indices)

count_org = {}
for k in patient_indices.keys():
    count_org[k] = len(patient_indices[k])


# idols = ['IDOL_output.CD8T',
#          'IDOL_output.CD4T',
#          'IDOL_output.NK',
#          'IDOL_output.Bcell',
#          'IDOL_output.Neu',
#          'IDOL_output.CD4T.CD8T',
#          'DNAmTL',
#          'PCDNAmTL']
idols = ['Immune.CD8T',
         'Immune.CD4T',
         'Immune.CD4T.CD8T',
         'Immune.NK',
         'Immune.Bcell',
         'Immune.Mono',
         'Immune.Neutrophil']
print(residuals)
for patient in kips.index:
    for idol in idols:
        residuals.loc[patient, idol] = kips.loc[patient, idol]
# residuals.to_csv('KiprovResiduals+IDOLS.csv')

print(kips)

for idol in idols:
    idol_vals = pd.DataFrame(index=patient_indices.keys(), columns=[1, 2, 3, 4, 5, 6, 7])
    print(len(idol_vals.index))
    print(idol)

    for x in range(5):
        x += 1

        valid = []
        for pid in count_org.keys():
            if count_org[pid] >= x:
                to_append = list(patient_indices[pid])
                to_append.sort()
                # print('Indices: ', to_append)
                valid.append(to_append)

        valid = [val for sublist in valid for val in sublist]
        first_set = pd.Series(index=valid)
        print('valid')
        for pid in patient_indices:
            pid = str(pid)
            # print('Patient: ', patient)
            try:
                pi = patient_indices[pid]
                first_set[pid] = np.array(kips.loc[pi, idol])
                for r in range(len(first_set[pid])):
                    patient = kips[kips['PID'] == int(pid)].index[r]
                    val = first_set[pid][r]
                    idol_vals.loc[pid, r+1] = val
                # second_set.append(kips.loc[patient, idol].values[x+1])
                # print(first_set, len(first_set))
                # print(second_set, len(second_set))
            except Exception as e:
                print('Screwup here', e)

    print('idol_vals: \n', idol_vals)

    p_vals = []
    p_lengths = []
    total_lengths = []
    for x in range(len(idol_vals.columns)-3):
        x+=1
        first_set = idol_vals[x].dropna()
        total_lengths.append(len(first_set))
        second_set = idol_vals[x+1].dropna()
        shared_patients = list((set(first_set.index) & set(second_set.index)))
        first_set, second_set = first_set.loc[shared_patients].sort_index(), second_set.loc[shared_patients].sort_index()
        # print('First set: \n', first_set)
        # print('Second set: \n', second_set)
        p_lengths.append(len(shared_patients))

        t_test, p_val = scipy.stats.ttest_rel(first_set, second_set)
        p_vals.append(p_val)
    # print('P_vals: ', p_vals)

    fig = plt.figure()
    box = fig.add_subplot()

    exec_string = 'box.boxplot(['
    for x in range(len(idol_vals.keys())-1)[:-2]:
        if x == len(idol_vals.keys()):
            exec_string += 'idol_vals[' + str(x+1) + '].dropna()'
        else:
            exec_string += 'idol_vals[' + str(x+1) + '].dropna(), '
    exec_string += '])'
    eval(exec_string)

    for v in range(len(p_vals[:-2])):
        p_vals[v] = round(p_vals[v], 4)

    box.set_title(idol.replace('IDOL_output.','') + ' || p-vals: ' + str(p_vals[:-2]).replace('[', '').replace(']', '') +
                  '\n' + 'p-Val n-sizes: ' + str(p_lengths[:-2]).replace('[', '').replace(']', '')
                  + '|| total n-sizes: ' + str(total_lengths[:-1]).replace('[', '').replace(']', ''))
    box.set_xlabel('Test #')
    box.set_ylabel('%')
    plt.savefig('IDOL Figs/' + idol + 'IDOL Figure.png')

for clock in clocks:
    if clock != 'Collection Date':
        clock_vals = pd.DataFrame(index=patient_indices.keys(), columns=[1, 2, 3, 4, 5, 6, 7])

        for x in range(5):
            x += 1
            print('Testing point', x)
            valid = []
            for p in count_org.keys():
                indices = list(patient_indices[p])
                indices.sort()
                valid.append(indices)

            valid = [val for sublist in valid for val in sublist]
            first_set = pd.Series(index=valid)
            for pid in patient_indices:
                pid = str(pid)
                # print('Patient: ', patient)
                try:
                    pi = patient_indices[pid]
                    first_set[pid] = np.array(kips.loc[pi, clock])
                    for r in range(len(first_set[pid])):
                        patient = kips[kips['PID'] == int(pid)].index[r]
                        val = first_set[pid][r]
                        clock_vals.loc[pid, r + 1] = val
                    # second_set.append(kips.loc[patient, idol].values[x+1])
                    # print(first_set, len(first_set))
                    # print(second_set, len(second_set))
                except Exception as e:
                    print('Screwup here', e)

        print('clock_vals: \n', clock_vals)

        p_vals = []
        p_lengths = []
        total_lengths = []
        for x in range(len(clock_vals.columns)-2):
            x += 1
            first_set = clock_vals[x].dropna()
            total_lengths.append(len(first_set))
            second_set = clock_vals[x+1].dropna()
            shared_patients = list((set(first_set.index) & set(second_set.index)))
            first_set, second_set = first_set.loc[shared_patients].sort_index(), second_set.loc[shared_patients].sort_index()
            print('First set: \n', first_set)
            print('Second set: \n', second_set)
            p_lengths.append(len(shared_patients))

            t_test, p_val = scipy.stats.ttest_rel(first_set, second_set)
            p_vals.append(p_val)
        print('P_vals: ', p_vals)

        fig = plt.figure()
        box = fig.add_subplot()

        exec_string = 'box.boxplot(['
        for x in range(len(clock_vals.keys())-1)[:-2]:
            if x == len(clock_vals.keys()):
                exec_string += 'clock_vals[' + str(x+1) + '].dropna()'
            else:
                exec_string += 'clock_vals[' + str(x+1) + '].dropna(), '
        exec_string += '])'
        eval(exec_string)

        for v in range(len(p_vals[:-2])):
            p_vals[v] = round(p_vals[v], 4)

        box.set_title(clock + ' || p-vals: ' + str(p_vals[:-2]).replace('[', '').replace(']', '') +
                      '\n' + 'p-val n-sizes: ' + str(p_lengths[:-2]).replace('[', '').replace(']', '') +
                      '|| total n-sizes: ' + str(total_lengths[:-1]).replace('[', '').replace(']', ''))
        box.set_xlabel('Test #')
        box.set_ylabel('%')
        plt.savefig('Clock Figs/' + clock + 'Clock Figure.png')
        # plt.show()


for idol in idols:
    print(idol)

    for patient in patient_indices.keys():
        indices = []
        for idx in kips.index:
            if str(int(patient)) in str(idx):
                indices.append(idx)

        patient_set = residuals.loc[indices].sort_values(by=['Collection Date']).dropna()

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

n_clocks = clocks.copy()
n_clocks.extend(idols)
for clock in n_clocks:
    for pid in patient_indices.keys():
        indices = kips[kips['PID'] == int(pid)].index
        patient_set = residuals.loc[indices].sort_values(by=['Collection Date']).dropna()
        print(patient_set)
        if len(patient_set.index) > 1:
            clock_vals = patient_set[clock]
            print(clock_vals)

            age = patient_set['Collection Date']
            minAge = np.min(age)
            print(age)
            try:
                for x in age.index:
                    age.loc[x] = age.loc[x] - minAge

                fig = plt.figure()
                print(age, clock_vals)
                plt.plot(age, clock_vals)

                plt.title('Analysis of ' + clock + ' values for PID: ' + pid)
                plt.xticks()
                plt.xlabel('Chronological Age')

                    plt.ylabel('Residuals in Years')
                plt.savefig('Longitudinal Analysis/' + clock + pid + 'Clock Figure.png')
                # plt.show()
                plt.close()
            except Exception as e:
                print(e, 'Error in plotting')


