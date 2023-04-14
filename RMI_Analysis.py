import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import datetime
import scipy.stats
import markdown
import imageio
from glob import glob
from PIL import Image
from xhtml2pdf import pisa
import os

# for file in glob('Clock Figs/Individual Figs/*.png'):
#     os.remove(file)
# for file in glob('Clock Figs/Group Figs/*.png'):
#     os.remove(file)

best_fit = False
# meta_df = pd.read_csv('Jack_PatientMetaData_052522 - Organized.csv').set_index('PatientID')
meta_df = pd.read_csv('PatientMetaData.csv', encoding='cp1252').set_index('PatientID')
algo_df = pd.read_csv('RMI_PopData.csv').set_index('Patient ID')
all_df = pd.read_csv('PopulationData_091222.csv').set_index('Patient ID')
algo_df.rename(columns={'DunedinPoAm': 'DunedinPACE'}, inplace=True)
all_df.rename(columns={'DunedinPoAm': 'DunedinPACE'}, inplace=True)
algo_df.rename(columns={'GrimAge PC ': 'GrimAge PC'}, inplace=True)
all_df.rename(columns={'GrimAge PC ': 'GrimAge PC'}, inplace=True)

for patient in meta_df.index:
    diseased = False
    for disease in ['Cardiovascular', 'Respiratory Disease', 'Endocrine Disease', 'Musculoskeletal', 'Immune', 'Gastrointestinal']:
        if str(meta_df.loc[patient, disease]).replace(' ', '').lower() != 'nan':
            diseased = True
            break
    if diseased:
        meta_df.loc[patient, 'Diseased'] = 1
    else:
        meta_df.loc[patient, 'Diseased'] = 0
        print(meta_df.loc[patient, disease])


clocks = ['Collection Date',
          'DunedinPACE',
          'Horvath PC',
          'Hannum PC',
          'PhenoAge PC',
          'GrimAge PC']
residuals = pd.DataFrame(index=algo_df.index, columns=clocks)

# df = pd.read_csv('PatientMetaData.csv', encoding='cp1252').set_index('PatientID').astype(str)
# new_df = df[df['Neuropsychological'] != np.nan]
# new_df = new_df[new_df['Neuropsychological'] != '']
# new_df = new_df[new_df['Neuropsychological'] != 'nan'].replace('nan', np.nan)
# # new_df = new_df[new_df['Intrinsic Age'] < new_df['Decimal Chronological Age']]
# new_df.to_csv('MentalIllnessPatients.csv')
# exit()

'''Creating residuals'''
drop_indices = []
print(algo_df.columns)
for clock in clocks:
    for patient in algo_df.index:
        try:
            algo_df.loc[patient, 'Unix Time'] = time.mktime(datetime.datetime.strptime(algo_df.loc[patient, 'Collection Date'], '%m/%d/%Y').timetuple())
        except Exception as e:
            print(e), algo_df.drop(patient)

        if str(algo_df.loc[patient, clock]) == '---' or str(algo_df.loc[patient, 'Decimal Chronological Age']) == '---':
            drop_indices.append(patient)
        elif clock == 'DunedinPACE':
            residuals.loc[patient, clock] = float(algo_df.loc[patient, clock])
        elif clock == 'Collection Date':
            dateVal = algo_df.loc[patient, clock]
            # print('First dateval: ', dateVal)
            # day, month, year = dateVal.split('/')[0], dateVal.split('/')[1], dateVal.split('/')[2]
            # dateVal = day + '/' + month + '/' + '20' + year
            # print(dateVal)
            try:
                residuals.loc[patient, clock] = datetime.datetime.strptime(dateVal, '%m/%d/%Y')
            except Exception as e:
                residuals.loc[patient, clock] = np.nan
        else:
            residuals.loc[patient, clock] = float(algo_df.loc[patient, clock]) - float(algo_df.loc[patient, 'Decimal Chronological Age'])
residuals.drop(index=drop_indices, inplace=True)
# residuals.to_csv('Residuals.csv')

