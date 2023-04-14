import markdown
import imageio
from glob import glob
from PIL import Image
from xhtml2pdf import pisa

full_output = markdown.markdown('''
<center>
# **Meglin Cohort Analysis**
### TruDiagnostic - 2022-08-08

***
***
***

## Overview
There was no statistical significance found between any of the values. However, this is very likely due to the extremely <br>
small sample size of 8, and there was a noticeable pattern in each of the classes of values. 
<br>

### Epigenetic Clocks
The majority of clock outputs showed a decrease in aging rate. Interestingly, the DunedinPACE showed nearly no change, <br>
and the telomere lengths for the PC algorithm show a slight decrease, but the algorithm using full-spectrum beta values <br>
showed a massive increase in telomere length. Overall, there seems to be a significant positive impact on the epigenome <br>
in terms of aging.
<br>

### Mitotic Clock Values
There is a consistent and substantial increase in mitotic activity across all measurements except the old Hypo-Clock <br>
algorithm, which showed no changes whatsoever.
<br>

### Immune Cell Subsets
B-cells, CD4T-cells, CD8T-cells, natural killer cells, and monocytes all saw a moderate to high increase in volume, while <br>
the CD4T/CD8T-cell ratio and neutrophil levels dropped significantly. The inverse relationship between neutrophils and other <br>
inflammatory/immune response markers is consistent with the effect seen on other analyses investigating the impact of a treatment <br>
that impacts the immune system. 
***
***
***
<br>
<br>
<br>
## <font size="6">*Epigenetic Clock Outputs*</font>
''')
clock_figs = glob('non-significant figures/clocks/*.png')
for pic_path in clock_figs:
    if pic_path == 'non-significant figures/clocks\DunedinPoAm.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\EEAA_PC.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**The median change showed little trend, but the average moved down from test 1 to test 2 significantly**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Extrinsic Age.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Extrinsic age showed a notable increase through median and mean, though no statistical significance**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Extrinsic_EEAA.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Shows a moderate decrease in aging rate**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Extrinsic_IEAA.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Shows a significant decrease in aging rate**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\GrimAge PC .png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Hannum PC.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance present, though has slight downward trend**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Horvath PC.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Slight downward trend in aging rate**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\IEAA_PC.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate decrease in aging rate**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Intrinsic Age.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Very large increase in aging rate**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Intrinsic_IEAA.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate decrease in aging rate**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\PhenoAge PC.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Telomere Values PC.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif pic_path == 'non-significant figures/clocks\Telomere Values.png':
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

mitotic_figs = glob('non-significant figures/Mitotic Clocks/*.png')
for pic_path in mitotic_figs:
    if pic_path == 'non-significant figures/Mitotic Clocks\Avg_LifeTime_IntrinsicStemCellDivisionRate.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Very significant increase in average division rate**</font>'
        )
    elif pic_path == 'non-significant figures/Mitotic Clocks\Full_CumulativeStemCellDivisions.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Very significant increase in cumulative divisions**</font>'
        )
    elif pic_path == 'non-significant figures/Mitotic Clocks\HypoClock_Score_Old.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**No statistical significance nor overall trend was discernible**</font>'
        )
    elif pic_path == 'non-significant figures/Mitotic Clocks\Median_Lifetime_IntrinsicStemCellDivisionRate.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Significant increase in median division rate**</font>'
        )
    elif pic_path == 'non-significant figures/Mitotic Clocks\MitoticScore_OldEpitoc.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate increase in mitotic score**</font>'
        )
    else:
        print('Error in mitotic picture path: ', pic_path)
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
<br>
<br>
<br>
## <font size="6">*Immune Subset Outputs*</font>
''')

mitotic_figs = glob('non-significant figures/Immune Subsets/*.png')
for pic_path in mitotic_figs:
    if pic_path == 'non-significant figures/Immune Subsets\Immune.Bcell.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Slight increase in cell values**</font>'
        )
    elif pic_path == 'non-significant figures/Immune Subsets\Immune.CD4T.CD8T.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate decrease in cell values**</font>'
        )
    elif pic_path == 'non-significant figures/Immune Subsets\Immune.CD4T.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Significant increase in cell values**</font>'
        )
    elif pic_path == 'non-significant figures/Immune Subsets\Immune.CD8T.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Significant increase in cell values**</font>'
        )
    elif pic_path == 'non-significant figures/Immune Subsets\Immune.Mono.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Moderate increase in cell values**</font>'
        )
    elif pic_path == 'non-significant figures/Immune Subsets\Immune.Neutrophil.png':
        figure = markdown.markdown(
            '<kbd>![](' + pic_path + ')</kbd><br><br><font size="5">' +
            '**Very significant decrease in cell values**</font>'
        )
    elif pic_path == 'non-significant figures/Immune Subsets\Immune.NK.png':
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
with open('MeglinAnalysis.html', 'w') as f:
    f.write(full_output)

convert_html_to_pdf(full_output, 'MeglinAnalysis.pdf')
