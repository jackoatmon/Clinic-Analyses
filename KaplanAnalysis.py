import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import markdown
import glob
from scipy import stats

metadata = pd.read_csv('Metadata.csv', encoding='cp1252').set_index('PatientID')
allpopdata = pd.read_csv('PopulationData.csv').set_index('Patient ID')
ages = pd.read_csv('KaplanPopulationData.csv').set_index('Patient ID')
healthy = list(pd.read_csv('HealthyAboveAverage.csv')['Patient ID'])
avg = list(pd.read_csv('HealthyAverage.csv')['Patient ID'])
b_avg = list(pd.read_csv('BelowAverageRange.csv')['Patient ID'])

# print('Original number of patients: ', len(ages))
# shared = list(set(ages.index) & set(metadata.index))
# print('Number of overlapping patients: ', len(shared))

plt.hist(ages['Decimal Chronological Age'])
plt.title('Age Demographics for Kaplan Cohort')
plt.xlabel('Age in years')
plt.ylabel('Number of Patients')
plt.savefig('Kaplan Age Demographics.png')
plt.close()

plt.bar(x=['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'], height=[len(ages.index), len(healthy), len(avg), len(b_avg)])
plt.title('Sample Size Demographics')
plt.ylabel('Number of Samples')
plt.figtext(0.5, 0.01, 'Sample sizes: ' + str(len(ages.index)) + ', ' + str(len(healthy)) + ', ' + str(len(avg)) + ', ' + str(len(b_avg)), horizontalalignment='center')
plt.savefig('SampleSizeDemographics.png')
plt.close()

healthy_hor = allpopdata.loc[healthy, 'Intrinsic Age']
healthy_han = allpopdata.loc[healthy, 'Extrinsic Age']
healthy_dun = allpopdata.loc[healthy, 'DunedinPoAm']
healthy_cd8 = allpopdata.loc[healthy, 'Immune.CD8T']
healthy_cd4 = allpopdata.loc[healthy, 'Immune.CD4T']
healthy_cdr = allpopdata.loc[healthy, 'Immune.CD4T.CD8T']
healthy_cdr_filtered = allpopdata[allpopdata['Immune.CD4T.CD8T']<30].loc[healthy, 'Immune.CD4T.CD8T']
healthy_nkc = allpopdata.loc[healthy, 'Immune.NK']
healthy_bce = allpopdata.loc[healthy, 'Immune.Bcell']
healthy_bce_filtered = allpopdata[allpopdata['Immune.Bcell']<40]
share = list(set(healthy_bce_filtered.index) & set(healthy))
healthy_bce_filtered = healthy_bce_filtered.loc[share, 'Immune.Bcell']
healthy_mon = allpopdata.loc[healthy, 'Immune.Mono']
healthy_neu = allpopdata.loc[healthy, 'Immune.Neutrophil']

avg_hor = allpopdata.loc[avg, 'Intrinsic Age']
avg_han = allpopdata.loc[avg, 'Extrinsic Age']
avg_dun = allpopdata.loc[avg, 'DunedinPoAm']
avg_cd8 = allpopdata.loc[avg, 'Immune.CD8T']
avg_cd4 = allpopdata.loc[avg, 'Immune.CD4T']
avg_cdr = allpopdata.loc[avg, 'Immune.CD4T.CD8T']
avg_cdr_filtered = allpopdata[allpopdata['Immune.CD4T.CD8T']<30]
share = list(set(avg_cdr_filtered.index) & set(avg))
avg_cdr_filtered = avg_cdr_filtered.loc[share, 'Immune.CD4T.CD8T']
avg_nkc = allpopdata.loc[avg, 'Immune.NK']
avg_bce = allpopdata.loc[avg, 'Immune.Bcell']
avg_bce_filtered = allpopdata[allpopdata['Immune.Bcell']<40]
share = list(set(avg_bce_filtered.index) & set(avg))
avg_bce_filtered = avg_bce_filtered.loc[share, 'Immune.Bcell']
avg_mon = allpopdata.loc[avg, 'Immune.Mono']
avg_neu = allpopdata.loc[avg, 'Immune.Neutrophil']

b_avg_hor = allpopdata.loc[b_avg, 'Intrinsic Age']
b_avg_han = allpopdata.loc[b_avg, 'Extrinsic Age']
b_avg_dun = allpopdata.loc[b_avg, 'DunedinPoAm']
b_avg_cd8 = allpopdata.loc[b_avg, 'Immune.CD8T']
b_avg_cd4 = allpopdata.loc[b_avg, 'Immune.CD4T']
b_avg_cdr = allpopdata.loc[b_avg, 'Immune.CD4T.CD8T']
b_avg_cdr_filtered = allpopdata[allpopdata['Immune.CD4T.CD8T']<30]
share = list(set(b_avg_cdr_filtered.index) & set(b_avg))
b_avg_cdr_filtered = b_avg_cdr_filtered.loc[share, 'Immune.CD4T.CD8T']
b_avg_nkc = allpopdata.loc[b_avg, 'Immune.NK']
b_avg_bce = allpopdata.loc[b_avg, 'Immune.Bcell']
b_avg_bce_filtered = allpopdata[allpopdata['Immune.Bcell']<40]
share = list(set(b_avg_bce_filtered.index) & set(b_avg))
b_avg_bce_filtered = b_avg_bce_filtered.loc[share, 'Immune.Bcell']
b_avg_mon = allpopdata.loc[b_avg, 'Immune.Mono']
b_avg_neu = allpopdata.loc[b_avg, 'Immune.Neutrophil']

individual_comparison = pd.DataFrame(index=ages.index, columns=['Average Horvath Difference',
                                                                'Healthy Horvath Difference',
                                                                'Unhealthy Horvath Difference',
                                                                'Average Hannum Difference',
                                                                'Healthy Hannum Difference',
                                                                'Unhealthy Hannum Difference',
                                                                'Average DunedinPACE Difference',
                                                                'Healthy DunedinPACE Difference',
                                                                'Unhealthy DunedinPACE Difference',
                                                                'Average Immune.CD8T Difference',
                                                                'Healthy Immune.CD8T Difference',
                                                                'Unhealthy Immune.CD8T Difference',
                                                                'Average Immune.CD4T Difference',
                                                                'Healthy Immune.CD4T Difference',
                                                                'Unhealthy Immune.CD4T Difference',
                                                                'Average Immune.CD4T.CD8T Difference',
                                                                'Healthy Immune.CD4T.CD8T Difference',
                                                                'Unhealthy Immune.CD4T.CD8T Difference',
                                                                'Average Immune.NK Difference',
                                                                'Healthy Immune.NK Difference',
                                                                'Unhealthy Immune.NK Difference',
                                                                'Average Immune.Bcell Difference',
                                                                'Healthy Immune.Bcell Difference',
                                                                'Unhealthy Immune.Bcell Difference',
                                                                'Average Immune.Mono Difference',
                                                                'Healthy Immune.Mono Difference',
                                                                'Unhealthy Immune.Mono Difference',
                                                                'Average Immune.Neutrophil Difference',
                                                                'Healthy Immune.Neutrophil Difference',
                                                                'Unhealthy Immune.Neutrophil Difference',
                                                                ])