drop_list = []
for patient in all_df.index:
    try:
        all_df.loc[patient, 'Unix Time'] = time.mktime(
            datetime.datetime.strptime(all_df.loc[patient, 'Collection Date'], '%m/%d/%Y').timetuple())
    except Exception as e:
        print(e), drop_list.append(patient)
    try:
        if all_df.loc[patient, 'DunedinPACE'] < .01:
            drop_list.append(patient)
    except Exception as e:
        print(e)
all_df.drop(drop_list, inplace=True)

drops = []
pids = np.unique(all_df['PID'])
for pid in pids:
    if len(all_df[all_df['PID'] == pid].index) > 1:
        pass
    else:
        drops.extend(all_df[all_df['PID'] == pid].index)

all_df.drop(index=drops, inplace=True)

# diseased = meta_df[meta_df['Total Disease Count'] > 0].index
# healthy = meta_df[meta_df['Total Disease Count'] == 0].index
diseased = meta_df[meta_df['Diseased'] != 0].index
healthy = meta_df[meta_df['Diseased'] == 0].index


print(diseased, healthy)

shared = list(set(diseased) & set(all_df.index))
diseased = all_df.loc[shared]
diseased1 = meta_df.loc[shared]

shared = list(set(healthy) & set(all_df.index))
healthy = all_df.loc[shared]
healthy1 = meta_df.loc[shared]

print(len(diseased), len(healthy))

outputs = {}  # use this later to as a container for all algo outputs to recursively plot all outputs
def make_data(df, clock, real_test=True):
    try:
        os.mkdir('clock figs/individual figs/' + clock)
    except:
        pass

    all_pids = np.unique(df['PID'])
    patient_indices = {}
    ages = []
    dates = []
    for pid in all_pids:
        patient_set = df[df['PID'] == pid].sort_values(by=['Unix Time'])

        if len(patient_set.index) > 1:
            value = list(patient_set.index)
            value.sort()
            patient_indices[pid] = value

            # print('PID: ', pid)
            # print(patient_set)

            days_from_first = []
            patient_drop = []
            for test in range(len(patient_set.index)):
                now = datetime.datetime.strptime(patient_set.iloc[test]['Collection Date'], '%m/%d/%Y')
                previous = datetime.datetime.strptime(patient_set.iloc[0]['Collection Date'], '%m/%d/%Y')
                # print(now, previous)
                difference = (now - previous).days
                if abs(difference) < 10000:
                    days_from_first.append(difference)
                else:
                    patient_drop.append(patient_set.index[test])
            patient_set.drop(patient_drop, inplace=True)

            if pid != 126274:
                ages.extend(list(patient_set[clock]))
                dates.extend(days_from_first)

            if real_test and len(days_from_first) > 0 and len(list(patient_set[clock])) > 0 and pid != 126274:
                plt.title(clock + ' Over Time for PID:' + str(pid))
                plt.xlabel('Days since first test')
                if clock == 'DunedinPACE':
                    plt.ylabel(clock + ' Aging Rate')
                else:
                    plt.ylabel(clock)
                plt.grid(color='grey', linestyle='-', alpha=.5)

                plt.plot(days_from_first, list(patient_set[clock]))
                # plt.show()
                plt.savefig('Clock Figs/Individual Figs/' + clock + '/' + str(pid) + '.png')
                plt.close()

    return ages, dates


