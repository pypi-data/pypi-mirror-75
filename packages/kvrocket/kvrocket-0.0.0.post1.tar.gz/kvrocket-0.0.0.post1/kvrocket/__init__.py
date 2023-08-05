import os
import dill

# TODO: add encryption capabilities
# TODO: backup / restore database

class KVRocket:

    def __init__(self, root_data_dir, secret_key):
        self.root_data_dir = "{}/kv".format(root_data_dir)
        self.secret_key = secret_key # this is used to encrypt protected keys before writing it to disk.
        if not os.path.exists:
            os.mkdir(self.root_data_dir)

    def set(self, d, path, protected=False):
        # NOTE: if protected is true, then the values are encrypted before being written to disk.
        full_path = "{}/{}".format(self.root_data_dir, path)
        if type(d) != dict:
            raise Exception("invalid parameter to 'set' method. Must be dict.")

        if "/" in path:
            key = os.path.basename(full_path)
            short_path = full_path.replace(key, "")
            if not os.path.exists(short_path):
                os.makedirs(short_path)
        
        with open(full_path, "wb+") as f:
            dill.dump(d, f)
        return True

    def get(self, path):
        if not path.startswith(self.root_data_dir):
            path = "{}/{}".format(self.root_data_dir, path)
        with open(path, "rb+") as f:
            return dill.load(f)

    def rem(self, path):
        if not path.startswith(self.root_data_dir):
            path = "{}/{}".format(self.root_data_dir, path)
        if os.path.exists(path):
            os.remove(path)
        # TODO: consider removing empty sibling paths as cleanup?

    def scan(self, prefix):
        matches = []
        prefix = "{}/{}".format(self.root_data_dir, prefix)
        for root, dirs, files in os.walk(self.root_data_dir, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                if path.startswith(prefix):
                    matches.append(path)
        return matches
    
    def gscan(self, prefix):
        """ will return the values of the matching prefixes as a k/v data structure """
        matches = self.scan(prefix)
        results = {}
        for m in matches:
            results[m.replace("{}/".format(self.root_data_dir), "")] = self.get(m)
        return results
    
    def rmscan(self, prefix):
        """ will remove the keys of the matching prefixes """
        matches = self.scan(prefix)
        for m in matches:
            self.rem(m)
        # TODO: verfiy removal?