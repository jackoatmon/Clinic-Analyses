import markdown
import imageio
from glob import glob
from PIL import Image
from xhtml2pdf import pisa

full_output = markdown.markdown('''
<center>
# **Lifeworks Cohort Analysis**
### TruDiagnostic - 2022-12-06

***
***
***

## Overview
There was very little systematic change among the population in most of the clocks. However, some of the aging clocks showed <br> 
a slight increase in aging residuals on average. 
<br>

### Epigenetic Clocks
xx
<br>

### Mitotic Clock Values
xx
<br>

### Immune Cell Subsets
xx
***
***
***
<br>
<br>
<br>
## <font size="6">*Epigenetic Clock Outputs*</font>
''')
clock_figs = glob('Longitudinal Analysis/*.png')
for pic_path in clock_figs:
    if 'DunedinPoAm.png' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif 'EEAA_PC.png' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**The median change showed little trend, but the average moved down from test 1 to test 2 significantly**</font>'
        )
    elif 'Extrinsic Age' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Extrinsic age showed a notable increase through median and mean, though no statistical significance**</font>'
        )
    elif 'Extrinsic_EEAA' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Shows a moderate decrease in aging rate**</font>'
        )
    elif 'Extrinsic_IEAA' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Shows a significant decrease in aging rate**</font>'
        )
    elif 'GrimAge PC ' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif 'Hannum PC' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance present, though has slight downward trend**</font>'
        )
    elif 'Horvath PC' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Slight downward trend in aging rate**</font>'
        )
    elif 'IEAA_PC''' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate decrease in aging rate**</font>'
        )
    elif 'Intrinsic Age' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Very large increase in aging rate**</font>'
        )
    elif 'Intrinsic_IEAA' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate decrease in aging rate**</font>'
        )
    elif 'PhenoAge PC' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif 'Telomere Values PC' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif 'Telomere Values' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**There was a significant increase in measured telomere lengths**</font>'
        )
    else:
        print('Error in clock figure path name: ', pic_path)
        exit()
    full_output += figure
    full_output += '<br><br>'
full_output += markdown.markdown('''
<br>
<br>
<br>
***
***
***
<br>
<br>
<br>
## <font size="6">*Mitotic Clock Outputs*</font>
''')
#
# mitotic_figs = glob('C/*.png')
# for pic_path in mitotic_figs:
#     if in pic_path 'non-significant figures/Mitotic Clocks\Avg_LifeTime_IntrinsicStemCellDivisionRate.png':
#         figure = markdown.markdown(
#             '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
#             '**Very significant increase in average division rate**</font>'
#         )
#     elif in pic_path 'non-significant figures/Mitotic Clocks\Full_CumulativeStemCellDivisions.png':
#         figure = markdown.markdown(
#             '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
#             '**Very significant increase in cumulative divisions**</font>'
#         )
#     elif in pic_path 'non-significant figures/Mitotic Clocks\HypoClock_Score_Old.png':
#         figure = markdown.markdown(
#             '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
#             '**No statistical significance nor overall trend was discernible**</font>'
#         )
#     elif in pic_path 'non-significant figures/Mitotic Clocks\Median_Lifetime_IntrinsicStemCellDivisionRate.png':
#         figure = markdown.markdown(
#             '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
#             '**Significant increase in median division rate**</font>'
#         )
#     elif in pic_path 'non-significant figures/Mitotic Clocks\MitoticScore_OldEpitoc.png':
#         figure = markdown.markdown(
#             '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
#             '**Moderate increase in mitotic score**</font>'
#         )
#     else:
#         print('Error in mitotic picture path: ', pic_path)
#         exit()
#     full_output += figure
#     full_output += '<br><br>'
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
## <font size="6">*Immune Subset Outputs*</font>
''')

mitotic_figs = glob('IDOL Figs/*.png')
for pic_path in mitotic_figs:
    if 'Immune.Bcell' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Slight increase in cell values**</font>'
        )
    elif 'Immune.CD4T.CD8T' in pic_path :
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate decrease in cell values**</font>'
        )
    elif 'Immune.CD4T' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Significant increase in cell values**</font>'
        )
    elif 'Immune.CD8T' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Significant increase in cell values**</font>'
        )
    elif 'Immune.Mono' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate increase in cell values**</font>'
        )
    elif 'Immune.Neutrophil' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Very significant decrease in cell values**</font>'
        )
    elif 'Immune.NK' in pic_path:
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate increase in cell values**</font>'
        )
    else:
        print('Error in immune picture path: ', pic_path)
        exit()
    full_output += figure
    full_output += '<br><br>'
full_output += markdown.markdown('''
<br>
<br>
<br>
<br>
***
***
***
''')

def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

full_output += markdown.markdown('</center>')
with open('LifeworksAnalysis.html', 'w') as f:
    f.write(full_output)

convert_html_to_pdf(full_output, 'LifeworksAnalysis.pdf')