'''GENERATING THE POLYFIT BEST-FIT LINES'''
if not best_fit:
    grim_a, grim_b = np.polyfit(all_df['Decimal Chronological Age'], all_df['GrimAge PC'], 1)
    dun_a, dun_b = np.polyfit(all_df['Decimal Chronological Age'], all_df['DunedinPACE'], 1)
    for patient in all_df.index:
        all_df.loc[patient, 'GrimAge Residual'] = all_df.loc[patient, 'GrimAge PC'] - all_df.loc[patient, 'Decimal Chronological Age']  # all_df.loc[patient, 'Decimal Chronological Age']*grim_a + grim_b)
    for patient in all_df.index:
        all_df.loc[patient, 'DunedinPACE Residual'] = all_df.loc[patient, 'DunedinPACE'] - all_df.loc[patient, 'Decimal Chronological Age']  # all_df.loc[patient, 'Decimal Chronological Age']*dun_a + dun_b)
    grim_a, grim_b = np.polyfit(algo_df['Decimal Chronological Age'], algo_df['GrimAge PC'], 1)
    dun_a, dun_b = np.polyfit(algo_df['Decimal Chronological Age'], algo_df['DunedinPACE'], 1)
    for patient in algo_df.index:
        algo_df.loc[patient, 'GrimAge Residual'] = algo_df.loc[patient, 'GrimAge PC'] - algo_df.loc[patient, 'Decimal Chronological Age']  # algo_df.loc[patient, 'Decimal Chronological Age']*grim_a + grim_b)
    for patient in algo_df.index:
        algo_df.loc[patient, 'DunedinPACE Residual'] = algo_df.loc[patient, 'DunedinPACE'] - algo_df.loc[patient, 'Decimal Chronological Age']  # algo_df.loc[patient, 'Decimal Chronological Age']*dun_a + dun_b)
    grim_a, grim_b = np.polyfit(healthy['Decimal Chronological Age'], healthy['GrimAge PC'], 1)
    dun_a, dun_b = np.polyfit(healthy['Decimal Chronological Age'], healthy['DunedinPACE'], 1)
    for patient in healthy.index:
        healthy.loc[patient, 'GrimAge Residual'] = healthy.loc[patient, 'GrimAge PC'] - healthy.loc[patient, 'Decimal Chronological Age']  # healthy.loc[patient, 'Decimal Chronological Age']*grim_a + grim_b)
    for patient in healthy.index:
        healthy.loc[patient, 'DunedinPACE Residual'] = healthy.loc[patient, 'DunedinPACE'] - healthy.loc[patient, 'Decimal Chronological Age']  # (healthy.loc[pa tient, 'Decimal Chronological Age']*dun_a + dun_b)
    grim_a, grim_b = np.polyfit(diseased['Decimal Chronological Age'], diseased['GrimAge PC'], 1)
    dun_a, dun_b = np.polyfit(diseased['Decimal Chronological Age'], diseased['DunedinPACE'], 1)
    for patient in diseased.index:
        diseased.loc[patient, 'GrimAge Residual'] = diseased.loc[patient, 'GrimAge PC'] - diseased.loc[patient, 'Decimal Chronological Age'] # diseased.loc[patient, 'Decimal Chronological Age']*grim_a + grim_b)
    for patient in diseased.index:
        diseased.loc[patient, 'DunedinPACE Residual'] = diseased.loc[patient, 'DunedinPACE'] - diseased.loc[patient, 'Decimal Chronological Age']  # (diseased.loc[patient, 'Decimal Chronological Age']*dun_a + dun_b)
