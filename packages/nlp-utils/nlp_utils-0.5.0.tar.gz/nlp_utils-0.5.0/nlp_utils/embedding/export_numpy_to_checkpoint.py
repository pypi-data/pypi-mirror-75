import numpy as np
import tensorflow as tf


def export_numpy_to_checkpoint(data, checkpoint, tensor_name="embedding"):
    variable = tf.Variable(data, dtype=tf.float32, trainable=False, name=tensor_name)

    # Add an op to initialize the variables.
    init_op = tf.global_variables_initializer()

    # Add ops to save and restore all the variables.
    saver = tf.train.Saver()

    with tf.Session() as sess:
        # sess = tf_debug.LocalCLIDebugWrapperSession(sess)

        sess.run(init_op)
        result = sess.run(variable)

        print(result)

        save_path = saver.save(sess, checkpoint)
        print("Model saved in path: %s" % save_path)
