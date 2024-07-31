set term pdfcairo size 4,2
set output "/Users/sunwu/Nextcloud/B1-Papers/01-less-is-more/submits/source_code_of_fastuts_ad/figs/fig.4_overfitting/plot_uts_and_score/Fig.4.pdf"
$df << EOF
index	data_sample_rate	train_loss	test_loss
0	5	-0.29	3.00
1	10	-0.55	1.48
2	15	-1.52	5.31
3	20	-1.42	1.71
4	25	-4.91	-1.40
5	30	-7.11	-2.45
6	35	-7.75	-2.33
7	40	-7.88	-2.10
8	45	-9.93	-2.26
9	50	-7.02	3.59
10	55	-11.99	-1.03
11	60	-8.39	3.76
12	65	-15.25	0.17
13	70	-16.40	-1.39
14	75	-17.81	-0.81
15	80	-11.06	3.04
16	85	-20.74	1.49
17	90	-13.07	5.04
18	95	-22.57	0.21
19	100	-12.85	3.01
EOF
set ytics nomirror
set y2tics
unset y2tics
unset ytics
set ylabel "Loss"
set key outside center top maxrows 1
set xlabel "The percentage of training windows"
plot $df using 0:3:xticlabels(2)  axis x1y1 with lp  pt 10 lc 15 title "Training loss",""  using 0:4 axis x1y2 with lp lc 17 pt 16 title "Test loss"
