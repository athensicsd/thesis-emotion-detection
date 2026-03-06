file = "ECG_EDA_user20.xlsx";
sheet = "Image_10";

T = readtable(file, "Sheet", sheet);
t_rel = T.time_stamps - T.time_stamps(1);

figure;
tiledlayout(2,1);

nexttile;
plot(t_rel, T.ECG);
title("ECG - " + sheet);
xlabel("Time (s)");
ylabel("ECG (raw)");

nexttile;
plot(t_rel, T.EDA);
title("EDA - " + sheet);
xlabel("Time (s)");
ylabel("EDA (raw)");
