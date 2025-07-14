% changes the default Godosim annotations to COCO JSON format
clc;clear;close all;

% path to the folder which contains the generated data folders "annotations" and "images"
path_data = 'C:\Users\JohnDoe\Documents\Godosim_validation';
% relative path to the annotations.csv file
file_annotations = fullfile('annotations','annotations.csv');

cd(path_data);

T = readtable(file_annotations);
file_info = dir(file_annotations);
date_created = datetime(file_info.date);
[y, m, d] = ymd(date_created);

% create a struct that will hold the relevant information in the annotations table; a struct is simple to convert to JSON in MATLAB with the jsonencode() function
dataset = struct;

field_names = fieldnames(T);

% loop through rows in the original annotations table
for row = 1:height(T)

    keypoints = [];
    keypoint_names = field_names(contains(field_names,'vm_'));
    keypoint_names = cellfun(@(x) x(4:end-2) , keypoint_names, 'UniformOutput', false);
    keypoint_names = unique(keypoint_names);
    % keypoints are added in 1D vector in format [x, y, visibility, x, y, visibility, ...]
    for i = 1:numel(keypoint_names)
        current_keypoint_name = keypoint_names{i};
        new_keypoints = [T.(['vm_' current_keypoint_name '_x'])(row), T.(['vm_' current_keypoint_name '_y'])(row), T.(['visibility_' current_keypoint_name])(row)];

        % we modify the visibility flag (3rd element of new_keypoints) so that it's 0 if the annotation is out of image bounds, 1 if it's clearly occluded, and 2 otherwise (visible, unoccluded)
        if new_keypoints(1) < 0 || new_keypoints(2) < 0 || new_keypoints(1) > 1024 || new_keypoints(2) > 1024
            new_keypoints(3) = 0;
        elseif round(1/new_keypoints(3)) > 1
            new_keypoints(3) = 1;
        else
            new_keypoints(3) = 2;
        end

        keypoints = [keypoints, new_keypoints];
    end

    img_id = T.file_names{row}(end-9:end);

    % annotations
    dataset.annotations(row).area = T.bb_w(row)*T.bb_h(row);
    dataset.annotations(row).bbox = [T.bb_x(row), T.bb_y(row), T.bb_w(row), T.bb_h(row)];
    dataset.annotations(row).category_id = 1;
    dataset.annotations(row).id = img_id;
    dataset.annotations(row).image_id = img_id;
    dataset.annotations(row).iscrowd = 0;
    dataset.annotations(row).keypoints = keypoints;
    dataset.annotations(row).num_keypoints = numel(keypoint_names);
    % we don't use segmentation in this script, so we just set it to bbox
    dataset.annotations(row).segmentation = dataset.annotations(row).bbox;

    % images
    dataset.images(row).file_name = ['../images/' T.file_names{row} '.jpg'];
    dataset.images(row).id = img_id;
    dataset.images(row).height = 1024;
    dataset.images(row).width = 1024;
    dataset.images(row).license = 1;

end

% categories
dataset.categories = {struct};
dataset.categories{1}.id = 1;
dataset.categories{1}.name = 'person';

% info
dataset.info.contributor = 'Jere Lavikainen';
dataset.info.date_created = [num2str(y) '/' num2str(m,'%.2i') '/' num2str(d,'%.2i')];
dataset.info.description = 'Godosim sample dataset';
dataset.info.url = 'https://github.com/jerela/Godosim';
dataset.info.version = 1;
dataset.info.year = 2025;

% licenses
dataset.licenses = {struct};
dataset.licenses{1}.id = 1;
dataset.licenses{1}.name = 'License for non-commercial scientific research purposes';
dataset.licenses{1}.url = 'https://bedlam.is.tue.mpg.de/license.html';

% finally, convert MATLAB struct to JSON
% using prettyprint makes it a bit more readable; set to false if you want
% to minimize file size
dataset_coco = jsonencode(dataset,'PrettyPrint',true);

% save the JSON format annotations to file
fid = fopen('annotations_coco_format.json','w');
fprintf(fid,'%s',dataset_coco);
fclose(fid);
