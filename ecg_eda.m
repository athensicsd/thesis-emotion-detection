phys = streams{idxPhys};
outFile = "ECG_EDA_user20.xlsx";

t = phys.time_stamps(:);
noise = double(phys.time_series(1, :))';
eda   = double(phys.time_series(3, :))';
ecg   = double(phys.time_series(2, :))';


if isfile(outFile), delete(outFile); end

for i = 1:height(summary)
    t_start = summary.t_start(i);
    t_end   = summary.t_end(i);

    idx = (t >= t_start) & (t < t_end);

    Ti = table(t(idx), noise(idx), ecg(idx), eda(idx), ...
        'VariableNames', {'time_stamps','nSeq','ECG','EDA'});

    writetable(Ti, outFile, 'Sheet', sprintf("Image_%02d", i));
end

