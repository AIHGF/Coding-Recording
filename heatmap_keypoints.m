
clear

test_image = ‘xxx.jpg’;
points_data = [];% 关键点位置，2D形式

points = zeros(16, 2);
for i = 1:16
    id = points_data(i).id + 1;
    points(id,:) = [points_data(id).x, points_data(id).y];
end

heatmapVisualize(test_image,  points)

%%
function heatmapVisualize(test_image,  points)

np =16;
im = imread(test_image);
im_size = [size(im, 2), size(im, 1)];

sigma = 20;
% plot all body parts and background
imToShow  = single(zeros(size(im, 1), size(im, 2), 3));
for id = 1:np
    point = points(id, :);
    x = point(1);
    y = point(2);
    response = producePointMap(im_size, x, y, sigma);
    response = response{1};
    max_value = max(max(response));
    mapIm = mat2im(response, jet(100), [0 max_value]);
    imHeatMap = mapIm*0.5 + (single(im)/255)*0.5;
    imToShow = imToShow + imHeatMap;
    imshow(imHeatMap);
    
    hold on;
    plot(points(id,1), points(id,2), 'wx', 'LineWidth', 2);
end

%% plot full pose
imshow(im(y_start:y_end, x_start:x_end, :));
hold on;
bodyHeight = max(points(:,2)) - min(points(:,2));
plot(points(:,1), points(:,2), 'k.', 'MarkerSize', bodyHeight/32);
title('Full Pose');

function label = producePointMap(im_size, x, y, sigma)
    % this function generates a gaussian peak centered at position (x,y)
    % it is only for center map in testing
    [X,Y] = meshgrid(1:im_size(1), 1:im_size(2));
    X = X - x;
    Y = Y - y;
    D2 = X.^2 + Y.^2;
    Exponent = D2 ./ 2.0 ./ sigma ./ sigma;
    label{1} = exp(-Exponent);
