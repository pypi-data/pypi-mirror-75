from math import sin, cos, tan, sqrt, pi


class Object:
    def __init__(self, position, vertices, faces, colors):
        self.position = position
        self.vertices = vertices
        self.faces = faces
        self.colors = colors


class Camera:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation

    def get_rotation_matrix(self):
        return rotation_matrix(*self.rotation)


class Vector:
    def __init__(self, vector):
        self.vector = vector

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.vector, other.vector)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.vector, other.vector)])

    def dot_product(self, other):
        """returns the dot product of two 3D vectors"""
        return self.vector[0] * other.vector[0] + self.vector[1] * other.vector[1] + self.vector[2] * other.vector[2]

    def cross_product(self, other):
        """returns the cross product of two 3D vectors"""
        return (self.vector[1] * other.vector[2] - self.vector[2] * other.vector[1],
                self.vector[2] * other.vector[0] - self.vector[0] * other.vector[2],
                self.vector[0] * other.vector[1] - self.vector[1] * other.vector[0])


class Matrices:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])

    def __mul__(self, other):
        """multiples 2 matrices together"""
        assert self.columns == other.rows, "Multiplying matrix rules not met"  # remove this line
        new_matrix_dimensions = (self.rows, other.columns)
        new_matrix = list()
        for a in range(self.rows):
            for b in range(other.columns):
                value = 0
                for c in range(other.rows):
                    value += self.matrix[a][c] * other.matrix[c][b]
                new_matrix.append(round(value, 10))
        new_matrix = [new_matrix[i:i + new_matrix_dimensions[1]]
                      for i in range(0, len(new_matrix), new_matrix_dimensions[1])]
        return Matrices(new_matrix)


def init(screen_width, screen_height, field_of_view, z_near, z_far):
    """required to initiate this library"""
    global _screen_height, _screen_width, _aspect_ratio, _field_of_view, _z_near, _z_far
    _screen_width = screen_width
    _screen_height = screen_height
    _aspect_ratio = screen_height / screen_width
    _field_of_view = field_of_view
    _z_near = z_near
    _z_far = z_far


def rotation_matrix(x, y, z) -> Matrices:
    """rotation matrix of x, y, z radians around x, y, z axes (respectively)"""
    sx, cx = sin(x), cos(x)
    sy, cy = sin(y), cos(y)
    sz, cz = sin(z), cos(z)
    return Matrices((
        (cy * cz, -cy * sz, sy),
        (cx * sz + sx * sy * cz, cx * cz - sz * sx * sy, -cy * sx),
        (sz * sx - cx * sy * cz, cx * sz * sy + sx * cz, cx * cy)
    ))


def get_normal(vector0, vector1, vector2):
    A = vector1 - vector0
    B = vector2 - vector0
    vector = A.cross_product(B)
    magnitude = sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    return vector[0] / magnitude, vector[1] / magnitude, vector[2] / magnitude


def projection(vertex):
    if vertex[2] == 0:
        vertex[2] += 0.001
    field_of_view = 1 / tan(_field_of_view / 2)
    q_val = _z_far / (_z_far - _z_near)
    x = _aspect_ratio * field_of_view * vertex[0] / vertex[2]
    y = field_of_view * vertex[1] / vertex[2]
    z = vertex[2] * q_val - _z_near * q_val
    return x, y, z


def display(obj: Object, cam: Camera):
    points_list = []
    camera_rotation = cam.get_rotation_matrix()
    for faces, color in zip(obj.faces, obj.colors):
        vertices = [projection((Vector((Matrices([obj.vertices[vertex]]) * camera_rotation).matrix[0]) +
                                Vector(obj.position) - Vector(cam.position)).vector) for vertex in faces]
        normal_vector = Vector(get_normal(Vector(vertices[0][:3]), Vector(vertices[1][:3]), Vector(vertices[2][:3])))
        if normal_vector.dot_product(Vector(vertices[0]) - Vector(cam.position)) < 0.2:  # normal_vector.vector[2] < 0:
            points = [(int((vertex[0] + 1) / 2 * _screen_width),
                       int(_screen_height - (vertex[1] + 1) / 2 * _screen_height)) for vertex in vertices]
            points_list.append((points, vertices[0][2], color))
    points_list = sorted(points_list, key=lambda z: z[1], reverse=True)
    return points_list
