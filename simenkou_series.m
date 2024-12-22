clc;clear;close all;
%% read table
opts = delimitedTextImportOptions("NumVariables", 2);
opts.DataLines = [1, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["time", "level"];
opts.VariableTypes = ["string", "double"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
opts = setvaropts(opts, "time", "WhitespaceRule", "preserve");
opts = setvaropts(opts, "time", "EmptyFieldRule", "auto");
tbl = readtable("./result/focus_info.csv", opts);
time = tbl.time;
level = tbl.level;
clear opts tbl
%% precedure time series
n = length(time);
formatX = cell(1,n);
for i = 1 : n
    time{i} = time{i}(1:8);
    formatX{i} = time{i};
    %day = time{i}(1:2);
    %hour = time{i}(4:5);
    %minute = time{i}(7:8);
    %formatTimeStr = [day, '/12/2024 ',hour,':',minute,':00'];
    %formatX{i} = datetime(formatTimeStr,'InputFormat','dd/MM/uuuu HH:mm:ss');
end
plot(1:n,level,'LineWidth',2,'Color','black');
xticklabels(formatX)
yticks(1:4);
yticklabels({'畅通','轻度拥堵','拥堵','重度拥堵'})
xlabel("观测时间",FontSize=14)
ylabel("拥堵等级",FontSize=14)
axis([0.5 n+1 0.5 4.5])