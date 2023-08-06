from keras.models import model_from_json
from license_recognition.utils.tools import *

class WPOD():
	""" WPOD Model
	"""

	def __init__(self, config):
		self.model_plate = None
		self.config = config

		self.load_model_plate()

	def load_model_plate(self):
	    """Load plate detection model"""

	    model_path = self.config['model1']['path']

	    with tf.device('/cpu:0'):
	        model_path = os.path.splitext(model_path)[0]
	        with open('%s.json' % model_path, 'r') as json_file:
	            model_json = json_file.read()

	        self.model_plate = model_from_json(model_json, custom_objects={})
	        self.model_plate.load_weights('%s.h5' % model_path)

	def get_plate(self, input, resized, origin):
	    """ Get the license plate from image

	    Args:
	        input (np.array): the image
	        resized (np.array):
	        origin (np.array):

	    Returns:

	    """
	    output = self.model_plate.predict(input)
	    output = np.squeeze(output)

	    Llp, LlpImgs, is_square_list = postprocess_plate(origin, resized, output)

	    if len(LlpImgs):
	        Ilp = LlpImgs[0]
	        Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
	        Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)
	        res_img = (Ilp * 255.).astype(np.uint8)
	        is_square = is_square_list[0]

	        LlpImgs.pop(0)

	        return res_img, is_square

	    return None, None