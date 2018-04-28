import sys
import tensorflow as tf
from model import captcha_cnn,X,keep_prob
import numpy as np
import cv2
import denoise_opencv
import conf

num2str = {
    0: "2",1: "3",2: "4",3: "5",4: "6",5: "7",6: "8",7: "9",8: "A",
    9: "B",10: "C",11: "D",12: "E",13: "F",14: "G",15: "H",16: "J",
    17: "K",18: "L",19: "M",20: "N",21: "P",22: "Q",23: "R",24: "S",
    25: "T",26: "U",27: "V",28: "W",29: "X",30: "Y",31: "Z"
}

def test(output,sess):
    prediction = tf.nn.softmax(output)
    result = tf.argmax(prediction, 1)
    f = open("mappings.txt", "w")

    for i in range(conf.TEST_NUMBER):
        # Open images
        name = str(i).zfill(4)
        image = cv2.imread(conf.TEST_IMAGE_PATH+"/"+name+".jpg", cv2.IMREAD_GRAYSCALE)

        # Cut the captcha into five characters.
        cut_list = [image[:, 0:44], image[:, 36:80], image[:, 76:120], image[:, 116:160], image[:, 153:197]]

        # Image preprocessing.
        for j in range(len(cut_list)):
            cut_list[j] = denoise_opencv.remove_noise(cut_list[j])
            cut_list[j] = cut_list[j].reshape([44,60,1]) / 255.0

        # Get predictions.
        num_list = sess.run(result, feed_dict={X: cut_list, keep_prob: 1.0}) # 传入模型进行预测
        prediction_list = [num2str[num] for num in num_list]

        # Write predictions into mappings.txt.
        f.write(str(i).zfill(4)+","+"".join(prediction_list)+"\n")
        sys.stdout.write('\r>> Testing image %d/%d' % (i+1,conf.TEST_NUMBER))
        sys.stdout.flush()

if __name__ == '__main__':
    output, _ = captcha_cnn()
    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver.restore(sess, conf.MODEL_PATH)
    test(output,sess)