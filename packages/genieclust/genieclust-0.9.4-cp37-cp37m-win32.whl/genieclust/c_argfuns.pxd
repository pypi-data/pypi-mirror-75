# distutils: language=c++
# cython: boundscheck=False
# cython: cdivision=True
# cython: nonecheck=False
# cython: wraparound=False
# cython: language_level=3



"""
Provides access to the Cargsort() and Cargkmin() functions.

Copyright (C) 2018-2020 Marek Gagolewski (https://www.gagolewski.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License
Version 3, 19 November 2007, published by the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License Version 3 for more details.
You should have received a copy of the License along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""


cdef extern from "../src/c_argfuns.h":
    void Cargsort[T](ssize_t* ret, T* x, ssize_t n, bint stable)
    ssize_t Cargkmin[T](T* x, ssize_t n, ssize_t k, ssize_t* buf)
