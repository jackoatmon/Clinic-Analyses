import pandas as pd
import numpy as np
import sklearn.metrics
from scipy import stats
import matplotlib.pyplot as plt

data = pd.read_csv('PopulationData_84790.csv').set_index('Patient ID')
sexes = pd.read_csv('C:/Users/jack/PycharmProjects/TruDiagnostic/Covariate Models/Blood Type/Data/PatientMetaData_052322.csv', encoding='cp1252').set_index('PID').loc[:, 'Biological Sex']
measures = ['Hannum PC',
            'Horvath PC',
            'GrimAge PC ',
            'PhenoAge PC',
            'DunedinPoAm',
            'Telomere Values PC',
            'Full_CumulativeStemCellDivisions',
            'Avg_LifeTime_IntrinsicStemCellDivisionRate',
            'Median_Lifetime_IntrinsicStemCellDivisionRate',
            'Immune.CD8T',
            'Immune.CD4T',
            'Immune.CD4T.CD8T',
            'Immune.NK',
            'Immune.Bcell',
            'Immune.Mono',
            'Immune.Neutrophil']
methods = ['Chrono', 'Best fit']

statVals = pd.DataFrame(columns=measures, index=['T-test',
                                                 'T-test p-Value',
                                                 'Wilcoxon',
                                                 'Wilcoxon p-Value'])

