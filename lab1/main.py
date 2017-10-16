from lab1 import method_1_, method_2_
from independence import testing_independence
from uniformity import testing_uniformity

if __name__ == '__main__':
    testing_uniformity(method_1_, file_name='method_1_test_1.png')
    testing_uniformity(method_2_, file_name='method_2_test_1.png')

    testing_independence(method_1_)
    testing_independence(method_2_)
