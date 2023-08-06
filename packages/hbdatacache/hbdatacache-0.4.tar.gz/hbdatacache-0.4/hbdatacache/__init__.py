import pickle
import os
import hashlib

def load_temp_data(label, parameters=[]):
    """Check if exists temp file and load persisted object and return.

    Args:
      label: A string with the data identifier.
      parameters: A list with te variable parameters of data.

    Returns:
      Persisted data object.
    """    
    if check_temp_data(label, parameters) and ACTIVE:
        file = os.path.join(TEMPDIR, _hash_tempfile(label, parameters))
        return pickle.load(file, 'rb')            
    return False

def check_temp_data(label, parameters=[]):
    """Check if exists temp file for those label and parameters.

    Args:
      label: A string with the data identifier.
      parameters: A list with te variable parameters of data.

    Returns:
      A boolean with true if exists.
    """
    file = os.path.join(TEMPDIR, _hash_tempfile(label, parameters))
    return os.path.exists(file)

def save_temp_data(data, label, parameters=[]):
    """Save the data object in temp file.

    Args:
      data: Object to persist
      label: A string with the data identifier.
      parameters: A list with te variable parameters of data.

    Returns:
      A string for the file name.

    Raises:
      ValueError: If no cadidate folder found
    """
    file = os.path.join(TEMPDIR, _hash_tempfile(label, parameters))
    pickle.dump(data,open(file,'wb'))

def _hash_tempfile(label, parameters=[]):
    """Generate a hash for temp file name.

    Args:
      label: A string with the data identifier.
      parameters: A list with te variable parameters of data.

    Returns:
      A string for the file name.

    Raises:
      ValueError: If no cadidate folder found
    """
    return label +"_"+hashlib.md5(''.join(parameters).encode()).hexdigest()

def _load_tempdir():
    """Browse the temporary directories and return the first one that is available.

    Returns:
      The new minimum port.

    Raises:
      ValueError: If no cadidate folder found
    """
    tempdir_list = _candidate_tempdir_list()
    for directory in tempdir_list:
        if os.path.isdir(directory):
            return directory
    
    raise ValueError(f'No temp data folder found, checked: {tempdir_list}.')

def _candidate_tempdir_list():
    """Browse the temporary directories in operational system.

    Returns:
      A list with directories path.
    """
    dirlist = []

    # First, try the environment.
    for envname in 'TMPDIR', 'TEMP', 'TMP':
        dirname = os.getenv(envname)
        if dirname: dirlist.append(dirname)

    # Failing that, try OS-specific locations.
    if os.name == 'nt':
        dirlist.extend([ os.path.expanduser(r'~\AppData\Local\Temp'),
                         os.path.expandvars(r'%SYSTEMROOT%\Temp'),
                         r'c:\temp', r'c:\tmp', r'\temp', r'\tmp' ])
    else:
        dirlist.extend([ '/tmp', '/var/tmp', '/usr/tmp' ])

    # As a last resort, the current directory.
    try:
        dirlist.append(os.getcwd())
    except (AttributeError, OSError):
        dirlist.append(os.curdir)

    return dirlist

TEMPDIR = _load_tempdir()
ACTIVE = True

if __name__ == "__main__":
  #Check if exist temp file
  if (check_temp_data("example_data", parameters=["teste",])):
      #Loading data from temp
      data = load_temp_data("example_data", parameters=["teste",])
  else:
      #Generate new data
      data = [1,2,3,4,5,6,7,8,9,10] #Your data generating...
      #Save data
      save_temp_data(data, "example_data", parameters=["teste",])