else:
    grim_a, grim_b = np.polyfit(all_df['Decimal Chronological Age'], all_df['GrimAge PC'], 1)
    dun_a, dun_b = np.polyfit(all_df['Decimal Chronological Age'], all_df['DunedinPACE'], 1)
    for patient in all_df.index:
        all_df.loc[patient, 'GrimAge Residual'] = all_df.loc[patient, 'GrimAge PC'] -(all_df.loc[patient, 'Decimal Chronological Age']*grim_a + grim_b)  # all_df.loc[patient, 'Decimal Chronological Age']
    for patient in all_df.index:
        all_df.loc[patient, 'DunedinPACE Residual'] = all_df.loc[patient, 'DunedinPACE'] -(all_df.loc[patient, 'Decimal Chronological Age']*dun_a + dun_b)  # all_df.loc[patient, 'Decimal Chronological Age']
    grim_a, grim_b = np.polyfit(algo_df['Decimal Chronological Age'], algo_df['GrimAge PC'], 1)
    dun_a, dun_b = np.polyfit(algo_df['Decimal Chronological Age'], algo_df['DunedinPACE'], 1)
    for patient in algo_df.index:
        algo_df.loc[patient, 'GrimAge Residual'] = algo_df.loc[patient, 'GrimAge PC'] -(algo_df.loc[patient, 'Decimal Chronological Age']*grim_a + grim_b)  # algo_df.loc[patient, 'Decimal Chronological Age']
    for patient in algo_df.index:
        algo_df.loc[patient, 'DunedinPACE Residual'] = algo_df.loc[patient, 'DunedinPACE'] -(algo_df.loc[patient, 'Decimal Chronological Age']*dun_a + dun_b)  # algo_df.loc[patient, 'Decimal Chronological Age']
    grim_a, grim_b = np.polyfit(healthy['Decimal Chronological Age'], healthy['GrimAge PC'], 1)
    dun_a, dun_b = np.polyfit(healthy['Decimal Chronological Age'], healthy['DunedinPACE'], 1)
    for patient in healthy.index:
        healthy.loc[patient, 'GrimAge Residual'] = healthy.loc[patient, 'GrimAge PC'] - (healthy.loc[patient, 'Decimal Chronological Age']*grim_a + grim_b)  # healthy.loc[patient, 'Decimal Chronological Age']
    for patient in healthy.index:
        healthy.loc[patient, 'DunedinPACE Residual'] = healthy.loc[patient, 'DunedinPACE'] - (healthy.loc[patient, 'Decimal Chronological Age']*dun_a + dun_b)   # healthy.loc[patient, 'Decimal Chronological Age']
    grim_a, grim_b = np.polyfit(diseased['Decimal Chronological Age'], diseased['GrimAge PC'], 1)
    dun_a, dun_b = np.polyfit(diseased['Decimal Chronological Age'], diseased['DunedinPACE'], 1)
    for patient in diseased.index:
        diseased.loc[patient, 'GrimAge Residual'] = diseased.loc[patient, 'GrimAge PC'] - (diseased.loc[patient, 'Decimal Chronological Age']*dun_a + dun_b) # diseased.loc[patient, 'Decimal Chronological Age']*grim_a + grim_b)
    for patient in diseased.index:
        diseased.loc[patient, 'DunedinPACE Residual'] = diseased.loc[patient, 'DunedinPACE'] - (diseased.loc[patient, 'Decimal Chronological Age']*dun_a + dun_b)  # diseased.loc[patient, 'Decimal Chronological Age'])