new_df = data.copy()
print('New: ', new_df)
for method in methods:
    for measure in measures:
        print(measure)
        x_vals = []
        meta_times = []

        first_group = []
        second_group = []
        times_between = []
        num_male = 0
        total = 0
        a, b = np.polyfit(data['Decimal Chronological Age'], data[measure], 1)

        for idx in np.unique(data['PID']):
            group = data[data['PID'] == idx].sort_values(by='Decimal Chronological Age')
            for patient in group.index:
                for clock in measures[:4]:
                    if method == 'Chrono':
                        group.loc[patient, clock + ' Residual ' + method] = group.loc[patient, clock] - group.loc[patient, 'Decimal Chronological Age']
                    else:
                        group.loc[patient, clock + ' Residual ' + method] = group.loc[patient, clock] - (a*group.loc[patient, 'Decimal Chronological Age']+b)


            if len(group) > 1:
                if sexes.loc[idx].lower() == 'male':
                    num_male += 1
                total += 1

                first, second = group.iloc[0][measure], group.iloc[-1][measure]

                new_df.loc[group.index[0], 'Test'], new_df.loc[group.index[-1], 'Test'] = 0, 1
                if len(group) > 3:
                    try:
                        new_df.drop(index=group.index[1:-1], inplace=True)
                    except:
                        pass
                elif len(group) > 2:
                    try:
                        new_df.drop(index=group.index[1], inplace=True)
                    except:
                        pass

                first_age, last_age = group.iloc[0]['Decimal Chronological Age'], group.iloc[-1]['Decimal Chronological Age']
                time_between = (last_age - first_age) * 365
                if group.iloc[-1]['Decimal Chronological Age'] - group.iloc[0]['Decimal Chronological Age'] < 0:
                    print("Error in testing order, fix here")

                firstIdx, secondIdx = group[group[measure] == first].index, group[group[measure] == second].index
                if measure in measures[:4]:
                    first_chrono_age = data.loc[firstIdx, 'Decimal Chronological Age']
                    second_chrono_age = data.loc[secondIdx, 'Decimal Chronological Age']

                    if method == 'Best fit':
                        first_val = a * first_chrono_age + b
                        second_val = a * second_chrono_age + b
                        first = first - first_val
                        second = second - second_val
                    else:
                        first = first - first_chrono_age
                        second = second - second_chrono_age

                # Generate individual-based statistical significances
                times = []
                for gap in range(len(group)-1):
                    first_val = group.iloc[gap][measure]
                    second_val = group.iloc[gap+1][measure]

                    time1, time2 = group.iloc[gap]['Decimal Chronological Age'], group.iloc[gap+1]['Decimal Chronological Age']
                    days_between = (time2 - time1) * 365
                    times.append(round(days_between))

                dates = []
                for d in range(len(group)):
                    dates.append(group.iloc[d]['Decimal Chronological Age'])
                start = dates[0]
                for d in range(len(dates)):
                    dates[d] = (dates[d] - start) * 365
                meta_times.append(dates)

                time_across = [0]
                for x in range(len(times)):
                    passed = times[x]
                    if x == 0:
                        time_across.append(passed)
                    else:
                        time_across.append(passed+time_across[x])

                if measure in measures[:4]:
                    metric_values = group.sort_values(by='Decimal Chronological Age')[measure + ' Residual ' + method]
                else:
                    metric_values = group.sort_values(by='Decimal Chronological Age')[measure]

                correlation = round(np.corrcoef(time_across, metric_values)[0][1], 4)
                x_vals.append(list(metric_values))

                plt.plot(metric_values)
                plt.grid(color='grey', linestyle='-', alpha=.5)

                # a, b = np.polyfit([1, 2], [first_avg, second_avg], 1)
                # box.plot([1, 2], pd.Series([1, 2]) * a + b, 'r-')

                # box.set_xticklabels(range(len(group)))
                plt.title('Longitudinal Analysis of ' + measure + '\nPearson correlation with time: ' + str(correlation))

                plt.figtext(0.5, 0.001, 'PID: ' + str(idx) + '\nTimes between tests in days: ' + str(times), horizontalalignment='center')

                # plt.show()
                plt.savefig('Individual Figs/' + method + measure + str(group['PID'][0]) + '.png')
                plt.close()

                first_group.append(float(first))
                second_group.append(float(second))
                times_between.append(time_between)
            else:
                try:
                    new_df.drop(index=list(data[data['PID'] == idx].index), inplace=True)
                    # print('Worked at least once')
                except Exception as e:
                    # print(e, list(data[data['PID'] == idx].index))
                    pass

        # print(len(first_group))
        # print(len(second_group))
        # print(second_group)

        t_val, t_p = stats.ttest_rel(first_group, second_group)
        kk_val, kk_p = stats.wilcoxon(first_group, second_group)

        avg_time = round(np.mean(times_between))
        max_time = round(np.max(times_between))
        min_time = round(np.min(times_between))
        std_time = round(np.std(times_between))

        # print(avg_time)
        # print(max_time)
        # print(min_time)
        # print(std_time)
        # print(first_group[:5], second_group[:5])
        # print(t_val, t_p, '\n')

        if measure in measures[:4] and method == 'Best fit':
            statVals.loc['T-test', measure + ' Best fit'] = t_val
            statVals.loc['T-test p-Value', measure + ' Best fit'] = t_p
            statVals.loc['Wilcoxon', measure + ' Best fit'] = kk_val
            statVals.loc['Wilcoxon p-Value', measure + ' Best fit'] = kk_p
        else:
            statVals.loc['T-test', measure] = t_val
            statVals.loc['T-test p-Value', measure] = t_p
            statVals.loc['Wilcoxon', measure] = kk_val
            statVals.loc['Wilcoxon p-Value', measure] = kk_p

        fig = plt.figure()
        box = fig.add_subplot()
        box.boxplot([first_group, second_group])

        first_avg = np.mean(first_group)
        second_avg = np.mean(second_group)
        a, b = np.polyfit([1, 2], [first_avg, second_avg], 1)
        box.plot([1, 2], pd.Series([1, 2]) * a + b, 'r-')

        print('Percent male: ', num_male / total * 100)

        box.set_xticklabels(['First Test', 'Second Test'])
        box.set_title('First to last test comparison for ' + measure + '\nT-test, Wilcoxon p-Vals: ' + str(round(t_p, 3))
                      + ', ' + str(round(kk_p, 3)) + ' | First, second mean: ' + str(round(first_avg, 4))
                      + ', ' + str(round(second_avg, 3)))

        # plt.figtext(0.5, 0.01, 'Avg, max, min, std times between tests in days: ' + str(avg_time) + ', ' + str(max_time)
        #             + ', ' + str(min_time) + ', ' + str(std_time), horizontalalignment='center')

        # plt.show()

        if t_p < .05 or kk_p < .05:
            if measure in measures[:4] and method == 'Best fit':
                plt.savefig('Best fit EAR figs/' + measure + ' (best fit).png')
                print(measure, method, t_p, kk_p)
            elif measure in measures[:4] and method == 'Chrono':
                plt.savefig('Chrono EAR figs/' + measure + ' (chrono).png')
                print(measure, method, t_p, kk_p)
            else:
                print(measure, method, t_p, kk_p)
                plt.savefig('Figures/' + measure + '.png')
        else:
            if measure in measures[:4] and method == 'Best fit':
                plt.savefig('Best fit EAR figs (ns)/' + measure + ' (best fit).png')
                print(measure, method, t_p, kk_p)
            elif measure in measures[:4] and method == 'Chrono':
                plt.savefig('Chrono EAR figs (ns)/' + measure + ' (chrono).png')
                print(measure, method, t_p, kk_p)
            else:
                print(measure, method, t_p, kk_p)
                plt.savefig('Figures (ns)/' + measure + '.png')

        # plt.show()
        plt.close()

        plt.title('Longitudinal Analysis of ' + measure)
        plt.grid(color='grey', linestyle='-', alpha=.5)
        plt.xlabel('Time in days from first test')
        plt.ylabel(measure + ' Values')
        for x in range(len(x_vals)):
            x_set, time = x_vals[x], meta_times[x]
            plt.plot(time, x_set, alpha=.8)
        # plt.show()
        plt.savefig('Collective Individual Figures/' + method + measure + '.png')

            # a, b = np.polyfit([1, 2], [first_avg, second_avg], 1)
            # box.plot([1, 2], pd.Series([1, 2]) * a + b, 'r-')

            # box.set_xticklabels(range(len(group)))


new_df.to_csv('ToddsPopData.csv')
statVals.to_csv('LongitudinalCohort.csv')