kap_hor = ages['Intrinsic Age']
kap_han = ages['Extrinsic Age']
kap_dun = ages['DunedinPoAm']
kap_cd8 = ages['Immune.CD8T']
kap_cd4 = ages['Immune.CD4T']
kap_cdr = ages['Immune.CD4T.CD8T']
kap_cdr_filtered = ages[ages['Immune.CD4T.CD8T']<30]['Immune.CD4T.CD8T']
kap_nkc = ages['Immune.NK']
kap_bce = ages['Immune.Bcell']
kap_bce_filtered = ages[ages['Immune.Bcell']<40]['Immune.Bcell']
kap_mon = ages['Immune.Mono']
kap_neu = ages['Immune.Neutrophil']

for patient in ages.index:
    hor, han, dun = ages.loc[patient, 'Intrinsic Age'], ages.loc[patient, 'Extrinsic Age'], ages.loc[patient, 'DunedinPoAm']
    individual_comparison.loc[patient, 'Average Horvath Difference'] = hor - np.average(avg_hor)
    individual_comparison.loc[patient, 'Healthy Horvath Difference'] = hor - np.average(healthy_hor)
    individual_comparison.loc[patient, 'Unhealthy Horvath Difference'] = hor - np.average(b_avg_hor)
    individual_comparison.loc[patient, 'Average Hannum Difference'] = han - np.average(avg_han)
    individual_comparison.loc[patient, 'Healthy Hannum Difference'] = han - np.average(healthy_han)
    individual_comparison.loc[patient, 'Unhealthy Hannum Difference'] = han - np.average(b_avg_han)
    individual_comparison.loc[patient, 'Average DunedinPACE Difference'] = dun - np.average(avg_dun)
    individual_comparison.loc[patient, 'Healthy DunedinPACE Difference'] = dun - np.average(healthy_dun)
    individual_comparison.loc[patient, 'Unhealthy DunedinPACE Difference'] = dun - np.average(b_avg_dun)
    individual_comparison.loc[patient, 'Average Immune.CD8T Difference'] = dun - np.average(avg_cd8)
    individual_comparison.loc[patient, 'Healthy Immune.CD8T Difference'] = dun - np.average(healthy_cd8)
    individual_comparison.loc[patient, 'Unhealthy Immune.CD8T Difference'] = dun - np.average(b_avg_cd8)
    individual_comparison.loc[patient, 'Average Immune.CD4T Difference'] = dun - np.average(avg_cd4)
    individual_comparison.loc[patient, 'Healthy Immune.CD4T Difference'] = dun - np.average(healthy_cd4)
    individual_comparison.loc[patient, 'Unhealthy Immune.CD4T Difference'] = dun - np.average(b_avg_cd4)
    individual_comparison.loc[patient, 'Average Immune.CD4T.CD8T Difference'] = dun - np.average(avg_cdr)
    individual_comparison.loc[patient, 'Healthy Immune.CD4T.CD8T Difference'] = dun - np.average(healthy_cdr)
    individual_comparison.loc[patient, 'Unhealthy Immune.CD4T.CD8T Difference'] = dun - np.average(b_avg_cdr)
    individual_comparison.loc[patient, 'Average Immune.NK Difference'] = dun - np.average(avg_nkc)
    individual_comparison.loc[patient, 'Healthy Immune.NK Difference'] = dun - np.average(healthy_nkc)
    individual_comparison.loc[patient, 'Unhealthy Immune.NK Difference'] = dun - np.average(b_avg_nkc)
    individual_comparison.loc[patient, 'Average Immune.Mono Difference'] = dun - np.average(avg_mon)
    individual_comparison.loc[patient, 'Healthy Immune.Mono Difference'] = dun - np.average(healthy_mon)
    individual_comparison.loc[patient, 'Unhealthy Immune.Mono Difference'] = dun - np.average(b_avg_mon)
    individual_comparison.loc[patient, 'Average Immune.Bcell Difference'] = dun - np.average(avg_bce)
    individual_comparison.loc[patient, 'Healthy Immune.Bcell Difference'] = dun - np.average(healthy_bce)
    individual_comparison.loc[patient, 'Unhealthy Immune.Bcell Difference'] = dun - np.average(b_avg_bce)
    individual_comparison.loc[patient, 'Average Immune.Neutrophil Difference'] = dun - np.average(avg_neu)
    individual_comparison.loc[patient, 'Healthy Immune.Neutrophil Difference'] = dun - np.average(healthy_neu)
    individual_comparison.loc[patient, 'Unhealthy Immune.Neutrophil Difference'] = dun - np.average(b_avg_neu)

