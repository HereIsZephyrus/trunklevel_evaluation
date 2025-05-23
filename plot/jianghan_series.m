clc;clear;close all;
%% read table1
opts = delimitedTextImportOptions("NumVariables", 6);
opts.DataLines = [1, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["name","time", "distance","speed","status","trend"];
opts.VariableTypes = ["categorical","string", "double","double","double","categorical"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
opts = setvaropts(opts, "time", "WhitespaceRule", "preserve");
opts = setvaropts(opts, "time", "EmptyFieldRule", "auto");
tbl = readtable("../result/jianghan_section_info_adjust.csv", opts);
time = tbl.time(2:end);
level = tbl.status(2:end);
speed = tbl.speed(2:end);
clear opts tbl
%% read table2
opts = delimitedTextImportOptions("NumVariables", 2);
opts.DataLines = [2, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["time", "count1"];
opts.VariableTypes = ["datetime", "double"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
opts = setvaropts(opts, "time", "InputFormat", "yyyy-MM-dd HH:mm:ss");
tbl = readtable("../result/count_result_total_adjust.csv", opts);
ntime = tbl.time(2:end);
ncount = tbl.count1(2:end);
%% load colormap
colormap = TheColor('hunt',570);
%% precedure time series
n = length(time);
formatX = cell(1,n);
for i = 1 : n
    formatX{i} = time{i};
end
hold on
yyaxis left
statusline = line(1:n,level,'LineWidth',3,'Color',colormap(1,:));
hYLabel1 = ylabel("拥堵等级",FontSize=14);
set(gca, 'YColor', [.1 .1 .1],...  
         'YTick', 1:4,... 
         'Ylim' , [0.5 4.5], ...
         'Yticklabel',{'畅通','轻度拥堵','拥堵','重度拥堵'});  
yyaxis right
numberbar = bar(1:length(ntime),ncount/12,'grouped','FaceAlpha',0.5,'FaceColor',colormap(3,:));
speedline = plot(1:n,speed,'LineWidth',2,'Color',colormap(4,:),'LineStyle','-','Marker','+');
text(numberbar.XEndPoints,numberbar.YEndPoints,string(ncount),'HorizontalAlignment','center',...
    'VerticalAlignment','bottom','FontSize',10);
hYLabel2 = ylabel("通行速度(km/h)",FontSize=14);
set(gca, 'YColor', [.1 .1 .1],... 
         'YTick', 0:5:20,... 
         'Ylim' , [0 20]); 
hold off
legend("拥堵等级","通行数量","通行速度",'Location','north',Orientation='horizontal',fontsize = 12)
xticks(1:5:23)
xticklabels(formatX(1:5:23))
%xticklabels(formatX)
xlabel("观测时间",FontSize=14)
hold on

hold off