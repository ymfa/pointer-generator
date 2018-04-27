import sys, os, glob, subprocess, struct
from tensorflow.core.example import example_pb2

def filename_converter(filepath):
  """
  Function to name the tokenized file according to the full path of the text.
  Change this to whatever you like, e.g. filename, hash, etc.
  """
  return filepath[-15:-12] + ".tok.txt"

def tokenize(filepath_pattern, output_dir):
  filepaths = glob.glob(filepath_pattern)
  print("Tokenzing %d files..." % len(filepaths))
  # inventory the files to tokenize
  with open("temp.txt", "w") as f:
    for filepath in filepaths:
      f.write("%s \t %s\n" % (filepath, os.path.join(output_dir, filename_converter(filepath))))
  # call Stanford CoreNLP
  command = ['java', 'edu.stanford.nlp.process.PTBTokenizer', '-ioFileList', '-preserveLines', 'temp.txt']
  subprocess.call(command)
  print("Finished tokenizing.")
  os.remove("temp.txt")

def write_to_bin(filepath_pattern, output_filename):
  filepaths = sorted(glob.glob(filepath_pattern))
  with open(output_filename, 'wb') as f_out:
    for filepath in filepaths:
      with open(filepath, 'r') as f_in:
        lines = [l.strip().lower() for l in f_in]
      text = ' '.join(lines)
      tf_example = example_pb2.Example()
      tf_example.features.feature['article'].bytes_list.value.extend([text.encode()])
      tf_example.features.feature['abstract'].bytes_list.value.extend([b''])
      tf_example_str = tf_example.SerializeToString()
      str_len = len(tf_example_str)
      f_out.write(struct.pack('q', str_len))
      f_out.write(struct.pack('%ds' % str_len, tf_example_str))
  print("Finished writing file %s." % output_filename)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Usage: python make_data.py <filepath_pattern> <output_dir>")
    print("Notes:")
    print("1. <filepath_pattern> containing wildcards has to be quoted to be read correctly.")
    print("2. The path to stanford-corenlp-3.7.0.jar must be `export`ed as CLASSPATH in Bash.")
    sys.exit()
  file_pattern = sys.argv[1]
  out_dir = sys.argv[2]

  tokenize(file_pattern, out_dir)
  write_to_bin(os.path.join(out_dir, '*.tok.txt'), os.path.join(out_dir, 'test.bin'))
