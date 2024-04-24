from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define your data augmentation
data_augmentation = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2  # Using this for validation split as cross-validation is more complex and not directly supported
)

# Training data generator
train_generator = data_augmentation.flow_from_directory(
    'images/',  # Assuming this is your dataset directory with subfolders for each class
    target_size=(224, 224),  # Adjust based on your model input size
    batch_size=32,
    class_mode='categorical',  # Assuming a multi-class classification problem
    subset='training'  # Use this for splitting dataset
)

# Validation data generator
validation_generator = data_augmentation.flow_from_directory(
    'images/',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'  # Use this for splitting dataset
)
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Load MobileNetV2 as the base model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the base model
base_model.trainable = False

# Add custom layers on top for the classification task
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

# Final model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(
    train_generator,
    epochs=100,  # Adjust based on requirements
    validation_data=validation_generator
)
model.save('your_model.h5')

# Access and print the class indicies to use in app.py
class_indices = train_generator.class_indices
print(class_indices)