individual_comparison.to_csv('KaplanComparison NEW.csv')

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_dun, healthy_dun, avg_dun, b_avg_dun])
box.plot([1, 2], [np.median(kap_dun), np.median(healthy_dun)], 'b-')
box.plot([1, 3], [np.median(kap_dun), np.median(avg_dun)], 'g-')
box.plot([1, 4], [np.median(kap_dun), np.median(b_avg_dun)], 'r-')
box.set_title('DunedinPACE Kaplan vs TruCohort')
box.set_ylabel('DunedinPACE Age (bio-aging/chrono-year)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_dun, healthy_dun, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_dun, avg_dun, equal_var=False)[1], 3), round(stats.ttest_ind(avg_dun, b_avg_dun, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_dun)-np.median(healthy_dun), 3)) + ', '
            + str(round(np.median(kap_dun)-np.median(avg_dun), 3)) + ', ' + str(round(np.median(kap_dun)-np.median(b_avg_dun), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('figures/DunedinPACE.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_hor, healthy_hor, avg_hor, b_avg_hor])
box.plot([1, 2], [np.median(kap_hor), np.median(healthy_hor)], 'b-')
box.plot([1, 3], [np.median(kap_hor), np.median(avg_hor)], 'g-')
box.plot([1, 4], [np.median(kap_hor), np.median(b_avg_hor)], 'r-')
box.set_title('Horvath Kaplan vs TruCohort')
box.set_ylabel('Horvath Age (years)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_hor, healthy_hor, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_hor, avg_hor, equal_var=False)[1], 3), round(stats.ttest_ind(avg_hor, b_avg_hor, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_hor)-np.median(healthy_hor), 3)) + ', '
            + str(round(np.median(kap_hor)-np.median(avg_hor), 3)) + ', ' + str(round(np.median(kap_hor)-np.median(b_avg_hor), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('figures/Horvath.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_han, healthy_han, avg_han, b_avg_han])
box.plot([1, 2], [np.median(kap_han), np.median(healthy_han)], 'b-')
box.plot([1, 3], [np.median(kap_han), np.median(avg_han)], 'g-')
box.plot([1, 4], [np.median(kap_han), np.median(b_avg_han)], 'r-')
box.set_title('Hannum Kaplan vs TruCohort')
box.set_ylabel('Hannum Age (years)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_han, healthy_han, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_han, avg_han, equal_var=False)[1], 3), round(stats.ttest_ind(avg_han, b_avg_han, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_han)-np.median(healthy_han), 3)) + ', '
            + str(round(np.median(kap_han)-np.median(avg_han), 3)) + ', ' + str(round(np.median(kap_han)-np.median(b_avg_han), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('figures/Hannum.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_cd8, healthy_cd8, avg_cd8, b_avg_cd8])
box.plot([1, 2], [np.median(kap_cd8), np.median(healthy_cd8)], 'b-')
box.plot([1, 3], [np.median(kap_cd8), np.median(avg_cd8)], 'g-')
box.plot([1, 4], [np.median(kap_cd8), np.median(b_avg_cd8)], 'r-')
box.set_title('CD8T Kaplan vs TruCohort')
box.set_ylabel('CD8T Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_cd8, healthy_cd8, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_cd8, avg_cd8, equal_var=False)[1], 3), round(stats.ttest_ind(avg_cd8, b_avg_cd8, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_cd8)-np.median(healthy_cd8), 3)) + ', '
            + str(round(np.median(kap_cd8)-np.median(avg_cd8), 3)) + ', ' + str(round(np.median(kap_cd8)-np.median(b_avg_cd8), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/CD8T.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_cd4, healthy_cd4, avg_cd4, b_avg_cd4])
box.plot([1, 2], [np.median(kap_cd4), np.median(healthy_cd4)], 'b-')
box.plot([1, 3], [np.median(kap_cd4), np.median(avg_cd4)], 'g-')
box.plot([1, 4], [np.median(kap_cd4), np.median(b_avg_cd4)], 'r-')
box.set_title('CD4T Kaplan vs TruCohort')
box.set_ylabel('CD4T Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_cd4, healthy_cd4, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_cd4, avg_cd4, equal_var=False)[1], 3), round(stats.ttest_ind(avg_cd4, b_avg_cd4, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_cd4)-np.median(healthy_cd4), 3)) + ', '
            + str(round(np.median(kap_cd4)-np.median(avg_cd4), 3)) + ', ' + str(round(np.median(kap_cd4)-np.median(b_avg_cd4), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/CD4T.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_cdr, healthy_cdr, avg_cdr, b_avg_cdr])
box.plot([1, 2], [np.median(kap_cdr), np.median(healthy_cdr)], 'b-')
box.plot([1, 3], [np.median(kap_cdr), np.median(avg_cdr)], 'g-')
box.plot([1, 4], [np.median(kap_cdr), np.median(b_avg_cdr)], 'r-')
box.set_title('CD4T.CD8T Kaplan vs TruCohort')
box.set_ylabel('CD4T.CD8T Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_cdr, healthy_cdr, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_cdr, avg_cdr, equal_var=False)[1], 3), round(stats.ttest_ind(avg_cdr, b_avg_cdr, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_cdr)-np.median(healthy_cdr), 3)) + ', '
            + str(round(np.median(kap_cdr)-np.median(avg_cdr), 3)) + ', ' + str(round(np.median(kap_cdr)-np.median(b_avg_cdr), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/CD4T.CD8T.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_cdr_filtered, healthy_cdr_filtered, avg_cdr_filtered, b_avg_cdr_filtered])
box.plot([1, 2], [np.median(kap_cdr_filtered), np.median(healthy_cdr_filtered)], 'b-')
box.plot([1, 3], [np.median(kap_cdr_filtered), np.median(avg_cdr_filtered)], 'g-')
box.plot([1, 4], [np.median(kap_cdr_filtered), np.median(b_avg_cdr_filtered)], 'r-')
box.set_title('CD4T.CD8T Kaplan vs TruCohort (outliers filtered)')
box.set_ylabel('CD4T.CD8T Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
try:
    p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_cdr_filtered, healthy_cdr_filtered, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_cdr_filtered, avg_cdr_filtered, equal_var=False)[1], 3), round(stats.ttest_ind(avg_cdr_filtered, b_avg_cdr_filtered, equal_var=False)[1], 3)
    plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_cdr_filtered)-np.median(healthy_cdr_filtered), 3)) + ', '
                + str(round(np.median(kap_cdr_filtered)-np.median(avg_cdr_filtered), 3)) + ', ' + str(round(np.median(kap_cdr_filtered)-np.median(b_avg_cdr_filtered), 3))
                + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
except Exception as e:
    print(e)
    plt.figtext(0.5, 0.01, 'Trends: ' + str(np.median(kap_cdr_filtered)-np.median(healthy_cdr_filtered)) + ', '
                + str(np.median(healthy_cdr_filtered)-np.median(kap_filtered)) + ', ' +avgr(np.median(avg_cdr_filtered)-np.median(b_avg_cdr_filtered))
                + 'kap p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/CD4T.CD8T-filtered.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_nkc, healthy_nkc, avg_nkc, b_avg_nkc])
box.plot([1, 2], [np.median(kap_nkc), np.median(healthy_nkc)], 'b-')
box.plot([1, 3], [np.median(kap_nkc), np.median(avg_nkc)], 'g-')
box.plot([1, 4], [np.median(kap_nkc), np.median(b_avg_nkc)], 'r-')
box.set_title('Natural Killer Kaplan vs TruCohort')
box.set_ylabel('Natural Killer Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_nkc, healthy_nkc, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_nkc, avg_nkc, equal_var=False)[1], 3), round(stats.ttest_ind(avg_nkc, b_avg_nkc, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_nkc)-np.median(healthy_nkc), 3)) + ', '
            + str(round(np.median(kap_nkc)-np.median(avg_nkc), 3)) + ', ' + str(round(np.median(kap_nkc)-np.median(b_avg_nkc), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/Natural Killer.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_mon, healthy_mon, avg_mon, b_avg_mon])
box.plot([1, 2], [np.median(kap_mon), np.median(healthy_mon)], 'b-')
box.plot([1, 3], [np.median(kap_mon), np.median(avg_mon)], 'g-')
box.plot([1, 4], [np.median(kap_mon), np.median(b_avg_mon)], 'r-')
box.set_title('Monocyte Kaplan vs TruCohort')
box.set_ylabel('Monocyte Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_mon, healthy_mon, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_mon, avg_mon, equal_var=False)[1], 3), round(stats.ttest_ind(avg_mon, b_avg_mon, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_mon)-np.median(healthy_mon), 3)) + ', '
            + str(round(np.median(kap_mon)-np.median(avg_mon), 3)) + ', ' + str(round(np.median(kap_mon)-np.median(b_avg_mon), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/Monocyte.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_bce, healthy_bce, avg_bce, b_avg_bce])
box.plot([1, 2], [np.median(kap_bce), np.median(healthy_bce)], 'b-')
box.plot([1, 3], [np.median(kap_bce), np.median(avg_bce)], 'g-')
box.plot([1, 4], [np.median(kap_bce), np.median(b_avg_bce)], 'r-')
box.set_title('B-Cell Kaplan vs TruCohort')
box.set_ylabel('B-Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_bce, healthy_bce, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_bce, avg_bce, equal_var=False)[1], 3), round(stats.ttest_ind(avg_bce, b_avg_bce, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_bce)-np.median(healthy_bce), 3)) + ', '
            + str(round(np.median(kap_bce)-np.median(avg_bce), 3)) + ', ' + str(round(np.median(kap_bce)-np.median(b_avg_bce), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/B-Cell.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_bce_filtered, healthy_bce_filtered, avg_bce_filtered, b_avg_bce_filtered])
box.plot([1, 2], [np.median(kap_bce_filtered), np.median(healthy_bce_filtered)], 'b-')
box.plot([1, 3], [np.median(kap_bce_filtered), np.median(avg_bce_filtered)], 'g-')
box.plot([1, 4], [np.median(kap_bce_filtered), np.median(b_avg_bce_filtered)], 'r-')
box.set_title('B-Cell Kaplan vs TruCohort (outliers filtered)')
box.set_ylabel('B-Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_bce_filtered, healthy_bce_filtered, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_bce_filtered, avg_bce_filtered, equal_var=False)[1], 3), round(stats.ttest_ind(avg_bce_filtered, b_avg_bce_filtered, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_bce_filtered)-np.median(healthy_bce_filtered), 3)) + ', '
            + str(round(np.median(kap_bce_filtered)-np.median(avg_bce_filtered), 3)) + ', ' + str(round(np.median(kap_bce_filtered)-np.median(b_avg_bce_filtered), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/B-Cell-filtered.png')
plt.close()

fig = plt.figure()
box = fig.add_subplot()
box.boxplot([kap_neu, healthy_neu, avg_neu, b_avg_neu])
box.plot([1, 2], [np.median(kap_neu), np.median(healthy_neu)], 'b-')
box.plot([1, 3], [np.median(kap_neu), np.median(avg_neu)], 'g-')
box.plot([1, 4], [np.median(kap_neu), np.median(b_avg_neu)], 'r-')
box.set_title('Neutrophil Kaplan vs TruCohort')
box.set_ylabel('Neutrophil Cell Values (%)')
box.set_xticklabels(['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])
p_val1, p_val2, p_val3 = round(stats.ttest_ind(kap_neu, healthy_neu, equal_var=False)[1], 3), round(stats.ttest_ind(healthy_neu, avg_neu, equal_var=False)[1], 3), round(stats.ttest_ind(avg_neu, b_avg_neu, equal_var=False)[1], 3)
plt.figtext(0.5, 0.01, 'Trends: ' + str(round(np.median(kap_neu)-np.median(healthy_neu), 3)) + ', '
            + str(round(np.median(kap_neu)-np.median(avg_neu), 3)) + ', ' + str(round(np.median(kap_neu)-np.median(b_avg_neu), 3))
            + ' || p-Values: ' + str(p_val1) + ', ' + str(p_val2) + ', ' + str(p_val3), horizontalalignment='center')
# plt.show()
plt.savefig('immune figures/Neutrophil.png')
plt.close()


overall_comparison = pd.DataFrame(index=['Mean Horvath',
                                         'Median Horvath',
                                         'STD Horvath',
                                         'Max Horvath',
                                         'Min Horvath',

                                         'Mean Hannum',
                                         'Median Hannum',
                                         'STD Hannum',
                                         'Max Hannum',
                                         'Min Hannum',

                                         'Mean DunedinPACE',
                                         'Median DunedinPACE',
                                         'STD DunedinPACE',
                                         'Max DunedinPACE',
                                         'Min DunedinPACE',

                                         'Mean Immune.CD8T',
                                         'Median Immune.CD8T',
                                         'STD Immune.CD8T',
                                         'Max Immune.CD8T',
                                         'Min Immune.CD8T',

                                         'Mean Immune.CD4T',
                                         'Median Immune.CD4T',
                                         'STD Immune.CD4T',
                                         'Max Immune.CD4T',
                                         'Min Immune.CD4T',

                                         'Mean Immune.CD4T.CD8T',
                                         'Median Immune.CD4T.CD8T',
                                         'STD Immune.CD4T.CD8T',
                                         'Max Immune.CD4T.CD8T',
                                         'Min Immune.CD4T.CD8T',

                                         'Mean Immune.NK',
                                         'Median Immune.NK',
                                         'STD Immune.NK',
                                         'Max Immune.NK',
                                         'Min Immune.NK',

                                         'Mean Immune.Bcell',
                                         'Median Immune.Bcell',
                                         'STD Immune.Bcell',
                                         'Max Immune.Bcell',
                                         'Min Immune.Bcell',

                                         'Mean Immune.Mono',
                                         'Median Immune.Mono',
                                         'STD Immune.Mono',
                                         'Max Immune.Mono',
                                         'Min Immune.Mono',

                                         'Mean Immune.Neutrophil',
                                         'Median Immune.Neutrophil',
                                         'STD Immune.Neutrophil',
                                         'Max Immune.Neutrophil',
                                         'Min Immune.Neutrophil',
                                         ], columns=['Kaplan', 'TruHealthy', 'TruAverage', 'TruUnhealthy'])

mean_hor, median_hor, std_hor, max_hor, min_hor = np.mean(kap_hor), np.median(kap_hor), np.std(kap_hor), np.max(kap_hor), np.min(kap_hor)
mean_han, median_han, std_han, max_han, min_han = np.mean(kap_han), np.median(kap_han), np.std(kap_han), np.max(kap_han), np.min(kap_han)
mean_dun, median_dun, std_dun, max_dun, min_dun = np.mean(kap_dun), np.median(kap_dun), np.std(kap_dun), np.max(kap_dun), np.min(kap_dun)
mean_cd8, median_cd8, std_cd8, max_cd8, min_cd8 = np.mean(kap_cd8), np.median(kap_cd8), np.std(kap_cd8), np.max(kap_cd8), np.min(kap_cd8)
mean_cd4, median_cd4, std_cd4, max_cd4, min_cd4 = np.mean(kap_cd4), np.median(kap_cd4), np.std(kap_cd4), np.max(kap_cd4), np.min(kap_cd4)
mean_cdr, median_cdr, std_cdr, max_cdr, min_cdr = np.mean(kap_cdr), np.median(kap_cdr), np.std(kap_cdr), np.max(kap_cdr), np.min(kap_cdr)
mean_nkc, median_nkc, std_nkc, max_nkc, min_nkc = np.mean(kap_nkc), np.median(kap_nkc), np.std(kap_nkc), np.max(kap_nkc), np.min(kap_nkc)
mean_bce, median_bce, std_bce, max_bce, min_bce = np.mean(kap_bce), np.median(kap_bce), np.std(kap_bce), np.max(kap_bce), np.min(kap_bce)
mean_mon, median_mon, std_mon, max_mon, min_mon = np.mean(kap_mon), np.median(kap_mon), np.std(kap_mon), np.max(kap_mon), np.min(kap_mon)
mean_neu, median_neu, std_neu, max_neu, min_neu = np.mean(kap_neu), np.median(kap_neu), np.std(kap_neu), np.max(kap_neu), np.min(kap_neu)

mean_hor_healthy, median_hor_healthy, std_hor_healthy, max_hor_healthy, min_hor_healthy = np.mean(healthy_hor), np.median(healthy_hor), np.std(healthy_hor), np.max(healthy_hor), np.min(healthy_hor)
mean_han_healthy, median_han_healthy, std_han_healthy, max_han_healthy, min_han_healthy = np.mean(healthy_han), np.median(healthy_han), np.std(healthy_han), np.max(healthy_han), np.min(healthy_han)
mean_dun_healthy, median_dun_healthy, std_dun_healthy, max_dun_healthy, min_dun_healthy = np.mean(healthy_dun), np.median(healthy_dun), np.std(healthy_dun), np.max(healthy_dun), np.min(healthy_dun)
mean_cd8_healthy, median_cd8_healthy, std_cd8_healthy, max_cd8_healthy, min_cd8_healthy = np.mean(healthy_cd8), np.median(healthy_cd8), np.std(healthy_cd8), np.max(healthy_cd8), np.min(healthy_cd8)
mean_cd4_healthy, median_cd4_healthy, std_cd4_healthy, max_cd4_healthy, min_cd4_healthy = np.mean(healthy_cd4), np.median(healthy_cd4), np.std(healthy_cd4), np.max(healthy_cd4), np.min(healthy_cd4)
mean_cdr_healthy, median_cdr_healthy, std_cdr_healthy, max_cdr_healthy, min_cdr_healthy = np.mean(healthy_cdr), np.median(healthy_cdr), np.std(healthy_cdr), np.max(healthy_cdr), np.min(healthy_cdr)
mean_nkc_healthy, median_nkc_healthy, std_nkc_healthy, max_nkc_healthy, min_nkc_healthy = np.mean(healthy_nkc), np.median(healthy_nkc), np.std(healthy_nkc), np.max(healthy_nkc), np.min(healthy_nkc)
mean_bce_healthy, median_bce_healthy, std_bce_healthy, max_bce_healthy, min_bce_healthy = np.mean(healthy_bce), np.median(healthy_bce), np.std(healthy_bce), np.max(healthy_bce), np.min(healthy_bce)
mean_mon_healthy, median_mon_healthy, std_mon_healthy, max_mon_healthy, min_mon_healthy = np.mean(healthy_mon), np.median(healthy_mon), np.std(healthy_mon), np.max(healthy_mon), np.min(healthy_mon)
mean_neu_healthy, median_neu_healthy, std_neu_healthy, max_neu_healthy, min_neu_healthy = np.mean(healthy_neu), np.median(healthy_neu), np.std(healthy_neu), np.max(healthy_neu), np.min(healthy_neu)

mean_hor_avg, median_hor_avg, std_hor_avg, max_hor_avg, min_hor_avg = np.mean(avg_hor), np.median(avg_hor), np.std(avg_hor), np.max(avg_hor), np.min(avg_hor)
mean_han_avg, median_han_avg, std_han_avg, max_han_avg, min_han_avg = np.mean(avg_han), np.median(avg_han), np.std(avg_han), np.max(avg_han), np.min(avg_han)
mean_dun_avg, median_dun_avg, std_dun_avg, max_dun_avg, min_dun_avg = np.mean(avg_dun), np.median(avg_dun), np.std(avg_dun), np.max(avg_dun), np.min(avg_dun)
mean_cd8_avg, median_cd8_avg, std_cd8_avg, max_cd8_avg, min_cd8_avg = np.mean(avg_cd8), np.median(avg_cd8), np.std(avg_cd8), np.max(avg_cd8), np.min(avg_cd8)
mean_cd4_avg, median_cd4_avg, std_cd4_avg, max_cd4_avg, min_cd4_avg = np.mean(avg_cd4), np.median(avg_cd4), np.std(avg_cd4), np.max(avg_cd4), np.min(avg_cd4)
mean_cdr_avg, median_cdr_avg, std_cdr_avg, max_cdr_avg, min_cdr_avg = np.mean(avg_cdr), np.median(avg_cdr), np.std(avg_cdr), np.max(avg_cdr), np.min(avg_cdr)
mean_nkc_avg, median_nkc_avg, std_nkc_avg, max_nkc_avg, min_nkc_avg = np.mean(avg_nkc), np.median(avg_nkc), np.std(avg_nkc), np.max(avg_nkc), np.min(avg_nkc)
mean_bce_avg, median_bce_avg, std_bce_avg, max_bce_avg, min_bce_avg = np.mean(avg_bce), np.median(avg_bce), np.std(avg_bce), np.max(avg_bce), np.min(avg_bce)
mean_mon_avg, median_mon_avg, std_mon_avg, max_mon_avg, min_mon_avg = np.mean(avg_mon), np.median(avg_mon), np.std(avg_mon), np.max(avg_mon), np.min(avg_mon)
mean_neu_avg, median_neu_avg, std_neu_avg, max_neu_avg, min_neu_avg = np.mean(avg_neu), np.median(avg_neu), np.std(avg_neu), np.max(avg_neu), np.min(avg_neu)

mean_hor_unhealthy, median_hor_unhealthy, std_hor_unhealthy, max_hor_unhealthy, min_hor_unhealthy = np.mean(b_avg_hor), np.median(b_avg_hor), np.std(b_avg_hor), np.max(b_avg_hor), np.min(b_avg_hor)
mean_han_unhealthy, median_han_unhealthy, std_han_unhealthy, max_han_unhealthy, min_han_unhealthy = np.mean(b_avg_han), np.median(b_avg_han), np.std(b_avg_han), np.max(b_avg_han), np.min(b_avg_han)
mean_dun_unhealthy, median_dun_unhealthy, std_dun_unhealthy, max_dun_unhealthy, min_dun_unhealthy = np.mean(b_avg_dun), np.median(b_avg_dun), np.std(b_avg_dun), np.max(b_avg_dun), np.min(b_avg_dun)
mean_cd8_unhealthy, median_cd8_unhealthy, std_cd8_unhealthy, max_cd8_unhealthy, min_cd8_unhealthy = np.mean(b_avg_cd8), np.median(b_avg_cd8), np.std(b_avg_cd8), np.max(b_avg_cd8), np.min(b_avg_cd8)
mean_cd4_unhealthy, median_cd4_unhealthy, std_cd4_unhealthy, max_cd4_unhealthy, min_cd4_unhealthy = np.mean(b_avg_cd4), np.median(b_avg_cd4), np.std(b_avg_cd4), np.max(b_avg_cd4), np.min(b_avg_cd4)
mean_cdr_unhealthy, median_cdr_unhealthy, std_cdr_unhealthy, max_cdr_unhealthy, min_cdr_unhealthy = np.mean(b_avg_cdr), np.median(b_avg_cdr), np.std(b_avg_cdr), np.max(b_avg_cdr), np.min(b_avg_cdr)
mean_nkc_unhealthy, median_nkc_unhealthy, std_nkc_unhealthy, max_nkc_unhealthy, min_nkc_unhealthy = np.mean(b_avg_nkc), np.median(b_avg_nkc), np.std(b_avg_nkc), np.max(b_avg_nkc), np.min(b_avg_nkc)
mean_bce_unhealthy, median_bce_unhealthy, std_bce_unhealthy, max_bce_unhealthy, min_bce_unhealthy = np.mean(b_avg_bce), np.median(b_avg_bce), np.std(b_avg_bce), np.max(b_avg_bce), np.min(b_avg_bce)
mean_mon_unhealthy, median_mon_unhealthy, std_mon_unhealthy, max_mon_unhealthy, min_mon_unhealthy = np.mean(b_avg_mon), np.median(b_avg_mon), np.std(b_avg_mon), np.max(b_avg_mon), np.min(b_avg_mon)
mean_neu_unhealthy, median_neu_unhealthy, std_neu_unhealthy, max_neu_unhealthy, min_neu_unhealthy = np.mean(b_avg_neu), np.median(b_avg_neu), np.std(b_avg_neu), np.max(b_avg_neu), np.min(b_avg_neu)



overall_comparison.loc[['Mean Horvath',
                         'Median Horvath',
                         'STD Horvath',
                         'Max Horvath',
                         'Min Horvath'], 'Kaplan'] = mean_hor, median_hor, std_hor, max_hor, min_hor
overall_comparison.loc[['Mean Hannum',
                         'Median Hannum',
                         'STD Hannum',
                         'Max Hannum',
                         'Min Hannum'], 'Kaplan'] = mean_han, median_han, std_han, max_han, min_han
overall_comparison.loc[['Mean DunedinPACE',
                         'Median DunedinPACE',
                         'STD DunedinPACE',
                         'Max DunedinPACE',
                         'Min DunedinPACE'], 'Kaplan'] = mean_dun, median_dun, std_dun, max_dun, min_dun
overall_comparison.loc[['Mean DunedinPACE',
                         'Median Immune.CD8T',
                         'STD Immune.CD8T',
                         'Max Immune.CD8T',
                         'Min Immune.CD8T'], 'Kaplan'] = mean_cd8, median_cd8, std_cd8, max_cd8, min_cd8
overall_comparison.loc[['Mean Immune.CD4T',
                         'Median Immune.CD4T',
                         'STD Immune.CD4T',
                         'Max Immune.CD4T',
                         'Min Immune.CD4T'], 'Kaplan'] = mean_cd4, median_cd4, std_cd4, max_cd4, min_cd4
overall_comparison.loc[['Mean Immune.CD4T.CD8T',
                         'Median Immune.CD4T.CD8T',
                         'STD Immune.CD4T.CD8T',
                         'Max Immune.CD4T.CD8T',
                         'Min Immune.CD4T.CD8T'], 'Kaplan'] = mean_cdr, median_cdr, std_cdr, max_cdr, min_cdr
overall_comparison.loc[['Mean Immune.NK',
                         'Median Immune.NK',
                         'STD Immune.NK',
                         'Max Immune.NK',
                         'Min Immune.NK'], 'Kaplan'] = mean_nkc, median_nkc, std_nkc, max_nkc, min_nkc
overall_comparison.loc[['Mean Immune.Bcell',
                         'Median Immune.Bcell',
                         'STD Immune.Bcell',
                         'Max Immune.Bcell',
                         'Min Immune.Bcell'], 'Kaplan'] = mean_bce, median_bce, std_bce, max_bce, min_bce
overall_comparison.loc[['Mean Immune.Mono',
                         'Median Immune.Mono',
                         'STD Immune.Mono',
                         'Max Immune.Mono',
                         'Min Immune.Mono'], 'Kaplan'] = mean_mon, median_mon, std_mon, max_mon, min_mon
overall_comparison.loc[['Mean Immune.Neutrophil',
                         'Median Immune.Neutrophil',
                         'STD Immune.Neutrophil',
                         'Max Immune.Neutrophil',
                         'Min Immune.Neutrophil'], 'Kaplan'] = mean_neu, median_neu, std_neu, max_neu, min_neu

overall_comparison.loc[['Mean Horvath',
                         'Median Horvath',
                         'STD Horvath',
                         'Max Horvath',
                         'Min Horvath'], 'TruHealthy'] = mean_hor_healthy, median_hor_healthy, std_hor_healthy, max_hor_healthy, min_hor_healthy
overall_comparison.loc[['Mean Hannum',
                         'Median Hannum',
                         'STD Hannum',
                         'Max Hannum',
                         'Min Hannum'], 'TruHealthy'] = mean_han_healthy, median_han_healthy, std_han_healthy, max_han_healthy, min_han_healthy
overall_comparison.loc[['Mean DunedinPACE',
                         'Median DunedinPACE',
                         'STD DunedinPACE',
                         'Max DunedinPACE',
                         'Min DunedinPACE'], 'TruHealthy'] = mean_dun_healthy, median_dun_healthy, std_dun_healthy, max_dun_healthy, min_dun_healthy
overall_comparison.loc[['Mean Immune.CD8T',
                         'Median Immune.CD8T',
                         'STD Immune.CD8T',
                         'Max Immune.CD8T',
                         'Min Immune.CD8T'], 'TruHealthy'] = mean_cd8_healthy, median_cd8_healthy, std_cd8_healthy, max_cd8_healthy, min_cd8_healthy
overall_comparison.loc[['Mean Immune.CD4T',
                         'Median Immune.CD4T',
                         'STD Immune.CD4T',
                         'Max Immune.CD4T',
                         'Min Immune.CD4T'], 'TruHealthy'] = mean_cd4_healthy, median_cd4_healthy, std_cd4_healthy, max_cd4_healthy, min_cd4_healthy
overall_comparison.loc[['Mean Immune.CD4T.CD8T',
                         'Median Immune.CD4T.CD8T',
                         'STD Immune.CD4T.CD8T',
                         'Max Immune.CD4T.CD8T',
                         'Min Immune.CD4T.CD8T'], 'TruHealthy'] = mean_cdr_healthy, median_cdr_healthy, std_cdr_healthy, max_cdr_healthy, min_cdr_healthy
overall_comparison.loc[['Mean Immune.NK',
                         'Median Immune.NK',
                         'STD Immune.NK',
                         'Max Immune.NK',
                         'Min Immune.NK'], 'TruHealthy'] = mean_nkc_healthy, median_nkc_healthy, std_nkc_healthy, max_nkc_healthy, min_nkc_healthy
overall_comparison.loc[['Mean Immune.Bcell',
                         'Median Immune.Bcell',
                         'STD Immune.Bcell',
                         'Max Immune.Bcell',
                         'Min Immune.Bcell'], 'TruHealthy'] = mean_bce_healthy, median_bce_healthy, std_bce_healthy, max_bce_healthy, min_bce_healthy
overall_comparison.loc[['Mean Immune.Mono',
                         'Median Immune.Mono',
                         'STD Immune.Mono',
                         'Max Immune.Mono',
                         'Min Immune.Mono'], 'TruHealthy'] = mean_mon_healthy, median_mon_healthy, std_mon_healthy, max_mon_healthy, min_mon_healthy
overall_comparison.loc[['Mean Immune.Neutrophil',
                         'Median Immune.Neutrophil',
                         'STD Immune.Neutrophil',
                         'Max Immune.Neutrophil',
                         'Min Immune.Neutrophil'], 'TruHealthy'] = mean_neu_healthy, median_neu_healthy, std_neu_healthy, max_neu_healthy, min_neu_healthy

overall_comparison.loc[['Mean Horvath',
                         'Median Horvath',
                         'STD Horvath',
                         'Max Horvath',
                         'Min Horvath'], 'TruAverage'] = mean_hor_avg, median_hor_avg, std_hor_avg, max_hor_avg, min_hor_avg
overall_comparison.loc[['Mean Hannum',
                         'Median Hannum',
                         'STD Hannum',
                         'Max Hannum',
                         'Min Hannum'], 'TruAverage'] = mean_han_avg, median_han_avg, std_han_avg, max_han_avg, min_han_avg
overall_comparison.loc[['Mean DunedinPACE',
                         'Median DunedinPACE',
                         'STD DunedinPACE',
                         'Max DunedinPACE',
                         'Min DunedinPACE'], 'TruAverage'] = mean_dun_avg, median_dun_avg, std_dun_avg, max_dun_avg, min_dun_avg
overall_comparison.loc[['Mean Immune.CD8T',
                         'Median Immune.CD8T',
                         'STD Immune.CD8T',
                         'Max Immune.CD8T',
                         'Min Immune.CD8T'], 'TruAverage'] = mean_cd8_avg, median_cd8_avg, std_cd8_avg, max_cd8_avg, min_cd8_avg
overall_comparison.loc[['Mean Immune.CD4T',
                         'Median Immune.CD4T',
                         'STD Immune.CD4T',
                         'Max Immune.CD4T',
                         'Min Immune.CD4T'], 'TruAverage'] = mean_cd4_avg, median_cd4_avg, std_cd4_avg, max_cd4_avg, min_cd4_avg
overall_comparison.loc[['Mean Immune.CD4T.CD8T',
                         'Median Immune.CD4T.CD8T',
                         'STD Immune.CD4T.CD8T',
                         'Max Immune.CD4T.CD8T',
                         'Min Immune.CD4T.CD8T'], 'TruAverage'] = mean_cdr_avg, median_cdr_avg, std_cdr_avg, max_cdr_avg, min_cdr_avg
overall_comparison.loc[['Mean Immune.NK',
                         'Median Immune.NK',
                         'STD Immune.NK',
                         'Max Immune.NK',
                         'Min Immune.NK'], 'TruAverage'] = mean_nkc_avg, median_nkc_avg, std_nkc_avg, max_nkc_avg, min_nkc_avg
overall_comparison.loc[['Mean Immune.Bcell',
                         'Median Immune.Bcell',
                         'STD Immune.Bcell',
                         'Max Immune.Bcell',
                         'Min Immune.Bcell'], 'TruAverage'] = mean_bce_avg, median_bce_avg, std_bce_avg, max_bce_avg, min_bce_avg
overall_comparison.loc[['Mean Immune.Mono',
                         'Median Immune.Mono',
                         'STD Immune.Mono',
                         'Max Immune.Mono',
                         'Min Immune.Mono'], 'TruAverage'] = mean_mon_avg, median_mon_avg, std_mon_avg, max_mon_avg, min_mon_avg
overall_comparison.loc[['Mean Immune.Neutrophil',
                         'Median Immune.Neutrophil',
                         'STD Immune.Neutrophil',
                         'Max Immune.Neutrophil',
                         'Min Immune.Neutrophil'], 'TruAverage'] = mean_neu_avg, median_neu_avg, std_neu_avg, max_neu_avg, min_neu_avg

overall_comparison.loc[['Mean Horvath',
                         'Median Horvath',
                         'STD Horvath',
                         'Max Horvath',
                         'Min Horvath'], 'TruUnhealthy'] = mean_hor_unhealthy, median_hor_unhealthy, std_hor_unhealthy, max_hor_unhealthy, min_hor_unhealthy
overall_comparison.loc[['Mean Hannum',
                         'Median Hannum',
                         'STD Hannum',
                         'Max Hannum',
                         'Min Hannum'], 'TruUnhealthy'] = mean_han_unhealthy, median_han_unhealthy, std_han_unhealthy, max_han_unhealthy, min_han_unhealthy
overall_comparison.loc[['Mean DunedinPACE',
                         'Median DunedinPACE',
                         'STD DunedinPACE',
                         'Max DunedinPACE',
                         'Min DunedinPACE'], 'TruUnhealthy'] = mean_dun_unhealthy, median_dun_unhealthy, std_dun_unhealthy, max_dun_unhealthy, min_dun_unhealthy
overall_comparison.loc[['Mean Immune.CD8T',
                         'Median Immune.CD8T',
                         'STD Immune.CD8T',
                         'Max Immune.CD8T',
                         'Min Immune.CD8T'], 'TruUnhealthy'] = mean_cd8_unhealthy, median_cd8_unhealthy, std_cd8_unhealthy, max_cd8_unhealthy, min_cd8_unhealthy
overall_comparison.loc[['Mean Immune.CD4T',
                         'Median Immune.CD4T',
                         'STD Immune.CD4T',
                         'Max Immune.CD4T',
                         'Min Immune.CD4T'], 'TruUnhealthy'] = mean_cd4_unhealthy, median_cd4_unhealthy, std_cd4_unhealthy, max_cd4_unhealthy, min_cd4_unhealthy
overall_comparison.loc[['Mean Immune.CD4T.CD8T',
                         'Median Immune.CD4T.CD8T',
                         'STD Immune.CD4T.CD8T',
                         'Max Immune.CD4T.CD8T',
                         'Min Immune.CD4T.CD8T'], 'TruUnhealthy'] = mean_cdr_unhealthy, median_cdr_unhealthy, std_cdr_unhealthy, max_cdr_unhealthy, min_cdr_unhealthy
overall_comparison.loc[['Mean Immune.NK',
                         'Median Immune.NK',
                         'STD Immune.NK',
                         'Max Immune.NK',
                         'Min Immune.NK'], 'TruUnhealthy'] = mean_nkc_unhealthy, median_nkc_unhealthy, std_nkc_unhealthy, max_nkc_unhealthy, min_nkc_unhealthy
overall_comparison.loc[['Mean Immune.Bcell',
                         'Median Immune.Bcell',
                         'STD Immune.Bcell',
                         'Max Immune.Bcell',
                         'Min Immune.Bcell'], 'TruUnhealthy'] = mean_bce_unhealthy, median_bce_unhealthy, std_bce_unhealthy, max_bce_unhealthy, min_bce_unhealthy
overall_comparison.loc[['Mean Immune.Mono',
                         'Median Immune.Mono',
                         'STD Immune.Mono',
                         'Max Immune.Mono',
                         'Min Immune.Mono'], 'TruUnhealthy'] = mean_mon_unhealthy, median_mon_unhealthy, std_mon_unhealthy, max_mon_unhealthy, min_mon_unhealthy
overall_comparison.loc[['Mean Immune.Neutrophil',
                         'Median Immune.Neutrophil',
                         'STD Immune.Neutrophil',
                         'Max Immune.Neutrophil',
                         'Min Immune.Neutrophil'], 'TruUnhealthy'] = mean_neu_unhealthy, median_neu_unhealthy, std_neu_unhealthy, max_neu_unhealthy, min_neu_unhealthy
'''Immune.CD8T	Immune.CD4T	Immune.CD4T.CD8T	Immune.NK	Immune.Bcell	Immune.Mono	Immune.Neutrophil
'''
overall_comparison.to_csv('OverallKaplanComparison NEW.csv')

full_output = markdown.markdown('''
<center>
# **<font color='blue'>Kaplan Cohort Analysis</font>**
### <font color='blue'>TruDiagnostic - 2022-08-24</font>

***
***
***

## <ins><font color='blue'>Overview</font><ins>
The patients in the Kaplan cohort were shown to have healthy, average aging rates and overall epigenetic age accelerations 
as compared to the "average" subsection of the TruFit cohort. The TruFit cohort only includes those with zero present diseases/disorders,
and was split by their deviation from the average pace of aging from DunedinPACE, (<.78 Healthy, .78<x<1.02 Average, >1.02 Healthy). 
Additionally, the Tru cohort has been shown to be healthier than most other cohorts in terms of epigenetic age acceleration.
That said, the similarities to the TruAverage cohort would indicate that the Kaplan cohort is still quite epigenetically healthy, 
but not exceptionally so. The health of said individuals may even be significantly higher if a one-to-one comparison was made by 
filtering those with diseases from the Kaplan cohort.
<br>

### <ins><font color='blue'>DunedinPACE Results</font><ins>
There were very high similarities between TruAverage and the Kaplan cohort. Overall suggests a healthy rate of aging. 
<br>

### <ins><font color='blue'>Horvath/Hannum Results</font><ins>
The Horvath clock is best applied to a variety of tissue types, meaning it performs best as a general capture of epigenetic 
aging, not tissue-specific changes. On the other hand, the Hannum clock shows better results with tissue-specific samples, 
and generally under-performs compared to the Horvath clock when predicting chronological age specifically. With this in mind, 
the slightly lower age residuals seen in the Hannum measurements compared to Horvath could indicate that there is a tissue-specific, 
positive impact on the epigenome. 
<br>

### <ins><font color='blue'>Immune Cell Profile Results</font><ins>
The immune subsets somewhat confirm the previous hypothesis of tissue-specific changes occurring, though the direction of the immune changes 
seem incongruent with the Hannum measure. Almost all measurements were slightly less healthy, according to the trends established by the Tru cohort,
but still quite healthy since they were very close to the TruAverage, on average. 
<br> 
***
***
***
<br>
<br>
<br>
## <ins><font color='blue'><font size="6">*Epigenetic Clock Outputs*</font></font></ins>
''')

full_output += markdown.markdown(
    '<kbd>![](SampleSizeDemographics.png)</kbd><br><br><font size="5">' +
    '**Sample sizes of each cohort.**</font>'
    '<br>'
)
full_output += markdown.markdown(
    '<kbd>![](Kaplan Age Demographics.png)</kbd><br><br><font size="5">' +
    '**Age demographics of the Kaplan Cohort.**</font>'
    '<br>'
    '<br>'
    '***')


age_figs = glob.glob('figures/*.png')

for fig_path in age_figs:
    if fig_path == 'figures\DunedinPACE.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**Shows very high correlation to the average cohort in aging rate.**</font>'
        )
    elif fig_path == 'figures\Hannum.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**Shows the greatest similarity with the healthy cohort. Possibly indicates a slight, positive, tissue-specific impact '
            'on the epigenome.**</font>'
        )
    elif fig_path == 'figures\Horvath.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**Greatest similarity to the average cohort, but still somewhat lower. Indicates a slightly healthier than average '
            'aging rate.**</font>'
        )
    else:
        print('Error in clock figure path name: ', fig_path)
        exit()
    full_output += figure

full_output += markdown.markdown('''
<br>
<br>
<br>
<br>
***
***
***
<br>
<br>
<br>
## <ins><font color='blue'><font size="6">*Immune Subset Outputs*</font></font></ins>
''')

immune_figs = glob.glob('immune figures/*.png')

for fig_path in immune_figs:
    if fig_path == 'immune figures\B-Cell.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**B-cell counts deviate from the healthiest and "average" healthy individuals, and most closely mimics the unhealthy cohort, showing '
            'statistically significant differences between the healthy and average cohort, and none with the unhealthy. Indicates an unhealthy '
            'lack of B-cells.**</font>'
        )
    elif fig_path == 'immune figures\B-Cell-filtered.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**The overall differences were more or less the same without outliers, though a slightly greater similarity was found'
            'with the healthy cohort in this case. Indicates relatively healthy**</font>'
        )
    elif fig_path == 'immune figures\CD4T.CD8T.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**The CD4T.CD8T ratio was very closely aligned with the healthy cohort, slightly less with the average, and '
            'showed no alignment with the unhealthy cohort. Indicates slightly less healthy.**</font>'
        )
    elif fig_path == 'immune figures\CD4T.CD8T-filtered.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**The statistical similarities were magnified when removing outliers.**</font>'
        )
    elif fig_path == 'immune figures\CD4T.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**Cell counts were most similar to the average healthy cohort, though slightly lower. No similarity was found in '
            'the other cases. Indicates averagely healthy.**</font>'
        )
    elif fig_path == 'immune figures\CD8T.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**Extremely similar results to the CD4T comparison, slightly lower than average. Indicates slightly less healthy.**</font>'
        )
    elif fig_path == 'immune figures\Monocyte.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**Despite the medians of Kaplan and the unhealthy cohort being most similar, the ttest of means showed greatest similarity '
            'with the healthy cohort. Though its quartiles and extremes show higher measurements than the other cohorts. Likely indicates less healthy in this regard.**</font>'
        )
    elif fig_path == 'immune figures\\Natural Killer.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**Shows greatest similarity with the healthy cohort statistically, but more median/quartile similarity with the average cohort. '
            'Indicates relatively average to somewhat above average levels of natural killer cells.**</font>'
        )
    elif fig_path == 'immune figures\\Neutrophil.png':
        figure = markdown.markdown(
            '<kbd>![](' + fig_path + ')</kbd><br><br><font size="5">' +
            '**Statistically different from all cohorts, but shows greatest visual similarity with the average healthy cohort.**</font>'
        )
    else:
        print('Error in clock figure path name: ', fig_path)
        exit()
    full_output += figure

full_output += markdown.markdown('</center>')
with open('KaplanAnalysis.html', 'w') as f:
    f.write(full_output)
