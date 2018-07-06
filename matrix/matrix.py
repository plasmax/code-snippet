import copy


class Matrix44(object):
    """Class representing a 4x4 matrix

    Thanks Stack Overflow !
    """

    # Error threshold
    ERR_THRESHOLD = 1e-09

    def __init__(self, m):
        """

        :param m: 4x4 float matrix
        :type m: list[list[float]]
        """
        assert isinstance(m, list), (type(m), m)
        assert len(m) == 4
        assert all((len(row) == 4 for row in m))
        assert all((isinstance(v, float)
                    for row in m
                    for v in row))

        self._m = m  # 4x4 floats

    def __repr__(self):
        """Matrix representation

        :return: Matrix representation
        :rtype: str
        """
        return "Matrix44({})".format(self._m)

    def __eq__(self, other):
        """Matrix equal operator

        :type other: Matrix44
        :rtype: bool
        """
        if isinstance(other, Matrix44):
            return self._m == other._m
        else:
            return super(Matrix44, self).__eq__(other)

    @classmethod
    def __close_from_zero(cls, v):
        """Return if given value is close from zero

        :param v: Value to compare to zero
        :type v: float
        :return: True if given value is close from zero
        :rtype: bool
        """
        return 0.0 if abs(v) <= cls.ERR_THRESHOLD else v

    @classmethod
    def __is_close(cls, a, b, abs_tol=0.0):

        return abs(a - b) <= max(cls.ERR_THRESHOLD * max(abs(a), abs(b)), abs_tol)

    @classmethod
    def identity(cls):
        """Simply return an entity matrix

        :return: Identity matrix
        :rtype: Matrix44
        """
        return cls([[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]])

    @property
    def is_identity(self):
        """Return if matrix is entity

        :return: True if matrix is entity
        :rtype: bool
        """
        return self == self.identity()

    def close_from(self, other):
        """Compare matrix to `other` one

        :param other: The other matrix to compare
        :type other: Matrix44
        :return: True if boths matrix are close to each other
        :rtype: bool
        """
        assert isinstance(other, Matrix44), (type(other), other)

        m1 = self.as_floats
        m2 = other.as_floats

        return all((self.__is_close(m1[i], m2[i])
                    for i in xrange(16)))

    @property
    def zero_rounded(self):
        """Return matrix with all values near 0.0 puts 0.0

        This is mostly useful before storage.

        :return: Zero rounded matrix
        :rtype: Matrix44
        """
        return Matrix44([[self.__close_from_zero(v)
                          for v in row]
                         for row in self._m])

    @classmethod
    def from_floats(cls, m):
        """Build Matrix44 from given list of 16 floats

        :param m: List of 16 floats to build matrix from
        :type m: list[float]
        :return: Generated matrix
        :rtype: Matrix44
        """
        assert isinstance(m, list), (type(m), m)
        assert all((isinstance(v, float) for v in m))

        # convert list of 16 floats to a 4x4 floats
        return cls([m[i:i + 4] for i in xrange(0, len(m), 4)])

    @property
    def as_floats(self):
        """Return a list of 16 floats

        :return: A list of 16 floats
        :rtype: list[float]
        """
        return [v for row in self._m for v in row]

    @property
    def as_m44(self):
        """Return a list of 4 lists of 4 floats.

        :return: list of 4 lists of 4 floats.
        :rtype: list[list[float]]
        """
        return copy.deepcopy(self._m)

    def mul(self, m):
        """Multiply matrix by given `m` matrix."""
        if not isinstance(m, Matrix44):
            raise TypeError("Invalid type, must be 'Matrix44'")

        zip_b = zip(*m._m)

        return Matrix44([[sum(ele_a * ele_b
                              for ele_a, ele_b in zip(row_a, col_b))
                          for col_b in zip_b] for row_a in self._m])

    @staticmethod
    def _matrix_minor(m, i, j):
        """Return minor matrix

        :param i:
        :param j:
        :return: Minor matrix
        :rtype: list[list[float]]
        """
        return [row[:j] + row[j+1:]
                for row in (m[:i]+m[i+1:])]

    @property
    def transposed(self):
        """Return the transposed matrix

        :return: Transposed matrix
        :rtype: Matrix44
        """
        return Matrix44([list(row) for row in zip(*self._m)])

    @classmethod
    def __determinant(cls, m):
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for c in range(len(m)):
            minor = cls._matrix_minor(m, 0, c)
            determinant += ((-1) ** c) * m[0][c] * cls.__determinant(minor)
        return determinant

    @property
    def determinant(self):
        """

        :return: Matrix determinant
        :rtype: int
        """
        return self.__determinant(self._m)

    @property
    def inverted(self):
        """Return inverted matrix

        :return: Inverted matrix
        :rtype: Matrix44
        """
        determinant = self.determinant

        # find matrix of cofactors
        cofactors = []

        for r in xrange(4):

            cofactor_row = []

            for c in xrange(4):
                minor = self._matrix_minor(self._m, r, c)
                determinant = self.__determinant(minor)
                cofactor_row.append(((-1) ** (r + c)) * determinant)

            cofactors.append(cofactor_row)

        cofactors = Matrix44(cofactors).transposed

        for r in range(4):
            for c in range(4):
                cofactors._m[r][c] = cofactors._m[r][c] / determinant

        return cofactors


if __name__ == '__main__':

    x = [0.9145861082867216, -0.25241135777748747, -0.3159442308285979, 0.0, 0.27367749365319183, 0.96152043249346, 0.02406423415147011, 0.0, 0.29771274745407905, -0.10847563948884964, 0.9484725381585009, 0.0, 3.4195801292371875, 3.754793548797828, -4.712486410677807, 1.0]
    y = [0.5665559852596026, -0.4053683401251144, 0.7174195595261748, 0.0, -0.32552431142067106, 0.689713110890662, 0.6467841582318041, 0.0, -0.7569994968562522, -0.5999769441318017, 0.2588038412961563, 0.0, -0.18783762953508187, 2.37158243978719, -1.590849200305307, 1.0]
    r = [0.8394998908922867, -0.35527642128590853, 0.41111871481375856, 0.0, -0.17616126778917057, 0.537795071679132, 0.8244656867381137, 0.0, -0.514010837359244, -0.7645620480745269, 0.3888929592077156, 0.0, 4.094619217084887, 6.4025064541081385, 2.0713558694305547, 1.0]

    m1 = Matrix44.from_floats(x)
    m2 = Matrix44.from_floats(y)
    m3 = Matrix44.from_floats(r)
    mr = m1.mul(m2)

    assert mr == m3
    assert mr.as_floats == m3.as_floats
    assert mr._m == m3._m

    assert mr.mul(m2.inverted).close_from(m1)

    m1_inv = m1.inverted

    assert m1.mul(m1_inv).zero_rounded.is_identity
    assert m1.inverted.mul(m1).zero_rounded.is_identity
