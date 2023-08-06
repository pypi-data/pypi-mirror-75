
class Display:
	def stack(self, scene) -> '[(place, key, callable)]':
		indev
	def duplicate(self, src, dst) -> 'display/None':
		indev
	def __getitem__(self, key) -> 'display':
		indev
	def upgrade(self, scene, key, displayable):
		indev
	
	# event management
	def control(self, scene, key, evt):
		pass
	
	# displays are obviously displayable as themselves
	def display(self, scene):	return self


class Turntable:
	def __init__(self, center: vec3, camera: vec3):
		self.center = center
		self.camera = camera
	def rotate(self, dx, dy):
		indev
	def pan(self, dx, dy):
		indev
	def zoom(self, f):
		indev
	@staticmethod
	def frommatrix(view):
		indev
	def tomatrix(self) -> mat4:
		indev
class Orbit:
	def __init__(self, center: vec3, distance, orient: vec3):
		self.center = center
		self.distance = distance
		self.orient = orient
	def rotate(self, dx, dy):
		indev
	def pan(self, dx, dy):
		indev
	def zoom(self, f):
		indev
	@staticmethod
	def frommatrix(view):
		indev
	def tomatrix(self) -> mat4:
		indev

class Perspective:
	def __init__(self, fov):
		self.fov = fov
	def tomatrix(self, ratio, distance) -> mat4:
		indev
class Orthographic:
	def __init__(self, size):
		self.size = size
	def tomatrix(self, ratio, distance) -> mat4:
		indev


class Scene:
	def __init__(self, objs=(), projection=None, navigation=None, parent=None):
		# super init
		indev
		
		# context variables
		self.ctx = None
		self.ressources = {}	# context-related ressources, shared across displays, but not across contexts (shaders, vertexarrays, ...)
		
		# rendering options
		self.options = deepcopy(settings.scene)
		
		# interaction methods
		self.projection = projection or Perspective()
		self.navigation = navigation or Turntable()
		self.tool = [] # tool stack, the last tool is used for input events, until it is removed 
		
		# render pipeline
		self.displays = {} # displays created from the inserted objects, associated to their insertion key
		self.queue = []	# list of objects to display, not yet loaded on the GPU
		self.stack = []	# list of callables, that constitute the render pipeline:  (place, key, callable)
		self.steps = [] # list of last rendered ids for each stack step
		self.frame = {'proj':None, 'view':None, 'projview':None}	# last frame rendering constants
		
		self.fb_screen = None	# UI framebuffer
		self.fb_idents = None	# framebuffer for id rendering
		
		# internal variables
		self.fresh = set()	# set of refreshed internal variables since the last render
		
	
	# methods to manage the rendering pipeline
	
	def add(displayable, key=None) -> 'key':
		indev
	def upgrade(key, displayable):
		indev
	def dequeue(self):
		indev
	def __getitem__(self, key) -> 'display':
		indev
	
	# methods to deal with the view
	
	def refreshmaps(self):
		if 'fb_idents' not in self.fresh:	
			indev
	def itemnear(point: QPoint) -> QPoint:
		indev
	def ptat(point: QPoint) -> vec3:
		indev
	def ptfrom(point: QPoint, center: vec3) -> vec3:
		indev
	def itemat(point: QPoint) -> '(key, display)':
		indev
	
	def look(self, box: Box):
		indev
	def adjust(self, box: Box):
		indev
	def center(self, center: vec3):
		indev
	
	# event system
	
	def event(self, evt):
		indev
	def inputEvent(self, evt):
		indev
	def navigate(self, evt):
		indev
	def control(self, evt):
		indev


