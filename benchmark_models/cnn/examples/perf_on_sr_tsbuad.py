from benchmark_models.tsbuad.models.cnn import cnn
from pysearchlib.share.example_helper import ExampleHelper

model = cnn(slidingwindow=ExampleHelper.WINDOW_SIZE, epochs=ExampleHelper.EPOCH, batch_size=ExampleHelper.BATCH_SIZE)
ExampleHelper.observation_model(model)
