# Convolutional Neural Network

## Uses the GTSRB (German Traffic Sign Recognition Benchmark) data set to train a CNN to be able to detect road signs in traffic.

## Uses Tensorflow.

## At first, I was trying the not so deep network in the lecture but I kept getting about 5% accuracy and then I kept trying more deep networks but the accuracy still didn't increase, then I searched for some deep networks architecture online and used some of them but accuracy kept at about 5%, until I finally found out that the problem was not in the model itself but in the loading data function, I used the resize function of numpy at first which resulted in the 5% accuracy, but once I used the cv2.resize() function the accuracy instantly shot up to the 90-96 % values.

## Then I found that the model was suffering heavily from overfitting as the training accuracy was about 2% higher than test accuracy since I had the deep networks from the first expirements, then I kept reducing the complexity of the network bit by bit and I increased the dropout rate in several layers, then the network's accuracy went down by about 3% so I kept only the dropout layer after the final layer and reduced layers to the one that looks like the one in the lecture, then I kept tweaking with the dropout rate in the final layer until I found that training accuracy and test accuracy are approximately equal.

## Final accuracy I reached was:
 * ## Training accuracy: 96.72%
 * ## Test accuracy: 97.3%

## GTSRB data set: https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip

## Demo Video: https://youtu.be/z_FonKyaZnw