def plotting(dataframe=pd.DataFrame(), metric=''):
    ages, dates = make_data(dataframe, metric, True)

    print(len(ages), len(dates))

    diseased_standard_ages, diseased_standard_dates = make_data(diseased, metric, False)
    healthy_standard_ages, healthy_standard_dates = make_data(healthy, metric, False)
    tru_standard_ages, tru_standard_dates = make_data(all_df, metric, False)

    # print(len(diseased_standard_ages), len(diseased_standard_dates))

    red_line, green_line, blue_line = mpatches.Patch(color='red', label='Diseased Standard Slope'), mpatches.Patch(color='green', label='Healthy Standard Slope'), mpatches.Patch(color='blue', label='RMI Slope')
    # green_line, blue_line = mpatches.Patch(color='green', label='TruStandard Slope'), mpatches.Patch(color='blue', label='RMI Slope')
    fig, ax = plt.subplots()
    ax.legend(handles=[red_line, green_line, blue_line])
    # ax.legend(handles=[green_line, blue_line])

    plt.title(metric + ' Over Time')
    plt.xlabel('Days since first test')
    plt.ylabel(metric + ' Aging Rate')
    plt.grid(color='grey', linestyle='-', alpha=.35)

    trustandard_a, trustandard_b = np.polyfit(tru_standard_dates, tru_standard_ages, 1)
    diseased_standard_a, diseased_standard_b = np.polyfit(diseased_standard_dates, diseased_standard_ages, 1)
    healthy_standard_a, healthy_standard_b = np.polyfit(healthy_standard_dates, healthy_standard_ages, 1)
    a, b = np.polyfit(dates, ages, 1)

    # print(diseased_standard_ages)
    # print(diseased_standard_dates)

    # plt.plot(tru_standard_dates, pd.Series(tru_standard_dates)*trustandard_a + trustandard_b, 'g-')
    plt.plot(diseased_standard_dates, pd.Series(diseased_standard_dates)*diseased_standard_a + diseased_standard_b, 'r-', alpha=.8)
    plt.plot(healthy_standard_dates, pd.Series(healthy_standard_dates)*healthy_standard_a + healthy_standard_b, 'g-', alpha=.8)

    plt.figtext(0.7, 0.2, 'R: ' + str(round(np.corrcoef(dates, ages)[0][1], 4)) + ' | Slope: ' + str(round(a, 6)) +
                '\nRMI - Diseased Slope: ' + str(round(a - diseased_standard_a, 6)), horizontalalignment='center',
                bbox=dict(facecolor='gray', alpha=0.6))

    plt.scatter(dates, ages, c='r', marker='o', edgecolors='b', alpha=.5)
    plt.plot(dates, pd.Series(dates)*a + b, 'b-', alpha=.8)

    # fig.figtext(0.7, 0.8, 'R: ' + str(round(np.corrcoef(dates, ages)[0][1], 4)) + ' | Slope: ' + str(round(a, 6)), horizontalalignment='center')

    plt.show()
    fig.savefig('Clock Figs/Group Figs/' + metric + '.png')
    plt.close()


plotting(algo_df, 'DunedinPACE')
plotting(algo_df, 'DunedinPACE Residual')
plotting(algo_df, 'GrimAge Residual')

full_output = markdown.markdown('''
<center>
# **<font color='blue'>RMI Cohort Analysis</font>**
### <font color='blue'>TruDiagnostic - 2022-09-13</font>

***
***
***

## <ins><font color='blue'>Overview</font><ins>
This analysis includes the DunedinPACE and GrimAgePC clocks, separated by overall trends and individual figures. The overall \n
trends are compared to a "healthy" standard, the TruDiagnostic cohort, for reference. The Pearson correlation, slope of the \n
best fit line, and the difference between the Tru cohort and RMI cohort's slopes are included in the bottom right of these \n
overall figures. These outputs seem to indicate that a there is an active factor, and potentially common general characteristics \n
of the cohort that have lead to a lower immediate aging rate and a lower accumulated biological age. The "residual" values, or subtraction \n
of the observed clock's value and another standard value such as chronological age, were calculated using linear regressions of the \n
respective datasets in the form of *best_fit_residual = chrono_age x dataset_slope + dataset_intercept*. This serves to standardize \n
the trendlines generated, reduce inter-set noise, and enhance trend visibility/statistical significance. 
<br>

### <ins><font color='blue'>DunedinPACE Results</font><ins>
This clock generates an aging rate based on a pheno-score that is calculated based on organ integrity/physiological function. \n
The slowing of aging observed in the RMI cohort indicates that patients should be experiencing lower rates of incident morbidity \n
and will tend to have higher physical functioning. The residual, calculated using the same method described in the "Overview" section, \n
corroborates the findings in the original values that the RMI cohort seems to have a relatively healthy rate of aging and organ integrity, \n
but is more similar to the diseased Tru cohort than the healthy cohort. In sum, the RMI cohort shows a relatively at-risk, but still overall \n
healthy pace of aging. 
<br>

### <ins><font color='blue'>GrimAge Results</font><ins>
This clock is trained on "time-to-death", meaning it is highly predictive of all-cause mortality, and thus the comorbidities that \n
contribute to it, particularly type 2 diabetes, heart disease, and cancer. The observed trend in the RMI cohort for this measure was \n
much lower than global and Tru standards, indicating a particular improvement in the probability of death by any cause, and the probability \n 
of developing the previously stated comorbidities. 
<br> 
***
***
***
<br>
<br>
<br>
## <ins><font color='blue'><font size="6">*Epigenetic Clock Outputs*</font></font></ins>
''')


