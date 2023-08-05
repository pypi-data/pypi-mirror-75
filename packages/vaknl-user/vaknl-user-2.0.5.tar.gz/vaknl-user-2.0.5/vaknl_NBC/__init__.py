import os
import pickle


class NBC(object):
    """Singleton NBC class

    This means there is always only one instance of this object. When the NBC class is created it will load the NBC data
    from the `NBC.pkl` file. This data file could be excluded from the package to avoid unrestricted information
    sharing. In such a case, add the `NBC.pkl` file at location.
    """
    __instance = None
    __nbc_data = None

    def __new__(cls):
        if NBC.__instance is None:
            NBC.__instance = object.__new__(cls)
            file_path = 'vaknl_NBC/NBC.pkl'  # Original location.
            if not os.path.exists(file_path):
                # When using a Cloud Function, the file should be situated in the root directory.
                file_path = 'NBC.pkl'
            with open(file_path, 'rb') as output:
                cls.__nbc_data = pickle.load(output)

        return NBC.__instance

    def get_by_giata_id(self, giata_id):
        return self.__nbc_data.get(giata_id)


if __name__ == '__main__':
    # Test cases.
    nbc = NBC()
    print(nbc.get_by_giata_id(18878))
    print(nbc.get_by_giata_id(123))
