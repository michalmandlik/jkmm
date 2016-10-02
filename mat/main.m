clc
clear
close all

fname = '../output/161002_000126_nodeList.csv'
% fname = '../output/aa'
% numlines = str2num( perl('count.pl', fname) );

% fid = fopen(fname);
% x=fscanf(fid,'%d',[2,2]);
% 
% 
% fclose(fid);

fileID = fopen(fname);
dates = textscan(fileID,'%s %*[^\n]');
fclose(fileID);


jj = 1;
for ii = 1 : size(dates{1})
    if dates{1,1}{ii,1}(1,1) == '+'
        weekday{jj} = dates{1,1}{ii,1};
        jj = jj + 1;
    end
end
clear dates

delimiter = ',';
C = strsplit(weekday{1,1},delimiter);
for ii = 2:size(C,2)
    data(ii) =  str2double(C{1,ii});
end
    