clock_figs = glob('Clock Figs/Group Figs/*.png')
grim_figs = glob('Clock Figs/Individual Figs/GrimAge PC/*.png')
dune_figs = glob('clock figs/Individual Figs/DunedinPACE/*.png')
# dune_figs = ['https://ibb.co/3f4B4LJ',
#              'https://ibb.co/vLxT6Wt',
#              'https://ibb.co/BssPCpF',
#              'https://ibb.co/sCq9gjW',
#              'https://ibb.co/K5qp4cT',
#              'https://ibb.co/Q8w8cZR',
#              'https://ibb.co/Sv0qb1M',
#              'https://ibb.co/LdBhTrx',
#              'https://ibb.co/M52KWLq',
#              'https://ibb.co/Wthf9j9',
#              'https://ibb.co/zZywMy1',
#              'https://ibb.co/b7ndXrj',
#              'https://ibb.co/1Xmmhvq',
#              'https://ibb.co/h2WPr45',
#              'https://ibb.co/JpJJpPw',
#              "https://ibb.co/Rj93QXF",
#              "https://ibb.co/kJzd74y",
#              "https://ibb.co/SrHDyy7",
#              'https://ibb.co/bJ4c3F2',
#              'https://ibb.co/McKFgJj',
#              'https://ibb.co/GvnFtgp',
#              'https://ibb.co/Rh6dyJ4',
#              'https://ibb.co/bWL7Z9L']
# grim_figs = ['https://ibb.co/CH2g3pF',
#              'https://ibb.co/vz8sLk5',
#              'https://ibb.co/TkbfntP',
#              'https://ibb.co/fvcwwLB',
#              'https://ibb.co/dMVr5nJ',
#              'https://ibb.co/v30ffpD',
#              'https://ibb.co/Cnggx83',
#              "https://ibb.co/bHm2fwq",
#              "https://ibb.co/QvTtQCS",
#              "https://ibb.co/NT2hYTt",
#              "https://ibb.co/qr0s16f",
#              "https://ibb.co/xYdgx1K",
#              "https://ibb.co/g70wq50",
#              "https://ibb.co/JmQV7zL",
#              'https://ibb.co/7K8qnW5',
#              'https://ibb.co/yPGZ3vb',
#              'https://ibb.co/B4sJnP2',
#              "https://ibb.co/8KW0QQ8",
#              "https://ibb.co/72n8KpL",
#              "https://ibb.co/42VZSPJ",
#              "https://ibb.co/kM2nTrB",
#              'https://ibb.co/DkmwqBZ',
#              'https://ibb.co/h1kvxn4']
print(grim_figs)
print(dune_figs)
grim_first_done = False
dune_first_done = False

total_paths = len(clock_figs)
for pic_path in reversed(clock_figs):
    if pic_path == 'Clock Figs/Group Figs\DunedinPACE.png':
        figure = markdown.markdown(
            '<kbd><img src="' + pic_path + '" width="500"></kbd><br><br><font size="5">' +
            'There was a very slight overall decrease in the rate of aging with a very low correlation coefficient. \n'
            'This could indicate the presence of an anti-aging influence, since generally, as individuals age, their \n'
            'DunedinPACE values increase. The average aging rate is even lower than the "healthy" standard established \n'
            'by the Tru Cohort.'
            '</font>'
        )
    elif pic_path == 'Clock Figs/Group Figs\GrimAgePC.png':
        figure = markdown.markdown(
            '<kbd><img src="' + pic_path + '" width="500"></kbd><br><br><font size="5">' +
            'The GrimAge PC output for the RMI cohort was lower than the expected global and Tru \n'
            'standards. This indicates the probability of the presence of an anti-aging factor.</font>'
        )
    elif pic_path == 'Clock Figs/Group Figs\DunedinPACE Residual.png':
        figure = markdown.markdown(
            '<kbd><img src="' + pic_path + '" width="500"></kbd><br><br><font size="5">' +
            'The dataset-adjusted DunedinPACE residual demonstrates further that the aging rate of the RMI cohort shows \n'
            'the most similarity with a "healthy" diseased cohort, indicating potential risk to the integrity of the 19 organ \n'
            'systems the clock was built on.</font>'
        )
    else:
        print('WHAT')
        exit()
    full_output += figure
