  # setup python

  python3 -m venv /data/cache/venv
  source /data/cache/venv/bin/activate
  python3 -m pip install -r /data/project/requirements.txt

  # remove idea directory (No Python interpreter configured for the project)
  # https://github.com/JetBrains/Qodana/discussions/134#discussioncomment-4329981
  rm -rf .idea