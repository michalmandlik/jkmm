clc
clear
close all

lambda = .3;
x = -10:0.1:200;

for ii = 1 : length(x)
    if x(ii) > 0
        out(ii) = 10 * lambda * exp(-lambda * x(ii));
    elseif x == 0
        out(ii) = 100 * rand(10,1);
    end
end

out = out + (0.5*rand(1, length(x))-1);
out = out + 0.1*rand(1, length(x));
out = out + 0.1*rand(1, length(x));


res(1,1) = mean(out');
res(2,1) = mode(out');
res(3,1) = median(out');
res(4,1) = std(out');

db_lin = 10.^(out/10);

res(1,2) = mean(db_lin');
res(2,2) = mode(db_lin');
res(3,2) = median(db_lin');
res(4,2) = std(db_lin');

font_size_label = 14;
font_size = 14;
h_figure = figure;
h_axes = axes();
plot(x, 10.^(out/10),'b.','linewidth',1,'markersize', 12);
hold on
xlabel('samples [-]','FontSize',font_size_label); 
ylabel('Distribution [-]','FontSize',font_size_label); 
title('Histogram test' , 'FontSize',font_size_label)
set(h_axes, 'FontSize', font_size)
set(h_figure, 'position',[200 100 800 700]); % dolni roh [x y] horni roh [x y]
set(h_figure(:),'color',[1 1 1]);
saveas(h_figure,['dist/dist_fce.tiff'])
