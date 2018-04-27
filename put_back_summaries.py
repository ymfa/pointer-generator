import sys, os, glob, subprocess

summary_file_extension = '.100.spl'  # change this to whatever you like

def untokenize(decoded_dir, filepath_pattern):
  in_paths = sorted(glob.glob(os.path.join(decoded_dir, '*_decoded.txt')))
  out_paths = sorted(glob.glob(filepath_pattern))
  if len(out_paths) == 1 and len(in_paths) > 1:
    out_paths = [os.path.join(out_paths[0], "%06d"%i + summary_file_extension) for i in range(len(in_paths))]
  elif len(out_paths) == len(in_paths):
    out_paths = [os.path.join(p, 'pgn' + summary_file_extension) for p in out_paths]
  else:
    print("Error: There are %d summaries but %d directories." % (len(in_paths), len(out_paths)))
    return
  print("Untokenzing %d files..." % len(in_paths))
  # inventory the files to untokenize
  with open("temp.txt", "w") as f:
    for p_in, p_out in zip(in_paths, out_paths):
      f.write("%s \t %s\n" % (p_in, p_out))
  # call Stanford CoreNLP
  command = ['java', 'edu.stanford.nlp.process.PTBTokenizer', '-ioFileList', '-untok', 'temp.txt']
  subprocess.call(command)
  print("Untokenized summaries have been put back to %s." % filepath_pattern)
  os.remove("temp.txt")

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Usage: python put_back_summaries.py <decoded_dir> <path_pattern>")
    print("Notes:")
    print("1. <path_pattern> containing wildcards has to be quoted to be read correctly.")
    print("2. The path to stanford-corenlp-3.7.0.jar must be `export`ed as CLASSPATH in Bash.")
    sys.exit()
  in_dir = sys.argv[1]
  out_dir = sys.argv[2]

  untokenize(in_dir, out_dir)