full_output += '<table><tr>'

x = 1
total_paths = len(grim_figs)
for pic_path in grim_figs:
    pic_path = str(pic_path)
    print(pic_path)
    if grim_first_done:
        figure = markdown.markdown(
            '<td><img src="' + pic_path + '"><br><br><font size="5"></td>'
        )
    else:
        figure = markdown.markdown(
            '<ins><font color="blue"><font size="6">*Individual GrimAge Figures*</font></font></ins> <br> <td><img src="' + pic_path + '"><br><br><font size="5"></td>'
        )
        grim_first_done = True
    full_output += figure

    if x == total_paths-1:
        full_output += '</tr></table>\n'
    elif x % 3 == 0 and x != 0:
        full_output += '</tr></table>'
        full_output += '<table><tr>'
    x += 1

full_output += '<table><tr>'
x = 1
total_paths = len(dune_figs)
for pic_path in dune_figs:
    pic_path = str(pic_path)
    print(pic_path)
    if dune_first_done:
        figure = markdown.markdown(
            '<td><img src="' + pic_path + '"><br><br><font size="5"></td>'
        )
    else:
        figure = markdown.markdown(
            '<ins><font color="blue"><font size="6">*Individual DunedinPACE Figures*</font></font></ins> <br> <td><img src="' + pic_path + '"><br><br><font size="5"></td>'
        )
        dune_first_done = True
    full_output += figure

    if x == total_paths-1:
        full_output += '</tr></table>\n'
    elif x % 3 == 0 and x != 0:
        full_output += '</tr></table>'
        full_output += '<table><tr>'

    x += 1

# print(full_output)
# full_output += markdown.markdown('''
# <br>
# <br>
# <br>
# <br>
# ***
# ***
# ***
# <br>
# <br>
# <br>
# ## <ins><font color='blue'><font size="6">*Immune Subset Outputs*</font></font></ins>
# ''')


def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        source_html,  # the HTML to convert
        dest=result_file)  # file handle to recieve result

    # close output file
    result_file.close()  # close output file

    # return False on success and True on errors
    return pisa_status.err


full_output += markdown.markdown('</center>')
with open('RMIAnalysis.html', 'w') as f:
    f.write(full_output)

convert_html_to_pdf(full_output, 'RMIAnalysis.pdf')

exit()


# print(patient_indices)
#
# count_org = {}
# for k in patient_indices.keys():
#     count_org[k] = len(patient_indices[k])
#     print(patient_indices[k])
# print('Count org: ', count_org)
#
# idols = ['Immune.CD8T',
#          'Immune.CD4T',
#          'Immune.NK',
#          'Immune.Bcell',
#          'Immune.Neutrophil',
#          'Immune.CD4T.CD8T',
#          'Telomere Values PC']
#
# print(residuals)
# for patient in algo_df.index:
#     for idol in idols:
#         residuals.loc[patient, idol] = algo_df.loc[patient, idol]
# residuals.to_csv('RMIResiduals+IDOLS.csv')
#
# print(patient_indices)
#
# most_tests = np.max(list(count_org.values()))
# print(most_tests)
# for x in reversed(range(most_tests)):
#     if list(count_org.values()).count(x) > 1:
#         most_shared_tests = x
#         break
# print('Most number of shared tests: ', most_shared_tests)
#
# group_1, group_2, group_3 = [], [], []
# for patient in patient_indices:
#     tests = patient_indices[patient]
#     try:
#         group_1.append(tests[0])
#         group_2.append(tests[1])
#         group_3.append(tests[2])
#     except Exception as e:
#         print(e)
