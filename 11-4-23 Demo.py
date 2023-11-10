import PIL
import keras
from keras.models import Sequential
from keras import layers
from keras.utils import np_utils
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from PIL import Image
import numpy as np

def convert_pic(file_name, size):
    temp_pic = PIL.Image.open(file_name, mode='r')
    temp_pic.thumbnail(size)
    temp_arr = np.array(temp_pic)
    temp_arr = temp_arr.astype('float32')
    temp_arr = temp_arr / 255
    return temp_arr

size = 32, 32
total_arr_prev = []
total_labels = []

temp_labels = ['plane','cat','frog', 'person']
#temp_labels = ['plane','cat','frog']
max_photos = 5
counter = 1
for label in temp_labels:
    for index in range(1,max_photos+1):
        temp_filename = label+"_test"+str(index)+".jpg"
        total_arr_prev.append(convert_pic(temp_filename, size))
        total_labels.append(counter)
    counter = counter + 1

#For demo only
#"""
test_person_photo = convert_pic('person_test6.jpg', size)
test_person_photo = np.array([test_person_photo])
#"""

total_arr = np.array(total_arr_prev)
total_labels = np.array(total_labels)
print(type(total_arr))
print(type(total_labels))
print("This is total_labels: ", total_labels)

X_train, X_test, y_train, y_test = train_test_split(total_arr, total_labels, test_size=0.25, random_state=10)

num_classes = len(temp_labels)+1

# One hot encoding the target class (labels)
y_train = np_utils.to_categorical(y_train, num_classes)
y_test = np_utils.to_categorical(y_test, num_classes)

model = Sequential()

model.add(layers.Conv2D(32, (3,3), padding='same', activation='relu', input_shape=(32,32,3)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(32, (3,3), padding='same', activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(64, (3,3), padding='same', activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(64, (3,3), padding='same', activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.5))

model.add(layers.Conv2D(128, (3,3), padding='same', activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(128, (3,3), padding='same', activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.5))

model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(num_classes, activation='softmax'))    # num_classes = 10

model.compile(optimizer='adam', loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])
history = model.fit(X_train, y_train, batch_size=64, epochs=100, validation_data=(X_test, y_test))

demo_model2 = keras.models.load_model("demo_model.h5")

# Visualizing some of the images from the training dataset
"""
plt.figure(figsize=[10,10])
for i in range (len(X_train)):    # for first 25 images
  plt.subplot(5, 5, i+1)
  plt.xticks([])
  plt.yticks([])
  plt.grid(False)
  plt.imshow(X_train[i], cmap=plt.cm.binary)
  plt.xlabel(temp_labels[y_train[i][0]])

plt.show()
"""

print("X_test: ", len(X_test))
pred_tot = model.predict(X_test)
#pred_tot = model.predict(total_arr)
#pred_tot = demo_model2.predict(total_arr)
pred_tot_class = np.argmax(pred_tot, axis=1)
print("This is pred_tot_class: ", pred_tot_class)

#For demo only
#"""
pred_human_example = model.predict(test_person_photo)
pred_human_example_class = np.argmax(pred_human_example, axis=1)
print("This is pred_human_example_class: ", pred_human_example_class)
#"""

# Plotting the Actual vs. Predicted results
fig, axes = plt.subplots(5, 5, figsize=(15,15))
axes = axes.ravel()

for i in np.arange(0, len(X_test)):
    axes[i].imshow(total_arr[i])
    axes[i].set_title("True: %s \nPredict: %s" % (temp_labels[np.argmax(total_labels[i])], temp_labels[pred_tot_class[i]]))
    axes[i].axis('off')
    plt.subplots_adjust(wspace=1)

plt.show()
