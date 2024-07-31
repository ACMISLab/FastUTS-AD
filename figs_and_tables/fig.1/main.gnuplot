set term pdfcairo size 12,7
set output "/Users/sunwu/Nextcloud/B1-Papers/01-less-is-more/submits/source_code_of_fastuts_ad/figs_and_tables/fig.1/Fig.1.pdf"
set multiplot layout 3,3 margins 0.05,0.94,0.10,0.95 spacing 0.07,0.08
set ytics nomirror
set label 1 "{/:Bold (a)}  AE" at graph 0.5, graph -0.24 center
set ylabel "Accuracy"
set y2label ""
set key at screen 0.5,screen 0.98 center maxrows 1
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel ""
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
ae	2	68.76	43.63	20.23	13.14	2.00
ae	4	71.32	46.64	21.72	13.04	4.00
ae	8	71.70	47.62	20.96	13.04	8.00
ae	16	71.90	49.10	24.39	13.12	16.00
ae	32	71.52	48.82	24.44	13.16	32.00
ae	64	71.20	48.98	24.84	13.18	64.00
ae	128	71.35	49.15	24.38	13.14	128.00
ae	256	71.47	49.60	23.13	14.48	256.00
ae	512	71.50	49.69	22.47	17.29	512.00
ae	1024	71.32	49.41	23.55	22.83	1024.00
ae	2048	71.48	49.58	23.33	31.48	2048.00
ae	3072	71.58	49.60	23.23	39.92	3072.00
ae	4096	71.60	49.70	23.49	47.99	4096.00
ae	5120	71.63	49.71	23.97	56.97	5120.00
ae	6144	71.72	49.78	23.98	65.55	6144.00
ae	7168	71.68	49.73	23.93	73.72	7168.00
ae	8192	71.62	49.67	23.94	80.72	8192.00
ae	9216	71.72	49.73	24.10	87.39	9216.00
ae	10240	71.70	49.78	23.96	94.21	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
set label 1 "{/:Bold (b)}  VAE" at graph 0.5, graph -0.24 center
set ylabel ""
set y2label ""
set key off
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel ""
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
vae	2	68.78	43.38	19.92	27.32	2.00
vae	4	71.35	46.50	21.52	28.97	4.00
vae	8	71.47	47.33	19.32	29.04	8.00
vae	16	72.75	48.42	21.24	29.15	16.00
vae	32	72.45	48.65	21.24	29.34	32.00
vae	64	72.52	49.36	21.43	29.38	64.00
vae	128	72.60	49.40	21.21	29.04	128.00
vae	256	73.06	50.00	21.94	31.59	256.00
vae	512	72.69	49.93	21.19	35.31	512.00
vae	1024	72.89	50.31	21.17	41.98	1024.00
vae	2048	73.10	50.21	23.25	53.29	2048.00
vae	3072	73.09	50.54	23.29	64.37	3072.00
vae	4096	73.09	50.36	23.04	74.88	4096.00
vae	5120	73.06	50.24	24.58	84.54	5120.00
vae	6144	72.63	49.74	23.95	96.61	6144.00
vae	7168	73.00	50.18	23.86	108.14	7168.00
vae	8192	72.94	49.98	23.88	117.55	8192.00
vae	9216	72.68	49.87	23.56	125.87	9216.00
vae	10240	73.30	50.63	24.21	132.61	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
set label 1 "{/:Bold (c)}  LSTM-AD" at graph 0.5, graph -0.24 center
set ylabel ""
set y2label "Training time (min)"
set key off
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel ""
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
lstm-ad	2	66.94	38.46	21.05	20.24	2.00
lstm-ad	4	68.80	40.02	22.16	20.47	4.00
lstm-ad	8	70.21	41.05	22.30	20.07	8.00
lstm-ad	16	70.59	41.75	23.33	20.06	16.00
lstm-ad	32	70.30	41.33	22.88	19.90	32.00
lstm-ad	64	70.22	41.29	23.00	19.99	64.00
lstm-ad	128	69.74	41.23	23.62	19.93	128.00
lstm-ad	256	70.12	42.19	25.02	23.29	256.00
lstm-ad	512	69.25	41.38	24.42	30.60	512.00
lstm-ad	1024	68.50	41.42	24.12	46.03	1024.00
lstm-ad	2048	67.22	41.33	23.34	68.79	2048.00
lstm-ad	3072	68.75	41.72	23.21	90.72	3072.00
lstm-ad	4096	67.30	40.84	23.16	112.91	4096.00
lstm-ad	5120	67.48	40.85	22.84	135.50	5120.00
lstm-ad	6144	66.30	40.40	22.68	156.98	6144.00
lstm-ad	7168	65.39	39.95	23.05	178.81	7168.00
lstm-ad	8192	67.88	41.50	22.98	197.54	8192.00
lstm-ad	9216	66.36	40.51	22.68	214.28	9216.00
lstm-ad	10240	67.33	41.08	22.86	230.83	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
set label 1 "{/:Bold (d)}  CNN" at graph 0.5, graph -0.24 center
set ylabel "Accuracy"
set y2label ""
set key off
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel ""
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
cnn	2	70.92	43.67	21.69	17.41	2.00
cnn	4	71.71	43.49	22.64	17.18	4.00
cnn	8	74.10	45.87	24.01	17.33	8.00
cnn	16	74.76	47.32	24.91	16.96	16.00
cnn	32	74.78	46.97	24.31	16.99	32.00
cnn	64	74.75	46.91	25.35	17.28	64.00
cnn	128	75.30	47.19	25.35	17.17	128.00
cnn	256	74.88	47.86	26.23	18.08	256.00
cnn	512	75.60	48.55	25.99	19.82	512.00
cnn	1024	75.27	48.58	25.99	23.44	1024.00
cnn	2048	74.89	48.98	26.66	29.61	2048.00
cnn	3072	74.88	48.81	26.25	35.29	3072.00
cnn	4096	74.51	48.99	25.79	41.54	4096.00
cnn	5120	73.94	48.38	26.22	48.41	5120.00
cnn	6144	75.11	49.33	26.17	54.49	6144.00
cnn	7168	73.74	48.26	25.60	60.44	7168.00
cnn	8192	73.84	48.12	25.73	66.31	8192.00
cnn	9216	73.62	47.57	25.64	71.54	9216.00
cnn	10240	72.79	47.21	25.51	76.48	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
set label 1 "{/:Bold (e)}  DAGMM" at graph 0.5, graph -0.24 center
set ylabel ""
set y2label ""
set key off
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel ""
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
dagmm	2	53.37	63.15	0.36	16.99	2.00
dagmm	4	55.07	63.45	0.02	16.90	4.00
dagmm	8	58.30	63.67	0.08	16.72	8.00
dagmm	16	64.87	63.03	0.79	16.62	16.00
dagmm	32	71.07	59.91	5.85	16.72	32.00
dagmm	64	74.38	55.81	13.08	16.48	64.00
dagmm	128	74.41	52.50	17.62	16.77	128.00
dagmm	256	75.15	54.06	16.62	19.93	256.00
dagmm	512	73.64	50.68	17.32	27.19	512.00
dagmm	1024	69.56	46.64	19.16	41.42	1024.00
dagmm	2048	67.99	46.30	20.30	63.46	2048.00
dagmm	3072	68.34	43.89	18.67	82.44	3072.00
dagmm	4096	68.69	44.53	19.17	104.10	4096.00
dagmm	5120	67.26	45.18	16.72	124.55	5120.00
dagmm	6144	66.87	42.10	16.89	145.00	6144.00
dagmm	7168	65.24	42.31	16.97	156.69	7168.00
dagmm	8192	65.18	41.34	16.47	183.62	8192.00
dagmm	9216	64.14	39.45	16.78	200.70	9216.00
dagmm	10240	65.32	42.28	15.74	215.41	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
set label 1 "{/:Bold (f)}  HBOS" at graph 0.5, graph -0.24 center
set ylabel ""
set y2label "Training time (min)"
set key off
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel ""
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
hbos	2	65.97	43.70	10.93	0.08	2.00
hbos	4	67.71	41.92	13.96	0.09	4.00
hbos	8	68.04	41.82	14.32	0.10	8.00
hbos	16	70.93	43.46	14.89	0.10	16.00
hbos	32	70.76	43.50	17.10	0.12	32.00
hbos	64	70.18	43.85	14.91	0.12	64.00
hbos	128	69.42	43.95	14.60	0.16	128.00
hbos	256	69.21	44.13	15.87	0.24	256.00
hbos	512	68.28	43.67	16.14	0.38	512.00
hbos	1024	68.51	43.86	16.23	0.64	1024.00
hbos	2048	67.79	43.88	16.85	1.07	2048.00
hbos	3072	67.79	44.41	17.82	1.35	3072.00
hbos	4096	67.80	44.69	17.28	1.74	4096.00
hbos	5120	67.77	44.71	17.34	2.09	5120.00
hbos	6144	67.44	44.94	17.40	2.42	6144.00
hbos	7168	67.37	45.20	17.59	2.79	7168.00
hbos	8192	67.25	45.52	18.13	3.15	8192.00
hbos	9216	67.20	45.45	17.92	3.35	9216.00
hbos	10240	67.13	45.40	17.81	3.75	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
set label 1 "{/:Bold (g)}  IForest" at graph 0.5, graph -0.35 center
set ylabel "Accuracy"
set y2label ""
set key off
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel "The number of training sliding windows"
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
iforest	2	53.32	63.56	0.00	1.27	2.00
iforest	4	61.29	35.48	12.16	1.22	4.00
iforest	8	64.50	38.96	12.79	1.22	8.00
iforest	16	69.45	42.83	14.74	1.25	16.00
iforest	32	70.05	42.69	14.08	1.24	32.00
iforest	64	70.11	43.69	14.55	1.29	64.00
iforest	128	72.46	45.49	17.29	1.32	128.00
iforest	256	73.47	47.58	18.18	1.48	256.00
iforest	512	73.56	47.32	17.09	1.73	512.00
iforest	1024	72.19	46.34	16.86	2.06	1024.00
iforest	2048	72.70	46.58	17.23	2.59	2048.00
iforest	3072	72.71	46.90	17.61	2.98	3072.00
iforest	4096	72.87	47.07	18.05	3.64	4096.00
iforest	5120	72.81	47.00	18.31	4.27	5120.00
iforest	6144	72.71	46.62	17.82	4.87	6144.00
iforest	7168	72.87	46.79	17.77	5.28	7168.00
iforest	8192	72.67	46.67	18.52	5.78	8192.00
iforest	9216	72.82	46.80	18.46	6.45	9216.00
iforest	10240	72.85	46.74	18.20	6.50	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
set label 1 "{/:Bold (h)}  LOF" at graph 0.5, graph -0.35 center
set ylabel ""
set y2label ""
set key off
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel "The number of training sliding windows"
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
lof	2	64.01	51.73	21.50	0.00	2.00
lof	4	63.74	46.84	21.85	0.00	4.00
lof	8	63.27	44.87	20.74	0.00	8.00
lof	16	63.97	43.93	21.18	0.01	16.00
lof	32	70.15	47.50	24.92	0.01	32.00
lof	64	70.15	47.45	23.42	0.00	64.00
lof	128	74.86	51.84	26.35	0.03	128.00
lof	256	76.95	53.54	26.86	0.07	256.00
lof	512	78.57	55.39	27.21	0.20	512.00
lof	1024	79.30	56.71	30.42	0.65	1024.00
lof	2048	78.89	55.75	29.26	1.93	2048.00
lof	3072	78.58	55.65	29.72	3.56	3072.00
lof	4096	78.51	55.61	29.13	8.07	4096.00
lof	5120	78.41	55.65	29.67	12.96	5120.00
lof	6144	78.40	55.67	29.63	19.16	6144.00
lof	7168	78.33	55.51	28.69	26.74	7168.00
lof	8192	78.35	55.48	29.26	36.11	8192.00
lof	9216	78.32	55.36	29.35	43.09	9216.00
lof	10240	78.30	55.31	28.60	51.25	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
set label 1 "{/:Bold (i)}  OCSVM" at graph 0.5, graph -0.35 center
set ylabel ""
set y2label "Training time (min)"
set key off
set xtics rotate by -45
set y2tics format "%0.0f"
set ytics format "%0.0f"
set xlabel "The number of training sliding windows"
$df << EOF
model_name	data_sample_rate	VUS_ROC	VUS_PR	RF	ori. train time mean	sort_index
ocsvm	2	70.46	47.81	28.54	0.00	2.00
ocsvm	4	72.63	49.57	31.00	0.00	4.00
ocsvm	8	73.89	50.45	31.24	0.00	8.00
ocsvm	16	76.18	52.87	34.17	0.00	16.00
ocsvm	32	76.27	52.96	34.79	0.00	32.00
ocsvm	64	76.46	53.33	33.88	0.00	64.00
ocsvm	128	77.29	53.93	35.37	0.00	128.00
ocsvm	256	77.69	54.83	36.46	0.04	256.00
ocsvm	512	76.83	54.42	35.92	0.10	512.00
ocsvm	1024	75.79	52.91	34.45	0.32	1024.00
ocsvm	2048	74.81	52.05	34.57	0.95	2048.00
ocsvm	3072	74.68	51.96	34.35	1.88	3072.00
ocsvm	4096	74.63	51.94	34.23	3.24	4096.00
ocsvm	5120	74.60	51.91	34.01	4.94	5120.00
ocsvm	6144	74.58	51.90	34.06	6.96	6144.00
ocsvm	7168	74.57	51.88	34.04	9.68	7168.00
ocsvm	8192	74.56	51.86	33.88	12.35	8192.00
ocsvm	9216	74.55	51.85	33.44	15.10	9216.00
ocsvm	10240	74.56	51.83	34.05	17.71	10240.00
EOF
plot $df using 0:3:xticlabels(2) axis x1y1 with lp lc 14 lt 14 title "VUS ROC", $df using 0:4 axis x1y1 with lp lc 15 lt 15  title "VUS PR",$df using 0:5 axis x1y1 with lp lc 16  lt 16 title "RF",$df using 0:6 axis x1y2 with line lc 17 lt 17 title "Training time"
