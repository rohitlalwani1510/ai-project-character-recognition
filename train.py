import tensorflow as tf
from emnist import list_datasets
from emnist import extract_training_samples
from emnist import extract_test_samples
import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns

# print(list_datasets())

letters_images, letters_labels = extract_training_samples('letters')
# print(images.shape)
# print(labels.shape)
digits_images, digits_labels = extract_training_samples('digits')
letters_labels=letters_labels + 9
final_images = np.concatenate((digits_images, letters_images), axis=0)
final_labels = np.concatenate((digits_labels, letters_labels), axis=0)
# print(final_labels)
# print(final_images[0]/255)
# plt.imshow(final_images[0]/255)
# plt.show()

test_images, test_labels = extract_test_samples('letters')
test_images1, test_labels1 = extract_test_samples('digits')
test_labels = test_labels + 9
test_images = np.concatenate((test_images1, test_images), axis=0)
test_labels = np.concatenate((test_labels1, test_labels), axis=0)
a = []
for i in test_labels:
    if i not in a:
        a.append(i)
# print(sorted(a))

final_images = final_images / 255.0
test_images = test_images / 255.0

model = tf.keras.Sequential([
    tf.keras.layers.Reshape((28,28,1)),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(36, activation='linear')
])

model.compile(optimizer='adam',
             loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
             metrics=['accuracy'])

# print(tf.keras.backend.eval(model.optimizer.lr))

model.fit(final_images, final_labels, epochs=5)

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

# print(test_loss, test_acc)

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

