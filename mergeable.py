""" A mixin to allow merging two objects in an additive fashion.

Given an arbitraryly nested object whose leaf objects consist of numbers,
provide a merge() operation that sums the numbers when the access paths to the
leaves are the same and otherwise does a union.

From another angle, support a kind of 'vector addition' for messy, complicated
objects. """

# I't s quite possible that this is too abstract/clever.
class MergeableObjectImpl(object):
    def merge(self, other):
        access_func = self._access_func
        self_dict = access_func(self)
        for k, v in access_func(other).iteritems():
            if k not in self_dict:
                self_dict[k] = v
            else:
                if hasattr(self_dict[k], 'merge'):
                    assert hasattr(v, 'merge')
                    self_dict[k].merge(v)
                else:
                    assert type(v) == type(self_dict[k])
                    assert type(v) in [int, float], ('%s %s %s' % (
                            v, k, type(v)))
                    self_dict[k] += v
                    

class MergeableObject(MergeableObjectImpl):
    def _access_func(self, other):
        return other.__dict__

class MergeableDict(MergeableObjectImpl):
    def _access_func(self, other):
        return other
