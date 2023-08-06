#ifndef PYTHONIC_INCLUDE_DISPATCH_SORT_HPP
#define PYTHONIC_INCLUDE_DISPATCH_SORT_HPP

#include <algorithm>

#include "pythonic/include/numpy/sort.hpp"
#include "pythonic/include/list/sort.hpp"

PYTHONIC_NS_BEGIN
namespace __dispatch__
{

  using numpy::sort;
  using __builtin__::list::sort;

  DEFINE_FUNCTOR(pythonic::__dispatch__, sort);
}
PYTHONIC_NS_END

#endif
