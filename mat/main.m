clc
clear
close all

fname = '../output/161002_000126_nodeList.csv'

% load data file
fileID = fopen(fname);
dates = textscan(fileID,'%s %*[^\n]');
fclose(fileID);

% scan for unique char
jj = 1;
for ii = 1 : size(dates{1})
    if dates{1,1}{ii,1}(1,1) == '>'
        struct2anal{jj} = dates{1,1}{ii,1};
        jj = jj + 1;
    end
end
clear dates

out(1) = 1;

font_size_label = 14;
font_size = 14;
for jj = 1 : size(struct2anal, 2)
    delimiter = ',';
    C = strsplit(struct2anal{1,jj},delimiter);
    for ii = 2:size(C,2)
        data2anal{jj}(ii) =  str2double(C{1,ii});
    end
    c_delay = data2anal{jj}(2:2:end);
    delay = data2anal{jj}(3:2:end);

    out = c_delay.*delay;
%    for ii = 1 : size(delay,2)
%        out = [out, repmat(c_delay(ii), 1, delay(ii))];
%     end
    stat(jj, 1) = sum(c_delay.*delay) / sum(delay);
    stat(jj, 2) = mean(out');
    stat(jj, 3) = mode(out');
    stat(jj, 4) = median(out');
    stat(jj, 5) = std(c_delay.*delay);
    clear out
    h_figure = figure;
    h_axes = axes();
    plot(c_delay, 10*log10(delay),'b.','linewidth',1,'markersize', 12);
    hold on
    xlabel('Delay [hours]','FontSize',font_size_label); 
    ylabel('Quantity [dB]','FontSize',font_size_label); 
    title(['Histogram of month ',C{1,1}([2])],'FontSize',font_size_label)
    set(h_axes, 'FontSize', font_size)
    set(h_figure, 'position',[200 100 800 700]); % dolni roh [x y] horni roh [x y]
    set(h_figure(:),'color',[1 1 1]);


    p = polyfit(c_delay, 10*log10(delay), 80)
   
    approx = polyval(p, c_delay);
    approx(approx<0)=0
    approx(approx>max(10*log10(delay)))=max(10*log10(delay));
    
    plot(c_delay, approx,'r.')
    saveas(h_figure,['pics/month',C{1,1}([2]),'.tiff'])
end



    
