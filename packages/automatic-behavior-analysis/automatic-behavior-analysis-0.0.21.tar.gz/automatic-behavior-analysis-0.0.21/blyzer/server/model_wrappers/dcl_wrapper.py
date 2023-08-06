import os

import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.contrib.slim.nets import resnet_v1

from blyzer.server.model_wrappers.base_wrapper import BaseModelWrapper


class DclModelWrapper(BaseModelWrapper):

    def __init__(self, model_root, config):
        super().__init__()

        self._model_path = os.path.join(model_root, config.get('model_path'))
        self._bodyparts = config.get('bodyparts')
        self._location_refinement = config.get('location_refinement', True)

        self._net_type = config.get('net_type')
        self._locref_stdev = config.get('locref_stdev')
        self._num_joints = config.get('num_joints')
        self._pcutoff = config.get('pcutoff', 0.0)

        self._output_stride = config.get('output_stride', 16)
        self._deconvolutionstride = config.get('deconvolutionstride', 2)
        self._weight_decay = config.get('weight_decay', 0.0001)
        self._stride = config.get('stride', 8.0)

        self.sess, self.inputs, self.outputs = self._setup_pose_prediction()
        self.name = "DLC"

    def _setup_pose_prediction(self):
        # tf.logging.set_verbosity(tf.logging.ERROR)
        tf.reset_default_graph()
        graph = tf.Graph()
        with graph.as_default():
            inputs = tf.placeholder(tf.float32, shape=(None, None, None, 3))
            net_heads = self._test(inputs)
            outputs = [net_heads['part_prob']]
            if self._location_refinement:
                outputs.append(net_heads['locref'])
            restorer = tf.train.Saver()
            sess = tf.Session()
            sess.run(tf.global_variables_initializer())
            sess.run(tf.local_variables_initializer())
            restorer.restore(sess, self._model_path)
        return sess, inputs, outputs

    def _prediction_layer(self, input_data, name, num_outputs):
        with slim.arg_scope([slim.conv2d, slim.conv2d_transpose],
                            padding='SAME',
                            activation_fn=None,
                            normalizer_fn=None,
                            weights_regularizer=slim.l2_regularizer(
                                self._weight_decay)):
            with tf.variable_scope(name):
                pred = slim.conv2d_transpose(
                    input_data,
                    num_outputs,
                    kernel_size=[3, 3],
                    stride=self._deconvolutionstride,
                    scope='block4')

                return pred

    def _extract_features(self, inputs):
        net_funcs = {
            'resnet_50': resnet_v1.resnet_v1_50,
            'resnet_101': resnet_v1.resnet_v1_101,
            'resnet_152': resnet_v1.resnet_v1_152
        }
        net_fun = net_funcs[self._net_type]

        with slim.arg_scope(resnet_v1.resnet_arg_scope()):
            net, end_points = net_fun(
                inputs,
                global_pool=False,
                output_stride=self._output_stride,
                is_training=False)

        return net, end_points

    def _prediction_layers(self, features, end_points, reuse=None):
        import re
        # num_layers = re.findall('resnet_([0-9]*)',
        #                         self._net_type)[0]
        # layer_name = 'resnet_v1_{}'.format(num_layers) + '/block{}/unit_{}/bottleneck_v1'

        out = {}
        with tf.variable_scope('pose', reuse=reuse):
            out['part_pred'] = self._prediction_layer(
                features, 'part_pred', self._num_joints)

            if self._location_refinement:
                out['locref'] = self._prediction_layer(
                    features, 'locref_pred', self._num_joints * 2)
        return out

    def _get_net(self, inputs):
        net, end_points = self._extract_features(inputs)
        return self._prediction_layers(net, end_points)

    def _test(self, inputs):
        heads = self._get_net(inputs)
        prob = tf.sigmoid(heads['part_pred'])
        return {'part_prob': prob, 'locref': heads['locref']}

    def _extract_cnn_output(self, outputs_np):
        scmap = outputs_np[0]
        locref = None
        if self._location_refinement:
            locref = outputs_np[1]
            shape = locref.shape
            locref = np.reshape(locref, (shape[0], shape[1], shape[2], -1, 2))
            locref *= self._locref_stdev
        # if len(scmap.shape) == 2:
        #     scmap = np.exand_dims(scmap, axis=2)
        return scmap, locref

    def _argmax_pose_predict(self, scmap, offmat):
        num_joints = scmap.shape[3]
        batch_size = scmap.shape[0]
        pose = []
        for batch_i in range(batch_size):
            batch_pose = []
            for joint_i in range(num_joints):
                maxloc = np.unravel_index(np.argmax(scmap[batch_i, :, :, joint_i]),
                                          scmap[batch_i, :, :, joint_i].shape)
                offset = np.array(offmat[batch_i][maxloc][joint_i])[::-1]
                pos_f8 = (np.array(maxloc).astype('float')
                          * self._stride + 0.5
                          * self._stride + offset)
                batch_pose.append(np.hstack((pos_f8[::-1], [scmap[batch_i][maxloc][joint_i]])))
            pose.append(np.array(batch_pose))
        return pose

    def _get_pose(self, output_np):
        scmap, locref = self._extract_cnn_output(output_np)
        pose = self._argmax_pose_predict(scmap, locref)
        return pose

    def _prepare_report_to_client(self, poses_batch, image):
        '''
        JSON_EXAMPLE
        {
           "objects":[
              {
                 "id":1,

                 "keypoints":{
                    "Nose":{
                       "rate":0.333,
                       "x1":0.5474013566039503,
                       "y1":0.7267645253075494
                    },
                    "Head":{
                       "rate":0.333,
                       "x1":0.5474013566039503,
                       "y1":0.7267645253075494
                    },
                    "Coccyx":{
                       "rate":0.333,
                       "x1":0.5474013566039503,
                       "y1":0.7267645253075494
                    },
                    "Tail":{
                       "rate":0.333,
                       "x1":0.5474013566039503,
                       "y1":0.7267645253075494
                    },

                 }
              }
           ]
        }
        '''
        height = image.shape[1]
        width = image.shape[2]
        report = []

        for num, sample in enumerate(poses_batch):
            bodyparts_dict = {}
            for i in range(sample.shape[0]):
                likelihood = sample[i, 2]
                if  likelihood > self._pcutoff:
                        bodyparts_dict[self._bodyparts[i]] = {"x": sample[i, 0],
                                                              "y": sample[i, 1],
                                                              "rate": sample[i, 2]}
                else:
                    bodyparts_dict[self._bodyparts[i]] = {}
            report.append(bodyparts_dict)

        return report

    def predict(self, image):
        '''
        Returns predict dictionary for an image or batch of images
        -----------
        parameters:
            image: numpy array
                    shape: (w, h, ch) -- image
                    shape: (bs, w, h, ch) -- batch
                Evaluation image or batch of images
        -----------
        returns:
            bodyparts: [dict]
                List of dictionaries 'bodypart': {"x":float, "y":float, "rate":float}, one for each image in batch.
                Passing single image to function will still result in returning a list.
        '''
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0).astype(float)

        net_output = self.sess.run(self.outputs, feed_dict={self.inputs: image})
        poses_batch = self._get_pose(net_output)

        return self._prepare_report_to_client(poses_batch, image)
