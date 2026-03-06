
names = strings(numel(streams),1);
for k = 1:numel(streams)
    names(k) = string(streams{k}.info.name);
end
disp(table((1:numel(streams))', names, 'VariableNames',{'idx','name'}));

% Προσπάθεια αυτόματου εντοπισμού
idxPhys = find(contains(lower(names), "opensignals") | contains(lower(names), "biosignals"), 1);
idxFace = find(contains(lower(names), "facestream") | contains(lower(names), "face"), 1);

if isempty(idxPhys)
    error("Δεν βρέθηκε Phys/OpenSignals stream. Δες τον πίνακα που εκτυπώθηκε και βάλε idxPhys χειροκίνητα.");
end
if isempty(idxFace)
    error("Δεν βρέθηκε FaceStream. Δες τον πίνακα που εκτυπώθηκε και βάλε idxFace χειροκίνητα.");
end


% 1) Φυσιολογικά σήματα
phys = streams{idxPhys};

phys_t = phys.time_stamps(:);                 % Nx1 LSL timestamps
ecg    = double(phys.time_series(3,:))';      % RAW0 -> ECG (A2)
eda    = double(phys.time_series(2,:))';      % RAW1 -> EDA (A3)

% 2) FaceStream timestamps (για boundaries ανά εικόνα)
face = streams{idxFace};

face_t = face.time_stamps(:);                 % Mx1 LSL timestamps



face_sec = floor(face_t);                  
[G, ~] = findgroups(face_sec);

% Για κάθε sec-group πάρε ένα αντιπροσωπευτικό timestamp (π.χ. το πρώτο)
t_bound = splitapply(@(x) x(1), face_t, G);
t_bound = sort(t_bound);

% Αν το πρώτο boundary είναι ήδη η αρχή της 2ης εικόνας, τότε το t0 = αρχή φυσιολογικού σήματος.
t0 = phys_t(1);

% Λίστα ορίων: [t0, t1, t2, ...]
bounds = [t0; t_bound];

if numel(bounds) < 11
    error("Δεν βρέθηκαν αρκετά χρονικά όρια από το FaceStream για 10 εικόνες.");
elseif numel(bounds) > 11
    bounds = bounds(1:11);
end

% 3) Κόψιμο ECG/EDA ανά εικόνα
segments = struct();
summary  = table('Size',[10 4], ...
    'VariableTypes',{'double','double','double','double'}, ...
    'VariableNames',{'image_id','t_start','t_end','num_samples'});

for i = 1:10
    t_start = bounds(i);
    t_end   = bounds(i+1);

    idx = (phys_t >= t_start) & (phys_t < t_end);

    segments(i).image_id = i;
    segments(i).t_start  = t_start;
    segments(i).t_end    = t_end;
    segments(i).t        = phys_t(idx);
    segments(i).ecg      = ecg(idx);
    segments(i).eda      = eda(idx);

    summary.image_id(i)    = i;
    summary.t_start(i)     = t_start;
    summary.t_end(i)       = t_end;
    summary.num_samples(i) = sum(idx);
end

% 4) Αποθήκευση
save("ECG_EDA_segments_by_image.mat", "segments", "summary");


writetable(summary, "ECG_EDA_segments_summary.txt", 'Delimiter','\t');

disp("Ολοκληρώθηκε η τμηματοποίηση ECG/EDA ανά εικόνα.");
disp(summary);
