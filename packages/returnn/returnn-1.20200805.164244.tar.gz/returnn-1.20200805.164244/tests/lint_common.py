
"""
Common settings for linters, e.g. pycharm-inspect.py or pylint.py.

Some resources:
https://github.com/google/styleguide
https://google.github.io/styleguide/pyguide.html
https://chromium.googlesource.com/chromium/src/+/master/docs/code_reviews.md#OWNERS-files

Our Python style:
2 space indentation, 120 char line limit, otherwise mostly PEP8,
and follow further common Python conventions (closely follow PyCharm warnings).
"""

import os

_my_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_my_dir)
assert os.path.exists("%s/rnn.py" % _root_dir)


# Proceed like this: Fix all warnings for some file, then remove it from this list.
# I removed already all files which really should not have warnings (mostly the TF backend + shared files).
ignore_count_for_files = {
  'returnn/theano/activation_functions.py',
  'returnn/theano/ops/best_path_decoder.py',
  'returnn/datasets/bundle_file.py',
  'returnn/theano/ops/ctc.py',
  'returnn/datasets/cached.py',
  'returnn/theano/ops/custom_lstm_functions.py',
  'returnn/theano/device.py',
  'returnn/theano/engine.py',
  'returnn/theano/engine_task.py',
  'returnn/util/fsa.py',
  'returnn/theano/ops/function_loader.py',
  'returnn/theano/ops/inv.py',
  'returnn/theano/ops/multi_batch_beam.py',
  'returnn/theano/network.py',
  'returnn/theano/layers/base.py',
  'returnn/theano/layers/cnn.py',
  'returnn/theano/network_copy_utils.py',
  'returnn/theano/layers/ctc.py',
  'returnn/network_description.py',
  'returnn/theano/layers/hidden.py',
  'returnn/theano/layers/basic.py',
  'returnn/theano/layers/lstm.py',
  'returnn/theano/layers/output.py',
  'returnn/theano/layers/rec.py',
  'returnn/theano/network_stream.py',
  'returnn/theano/layers/twod.py',
  'returnn/datasets/normalization_data.py',
  'returnn/theano/ops/blstm.py',
  'returnn/theano/ops/inv_align.py',
  'returnn/theano/ops/lstm.py',
  'returnn/theano/ops/lstm_cell.py',
  'returnn/theano/ops/lstm_custom.py',
  'returnn/theano/ops/lstm_rec.py',
  'returnn/theano/ops/numpy_align.py',
  'returnn/datasets/raw_wav.py',
  'returnn/theano/recurrent_transform.py',
  'returnn/theano/server.py',
  'returnn/datasets/stereo.py',
  'returnn/tf/layers/neural_transducer.py',
  'returnn/tf/layers/segmental_model.py',
  'returnn/tf/layers/signal_processing.py',
  'returnn/util/task_system.py',
  'returnn/util/task_system_example.py',
  'returnn/theano/util.py',
  'returnn/theano/ops/torch_wrapper.py',
  'returnn/theano/ops/two_state_best_path_decoder.py',
  'returnn/theano/ops/two_state_hmm.py',
  'returnn/theano/updater.py',
}


def find_all_py_source_files():
  """
  :rtype: list[str]
  """
  # Earlier this was a `glob("%s/*.py" % _root_dir)`. But not anymore, since we have the new package structure.
  src_files = []
  for root, dirs, files in os.walk(_root_dir):
    if root == _root_dir:
      root = ""
    else:
      assert root.startswith(_root_dir + "/")
      root = root[len(_root_dir) + 1:]  # relative to the root
      root += "/"
    for file in files:
      if file.endswith(".py"):
        src_files.append(root + file)
  src_files.sort(key=lambda fn: fn.split("/"))
  return src_files
