import tensorflow as tf
from mpunet.models import UNet

def loss(model, x, y, training):
    p = model(x, training=training)
    return model.loss[0](y_true=y, y_pred=p)


def grad(model, x, y):
    with tf.GradientTape() as tape:
        loss_value = loss(model, x, y, True)
    return tf.reduce_mean(loss_value), \
           tape.gradient(loss_value, model.trainable_variables)


def gen():
    import numpy as np
    while True:
        yield np.random.randn(16, 192, 192, 1).astype(np.float32), \
              np.random.randint(0, 3, 16*192*192).reshape([16, 192*192, 1]).astype(np.uint8)


@tf.function
def training_loop(model, train, optimizer, epochs=100):
    for epoch in range(epochs):
        for x, y in train.take(100):
            loss_value, gradients = grad(model, x, y)
            optimizer.apply_gradients(list(zip(gradients,
                                               model.trainable_variables)))
            print('here')


if __name__ == "__main__":
    model = UNet(n_classes=3, dim=192, flatten_output=True)
    model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy')

    train = tf.data.Dataset.from_generator(gen,
                                           (tf.float32, tf.uint8),
                                           (tf.TensorShape([16, 192, 192, 1]),
                                            tf.TensorShape([16, 192 *192, 1])))

    model.fit(train, epochs=10, steps_per_epoch=10)

    #training_loop(model, train, optimizer=model.optimizer)
