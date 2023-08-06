import mne
import re
import sys

from PyQt5.QtWidgets import *

def get_valid_save_name(main_window):
    # get filename to save file under
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fpath, _ = QFileDialog.getSaveFileName(main_window, "Save As...", "", "", options=options)
    # validate fname
    if fpath:
        fname = fpath.split("/")[-1]

        # check for invalid characters (alphanumeric and underscores only)
        invalid_char = re.findall(r"[\W\s]", fname)
        if len(invalid_char) > 0:
            print(invalid_char)
            QMessageBox.warning(main_window, "Invalid File Name", "Files names should only include letters, digits, and underscores")
            return -1

        else:
            return fpath

def write_fif(data, fpath):

    if isinstance(data, mne.io.BaseRaw):
        save_fname = fpath + "-raw.fif"
        data.save(save_fname)
        return True
    elif isinstance(data, mne.BaseEpochs):
        save_fname = fpath + "-epo.fif"
        data.save(save_fname)
        return True
    elif type(data) == mne.Evoked or type(data) == mne.EvokedArray:
        save_fname = fpath + "-epo.fif"
        data.save(save_fname)
        return True
    else:
        return False


# --- test -------------------------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.show()
    #data = 1
    fname = get_valid_save_name(main_window)
    if fname:
        print(fname)
        #write_fif(data, fname, main_window)
    sys.exit(app.exec_())
