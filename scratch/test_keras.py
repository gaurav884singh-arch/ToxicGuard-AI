import os
os.environ["KERAS_BACKEND"] = "torch"
try:
    import keras
    print("Keras loaded successfully with backend:", keras.backend.backend())
except Exception as e:
    import traceback
    traceback.print_exc()
