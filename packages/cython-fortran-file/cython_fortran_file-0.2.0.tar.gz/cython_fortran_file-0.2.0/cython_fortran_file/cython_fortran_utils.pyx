cimport numpy as np

import cython
import numpy as np

from libc.stdio cimport (FILE, SEEK_CUR, SEEK_SET, fclose, fopen, fread, fseek,
                         ftell, fwrite)


cdef INT32_SIZE = sizeof(np.int32_t)
cdef INT64_SIZE = sizeof(np.int64_t)
cdef DOUBLE_SIZE = sizeof(np.float64_t)

cdef class FortranFile:
    """This class provides facilities to interact with files written
    in fortran-record format.  Since this is a non-standard file
    format, whose contents depend on the compiler and the endianness
    of the machine, caution is advised. This code will assume that the
    record header is written as a 32bit (4byte) signed integer. The
    code also assumes that the records use the system's local
    endianness.

    Notes
    -----
    Since the assumed record header is an signed integer on 32bit, it
    will overflow at 2**31=2147483648 elements.

    This module has been inspired by scipy's FortranFile, especially
    the docstrings.
    """
    def __cinit__(self, str fname, str mode='r'):
        cdef char m[2]
        m[0] = ' '
        m[1] = ' '
        if mode == 'r':
            m[0] = 'r'
        elif mode == 'w':
            m[0] = 'w'
        elif mode == 'a':
            m[0] = 'a'
        elif mode == 'r+':
            m[0] = 'r'
            m[1] = '+'
        elif mode == 'w+':
            m[0] = 'w'
            m[1] = '+'
        elif mode == 'a+':
            m[0] = 'a'
            m[1] = '+'
        else:
            raise NotImplementedError

        self.cfile = fopen(fname.encode('utf-8'), m)
        self._closed = False
        if self.cfile == NULL:
            raise IOError("Cannot open '%s'" % fname)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    cpdef INT64_t skip(self, INT64_t n=1) except -1:
        """Skip records.

        Parameters
        ----------
        - n : integer
            The number of records to skip

        Returns
        -------
        value : int
            Returns 0 on success.
        """
        cdef INT32_t s1, s2, i

        if self._closed:
            raise ValueError("Read of closed file.")

        for i in range(n):
            fread(&s1, INT32_SIZE, 1, self.cfile)
            fseek(self.cfile, s1, SEEK_CUR)
            fread(&s2, INT32_SIZE, 1, self.cfile)

            if s1 != s2:
                raise IOError('Sizes do not agree in the header and footer for '
                              'this record - check header dtype. Got %s and %s' % (s1, s2))

        return 0

    cdef INT64_t get_size(self, str dtype):
        """Return the size of an element given its datatype.

        Parameters
        ----------
        dtype : str
           The dtype, see note for details about the values of dtype.

        Returns
        -------
        size : int
           The size in byte of the dtype

        Note:
        -----
        See
        https://docs.python.org/3.5/library/struct.html#format-characters
        for details about the formatting characters.
        """
        if dtype == 'i':
            return 4
        elif dtype == 'd':
            return 8
        elif dtype == 'f':
            return 4
        elif dtype == 'l':
            return 8
        else:
            # Fallback to (slow) numpy to compute the size
            return np.dtype(dtype).itemsize

    cpdef np.ndarray read_vector(self, str dtype):
        """Reads a record from the file and return it as numpy array.

        Parameters
        ----------
        d : data type
            This is the datatype (from the struct module) that we should read.

        Returns
        -------
        tr : numpy.ndarray
            This is the vector of values read from the file.

        Examples
        --------
        >>> f = FortranFile("fort.3")
        >>> rv = f.read_vector("d")  # Read a float64 array
        >>> rv = f.read_vector("i")  # Read an int32 array
        """
        cdef INT32_t s1, s2, size
        cdef np.ndarray data

        if self._closed:
            raise ValueError("I/O operation on closed file.")

        size = self.get_size(dtype)

        fread(&s1, INT32_SIZE, 1, self.cfile)

        # Check record is compatible with data type
        if s1 % size != 0:
            raise ValueError('Size obtained (%s) does not match with the expected '
                             'size (%s) of multi-item record' % (s1, size))

        data = np.empty(s1 // size, dtype=dtype)
        fread(<void *>data.data, size, s1 // size, self.cfile)
        fread(&s2, INT32_SIZE, 1, self.cfile)

        if s1 != s2:
            raise IOError('Sizes do not agree in the header and footer for '
                          'this record - check header dtype')

        return data


    cpdef INT64_t write_vector(self, np.ndarray data) except? -1:
        """Writes a record to the file.

        Parameters
        ----------
        data : np.ndarray of contiguous data
            The data to write to file. Can be any dtype.

        Returns
        -------
        int32 : the position in the file
        """

        # Compute size of record
        cdef INT32_t s1, size
        cdef INT64_t pos, total_size

        cdef size_t ret

        data = np.require(data, requirements='C')

        s1 = <INT32_t> data.nbytes         # total size
        total_size = <INT64_t> data.size   # number of elements
        element_size = <INT32_t> ((<INT64_t> s1) // total_size)
        ret = fwrite(&s1, INT32_SIZE, 1, self.cfile)
        ret = fwrite(<void *>data.data, element_size, total_size, self.cfile)
        if ret != total_size:
            raise IOError('Could not write to file.')
        ret = fwrite(&s1, INT32_SIZE, 1, self.cfile)

        return self.tell()

    cpdef peek_record_size(self):
        r""" This function returns the size of the next record and
        then rewinds the file to the previous position.

        Returns
        -------
        Number of bytes in the next record
        """
        cdef INT32_t s1
        cdef INT64_t pos

        pos = self.tell()
        fread(&s1, INT32_SIZE, 1, self.cfile)
        self.seek(pos)

        return s1

    cpdef INT32_t read_int(self) except? -1:
        """Reads a single int32 from the file and return it.

        Returns
        -------
        data : int32
            The value.

        Examples
        --------
        >>> f = FortranFile("fort.3")
        >>> rv = f.read_vector("d")  # Read a float64 array
        >>> rv = f.read_vector("i")  # Read an int32 array
        """

        cdef INT32_t s1, s2
        cdef INT32_t data

        if self._closed:
            raise ValueError("I/O operation on closed file.")

        fread(&s1, INT32_SIZE, 1, self.cfile)

        if s1 != INT32_SIZE != 0:
            raise ValueError('Size obtained (%s) does not match with the expected '
                             'size (%s) of record' % (s1, INT32_SIZE))

        fread(&data, INT32_SIZE, s1 // INT32_SIZE, self.cfile)
        fread(&s2, INT32_SIZE, 1, self.cfile)

        if s1 != s2:
            raise IOError('Sizes do not agree in the header and footer for '
                          'this record - check header dtype')

        return data

    cpdef INT64_t read_int64(self) except? -1:
        """Reads a single int64 from the file and return it.

        Returns
        -------
        data : int64
            The value.

        Examples
        --------
        >>> f = FortranFile("fort.3")
        >>> rv = f.read_int64()  # Read a single int64 element
        """

        cdef INT32_t s1, s2
        cdef INT64_t data

        if self._closed:
            raise ValueError("I/O operation on closed file.")

        fread(&s1, INT32_SIZE, 1, self.cfile)

        if s1 != INT64_SIZE:
            raise ValueError('Size obtained (%s) does not match with the expected '
                             'size (%s) of record' % (s1, INT64_SIZE))

        fread(&data, INT64_SIZE, s1 // INT64_SIZE, self.cfile)
        fread(&s2, INT32_SIZE, 1, self.cfile)

        if s1 != s2:
            raise IOError('Sizes do not agree in the header and footer for '
                          'this record - check header dtype')

        return data


    def read_attrs(self, object attrs):
        """This function reads from that file according to a
        definition of attributes, returning a dictionary.

        Fortran unformatted files provide total bytesize at the
        beginning and end of a record. By correlating the components
        of that record with attribute names, we construct a dictionary
        that gets returned. Note that this function is used for
        reading sequentially-written records. If you have many written
        that were written simultaneously.

        Parameters
        ----------
        attrs : iterable of iterables
            This object should be an iterable of one of the formats:
            [ (attr_name, count, struct type), ... ].
            [ ((name1,name2,name3),count, vector type]
            [ ((name1,name2,name3),count, 'type type type']
            [ (attr_name, count, struct type, optional)]

            `optional` : boolean.
                If True, the attribute can be stored as an empty Fortran record.

        Returns
        -------
        values : dict
            This will return a dict of iterables of the components of the values in
            the file.

        Examples
        --------

        >>> header = [ ("ncpu", 1, "i"), ("nfiles", 2, "i") ]
        >>> f = FortranFile("fort.3")
        >>> rv = f.read_attrs(header)
        """

        cdef str dtype
        cdef int n
        cdef dict data
        cdef key
        cdef np.ndarray tmp
        cdef bint optional

        if self._closed:
            raise ValueError("I/O operation on closed file.")

        data = {}

        for a in attrs:
            if len(a) == 3:
                key, n, dtype = a
                optional = False
            else:
                key, n, dtype, optional = a
            if n == 1:
                tmp = self.read_vector(dtype)
                if len(tmp) == 0 and optional:
                    continue
                elif len(tmp) == 1:
                    data[key] = tmp[0]
                else:
                    raise ValueError("Expected a record of length %s, got %s (%s)" % (n, len(tmp), key))
            else:
                tmp = self.read_vector(dtype)
                if len(tmp) == 0 and optional:
                    continue
                elif len(tmp) != n and n > 0:
                    raise ValueError("Expected a record of length %s, got %s (%s)" % (n, len(tmp), key))

                if isinstance(key, tuple):
                    # There are multiple keys
                    for ikey in range(n):
                        data[key[ikey]] = tmp[ikey]
                else:
                    data[key] = tmp

        return data


    cpdef np.ndarray direct_read_vector(self, str dtype, int count):
        """Reads directly elements from the file and return it as numpy array.

        Parameters
        ----------
        dtype : str
            This is the datatype (from the struct module) that we should read.
        count : int
            Number of elements to read

        Returns
        -------
        tr : numpy.ndarray
            This is the vector of values read from the file.

        Examples
        --------
        >>> f = FortranFile("fort.3")
        >>> rv = f.direct_read_vector("d", 10)  # Read a 10-float64 array
        >>> rv = f.direct_read_vector("i")  # Read an 10-int32 array
        """
        cdef INT32_t size
        cdef np.ndarray data

        if self._closed:
            raise ValueError("I/O operation on closed file.")

        size = self.get_size(dtype)

        data = np.empty(count, dtype=dtype)
        fread(<void *>data.data, size, count, self.cfile)

        return data


    cpdef INT64_t tell(self) except -1:
        """Return current stream position."""
        cdef INT64_t pos

        if self._closed:
            raise ValueError("I/O operation on closed file.")

        pos = ftell(self.cfile)
        return pos

    cpdef INT64_t seek(self, INT64_t pos, INT64_t whence=SEEK_SET) except -1:
        """Change stream position.

        Parameters
        ----------
        pos : int
            Change the stream position to the given byte offset. The offset is
            interpreted relative to the position indicated by whence.
        whence : int
            Determine how pos is interpreted. Can by any of
            * 0 -- start of stream (the default); offset should be zero or positive
            * 1 -- current stream position; offset may be negative
            * 2 -- end of stream; offset is usually negative

        Returns
        -------
        pos : int
            The new absolute position.
        """
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        if whence < 0 or whence > 2:
            raise ValueError("whence argument can be 0, 1, or 2. Got %s" % whence)

        fseek(self.cfile, pos, whence)
        return self.tell()

    cpdef void close(self):
        """Close the file descriptor.

        This method has no effect if the file is already closed.
        """
        if self._closed or self.cfile == NULL:
            return
        self._closed = True
        fclose(self.cfile)

    def __dealloc__(self):
        if not self._closed:
            self.close()
