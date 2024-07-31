set term pdfcairo size 4,3
set output "/Users/sunwu/SW-Research/sw-research-code/A01_result_analysis/04_01_data_ratio_fig/data_histogram.pdf"
set style data histogram
unset key
$df << EOF
eg	hist
G_0	61.90
G_1	14.29
G_2	9.52
G_3	4.76
G_4	1.59
G_5	0.00
G_6	4.76
G_7	0.00
G_8	3.17
G_9	0.00

EOF
set xr [0.5:10.5]
set ylabel "The percentage of groups"
set xlabel "The different class"
plot $df using 2:xticlabels(1)
