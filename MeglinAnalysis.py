import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from datetime import datetime
import markdown

meglin = pd.read_csv('MeglinCohort.csv').set_index('Patient ID')
firsts = meglin[meglin['Test Number'] == 1]
seconds = meglin[meglin['Test Number'] == 2]

metrics = ['Telomere Values',
           'Telomere Values PC',
           'Extrinsic Age',
           'Intrinsic Age',
           'Hannum PC',
           'Horvath PC',
           'GrimAge PC ',
           'PhenoAge PC',
           'IEAA_PC',
           'EEAA_PC',
           'DunedinPoAm',
           'Intrinsic_IEAA',
           'Extrinsic_IEAA',
           'Extrinsic_EEAA',
           'Full_CumulativeStemCellDivisions',
           'Avg_LifeTime_IntrinsicStemCellDivisionRate',
           'Median_Lifetime_IntrinsicStemCellDivisionRate',
           'MitoticScore_OldEpitoc',
           'HypoClock_Score_Old',
           'Immune.CD8T',
           'Immune.CD4T',
           'Immune.CD4T.CD8T',
           'Immune.NK',
           'Immune.Bcell',
           'Immune.Mono',
           'Immune.Neutrophil',
           'Immune.Eosino',
           'Alcohol.MRS']

first_names = []
first_dates = []
second_dates = []
diffs = []

for patient2 in seconds.index:
    pid2 = meglin.loc[patient2, 'PID']
    second_dates.append(meglin.loc[patient2, 'Collection Date'])
    # second_val = meglin.loc[patient2, metric]
    for patient1 in firsts.index:
        if pid2 == meglin.loc[patient1, 'PID']:
            first_names.append(patient1)
            first_dates.append(meglin.loc[patient1, 'Collection Date'])
            break

for x in range(len(first_dates)):
    date1 = datetime.strptime(first_dates[x], '%m/%d/%Y')
    date2 = datetime.strptime(second_dates[x], '%m/%d/%Y')
    diffs.append(int((date2 - date1).days))

avg_time = round(np.average(diffs))
sample_size = len(first_names)
for metric in metrics:
    first_vals = meglin.loc[first_names, metric]
    second_vals = meglin.loc[seconds.index, metric]
    ages = meglin.loc[first_names, 'Decimal Chronological Age']

    if metric in metrics[2:8]:
        print(metric)
        first_residuals = first_vals - ages
        second_residuals = second_vals - ages
        print(first_residuals)

        # PUT THE WHOLE PROCESS HERE AGAIN
    try:
        tt, tt_p = stats.ttest_rel(first_vals, second_vals)
        tt, tt_p = round(tt, 4), round(tt_p, 4)
        Kruskal, Kruskal_P = stats.kruskal(first_vals, second_vals)
        Kruskal, Kruskal_P = round(Kruskal, 4), round(Kruskal_P, 4)
    except Exception as e:
        print(e)
        tt, tt_p = 0,0
        tt, tt_p = 0,0
        Kruskal, Kruskal_P = 0,0
        Kruskal, Kruskal_P = 0,0

    avg1, avg2 = np.average(first_vals), np.average(second_vals)
    trend = round(avg2 - avg1, 3)
    fig = plt.figure()
    # fig.subplots_adjust(bottom=150, top=200)
    box = fig.add_subplot()

    labels = ['Test 1', 'Test 2']
    vals = [first_vals, second_vals]

    box.boxplot(vals, labels=labels)
    box.plot([1, 2], [avg1, avg2], color='red')
    box.grid(color='grey', axis='y', linestyle='-', alpha=.5)
    plt.figtext(0.5, 0.01, 'Sample size: ' + str(sample_size) + ' || Avg days between tests: ' + str(avg_time), horizontalalignment='center')

    if metric in metrics[20:-1]:
        box.set_title('Cell values for ' + metric + ', ' + '\nT-test p-Val: ' + str(tt_p) + ' || Kruskal p-Val: ' + str(Kruskal_P) + ' || Trend: ' + str(trend))
        # if Kruskal_P < .05 or tt_p < .05:
            # plt.savefig('significant figures/Immune Subsets/' + metric + '.png')
        # else:
            # plt.savefig('non-significant figures/Immune Subsets/' + metric + '.png')

    elif metric in metrics[15:20]:
        box.set_title('Mitotic values for ' + metric + ', ' + '\nT-test p-Val: ' + str(tt_p) + ' || Kruskal p-Val: ' + str(Kruskal_P) + ' || Trend: ' + str(trend))
        # if Kruskal_P < .05 or tt_p < .05:
            # plt.savefig('significant figures/Mitotic Clocks/' + metric + '.png')
        # else:
            # plt.savefig('non-significant figures/Mitotic Clocks/' + metric + '.png')

    elif metric == 'Alcohol.MRS':
        box.set_title('Risk score for ' + metric + ', ' + '\nT-test p-Val: ' + str(tt_p) + ' || Kruskal p-Val: ' + str(Kruskal_P) + ' || Trend: ' + str(trend))
        # if Kruskal_P < .05 or tt_p < .05:
            # plt.savefig('significant figures/' + metric + '.png')
        # else:
            # plt.savefig('non-significant figures/' + metric + '.png')
    else:
        if metric in ['Telomere Values', 'Telomere Values PC']:
            box.set_title('Lengths for ' + metric + ', ' + '\nT-test p-Val: ' + str(tt_p) + ' || Kruskal p-Val: ' + str(Kruskal_P) + ' || Trend: ' + str(trend))
        elif metric in ['DunedinPACE', 'Intrinsic_IEAA', 'Extrinsic_IEAA', 'Extrinsic_EEAA']:
            box.set_title('Aging Rate for ' + metric + ', ' + '\nT-test p-Val: ' + str(tt_p) + ' || Kruskal p-Val: ' + str(Kruskal_P) + ' || Trend: ' + str(trend))
        else:
            box.set_title('Residuals for ' + metric + ', ' + '\nT-test p-Val: ' + str(tt_p) + ' || Kruskal p-Val: ' + str(Kruskal_P) + ' || Trend: ' + str(trend))
        # if Kruskal_P < .05 or tt_p < .05:
            # plt.savefig('significant figures/Clocks/' + metric + '.png')
        # else:
            # plt.savefig('non-significant figures/Clocks/' + metric + '.png')
    # plt.show()
    plt.close()




















