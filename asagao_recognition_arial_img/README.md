# Asagao Tree Recognition from aerial images
> Simple test CNN performance on recognize asagao location using aerial image from difference heigth. The dataset is created by highlighed location (using red line) of Asagao. The program crops only target and segments the target into smaller images and then uses as dataset.
>The image is segment to smaller size and each tiled images are then fed to the network. Finally, the tiled prediction is stiched back to original size.

- Classifier   : UNET
- Framework    : Tensorflow + OpenCV
- languange    : Python